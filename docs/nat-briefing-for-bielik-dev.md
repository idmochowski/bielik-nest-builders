# NeMo Agent Toolkit (NAT) - Technical Briefing for Bielik Dev

You're presenting Part 2 of the workshop (18:30-19:30). Here's everything you need to know about NAT.

## What is NAT?

NVIDIA NeMo Agent Toolkit is an open-source Python library (`pip install nvidia-nat`) that lets you build, compose, and deploy AI agents. It's **framework-agnostic** - it wraps LangChain, CrewAI, LlamaIndex, etc. without replacing them.

The Python module is `nat` (not `nvidia_nat`). CLI is `nat`.

## Core Concepts (5 things to explain)

### 1. YAML-first configuration

Everything is declared in YAML with three main sections:

```yaml
llms:           # LLM endpoints (OpenAI-compatible)
functions:      # Tools and agents
workflow:       # How they connect
```

NAT reads env vars with `${VAR}` syntax. All our configs point to Bielik via `${VLLM_BASE_URL}`.

### 2. Built-in components

NAT ships with ready-to-use components. We use these in the workshop:

| Component | `_type` | What it does |
|-----------|---------|--------------|
| OpenAI LLM | `openai` | Connects to any OpenAI-compatible endpoint (vLLM) |
| Wiki search | `wiki_search` | Searches Wikipedia, returns document content |
| DateTime | `current_datetime` | Returns current date/time |
| ReAct Agent | `react_agent` | Reasoning + Acting loop (text-based tool calling) |
| Tool Calling Agent | `tool_calling_agent` | Uses native LLM tool calling (needs vLLM tool support) |

### 3. ReAct agent (what we demo)

The `react_agent` workflow type implements the ReAct pattern:

```
User Question
  -> LLM generates: "Thought: I need to search for X"
                     "Action: wiki_search"
                     "Action Input: X"
  -> NAT calls wiki_search("X")
  -> LLM sees result: "Observation: [wiki content]"
  -> LLM generates: "Thought: I now know the answer"
                     "Final Answer: ..."
```

The agent parses tool calls from **text output** (not native function calling). This means it works with Bielik even without `--enable-auto-tool-choice` on vLLM. The model just needs to follow the ReAct text format, which it does well.

### 4. Custom functions (`@register_function`)

This is the key pattern for Exercises 2-4. It wraps any Python code as a NAT-composable function:

```python
from nat.cli.register_workflow import register_function
from nat.builder.function_info import FunctionInfo
from nat.builder.builder import Builder
from nat.builder.framework_enum import LLMFrameworkEnum

@register_function(
    config_type=MyConfig,
    framework_wrappers=[LLMFrameworkEnum.LANGCHAIN]
)
async def my_agent(_config, _builder):
    # Get instrumented LLM and tools from the builder
    llm = await _builder.get_llm(_config.llm_ref, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    tools = await _builder.get_tools(_config.tools_ref, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
    
    # Build your agent with standard LangChain/CrewAI code
    # ...
    
    async def run(query: str) -> str:
        return await agent.ainvoke(query)
    
    yield FunctionInfo.from_fn(run, description="...")
```

Once registered, it can be referenced in YAML like any built-in:

```yaml
functions:
  my_agent:
    _type: my_custom_type
    llm_ref: bielik
```

### 5. Composition

The power move: put agents from different frameworks under `tool_names` in one workflow:

```yaml
workflow:
  _type: react_agent
  tool_names:
    - research_agent    # LangChain
    - writing_crew      # CrewAI
  llm_name: bielik      # Bielik decides which to call
```

Bielik acts as the orchestrator, choosing which sub-agent to invoke based on the user's query.

## CLI Commands You'll Use

```bash
nat run --config_file config.yaml --input "zapytanie"  # Run a workflow
nat validate --config_file config.yaml                # Validate config
nat serve --config_file config.yaml --port 8080       # Deploy as API
nat info components                                   # List available components
```

## Your Presentation Flow

| Time | Exercise | What to show |
|------|----------|-------------|
| 18:30-18:40 | Bielik intro | Your own slides/demo about Bielik model family |
| 18:40-18:55 | Exercise 1 | Walk through `config.yaml`, run `nat run`, explain ReAct loop |
| 18:55-19:10 | Exercise 2 | Show `functions.py` code walkthrough, explain `@register_function` |
| 19:10-19:20 | Exercise 3 | Show CrewAI crew, compare with LangChain approach |
| 19:20-19:30 | Exercise 4 | The payoff - unified config composing both agents |

## Key Messages

- "NAT doesn't replace your framework - it wraps it"
- "YAML-first: define what you have, declare how it connects"
- "The same Bielik model orchestrates agents from different frameworks"
- "Everything you build here gets observability for free in Part 3"
