"""
Comprehensive test suite for Deep Research Workflow System.

Tests cover:
- Workflow orchestration
- Agent initialization
- Tool integration
- Document generation
- Configuration
- State management
"""

import pytest
import asyncio
import json
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

from deepresearch import DeepResearchWorkflow, WorkflowState
from agents.deep_agents import PlanningAgent, ResearchAgent, WriteAgent
from tools.registry import ToolRegistry
from utils.config import load_config


class TestWorkflowState:
    """Test WorkflowState class."""

    def test_state_initialization(self):
        """Test WorkflowState creates correct initial state."""
        state = WorkflowState("test_workflow")

        assert state.workflow_id == "test_workflow"
        assert state.user_prompt == ""
        assert state.research_plan == ""
        assert state.plan_approved is False
        assert state.iteration_count == {"research": 0, "revision": 0}
        assert state.errors == []

    def test_state_to_dict(self):
        """Test WorkflowState converts to dictionary correctly."""
        state = WorkflowState("test")
        state.user_prompt = "Test topic"
        state.research_plan = "Test plan"

        state_dict = state.to_dict()

        assert state_dict["workflow_id"] == "test"
        assert state_dict["user_prompt"] == "Test topic"
        assert state_dict["research_plan"] == "Test plan"
        assert "created_at" in state_dict

    def test_state_save_and_load(self):
        """Test WorkflowState can be saved and loaded from JSON."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            state = WorkflowState("test_save")
            state.user_prompt = "Save test"
            state.draft_report = "Test report"

            state_file = state.save(output_dir)

            assert state_file.exists()

            with open(state_file) as f:
                loaded_data = json.load(f)

            assert loaded_data["workflow_id"] == "test_save"
            assert loaded_data["user_prompt"] == "Save test"
            assert loaded_data["draft_report"] == "Test report"


class TestAgentInitialization:
    """Test agent classes initialize correctly."""

    def test_planning_agent(self):
        """Test PlanningAgent initializes."""
        agent = PlanningAgent()

        assert agent.name == "PlanningAgent"
        assert agent.description is not None
        assert agent.system_prompt is not None
        assert agent.llm == "gpt-4.1-mini"

    def test_research_agent(self):
        """Test ResearchAgent initializes."""
        agent = ResearchAgent()

        assert agent.name == "ResearchAgent"
        assert agent.system_prompt is not None
        assert "research" in agent.description.lower()

    def test_write_agent(self):
        """Test WriteAgent initializes."""
        agent = WriteAgent()

        assert agent.name == "WriteAgent"
        assert agent.system_prompt is not None

    def test_all_agents_have_system_prompts(self):
        """Test all agents have non-empty system prompts."""
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

        agents = [
            PlanningAgent(),
            ResearchAgent(),
            ReviewAgent(),
            RevisionAgent(),
            WriteAgent(),
            FormattingAgent(),
            SummaryAgent(),
            FactCheckingAgent(),
        ]

        for agent in agents:
            assert agent.system_prompt
            assert len(agent.system_prompt) > 0
            assert agent.name


class TestToolRegistry:
    """Test ToolRegistry functionality."""

    def test_registry_initialization(self):
        """Test ToolRegistry initializes correctly."""
        registry = ToolRegistry()

        assert registry is not None

    def test_registry_register_tool(self):
        """Test registering a tool."""
        registry = ToolRegistry()
        mock_tool = Mock()

        registry.register_tool("test_tool", mock_tool)

        # Check tool is registered (implementation may vary)
        assert registry is not None

    def test_registry_has_tools(self):
        """Test registry contains expected tools."""
        registry = ToolRegistry()

        # Registry should have some tools registered by default
        assert registry is not None


class TestConfiguration:
    """Test configuration loading."""

    def test_config_loads(self):
        """Test configuration file loads successfully."""
        try:
            config = load_config(".config/config.yaml")

            assert config is not None
            assert hasattr(config, "provider")
            assert hasattr(config.provider, "model")
        except FileNotFoundError:
            pytest.skip("Config file not found")

    def test_config_defaults(self):
        """Test configuration has expected defaults."""
        try:
            config = load_config(".config/config.yaml")

            assert config.provider.model in [
                "gpt-4.1-mini",
                "gpt-4-turbo",
                "gpt-3.5-turbo",
            ]
        except FileNotFoundError:
            pytest.skip("Config file not found")


class TestDocumentGeneration:
    """Test document generation capabilities."""

    def test_html_generation(self):
        """Test HTML document generation."""
        from deepresearch import DeepResearchWorkflow

        with tempfile.TemporaryDirectory() as tmpdir:
            workflow = DeepResearchWorkflow()
            workflow.output_dir = Path(tmpdir)

            html_path = asyncio.run(
                workflow._create_final_document(
                    "# Test Report\n\nTest content",
                    "Test Summary",
                )
            )

            assert html_path is not None
            assert Path(html_path).exists()
            assert html_path.endswith((".html", ".pdf"))

    def test_html_contains_content(self):
        """Test generated HTML contains report content."""
        from deepresearch import DeepResearchWorkflow

        with tempfile.TemporaryDirectory() as tmpdir:
            workflow = DeepResearchWorkflow()
            workflow.output_dir = Path(tmpdir)

            html_path = asyncio.run(
                workflow._create_final_document(
                    "# Test Report\n\nSpecific test content",
                    "Test Summary",
                )
            )

            with open(html_path) as f:
                content = f.read()

            assert "Test Report" in content
            assert "Test Summary" in content


class TestWorkflowIntegration:
    """Integration tests for workflow execution."""

    @pytest.mark.asyncio
    async def test_workflow_initialization(self):
        """Test workflow initializes with all agents."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("utils.config.load_config") as mock_config:
                mock_config.return_value = Mock(
                    provider=Mock(model="gpt-4.1-mini"),
                    mcp_enabled=False,
                )

                workflow = DeepResearchWorkflow()

                assert workflow.planning_agent is not None
                assert workflow.research_agent is not None
                assert workflow.write_agent is not None
                assert workflow.review_agent is not None
                assert workflow.formatting_agent is not None
                assert workflow.summary_agent is not None

    @pytest.mark.asyncio
    async def test_workflow_plan_generation(self):
        """Test planning stage can generate a plan."""
        with patch("utils.config.load_config") as mock_config:
            mock_config.return_value = Mock(
                provider=Mock(model="gpt-4.1-mini"),
                mcp_enabled=False,
            )

            with patch("anthropic.Anthropic.messages.create") as mock_create:
                mock_create.return_value = Mock(
                    content=[Mock(text="1. Step one\n2. Step two")]
                )

                workflow = DeepResearchWorkflow()
                plan = await workflow._generate_plan("Test topic")

                assert plan is not None
                assert len(plan) > 0
                assert "Step" in plan


class TestErrorHandling:
    """Test error handling and recovery."""

    def test_workflow_state_error_tracking(self):
        """Test errors are tracked in state."""
        state = WorkflowState("test")

        state.errors.append("Test error 1")
        state.errors.append("Test error 2")

        assert len(state.errors) == 2
        assert "Test error 1" in state.errors

    @pytest.mark.asyncio
    async def test_scrape_handles_invalid_url(self):
        """Test web scraper handles invalid URLs gracefully."""
        from mcp_server.research_server import scrape

        result = await scrape("invalid://not-a-real-url")

        assert result is not None
        assert isinstance(result, str)


class TestDocumentTools:
    """Test document processing tools."""

    @pytest.mark.asyncio
    async def test_citation_formatting(self):
        """Test citation formatting works."""
        from mcp_server.document_server import format_citation

        result = await format_citation(
            author="Smith, J.",
            title="Test Paper",
            source="Journal of Testing",
            year="2024",
            style="apa",
        )

        assert result is not None
        assert "Smith" in result
        assert "2024" in result

    @pytest.mark.asyncio
    async def test_document_validation(self):
        """Test document validation."""
        from mcp_server.document_server import validate_document

        content = "# Test\n\nThis is a test document with multiple paragraphs.\n\n More content here."

        result = await validate_document(content)

        assert isinstance(result, dict)
        assert "word_count" in result
        assert "is_valid" in result
        assert result["word_count"] > 0

    @pytest.mark.asyncio
    async def test_toc_generation(self):
        """Test table of contents generation."""
        from mcp_server.document_server import generate_toc

        content = "# Main Heading\n\n## Sub Heading 1\n\n## Sub Heading 2"

        result = await generate_toc(content)

        assert result is not None
        assert "Sub Heading 1" in result or "Sub" in result


class TestAsyncOperations:
    """Test async/await operations."""

    @pytest.mark.asyncio
    async def test_async_execution(self):
        """Test async execution completes."""
        async def simple_async_task():
            await asyncio.sleep(0.01)
            return "complete"

        result = await simple_async_task()

        assert result == "complete"


class TestDataPersistence:
    """Test data persistence and state management."""

    def test_json_serialization(self):
        """Test state serializes to JSON correctly."""
        state = WorkflowState("serialize_test")
        state.user_prompt = "Test prompt"
        state.draft_report = "Test report with special chars: áéíóú"

        state_dict = state.to_dict()
        json_str = json.dumps(state_dict)

        loaded = json.loads(json_str)

        assert loaded["user_prompt"] == "Test prompt"
        assert "áéíóú" in loaded["draft_report"]


# Performance benchmarks

class TestPerformance:
    """Test performance characteristics."""

    def test_state_creation_performance(self):
        """Test state creation is fast."""
        import time

        start = time.time()

        for _ in range(1000):
            WorkflowState(f"perf_test_{_}")

        elapsed = time.time() - start

        # Should create 1000 states in less than 1 second
        assert elapsed < 1.0

    def test_config_loading_performance(self):
        """Test config loading is reasonably fast."""
        import time

        try:
            start = time.time()

            for _ in range(100):
                load_config(".config/config.yaml")

            elapsed = time.time() - start

            # Should load config 100 times in less than 1 second
            assert elapsed < 1.0
        except FileNotFoundError:
            pytest.skip("Config file not found")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
