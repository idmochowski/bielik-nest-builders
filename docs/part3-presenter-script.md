# Part 3: Presenter Script

**Duration:** 40 minutes (19:50 - 20:30)
**Lead:** NVIDIA

Use this script alongside the notebooks. Each section tells you what to say, what to show, and when to let participants try things.

---

## Opening (2 min)

> "In Part 2 you built a multi-agent workflow - a LangChain research agent and a CrewAI writing crew orchestrated by Bielik. It works. But right now it's a black box.
>
> If I ask you: how many LLM calls did that workflow make? Which agent took the longest? How much would it cost to run this 10,000 times a day? You can't answer any of that.
>
> That's what Part 3 fixes. Three exercises, three questions:
> 1. What's happening inside? - Observability
> 2. How much does it cost? - Token Factory pricing
> 3. Can we make it better? - Optimization"

---

## Exercise 1: Observability with Phoenix (15 min)

### Step 1: Launch Phoenix (cell-2)

> "First, we start Phoenix - it's a tracing UI that shows us everything our agents do."

**Run cell.** Phoenix URL appears.

> "Open that URL in a new tab. You'll see an empty dashboard - no traces yet."

### Step 2: Show the config (cell-5)

> "Now look at the config. This is the exact same workflow from Part 2 - same Bielik LLM, same wiki_search tool, same react_agent.
>
> Scroll to the bottom. See the `general.telemetry` section? That's ALL we added."

**Point to the screen:**

```yaml
general:
  telemetry:
    tracing:
      phoenix:
        _type: phoenix
        project: bielik-nest-workshop
        endpoint: "..."
```

> "Five lines of YAML. That's it. NAT has a native Phoenix plugin - `nvidia-nat-phoenix` - that handles everything. No `OpenAIInstrumentor`, no manual setup, no code changes. Just config.
>
> This is the power of a framework-agnostic toolkit. Observability is a config toggle, not a rewrite."

### Step 3: Run with tracing (cell-8)

> "Let's run a query and see what happens."

**Run cell.** Watch the output.

> "Notice in the logs: `Started exporter 'phoenix'` at the beginning, `Stopped exporter 'phoenix'` at the end. Every LLM call and tool invocation between those two lines was traced."

**Switch to Phoenix UI tab.**

> "Now look at Phoenix. You should see a trace. Click on it."

**Walk through the Phoenix UI:**

> "This is the full execution timeline. You can see:
> - The `<workflow>` span - the entire workflow from start to finish
> - `wiki_search` spans - each time the agent searched Wikipedia
> - The timing of each step
>
> Click on any span to see the exact input that was sent and the output that came back. This is what was invisible before."

### Step 5: Run multiple queries (cell-11)

> "Let's run three more queries to build up some data."

**Run cell.** Wait for all three to complete.

> "Now go back to Phoenix. You should see four traces. Compare them:
> - Which query took the longest?
> - Which query required the most tool calls?
> - Did any query fail or get a wrong Wikipedia result?
>
> Take a minute to explore."

**Give participants 2 minutes to look at Phoenix.**

### Step 6: Query programmatically (cell-13)

> "Phoenix isn't just a UI. You can query traces programmatically."

**Run cell.** Show the span listing.

> "We get every span with its name, duration, input and output. In production, you'd pipe this into dashboards, alerting, SLO tracking.
>
> NAT also supports other exporters - Langfuse, LangSmith, Weave, or just plain files. Same YAML pattern, different `_type`."

**Transition:**

> "So now we can SEE what's happening. Next question: how much does it COST?"

---

## Exercise 2: Cost Tracking (15 min)

### Open the notebook, explain the context (cell-0 markdown)

> "If you're running Bielik on your own GPU, you might think cost doesn't matter. But it does.
>
> Cloud providers like Nebius have something called Token Factory - you pay per token, not per GPU hour. Beyond is building something similar. The formula is simple:"

**Point to the screen:**

```
cost = (input_tokens × rate) + (output_tokens × rate)
```

> "Even if you self-host, token efficiency determines how many concurrent users your GPU can serve. More tokens per request = fewer users per GPU."

### Step 1: Token usage in every response (cell-3)

> "The good news: vLLM already gives us everything we need."

**Run cell.**

> "See `response.usage`? Every single API call returns prompt tokens, completion tokens, and total tokens. This is the same data Token Factory uses for billing. It's already there - we just need to track it."

### Step 2: Define pricing (cell-5)

> "Let's define a pricing model. Token Factory charges per million tokens, with output tokens costing more than input - because output tokens are generated one by one, which is slower."

**Run cell.** Show the pricing and demo cost.

> "That one question about the capital of Poland cost a fraction of a cent. But multiply that by a multi-agent workflow with 7 LLM calls, then by 10,000 requests a day..."

### Step 4: Simulate a full workflow (cell-9)

> "Let's simulate the full workflow from Part 2 - orchestrator, research agent, analyst, writer - and track every call."

**Run cell.** Wait for the cost report.

> "Look at this report. You can see exactly where the money goes:
> - The writer agent is the most expensive - it generates the longest output
> - The orchestrator is cheap - it just routes
> - The research agent makes multiple calls
>
> This tells you WHERE to optimize. Don't optimize the orchestrator - it's already cheap. Focus on the writer."

### Step 5: Visualize (cell-11)

**Run cell.** Show the bar chart.

> "The cost by role breakdown is what your CFO cares about. Orchestration overhead, research cost, writing cost. In our case, writing is ~40% of total cost."

### Step 6: Compare platforms (cell-13)

**Run cell.**

> "Same workflow, different platforms. Beyond's Token Factory with Bielik-7B is the cheapest. GPT-4o would cost 50x more for the same work. This is the value proposition of running your own model on your own infrastructure."

### Step 7: Monthly projection (cell-15)

**Run cell.**

> "At 1,000 requests per day, this workflow costs about [X] per month on Beyond's pricing. And we can see that cutting the writer's output by 20% would save [Y] per month. That's actionable."

### Step 8: Phoenix traces (cell-17)

**Run cell.**

> "And here's where observability meets cost tracking. The Phoenix traces from Exercise 1 give us workflow-level timing. Combined with the token costs from this exercise, you have the full picture: what's slow AND what's expensive."

**Transition:**

> "We know what's happening. We know what it costs. Last question: can we make it better?"

---

## Exercise 3: Optimization (10 min)

### Temperature sweep (cell-5)

> "The simplest optimization lever is temperature. Lower temperature = more deterministic, usually shorter answers, fewer tokens."

**Run cell.** Show the results table.

> "Look at the pattern:
> - All temperatures get the right answer for this factual question
> - But token counts and latency may differ
> - For factual Q&A, temp 0.0-0.3 is fine. For creative writing, you want 0.7+."

### Compare configurations (cell-7)

> "Now let's test multiple questions across different configs."

**Run cell.** Show the comparison table.

> "This is your optimization dashboard. For each config you see accuracy, token usage, and cost. The 'conservative' config uses fewer tokens but may truncate answers. The 'creative' config generates more but costs more.
>
> The sweet spot depends on your use case. For a customer-facing chatbot: conservative. For report generation: balanced."

### Max tokens impact (cell-11)

**Run cell.**

> "This is the most underrated optimization: `max_tokens`. It's a cost ceiling per call. A workflow with 7 LLM calls at max_tokens=1024 vs 256 can be 4x the cost. Set it as low as your use case allows."

### NAT optimizer (cell-9, commented out)

> "NAT includes an Optuna-based optimizer that automates this search:
>
> `nat optimize --config_file config.yaml --dataset eval_dataset.json`
>
> It takes a few minutes to run, so we've left it commented out. But in production, you'd run this against your evaluation dataset to find the optimal temperature, max_tokens, and even prompt wording."

---

## Closing (3 min)

> "Let's recap what we built today:
>
> **Part 1** - Beyond deployed Bielik on their infrastructure with Run:ai. You got a workspace and a model endpoint.
>
> **Part 2** - [Bielik rep] showed you how to build agents with NAT. You started with a simple ReAct agent, then registered LangChain and CrewAI agents as NAT Functions, and composed them into a unified workflow. All via YAML.
>
> **Part 3** - We made that workflow production-ready:
> - **Observability**: One YAML block gives you full tracing in Phoenix
> - **Cost tracking**: Token Factory pricing tells you exactly what each agent costs
> - **Optimization**: Systematic parameter tuning reduces cost without sacrificing quality
>
> The key insight: in production, you don't just deploy agents - you observe, measure, and optimize them. NAT gives you all three in one toolkit.
>
> One more thing to remember: we used Bielik-7B for everything today, including orchestration. In production, you'd use a larger model - Bielik-11B, GPT-4o - as the orchestrator, and keep the 7B for specialized tasks. That's where the real efficiency comes from.
>
> Thank you. Let's open it up for networking."
