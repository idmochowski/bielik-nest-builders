"""
LangChain ReAct Research Agent - registered as a NeMo Agent Toolkit Function.

This module creates a LangChain ReAct agent that can search Wikipedia.
It is wrapped as a NAT Function so it can be composed with other agents
(e.g., CrewAI) in a unified workflow.
"""

from typing import List
from pydantic import BaseModel, Field

from nat.cli.register_workflow import register_function
from nat.builder.function_info import FunctionInfo
from nat.builder.builder import Builder
from nat.builder.framework_enum import LLMFrameworkEnum


class LangChainResearchAgentConfig(BaseModel):
    """Configuration for the LangChain research agent."""

    _type: str = "langchain_research_agent"
    llm_ref: str = Field(description="Reference to the LLM to use")
    tools_ref: List[str] = Field(description="References to tools the agent can use")
    description: str = Field(default="Agent badawczy korzystający z LangChain ReAct")
    max_iterations: int = Field(default=10, description="Max reasoning iterations")


@register_function(
    config_type=LangChainResearchAgentConfig,
    framework_wrappers=[LLMFrameworkEnum.LANGCHAIN],
)
async def langchain_research_agent(_config: LangChainResearchAgentConfig, _builder: Builder):
    """
    Register a LangChain ReAct agent as a NAT Function.

    The agent:
    - Uses Bielik via the OpenAI-compatible vLLM endpoint
    - Has access to Wikipedia search and datetime tools
    - Follows the ReAct pattern: Thought -> Action -> Observation -> repeat
    """

    # Get LLM and tools through the builder - this gives us automatic
    # instrumentation for observability and profiling
    llm = await _builder.get_llm(
        _config.llm_ref,
        wrapper_type=LLMFrameworkEnum.LANGCHAIN,
    )
    tools = await _builder.get_tools(
        _config.tools_ref,
        wrapper_type=LLMFrameworkEnum.LANGCHAIN,
    )

    # Build a standard LangChain ReAct agent
    from langchain import hub
    from langchain.agents import create_react_agent, AgentExecutor

    # ReAct prompt template
    react_prompt = hub.pull("hwchase17/react")

    react_agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=react_prompt,
    )

    agent_executor = AgentExecutor(
        agent=react_agent,
        tools=tools,
        max_iterations=_config.max_iterations,
        handle_parsing_errors=True,
        verbose=True,
    )

    # Define the function that NAT will call
    async def research(question: str) -> str:
        """
        Research a topic using Wikipedia and other tools.

        Args:
            question: The research question to investigate

        Returns:
            Szczegółowa odpowiedź na podstawie badań w Wikipedii
        """
        result = await agent_executor.ainvoke({"input": question})
        return result["output"]

    # Yield FunctionInfo - this is what NAT uses to register the agent
    yield FunctionInfo.from_fn(
        research,
        description="Zbadaj temat korzystając z Wikipedii i innych narzędzi.",
    )
