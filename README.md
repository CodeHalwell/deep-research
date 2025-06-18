# Deep Research Workflow System

An intelligent, agent-based research automation system that conducts comprehensive research, generates high-quality reports, and delivers professionally formatted documents with human-in-the-loop quality control.

## 🎯 Overview

The Deep Research Workflow system automates the entire research-to-report pipeline using multiple AI agents, modular tool servers, and strategic human oversight points. From initial prompt to final PDF, the system ensures accuracy, comprehensiveness, and professional presentation while maintaining human control over critical decisions.

## ✨ Key Features

- **Multi-Agent Architecture**: Specialized agents for planning, research, writing, review, and formatting
- **Comprehensive Research Sources**: Web search, academic databases (arXiv, PubMed, Google Scholar), and fact-based resources
- **Human-in-the-Loop Control**: Strategic review points for plan approval and quality assurance
- **Professional Document Generation**: Automated formatting, citation management, and PDF output
- **Quality Assurance**: Built-in review cycles with automatic escalation when needed
- **Modular Tool Servers**: Extensible MCP-based architecture for research and document processing tools

## 🏗️ System Architecture

### Core Components

1. **Planning Agent** - Analyzes user prompts and generates structured research plans
2. **Research Agent** - Executes research using multiple data sources and tools
3. **Senior Research Agent** - Validates research quality and completeness
4. **Write Agent** - Drafts comprehensive reports from gathered research
5. **Review Agent** - Evaluates draft quality and flags necessary corrections
6. **Revision Agent** - Implements feedback and improvements
7. **Formatting Agent** - Applies professional styling and document templates
8. **Summary Agent** - Generates executive summaries and key takeaways

### Tool Servers (MCP)

**Research Tool Server**
- Web Search (DuckDuckGo, Tavily)
- Academic Search (Google Scholar, Semantic Scholar, arXiv, PubMed, OpenAlex, Crossref)
- Knowledge Bases (Wikipedia, Wikidata)
- Web Scraping capabilities

**Document Tool Server**
- Citation formatting and management
- Template engines and styling
- Chart and table generation
- Format conversion (PDF, DOCX)
- Quality checklists and validation

## 🚀 Workflow

![Workflow](images/Deep%20Research%20Workflow.png)

## 🛠️ Technology Stack

- **Language**: Python 3.12+
- **AI Framework**: LlamaIndex (agent orchestration)
- **LLM**: OpenAI GPT-4.1-mini
- **Tool Servers**: Gradio MCP
- **Research APIs**: SerpAPI, Tavily, DuckDuckGo Search
- **Document Processing**: Jinja2, Pandas, Matplotlib/Plotly
- **PDF Generation**: WeasyPrint/pdfkit
- **Testing**: pytest, pytest-asyncio

## 📁 Project Structure

```
DeepResearch/
├── agents/                    # AI agent implementations
│   ├── planning_agent.py     # Research plan generation
│   ├── research_agent.py     # Data gathering and synthesis
│   ├── write_agent.py        # Report drafting
│   ├── review_agent.py       # Quality assessment
│   ├── revision_agent.py     # Feedback implementation
│   ├── formatting_agent.py   # Document styling
│   └── summary_agent.py      # Executive summary generation
├── mcp_server/               # MCP tool server implementation
├── tools/                    # Research and document tools
│   ├── web_search.py         # Web search capabilities
│   ├── document_tools.py     # Document processing
│   ├── literature_tools.py   # Academic search tools
│   └── context_tools.py      # Context management
├── models/                   # Data models and schemas
├── utils/                    # Configuration and utilities
├── test/                     # Test suite
├── notebooks/                # Development notebooks
└── data/                     # Data storage and cache
```

## 🔧 Installation

### Prerequisites
- Python 3.12 or higher
- API keys for research services (OpenAI, SerpAPI, etc.)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DeepResearch
   ```

2. **Install dependencies using uv (recommended)**
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install -e .
   ```

3. **Environment Configuration**
   Create a `.env` file with your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   SERPAPI_API_KEY=your_serpapi_key
   TAVILY_API_KEY=your_tavily_key
   # Add other API keys as needed
   ```

## 🚀 Usage

### Quick Start

```python
from deepresearch import DeepResearchWorkflow

# Initialize the workflow
workflow = DeepResearchWorkflow()

# Submit a research prompt
prompt = "Analyze the current state of quantum computing and its potential impact on cybersecurity"

# Execute the workflow (with human review points)
result = await workflow.execute(prompt)

# Access the final report
print(f"Report saved to: {result.output_path}")
```

### Human-in-the-Loop Control Points

1. **Plan Review**: After the planning agent generates a research plan, you'll be prompted to review and approve it
2. **Quality Gates**: The system will escalate to you if automated quality checks fail after 3 iterations
3. **Final Review**: Optional review before document finalization

## 🧪 Testing

Run the test suite:
```bash
pytest test/
```

For async tests:
```bash
pytest test/ -v --asyncio-mode=auto
```

## 📋 Development Status

This project is currently in active development. The following components are planned/in progress:

- [x] Project structure and dependencies
- [x] Technical specification and requirements
- [ ] Core agent implementations
- [ ] MCP tool servers
- [ ] Research tool integrations
- [ ] Document processing pipeline
- [ ] Human-in-the-loop interfaces
- [ ] Quality assurance systems
- [ ] Final document generation
- [ ] Comprehensive testing suite

## 🤝 Contributing

Contributions are welcome! Please see our contributing guidelines for more information.

## 📄 License

[Add your license information here]

## 🎯 Target Users

- **Researchers and Analysts** - Comprehensive research automation
- **Decision Makers** - Executive-level research summaries
- **Content Creators** - Professional report generation
- **Technical Writers** - Structured document workflows

## 🔒 Security & Compliance

- Secure API key management via environment variables
- GDPR-compliant data handling
- Audit logging for all operations
- Configurable data retention policies

## 📚 Documentation

- [User Requirements Specification](Deep%20Research%20URS.md)
- [Technical Specification](Deep%20Research%20Technical%20Specification.md)
- [Workflow Diagram](Deep%20Research%20Workflow.png)

## 🆘 Support

For questions, issues, or contributions, please [open an issue](link-to-issues) or contact the development team.

---

*Automating research excellence with AI agents and human insight.*