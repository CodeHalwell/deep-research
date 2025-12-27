# Deep Research Workflow System - Usage Guide

## Quick Start

### Prerequisites
- Python 3.12+
- API key: OpenAI (required)
- Optional: Tavily API, SerpAPI

### Setup (5 minutes)

1. **Setup environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

2. **Verify installation:**
   ```bash
   source .venv/bin/activate
   python -c "from deepresearch import DeepResearchWorkflow; print('Ready!')"
   ```

3. **Run a workflow:**
   ```bash
   python run_workflow.py "Your research topic"
   ```

4. **Review output:**
   - Report: `output/report_YYYYMMDD_HHMMSS.html` (or .pdf)
   - State: `output/workflow_YYYYMMDD_HHMMSS.json`

## Running Workflows

### Command Line (Recommended)
```bash
python run_workflow.py "Quantum computing applications"
python run_workflow.py "Your topic" --config .config/config.yaml -v
```

### Python API
```python
import asyncio
from deepresearch import DeepResearchWorkflow

async def research():
    workflow = DeepResearchWorkflow()
    result = await workflow.execute("Your research topic")
    return result

result = asyncio.run(research())
print(f"Report: {result['output_path']}")
```

## Workflow Stages

1. **Planning** (~30-60s): LLM generates research plan → Human approves
2. **Research** (1-5m): Conducts web searches and gathers information
3. **Writing** (1-2m): Drafts comprehensive report
4. **Review** (2-5m): Reviews and improves report (max 3 iterations)
5. **Fact-Checking** (1-2m): Verifies key claims
6. **Formatting** (~1m): Applies professional styling
7. **Summary** (~1m): Creates executive summary
8. **Document** (10-30s): Generates HTML/PDF output

## Human Approval Points

### Plan Approval
You'll be asked to approve the research plan before the system starts researching. You can:
- `yes/y` - Approve and proceed
- `no/n` - Reject (cancels workflow)
- `show_full` - See complete plan

### Escalation (if max revisions reached)
If the report still needs work after 3 revision cycles, you must manually approve it to proceed.

## Configuration

### Environment Variables (in `.env`)
```env
OPENAI_API_KEY=sk-...           # Required
TAVILY_API_KEY=...              # Optional
SERPAPI_API_KEY=...             # Optional
MAX_ITERATIONS=3                # Revision loops
LOG_LEVEL=INFO
```

### Config File (`.config/config.yaml`)
```yaml
provider:
  model: "gpt-4.1-mini"  # or gpt-4-turbo, gpt-3.5-turbo
model_settings:
  temperature: 0.7       # 0=deterministic, 1=creative
  max_tokens: 1000
```

## Output Files

For each workflow, you get:
- **HTML Report**: Styled, viewable in any browser
- **PDF Report**: If WeasyPrint installed
- **State JSON**: Complete workflow history (for debugging/resuming)

Sample state file includes:
- Research plan
- Research notes
- Draft report
- Review feedback
- Final report
- Summary
- All iteration counts

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ImportError: No module named 'anthropic'` | Run `uv sync` |
| `API key not found` | Add keys to `.env` file |
| `Workflow timeout` | Press Ctrl+C, try simpler topic |
| `No HTML/PDF generated` | Check `output/` directory permissions |

## Cost Estimation

Approximate cost per workflow (using gpt-4.1-mini):
- Simple topic: $0.05-$0.10
- Medium topic: $0.15-$0.30
- Complex topic: $0.50-$1.00

## Advanced Usage

### Custom Configuration
```python
workflow = DeepResearchWorkflow(config_path="my_config.yaml")
```

### Access Intermediate Results
```python
import json
state = json.load(open("output/workflow_*.json"))
print(state["research_notes"])
```

### Integration Example
```python
async def generate_report(topic: str) -> str:
    workflow = DeepResearchWorkflow()
    result = await workflow.execute(topic)
    return result["output_path"]
```

## Getting Help

- Check logs: `tail -f *.log`
- Verbose mode: `python run_workflow.py "topic" -v`
- Review state: `cat output/workflow_*.json | python -m json.tool`
- See docs: [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md)

---

**Ready to research! 🚀**
