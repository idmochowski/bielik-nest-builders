# Agent Architectures: A Practical Guide

This document explains the most common LLM agent architectures — how they work, their trade-offs, and when to use each one. Tied to the NAT/Bielik workshop context where applicable.

---

## 1. ReAct (Reasoning + Acting)

The agent interleaves **thinking** and **doing** in a loop. Each step: the model reasons about what to do next, takes an action, observes the result, and reasons again.

```
User: "Kim był Mikołaj Kopernik?"

┌─ LLM ──────────────────────────────────────────────┐
│ Thought: I need to search Wikipedia for Copernicus  │
│ Action: wiki_search("Mikołaj Kopernik")             │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
              ┌──────────────┐
              │ Tool: search │ ──→ returns Wikipedia article
              └──────────────┘
                      │
                      ▼
┌─ LLM ──────────────────────────────────────────────┐
│ Observation: [Wikipedia content about Copernicus]   │
│ Thought: I now have enough information              │
│ Final Answer: Mikołaj Kopernik was...               │
└─────────────────────────────────────────────────────┘
```

**How it works step by step:**

1. User sends a query
2. LLM generates a **Thought** (reasoning) and **Action** (tool call)
3. NAT executes the tool, returns an **Observation**
4. LLM sees the observation and generates the next Thought/Action (or a Final Answer)
5. Loop repeats until Final Answer or `max_tool_calls` is reached

**Strengths:**
- Transparent — every reasoning step is visible in the trace
- Flexible — the model adapts its plan based on intermediate results
- No special model capabilities required — works with text-only models (like Bielik 7B)

**Weaknesses:**
- Token-heavy — each iteration sends the full conversation + tool results back to the LLM
- Can loop — the model may repeat actions or fail to converge on a Final Answer
- Sequential — tools are called one at a time, no parallelism

**When to use:** General-purpose tasks where the model needs to adapt its approach based on intermediate results. Good default choice for most agent workflows.

**NAT config:**
```yaml
workflow:
  _type: react_agent
  tool_names: [wiki_search, current_datetime]
  llm_name: bielik
  max_tool_calls: 5
```

> This is the architecture used throughout this workshop (Part 2, Exercises 1-4).

---

## 2. Tool Calling Agent (Native Function Calling)

Instead of parsing tool calls from free-form text (like ReAct), the model uses the **native tool calling API** — structured JSON function calls returned alongside the response.

```
User: "Jaka jest pogoda w Warszawie?"

┌─ LLM ──────────────────────────────────────────────┐
│ Returns structured tool_call:                       │
│   {"name": "get_weather", "args": {"city": "Warszawa"}} │
└─────────────────────────────────────────────────────┘
                      │
                      ▼
              ┌──────────────┐
              │ Tool: weather│ ──→ {"temp": 12, "conditions": "słonecznie"}
              └──────────────┘
                      │
                      ▼
┌─ LLM ──────────────────────────────────────────────┐
│ Final Answer: W Warszawie jest 12°C, słonecznie.    │
└─────────────────────────────────────────────────────┘
```

**How it works step by step:**

1. User sends a query + available tools (JSON schema)
2. LLM returns a **structured tool call** (not text to parse)
3. Framework executes the tool, returns the result
4. LLM sees the result and generates the final answer (or another tool call)

**Strengths:**
- More reliable — no text parsing, structured API response
- Faster — no need for ReAct prompt overhead
- Parallel tool calls — some models can call multiple tools at once

**Weaknesses:**
- Requires model + server support (vLLM needs `--enable-auto-tool-choice` + custom parser)
- Less transparent — reasoning is implicit, not visible in text
- Smaller models may struggle with complex tool schemas

**When to use:** When your inference server supports tool calling (vLLM with `--enable-auto-tool-choice`) and you want more reliable, faster tool invocation.

**NAT config:**
```yaml
workflow:
  _type: tool_calling_agent
  tool_names: [wiki_search, current_datetime]
  llm_name: bielik
```

> Requires vLLM configured with Bielik's custom chat template and tool parser (see `docs/vllm-deployment.md`).

---

## 3. ReWOO (Reasoning WithOut Observation)

The model creates a **complete plan upfront** — listing all the tools it would call and why — before executing any of them. Then all tools run, and a final solver step combines the results.

```
User: "Porównaj Python i Rust pod kątem wydajności."

┌─ Planner (LLM) ────────────────────────────────────┐
│ Plan:                                               │
│   Step 1: search("Python programming performance")  │
│   Step 2: search("Rust programming performance")    │
│   Step 3: Combine and compare results               │
└─────────────────────────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ▼                       ▼
  ┌──────────────┐        ┌──────────────┐
  │ Tool: search │        │ Tool: search │   ← All tools run
  │ "Python..."  │        │ "Rust..."    │      (can be parallel)
  └──────────────┘        └──────────────┘
          │                       │
          └───────────┬───────────┘
                      ▼
┌─ Solver (LLM) ─────────────────────────────────────┐
│ Combines all observations into the final answer     │
└─────────────────────────────────────────────────────┘
```

**How it works step by step:**

1. **Planner**: LLM generates a full list of planned tool calls (no execution yet)
2. **Worker**: Framework executes all planned tools (potentially in parallel)
3. **Solver**: LLM receives all observations at once and produces the final answer

**Strengths:**
- Fewer LLM calls — only 2-3 calls total (planner + solver), vs. N calls in ReAct
- Parallelizable — tools can run concurrently since the plan is known upfront
- Lower cost — fewer tokens consumed overall

**Weaknesses:**
- No adaptation — the plan is fixed, can't react to unexpected tool results
- Planning quality matters — a bad plan means bad or useless tool calls
- Requires a model capable of multi-step planning in one shot

**When to use:** Tasks where the information-gathering steps are predictable and independent (e.g., "compare X and Y", "gather data on A, B, and C"). Not ideal for exploratory tasks where each step depends on the previous result.

---

## 4. Plan-and-Execute

Two distinct phases: a **planner** LLM breaks the task into steps, then an **executor** agent carries out each step sequentially. The planner can revise the plan after each step.

```
User: "Napisz raport o stanie AI w Polsce."

┌─ Planner (LLM) ────────────────────────────────────┐
│ Step 1: Research AI companies in Poland              │
│ Step 2: Research AI education in Poland              │
│ Step 3: Research government AI initiatives           │
│ Step 4: Write report combining all findings          │
└─────────────────────────────────────────────────────┘
          │
          ▼
┌─ Executor ──────────────────────────────────────────┐
│ Executes Step 1 → result1                           │
│ Executes Step 2 → result2                           │
│ Executes Step 3 → result3                           │
│ Executes Step 4 (using result1+2+3) → final report  │
└─────────────────────────────────────────────────────┘
```

**How it works step by step:**

1. **Planner LLM** decomposes the user query into an ordered list of sub-tasks
2. **Executor agent** runs each sub-task (using tools or sub-agents)
3. After each step, results feed back to the planner
4. Planner may revise remaining steps based on what was learned
5. Final step synthesizes everything

**Strengths:**
- Handles complex, multi-step tasks that need decomposition
- Planner can adapt the plan based on intermediate results
- Clear separation of concerns — planning vs. execution

**Weaknesses:**
- Higher latency — two LLMs (planner + executor) per cycle
- Overkill for simple tasks — planning overhead isn't worth it for single-tool queries
- Planning errors compound — a bad decomposition leads to bad execution

**When to use:** Complex tasks that naturally decompose into distinct phases (research → analyze → write). The workshop's Exercise 4 (research agent → writing crew) is effectively a simple Plan-and-Execute pattern.

**In this workshop:** The unified workflow from Exercise 4 approximates this pattern — the ReAct orchestrator decides when to call the research agent and when to call the writing crew, effectively acting as a lightweight planner.

---

## 5. Reflexion

The agent acts, then **critiques its own output**, and revises it. Multiple rounds of self-evaluation improve quality.

```
User: "Wyjaśnij kwantowe obliczenia prostym językiem."

Round 1:
┌─ Agent (LLM) ──────────────────────┐
│ Generate initial answer              │
└─────────────────────────────────────┘
          │
          ▼
┌─ Evaluator (LLM) ──────────────────┐
│ "Answer is too technical.            │
│  Missing real-world analogies."      │
└─────────────────────────────────────┘
          │
          ▼
Round 2:
┌─ Agent (LLM) ──────────────────────┐
│ Revised answer with analogies        │
└─────────────────────────────────────┘
          │
          ▼
┌─ Evaluator (LLM) ──────────────────┐
│ "Good. Clear and accessible."        │
└─────────────────────────────────────┘
          │
          ▼
    Final revised answer
```

**How it works step by step:**

1. Agent generates an initial response (using tools if needed)
2. Evaluator (can be the same LLM with a different prompt) scores the response
3. If the score is below threshold, agent revises with the feedback
4. Loop continues until quality threshold or max iterations

**Strengths:**
- Higher output quality — iterative refinement catches mistakes
- Self-correcting — the agent can fix hallucinations or incomplete answers
- Works with any base model — evaluation is prompt-based

**Weaknesses:**
- Expensive — multiple LLM calls per user query (2× iterations)
- Slow — latency multiplies with each refinement round
- Evaluation quality depends on the model — a weak evaluator gives weak feedback

**When to use:** Tasks where output quality matters more than latency (report writing, code generation, complex analysis). Not suitable for real-time chat or low-latency tools.

---

## 6. LATS (Language Agent Tree Search)

The agent explores **multiple reasoning paths** simultaneously using tree search, evaluating each path and backtracking from dead ends.

```
User: "Rozwiąż problem matematyczny: ..."

                    ┌─ Start ─┐
                   /           \
          Path A: "use algebra"  Path B: "try substitution"
                /        \              \
    A1: result=3 ✓    A2: error    B1: result=3 ✓
                                   /          \
                              B1a: verify ✓   B1b: edge case
                                                   │
                                             backtrack → B1a is best
```

**How it works step by step:**

1. LLM generates multiple possible next actions (branches)
2. Each branch is evaluated (via LLM scoring or tool result)
3. Promising branches are explored further
4. Dead ends are pruned (backtracking)
5. Best path to a solution is selected

**Strengths:**
- Handles problems with multiple valid approaches
- Can recover from wrong paths — backtracking is built in
- Often finds better solutions than greedy single-path approaches

**Weaknesses:**
- Very expensive — explores multiple paths, each requiring LLM calls
- Complex to implement — requires tree management and evaluation heuristics
- Slow — multiple paths evaluated sequentially (or with significant parallel overhead)

**When to use:** Complex reasoning tasks where there are multiple solution strategies (math, logic puzzles, planning problems). Overkill for most information-retrieval tasks.

---

## 7. Multi-Agent Orchestration Patterns

Not a single architecture, but a family of patterns for **composing multiple agents** into larger systems. This is what NAT's YAML composition enables in Exercise 4.

### Router (Hub-and-Spoke)

```
                ┌──────────────┐
                │ Orchestrator │  ← decides which agent to call
                └──────┬───────┘
               /        |        \
        ┌─────┐   ┌─────┐   ┌─────┐
        │Research│  │Write │  │Code │   ← specialist agents
        │Agent  │  │Agent │  │Agent │
        └─────┘   └─────┘   └─────┘
```

One orchestrator agent receives the query and routes it to the appropriate specialist. This is the pattern in Exercise 4 — Bielik as the ReAct orchestrator chooses between `research_agent` and `writing_crew`.

### Sequential Pipeline

```
┌─────────┐    ┌─────────┐    ┌─────────┐
│Research  │───→│Analyze  │───→│Write    │
│Agent     │    │Agent    │    │Agent    │
└─────────┘    └─────────┘    └─────────┘
```

Agents pass results along a fixed chain. Output of one becomes input of the next. Deterministic — no routing decisions needed.

### Parallel Fan-out

```
              ┌─────────┐
              │Splitter  │
              └────┬────┘
           /       |       \
    ┌─────┐  ┌─────┐  ┌─────┐
    │Agent1│  │Agent2│  │Agent3│   ← run simultaneously
    └──┬──┘  └──┬──┘  └──┬──┘
       \       |       /
        ┌──────┴──────┐
        │ Aggregator  │
        └─────────────┘
```

Multiple agents work on sub-tasks in parallel, then an aggregator combines results. Faster for independent sub-tasks.

### Hierarchical

```
        ┌──────────────┐
        │  Manager     │
        └──────┬───────┘
          ┌────┴────┐
    ┌─────┐       ┌─────┐
    │Team  │       │Team  │
    │Lead 1│       │Lead 2│
    └──┬──┘       └──┬──┘
     / \           / \
    A   B         C   D           ← workers
```

Multi-level delegation. Manager assigns to team leads, who delegate to workers. Scales to large, complex workflows.

**When to use which:**
- **Router** — queries map to distinct capabilities (search, write, code)
- **Pipeline** — task naturally decomposes into fixed sequential stages
- **Parallel** — sub-tasks are independent and latency matters
- **Hierarchical** — large systems with many agents and complex delegation logic

---

## Comparison

| Pattern | LLM Calls | Adaptivity | Token Cost | Latency | Model Requirements |
|---------|-----------|------------|------------|---------|-------------------|
| **ReAct** | N (one per step) | High | Medium | Medium | Low (text-based) |
| **Tool Calling** | N | High | Medium | Low | Medium (tool API support) |
| **ReWOO** | 2-3 | None | Low | Low | High (multi-step planning) |
| **Plan-and-Execute** | 2N (planner + executor) | Medium | High | High | Medium |
| **Reflexion** | 2× iterations | Medium | High | High | Medium |
| **LATS** | N × branches | High | Very High | Very High | High |

## Key Takeaway

There is no "best" agent architecture. The right choice depends on:

- **Task complexity** — simple queries → Tool Calling or ReAct; complex multi-step → Plan-and-Execute
- **Model capability** — smaller models (7B) work well with ReAct; ReWOO and LATS need stronger planning
- **Latency tolerance** — real-time → Tool Calling; batch → Reflexion, LATS
- **Cost budget** — fewer LLM calls → ReWOO; quality at any cost → Reflexion, LATS
- **Orchestration needs** — single task → any; multiple capabilities → Multi-Agent Router

In this workshop, we use **ReAct** because it works reliably with Bielik-Minitron-7B without requiring native tool calling support, and its transparent reasoning loop is ideal for learning and debugging.
