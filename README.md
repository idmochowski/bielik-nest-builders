# Bielik Nest Builders Workshop

Hands-on workshop: Build, orchestrate, profile and optimize multi-agent AI workflows using **NVIDIA NeMo Agent Toolkit** and **Bielik-Minitron-7B**.

## Architecture

```
+------------------+     +--------------------+     +------------------+
|   Run:ai         |     |   vLLM Server      |     |  NeMo Agent      |
|   Workspace      |---->|   Bielik-Minitron  |<----|  Toolkit (NAT)   |
|   (Jupyter/Code) |     |   7B + Tool Calling|     |  Orchestration   |
+------------------+     +--------------------+     +------------------+
                                                           |
                                              +------------+------------+
                                              |            |            |
                                         LangChain    CrewAI      Phoenix
                                         ReAct Agent  Agent Crew  Tracing
```

## What You'll Build

1. **Basic agent** - ReAct agent with Bielik via NeMo Agent Toolkit
2. **LangChain ReAct agent** - Research agent registered as a NAT Function
3. **CrewAI agent crew** - Analyst + Writer crew registered as a NAT Function
4. **Unified multi-agent workflow** - Both agents composed via YAML config
5. **Observable, profiled workflow** - Phoenix tracing, cost tracking, optimization

## Agenda

| Time  | Session | Lead |
|-------|---------|------|
| 17:30 | Arrival & check-in + refreshments | |
| 17:50 | Welcome & Intro | |
| 18:00 | Run:ai intro & workspace setup | Beyond |
| 18:30 | Orchestrating pre-built Bielik agents | Bielik Team |
| 19:30 | Break & Food | |
| 19:50 | Profiling, optimizing & tracking multi-agent workflows | NVIDIA |
| 20:30 | Networking | |
| 21:30 | Closing | |

## Prerequisites

- Web browser (Chrome/Firefox recommended)
- Run:ai workspace credentials (provided at check-in)
- Basic Python knowledge

Everything else is pre-installed in your Run:ai workspace.

## Repository Structure

```
bielik-nest-builders/
├── docs/
│   └── vllm-deployment.md          # vLLM config for infra team
├── part1-setup/
│   └── verify_setup.py             # Verify connectivity to Bielik endpoint
├── part2-orchestration/             # [18:30-19:30] Bielik Team
│   ├── 01_basic_agent/             # Basic ReAct agent with NAT
│   ├── 02_langchain_agent/         # LangChain agent as NAT Function
│   ├── 03_crewai_agent/            # CrewAI crew as NAT Function
│   └── 04_unified_workflow/        # Compose agents into unified workflow
├── part3-profiling/                 # [19:50-20:30] NVIDIA
│   ├── 01_observability/           # Phoenix tracing setup
│   ├── 02_cost_tracking/           # Token usage & cost analysis
│   └── 03_optimization/            # Hyperparameter optimization
├── requirements.txt
└── .env.example
```

## Quick Start

Once in your Run:ai workspace:

```bash
# 1. Clone the repo
git clone <repo-url>
cd bielik-nest-builders

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate

# 3. Install dependencies (use uv for faster, reliable resolution)
pip install uv
uv pip install --prerelease=allow -r requirements.txt

# 4. Configure endpoint
cp .env.example .env
# Edit .env with the Bielik endpoint URL and API key provided by Beyond

# 5. Verify setup
python part1-setup/verify_setup.py
```

> **Note:** We use `uv` with `--prerelease=allow` because `arize-phoenix` requires
> a pre-release dependency (`graphql-core`), and `nvidia-nat-langchain` has deep
> dependency trees that cause pip's resolver to fail. `uv` handles this in seconds.

## Bielik Model Configuration

The workshop uses **Bielik-Minitron-7B-v3.0-Instruct** served via vLLM with tool calling enabled.

**Key parameters:**
- Model: `speakleash/Bielik-Minitron-7B-v3.0-Instruct`
- Chat format: ChatML (`<|im_start|>`, `<|im_end|>`)
- Tool calling: Enabled via `bielik-tools` parser
- Context window: 32,768 tokens
- Recommended temperature: 0.7
- Recommended max_tokens: 2048 (per agent call)

See [docs/vllm-deployment.md](docs/vllm-deployment.md) for full deployment details.

## Tech Stack

- [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit) - Agent orchestration
- [Bielik-Minitron-7B](https://huggingface.co/speakleash/Bielik-Minitron-7B-v3.0-Instruct) - Polish-optimized LLM
- [vLLM](https://github.com/vllm-project/vllm) - High-performance inference server
- [LangChain](https://github.com/langchain-ai/langchain) - Agent framework
- [CrewAI](https://github.com/crewAIInc/crewAI) - Multi-agent framework
- [Phoenix](https://github.com/Arize-AI/phoenix) - Observability & tracing
- [Run:ai](https://www.run.ai/) - GPU orchestration platform
