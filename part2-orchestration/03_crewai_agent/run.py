"""
Exercise 3: CrewAI Agent Crew as NAT Function

A CrewAI crew with Analyst + Writer agents, registered as a NAT Function.
See functions.py for the implementation.

CrewAI vs LangChain:
    - LangChain ReAct: single agent, multiple tools, dynamic flow
    - CrewAI Crew: multiple role-based agents, sequential pipeline

Usage:
    python run.py
    python run.py "Twój temat tutaj"
"""

import subprocess
import sys

DEFAULT_QUERY = (
    "Rodzina modeli językowych Bielik: polskie modele LLM zbudowane przez "
    "SpeakLeash, wykorzystujące destylację wiedzy i trenowane na wysokiej "
    "jakości polskich danych tekstowych."
)

query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY

print(f"Query: {query}\n")
subprocess.run(["nat", "run", "--config_file", "config.yaml", "--input", query])
