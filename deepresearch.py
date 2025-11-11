"""
Deep Research Workflow System - Core orchestration engine.

This module implements the main workflow that coordinates multiple AI agents
to conduct comprehensive research and generate professional reports.
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import logging

from anthropic import Anthropic
from agents.deep_agents import (
    PlanningAgent,
    ResearchAgent,
    ReviewAgent,
    RevisionAgent,
    WriteAgent,
    FormattingAgent,
    SummaryAgent,
    FactCheckingAgent,
)
from tools.registry import ToolRegistry
from models.agent import Agent
from utils.config import load_config
from utils.logging import setup_logger


class WorkflowState:
    """Manages the state of a research workflow execution."""

    def __init__(self, workflow_id: str):
        self.workflow_id = workflow_id
        self.created_at = datetime.now()
        self.user_prompt = ""
        self.research_plan = ""
        self.plan_approved = False
        self.research_notes = ""
        self.draft_report = ""
        self.review_feedback = ""
        self.revised_report = ""
        self.formatted_report = ""
        self.summary = ""
        self.final_document_path = ""
        self.iteration_count = {"research": 0, "revision": 0}
        self.errors = []
        self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert state to dictionary for serialization."""
        return {
            "workflow_id": self.workflow_id,
            "created_at": self.created_at.isoformat(),
            "user_prompt": self.user_prompt,
            "research_plan": self.research_plan,
            "plan_approved": self.plan_approved,
            "research_notes": self.research_notes,
            "draft_report": self.draft_report,
            "review_feedback": self.review_feedback,
            "revised_report": self.revised_report,
            "formatted_report": self.formatted_report,
            "summary": self.summary,
            "final_document_path": self.final_document_path,
            "iteration_count": self.iteration_count,
            "errors": self.errors,
            "metadata": self.metadata,
        }

    def save(self, output_dir: Path):
        """Save state to JSON file."""
        output_dir.mkdir(parents=True, exist_ok=True)
        state_file = output_dir / f"workflow_{self.workflow_id}.json"
        with open(state_file, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        return state_file


class DeepResearchWorkflow:
    """
    Main orchestrator for the Deep Research Workflow System.

    Coordinates multiple AI agents to conduct comprehensive research,
    generate reports, and produce professional documents.
    """

    def __init__(self, config_path: str = ".config/config.yaml"):
        """Initialize the workflow with configuration."""
        self.logger = setup_logger("DeepResearchWorkflow")
        self.config = load_config(config_path)
        self.tool_registry = ToolRegistry()
        self.client = Anthropic()
        self.output_dir = Path("output")
        self.max_iterations = int(os.getenv("MAX_ITERATIONS", 3))

        # Initialize agents
        self._initialize_agents()

    def _initialize_agents(self):
        """Initialize all agent instances."""
        self.planning_agent = PlanningAgent()
        self.research_agent = ResearchAgent()
        self.write_agent = WriteAgent()
        self.review_agent = ReviewAgent()
        self.revision_agent = RevisionAgent()
        self.formatting_agent = FormattingAgent()
        self.summary_agent = SummaryAgent()
        self.factchecking_agent = FactCheckingAgent()

        self.logger.info("All agents initialized successfully")

    async def execute(self, user_prompt: str) -> Dict[str, Any]:
        """
        Execute the complete research workflow.

        Args:
            user_prompt: The user's research topic/question

        Returns:
            Dictionary containing workflow results and output path
        """
        # Create workflow state
        workflow_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        state = WorkflowState(workflow_id)
        state.user_prompt = user_prompt

        self.logger.info(f"Starting workflow {workflow_id} for: {user_prompt}")

        try:
            # Step 1: Generate research plan
            self.logger.info("Step 1: Generating research plan...")
            state.research_plan = await self._generate_plan(user_prompt)
            self.logger.debug(f"Generated plan:\n{state.research_plan}")

            # Step 2: Human review of plan
            self.logger.info("Step 2: Awaiting human approval of plan...")
            state.plan_approved = self._get_user_approval(
                "Research Plan",
                state.research_plan,
            )

            if not state.plan_approved:
                self.logger.info("Plan rejected by user. Workflow cancelled.")
                return {"status": "cancelled", "reason": "Plan rejected by user"}

            # Step 3: Execute research
            self.logger.info("Step 3: Executing research plan...")
            state.research_notes = await self._execute_research(
                user_prompt,
                state.research_plan,
            )
            self.logger.debug(f"Research notes length: {len(state.research_notes)}")

            # Step 4: Write report
            self.logger.info("Step 4: Writing report...")
            state.draft_report = await self._write_report(
                user_prompt,
                state.research_notes,
            )
            self.logger.debug(f"Draft report length: {len(state.draft_report)}")

            # Step 5: Review and revision loop
            self.logger.info("Step 5: Review and revision loop...")
            state.revised_report = await self._review_and_revise(
                state.draft_report,
                state,
            )

            # Step 6: Fact-check
            self.logger.info("Step 6: Fact-checking report...")
            fact_check_notes = await self._fact_check(state.revised_report)
            self.logger.debug(f"Fact-check completed")

            # Step 7: Format document
            self.logger.info("Step 7: Formatting document...")
            state.formatted_report = await self._format_document(
                state.revised_report
            )

            # Step 8: Generate summary
            self.logger.info("Step 8: Generating summary...")
            state.summary = await self._generate_summary(state.formatted_report)

            # Step 9: Create final document
            self.logger.info("Step 9: Creating final document...")
            state.final_document_path = await self._create_final_document(
                state.formatted_report,
                state.summary,
            )

            self.logger.info(
                f"Workflow {workflow_id} completed successfully. "
                f"Output: {state.final_document_path}"
            )

            # Save state
            state_file = state.save(self.output_dir)

            return {
                "status": "success",
                "workflow_id": workflow_id,
                "output_path": state.final_document_path,
                "state_file": str(state_file),
                "summary": state.summary,
            }

        except Exception as e:
            self.logger.error(f"Workflow {workflow_id} failed: {str(e)}")
            state.errors.append(str(e))
            state.save(self.output_dir)
            raise

    async def _generate_plan(self, user_prompt: str) -> str:
        """Generate research plan using planning agent."""
        system_prompt = self.planning_agent.system_prompt.replace(
            "[INSERT TOPIC HERE]", user_prompt
        )

        message = self.client.messages.create(
            model=self.config.provider.model,
            max_tokens=2000,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Create a comprehensive research plan for: {user_prompt}",
                }
            ],
        )

        return message.content[0].text

    async def _execute_research(self, user_prompt: str, plan: str) -> str:
        """Execute research using research agent."""
        message = self.client.messages.create(
            model=self.config.provider.model,
            max_tokens=3000,
            system=self.research_agent.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Topic: {user_prompt}\n\n"
                        f"Research Plan:\n{plan}\n\n"
                        "Please conduct thorough research following this plan "
                        "and provide detailed notes with sources."
                    ),
                }
            ],
        )

        research_text = message.content[0].text

        return research_text

    async def _write_report(self, user_prompt: str, research_notes: str) -> str:
        """Generate draft report using write agent."""
        message = self.client.messages.create(
            model=self.config.provider.model,
            max_tokens=4000,
            system=self.write_agent.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Topic: {user_prompt}\n\n"
                        f"Research Notes:\n{research_notes}\n\n"
                        "Please write a comprehensive, well-structured report "
                        "based on these research notes."
                    ),
                }
            ],
        )

        return message.content[0].text

    async def _review_and_revise(self, draft: str, state: WorkflowState) -> str:
        """Review and revise report with iteration limit."""
        current_report = draft
        max_revisions = self.max_iterations

        for iteration in range(max_revisions):
            state.iteration_count["revision"] = iteration + 1

            # Review
            self.logger.info(f"Review iteration {iteration + 1}/{max_revisions}")
            review = self.client.messages.create(
                model=self.config.provider.model,
                max_tokens=2000,
                system=self.review_agent.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Please review this report and provide constructive feedback:\n\n"
                            f"{current_report}"
                        ),
                    }
                ],
            )

            feedback = review.content[0].text
            state.review_feedback = feedback

            # Check if report is good enough
            if (
                "excellent" in feedback.lower()
                or "no major issues" in feedback.lower()
                or "ready to publish" in feedback.lower()
            ):
                self.logger.info("Report approved after review")
                return current_report

            # Revise based on feedback
            self.logger.info(f"Revising report based on feedback...")
            revision = self.client.messages.create(
                model=self.config.provider.model,
                max_tokens=4000,
                system=self.revision_agent.system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Original Report:\n{current_report}\n\n"
                            f"Review Feedback:\n{feedback}\n\n"
                            "Please revise the report based on this feedback."
                        ),
                    }
                ],
            )

            current_report = revision.content[0].text

        self.logger.warning(
            f"Reached max revisions ({max_revisions}). "
            "Escalating for human review."
        )

        # Escalation: ask user for approval
        user_approved = self._get_user_approval(
            "Report After Max Revisions",
            current_report,
            state.review_feedback,
        )

        if not user_approved:
            raise RuntimeError("Report rejected by user after max revisions")

        return current_report

    async def _fact_check(self, report: str) -> str:
        """Perform fact-checking on the report."""
        message = self.client.messages.create(
            model=self.config.provider.model,
            max_tokens=2000,
            system=self.factchecking_agent.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Please fact-check this report:\n\n{report}",
                }
            ],
        )

        return message.content[0].text

    async def _format_document(self, report: str) -> str:
        """Format document using formatting agent."""
        message = self.client.messages.create(
            model=self.config.provider.model,
            max_tokens=4000,
            system=self.formatting_agent.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Please format this report with proper structure, "
                        f"headings, and professional styling:\n\n{report}"
                    ),
                }
            ],
        )

        return message.content[0].text

    async def _generate_summary(self, report: str) -> str:
        """Generate executive summary using summary agent."""
        message = self.client.messages.create(
            model=self.config.provider.model,
            max_tokens=1000,
            system=self.summary_agent.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"Please create an executive summary of this report:\n\n{report}"
                    ),
                }
            ],
        )

        return message.content[0].text

    async def _create_final_document(
        self,
        formatted_report: str,
        summary: str,
    ) -> str:
        """
        Create final formatted document (HTML/PDF).

        Args:
            formatted_report: The formatted report content
            summary: The executive summary

        Returns:
            Path to the generated document
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create HTML document
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_path = self.output_dir / f"report_{timestamp}.html"

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Report</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            background-color: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        .summary {{
            background-color: #ecf0f1;
            padding: 15px;
            border-left: 4px solid #3498db;
            margin: 20px 0;
        }}
        .timestamp {{
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        code {{
            background-color: #f8f8f8;
            padding: 2px 6px;
            border-radius: 3px;
        }}
        pre {{
            background-color: #f8f8f8;
            padding: 10px;
            border-radius: 3px;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Research Report</h1>
        <p class="timestamp">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="summary">
            <h2>Executive Summary</h2>
            {summary}
        </div>

        <h2>Full Report</h2>
        {formatted_report}
    </div>
</body>
</html>
"""

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        self.logger.info(f"HTML document created: {html_path}")

        # Try to create PDF if weasyprint is available
        pdf_path = None
        try:
            from weasyprint import HTML

            pdf_path = self.output_dir / f"report_{timestamp}.pdf"
            HTML(string=html_content).write_pdf(str(pdf_path))
            self.logger.info(f"PDF document created: {pdf_path}")
            return str(pdf_path)
        except ImportError:
            self.logger.warning(
                "WeasyPrint not available. Using HTML output instead."
            )
            return str(html_path)

    def _get_user_approval(
        self,
        item_name: str,
        content: str,
        additional_info: str = "",
    ) -> bool:
        """
        Get human approval for a workflow item.

        Args:
            item_name: Name of the item for approval
            content: Content to display for approval
            additional_info: Additional context information

        Returns:
            True if approved, False if rejected
        """
        print("\n" + "=" * 80)
        print(f"HUMAN APPROVAL REQUIRED: {item_name}")
        print("=" * 80)

        if additional_info:
            print(f"\nContext:\n{additional_info}\n")

        print(f"\n{item_name}:\n")
        # Show truncated content if too long
        if len(content) > 2000:
            print(content[:2000] + "\n\n[... truncated ...]")
        else:
            print(content)

        print("\n" + "=" * 80)
        while True:
            response = (
                input("Do you approve? (yes/no/show_full): ").strip().lower()
            )
            if response in ["yes", "y"]:
                print("✓ Approved by user\n")
                return True
            elif response in ["no", "n"]:
                print("✗ Rejected by user\n")
                return False
            elif response == "show_full":
                print(f"\n{content}\n")
            else:
                print("Please respond with 'yes', 'no', or 'show_full'")
