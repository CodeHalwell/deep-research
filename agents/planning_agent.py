import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from typing import List, Optional
import asyncio

from llama_index.core.agent.workflow import FunctionAgent
from models.agent import Agent

from dotenv import load_dotenv
load_dotenv()

class PlanningAgent(Agent):
    def __init__(
        self,
        name: str = "EnhancerAgent",
        description: str = "Useful for enhancing the content",
        system_prompt: str = (
            """
            Create a detailed, step-by-step plan to thoroughly research and analyze the topic of [INSERT TOPIC HERE].
            The plan should include:
            Steps for identifying key areas of focus and the most relevant aspects of the topic.
            How to search for and collect important sources of information (such as research papers, reports, news articles, or data).
            Actions for summarizing and organizing key findings, including comparisons where relevant.
            Guidance on identifying leading experts, organizations, or companies involved in the area.
            Suggestions for benchmarking, best practices, and identifying open questions or challenges.
            Consider additional angles such as historical context, current trends, future directions.
            Consider the positive and negative aspects of the topic, including potential benefits, risks, and ethical considerations.
            Structure the plan as a numbered list of steps, with each step briefly explaining what should be done and what information should be gathered at that stage.
            Example:
                (1) Analyze current research and real-world applications related to [TOPIC], focusing on the latest developments in the field.
                (2) Search for recent academic publications, preprints, industry reports, or technical documentation pertaining to [TOPIC].
                (3) For the approaches, methods, or technologies identified in the initial analysis, conduct targeted literature and patent searches to find advanced, state-of-the-art techniques and notable use-cases, especially those with strong experimental or practical validation.
                (4) For each significant method, case study, or solution found, gather and synthesize the following information:
                (a) The title and a summary of the key methodology or approach.
                (b) The data sources, features, or tools used (customize this point to fit the topic: e.g., datasets, instruments, frameworks).
                (c) Performance metrics or evaluation criteria reported (customize this to suit the field: e.g., accuracy, speed, ROI) and how these compare with alternative approaches.
                (d) Notable challenges, limitations, or open questions highlighted by the authors or practitioners.
                (5) Identify major research groups, organizations, companies, or consortia working on [TOPIC], and review their recent projects, publications, and any available opportunities for collaboration or partnership.
                (6) Review benchmarking studies, comparative analyses, and open datasets or tools relevant to [TOPIC], summarizing best practices for evaluation and comparing results across different approaches or solutions.
            Do not simply copy the structure of the example above; instead, adapt your plan thoughtfully based on the unique characteristics of the topic. Consider other relevant angles, questions, or lines of inquiry that would help achieve a comprehensive understanding, even if they are not explicitly included in the sample steps.
            """
        ),
        llm: str = "gpt-4.1-mini",
        tools: Optional[List[str]] = None,
        can_handoff_to: Optional[List[str]] = None
    ) -> None:
        if tools is None:
            tools = []
        if can_handoff_to is None:
            can_handoff_to = []
        super().__init__(name, description, system_prompt, llm, tools, can_handoff_to)

    def build_agent(self, api_key, config_path) -> FunctionAgent:
        """Builds the agent with the provided parameters."""
        return FunctionAgent(
            name=self.name,
            description=self.description,
            system_prompt=self.system_prompt,
            llm=self._get_llm_server(api_key=api_key, config_path=config_path),
            tools=[],
            can_handoff_to=self.can_handoff_to
        )
    
pa = PlanningAgent()

planning_agent = pa.build_agent(
    api_key=os.getenv("OPENAI_API_KEY"),
    config_path=".config/config.yaml")

async def main():
    result = await planning_agent.run(
        "retention time prediction using GNN's"
    )
    print(result)

asyncio.run(main())