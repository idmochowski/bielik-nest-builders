# Part 3: Profiling, Optimizing & Tracking Multi-Agent Workflows

**Duration:** 40 minutes (19:50 - 20:30)
**Lead:** NVIDIA

## Overview

Now that we have a working multi-agent workflow, we need to answer:

- **What's happening inside?** - Trace every LLM call, tool invocation, and agent step
- **How much does it cost?** - Track token usage and compute costs per agent
- **Can we make it better?** - Optimize parameters for quality, speed, and cost

## Exercises

### Exercise 1: Observability with Phoenix (15 min)
`01_observability/` - Add Phoenix tracing to the unified workflow. Visualize the full execution graph, inspect individual LLM calls, and identify bottlenecks.

### Exercise 2: Cost Tracking (10 min)
`02_cost_tracking/` - Implement token-level cost tracking. Compare costs across agents, identify expensive operations, and build a cost dashboard.

### Exercise 3: Optimization (15 min)
`03_optimization/` - Use NAT's optimizer to tune temperature, max_tokens, and prompts. Evaluate the impact on quality and cost.

## Key Concepts

- **Tracing**: Following a request through every component (LLM, tool, agent)
- **Spans**: Individual units of work within a trace (one LLM call, one tool execution)
- **Token tracking**: Counting input/output tokens per LLM call for cost estimation
- **Hyperparameter optimization**: Systematic search for optimal model parameters
