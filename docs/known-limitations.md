# Known Limitations

## Agent-in-Agent Orchestration with 7B Models

Exercises 2-4 wrap custom agents (LangChain, CrewAI) as NAT Functions inside a `react_agent` workflow. This creates a two-level agent pattern: an outer orchestrator agent that calls inner sub-agents as tools.

**The issue:** Bielik-Minitron-7B sometimes struggles with this pattern because:
- The outer ReAct agent must decide when to call the inner agent and how to use its output
- 7B models can loop (calling the same tool repeatedly) or fail to produce a `Final Answer`
- Broad queries ("Zbadaj historię Krakowa") are more prone to this than focused ones ("Kim był Chopin?")

**In production, this is solved by using a larger orchestrator model** (e.g., Bielik-11B, GPT-4o, or a dedicated routing model) to coordinate multiple smaller specialist agents. The orchestrator handles routing and synthesis while the 7B agents handle domain-specific tasks.

**Workshop workarounds:**
- Use focused, specific queries instead of broad ones
- `additional_instructions` in the config steers the agent toward quick convergence
- `parse_agent_response_max_retries: 3` and `raise_on_parsing_failure: false` add resilience
- `max_tool_calls: 5` prevents runaway loops

**This is a good teaching moment:** Production multi-agent systems rarely use the same model for orchestration and execution. The workshop demonstrates *why* that separation matters.
