"""
Unified workflow functions.

Both custom agents are registered via the workshop_agents package
(installed as a NAT plugin via pyproject.toml entry points).
This file is kept for reference only - NAT discovers the functions
automatically through the nat.components entry point.
"""

from workshop_agents.langchain_research_agent import langchain_research_agent  # noqa: F401
from workshop_agents.crewai_writing_crew import crewai_writing_crew  # noqa: F401
