"""
CrewAI Writing Crew - registered as a NeMo Agent Toolkit Function.

This module creates a CrewAI crew with two agents:
- Analyst: Examines the input and extracts key insights
- Writer: Takes the analysis and produces a structured report

The crew is wrapped as a NAT Function for composition with other agents.
"""

from pydantic import Field

from nat.cli.register_workflow import register_function
from nat.builder.function_info import FunctionInfo
from nat.builder.builder import Builder
from nat.data_models.function import FunctionBaseConfig
from nat.data_models.component_ref import LLMRef


class CrewAIWritingCrewConfig(FunctionBaseConfig, name="crewai_writing_crew"):
    """Configuration for the CrewAI writing crew."""

    llm_ref: LLMRef = Field(description="Reference to the LLM to use")
    description: str = Field(default="Zespół CrewAI do analizy i pisania raportów")


@register_function(
    config_type=CrewAIWritingCrewConfig,
)
async def crewai_writing_crew(_config: CrewAIWritingCrewConfig, _builder: Builder):
    """
    Register a CrewAI crew as a NAT Function.

    The crew consists of:
    - Analyst agent: breaks down research findings into key points
    - Writer agent: composes a structured report from the analysis
    """

    from crewai import Agent, Task, Crew, Process, LLM

    import os

    # Configure CrewAI to use Bielik via vLLM
    bielik_llm = LLM(
        model=f"openai/{os.getenv('VLLM_MODEL_NAME')}",
        base_url=os.getenv("VLLM_BASE_URL"),
        api_key=os.getenv("VLLM_API_KEY"),
        temperature=0.7,
        max_tokens=2048,
    )

    # --- Define Agents ---

    analyst = Agent(
        role="Analityk",
        goal="Przeanalizuj dostarczone informacje i wyodrębnij kluczowe wnioski, trendy i ważne fakty",
        backstory=(
            "Jesteś doświadczonym analitykiem badawczym, który potrafi rozkładać "
            "złożone tematy na jasne, uporządkowane wnioski. Koncentrujesz się na "
            "dokładności i identyfikowaniu najważniejszych punktów."
        ),
        llm=bielik_llm,
        verbose=True,
    )

    writer = Agent(
        role="Redaktor raportów",
        goal="Przekształć analizę w dobrze uporządkowany, czytelny raport",
        backstory=(
            "Jesteś profesjonalnym redaktorem technicznym, który doskonale "
            "przekształca surową analizę w dopracowane, uporządkowane raporty. "
            "Stosujesz czytelne nagłówki, punktory i zwięzły język."
        ),
        llm=bielik_llm,
        verbose=True,
    )

    # Define the callable function for NAT
    async def write_report(research_input: str) -> str:
        """
        Analyze research findings and produce a structured report.

        Args:
            research_input: Raw research findings or topic description to analyze and write about

        Returns:
            A structured report with analysis and insights
        """

        # --- Define Tasks ---
        analysis_task = Task(
            description=(
                f"Przeanalizuj poniższe dane wejściowe i wyodrębnij kluczowe wnioski:\n\n"
                f"{research_input}\n\n"
                "Podaj: 1) Główne ustalenia 2) Kluczowe fakty 3) Istotne trendy lub wzorce"
            ),
            expected_output="Uporządkowana analiza z kluczowymi wnioskami, faktami i trendami",
            agent=analyst,
        )

        writing_task = Task(
            description=(
                "Na podstawie ustaleń analityka napisz uporządkowany raport zawierający:\n"
                "- Streszczenie (2-3 zdania)\n"
                "- Kluczowe ustalenia (punktory)\n"
                "- Szczegółowa analiza\n"
                "- Wnioski końcowe"
            ),
            expected_output="Dopracowany raport w formacie markdown",
            agent=writer,
        )

        # --- Assemble and Run Crew ---
        crew = Crew(
            agents=[analyst, writer],
            tasks=[analysis_task, writing_task],
            process=Process.sequential,
            verbose=True,
        )

        result = crew.kickoff()
        return str(result)

    yield FunctionInfo.from_fn(
        write_report,
        description=_config.description,
    )
