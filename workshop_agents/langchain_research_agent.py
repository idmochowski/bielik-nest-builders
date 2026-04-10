"""
LangChain Research Agent - registered as a NeMo Agent Toolkit Function.

Uses langchain.agents.create_agent (LangGraph-based) to build a research
agent that can search Wikipedia. Wrapped as a NAT Function for composition.
"""

from typing import List
from pydantic import Field

from nat.cli.register_workflow import register_function
from nat.builder.function_info import FunctionInfo
from nat.builder.builder import Builder
from nat.builder.framework_enum import LLMFrameworkEnum
from nat.data_models.function import FunctionBaseConfig
from nat.data_models.component_ref import FunctionRef, LLMRef


class LangChainResearchAgentConfig(FunctionBaseConfig, name="langchain_research_agent"):
    """Configuration for the LangChain research agent."""

    llm_ref: LLMRef = Field(description="Reference to the LLM to use")
    tools_ref: List[FunctionRef] = Field(description="References to tools the agent can use")
    description: str = Field(default="Agent badawczy korzystający z LangChain")
    max_iterations: int = Field(default=10, description="Max reasoning iterations")


@register_function(
    config_type=LangChainResearchAgentConfig,
    framework_wrappers=[LLMFrameworkEnum.LANGCHAIN],
)
async def langchain_research_agent(_config: LangChainResearchAgentConfig, _builder: Builder):
    """
    Register a LangChain agent as a NAT Function.

    Uses langchain.agents.create_agent which builds a LangGraph-based
    tool-calling agent under the hood.
    """

    llm = await _builder.get_llm(
        _config.llm_ref,
        wrapper_type=LLMFrameworkEnum.LANGCHAIN,
    )
    tools = await _builder.get_tools(
        _config.tools_ref,
        wrapper_type=LLMFrameworkEnum.LANGCHAIN,
    )

    from langchain.agents import create_agent

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt="Jesteś pomocnym asystentem badawczym. Odpowiadaj po polsku.",
    )

    async def research(question: str) -> str:
        """
        Research a topic using Wikipedia and other tools.

        Args:
            question: The research question to investigate

        Returns:
            Szczegółowa odpowiedź na podstawie badań w Wikipedii
        """
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": question}]},
            config={"recursion_limit": _config.max_iterations * 2},
        )
        return result["messages"][-1].content

    yield FunctionInfo.from_fn(
        research,
        description="Zbadaj temat korzystając z Wikipedii i innych narzędzi.",
    )
