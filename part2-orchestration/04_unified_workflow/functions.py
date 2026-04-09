"""
Unified workflow functions.

This file re-exports the functions from Exercise 2 and 3 so they are
discoverable by NAT when running this config.

In a real project, these would be in a proper Python package with
entry points configured in pyproject.toml.
"""

# Import both registered functions so NAT can discover them
import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "02_langchain_agent"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "03_crewai_agent"))

from functions import langchain_research_agent  # noqa: E402, F401
from functions import crewai_writing_crew  # noqa: E402, F401
