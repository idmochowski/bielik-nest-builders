"""
Exercise 2: LangChain ReAct Agent as NAT Function

A LangChain ReAct research agent registered as a NAT Function
via @register_function. See functions.py for the implementation.

Key pattern:
    @register_function(config_type=..., framework_wrappers=[LLMFrameworkEnum.LANGCHAIN])
    async def langchain_research_agent(_config, _builder):
        llm = await _builder.get_llm(...)
        tools = await _builder.get_tools(...)
        # ... standard LangChain agent code ...
        yield FunctionInfo.from_fn(research, description="...")

Usage:
    python run.py
    python run.py "Twoje pytanie tutaj"
"""

import subprocess
import sys

DEFAULT_QUERY = "Zbadaj historię sztucznej inteligencji w Polsce."

query = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUERY

print(f"Query: {query}\n")
subprocess.run(["nat", "run", "--config_file", "config.yaml", "--input", query])
