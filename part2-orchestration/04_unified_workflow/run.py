"""
Exercise 4: Unified Multi-Agent Workflow

Composes agents from TWO different frameworks in one NAT workflow:
    1. LangChain ReAct research agent (from Exercise 2)
    2. CrewAI writing crew (from Exercise 3)

Bielik acts as the orchestrator, deciding which sub-agent to call.

Usage:
    python run.py
    python run.py "Twój temat - zbadaj go i napisz raport"
"""

import subprocess
import sys

DEFAULT_QUERY = (
    "Zbadaj Kopalnię Soli w Wieliczce - jej historię i status UNESCO. "
    "Następnie napisz raport."
)

query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY

print(f"Query: {query}\n")
subprocess.run(["nat", "run", "--config_file", "config.yaml", "--input", query])
