# Part 3: Profiling, Optimizing & Tracking Multi-Agent Workflows

**Duration:** 40 minutes (19:50 - 20:30)
**Lead:** NVIDIA

## Overview

Now that we have a working multi-agent workflow, we need to answer:

- **What's happening inside?** - Trace every workflow step, tool invocation, and agent action
- **How much does it cost?** - Token Factory pricing: per-token cost tracking across agents
- **Can we make it better?** - Optimize parameters for quality, speed, and cost

## Exercises

### Exercise 1: Observability with Phoenix (15 min)
`01_observability/` - Enable Phoenix tracing by adding one YAML block to the NAT config (`nvidia-nat-phoenix` plugin). Inspect workflow spans, tool calls, inputs/outputs, and timing in the Phoenix UI.

### Exercise 2: Cost Tracking (10 min)
`02_cost_tracking/` - Implement Token Factory-style per-token cost tracking. Track `response.usage` from every API call, apply input/output pricing rates, and compare per-agent costs. Includes platform cost comparison (Beyond vs Nebius vs OpenAI).

### Exercise 3: Optimization (15 min)
`03_optimization/` - Tune temperature and max_tokens to find the sweet spot between answer quality, speed, and cost. Manual parameter sweep + NAT's `nat optimize` command.

## Key Concepts

- **NAT Phoenix Plugin**: One YAML config block enables full tracing - no manual instrumentation
- **Token Factory Pricing**: `cost = (input_tokens × rate) + (output_tokens × rate)` per 1M tokens
- **`response.usage`**: vLLM returns token counts with every API response - the basis for cost tracking
- **Hyperparameter optimization**: Systematic search for optimal model parameters
