# Part 2: Orchestrating Pre-built Bielik Agents

**Duration:** 60 minutes (18:30 - 19:30)
**Lead:** Bielik Team

## Overview

In this part you will:

1. **Build a basic ReAct agent** using NeMo Agent Toolkit (NAT) with Bielik
2. **Explore a pre-built LangChain ReAct agent** and register it as a NAT Function
3. **Explore a pre-built CrewAI agent crew** and register it as a NAT Function
4. **Compose both agents** into a unified multi-agent workflow via YAML

## Exercises

### Exercise 1: Basic Agent (15 min)
`01_basic_agent/` - Create a simple ReAct agent that uses Bielik with `wiki_search` and `current_datetime` tools. Learn NAT's YAML configuration and `nat run` CLI.

### Exercise 2: LangChain Agent (10 min)
`02_langchain_agent/` - A pre-built LangChain ReAct research agent. Register it as a NAT Function so it can be composed with other agents.

### Exercise 3: CrewAI Agent Crew (10 min)
`03_crewai_agent/` - A pre-built CrewAI crew with analyst and writer roles. Register it as a NAT Function.

### Exercise 4: Unified Workflow (25 min)
`04_unified_workflow/` - Compose the LangChain research agent and CrewAI writing crew into a single NAT workflow via YAML. The research agent gathers information, then the writing crew produces a structured report.

## Key Concepts

- **NAT Function**: A wrapper that makes any agent (LangChain, CrewAI, custom) composable within NAT workflows
- **YAML Workflow**: Declarative configuration that defines LLMs, functions, and how they connect
- **`nat run`**: CLI command to execute a workflow from a config file
- **`nat serve`**: Deploy a workflow as an API server
- **ReAct**: Text-based reasoning + action loop - no native tool calling required
