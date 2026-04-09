"""
Exercise 1: Basic ReAct Agent with Bielik

Demonstrates NAT's YAML-first workflow configuration.
The agent uses wiki_search and current_datetime tools
with the ReAct reasoning pattern.

Usage:
    python run.py
    python run.py "Twoje pytanie tutaj"
"""

import subprocess
import sys

DEFAULT_QUERY = "Kim był Mikołaj Kopernik i jaki był jego główny wkład w naukę?"

query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY

print(f"Query: {query}\n")
subprocess.run(["nat", "run", "--config_file", "config.yaml", "--input", query])
