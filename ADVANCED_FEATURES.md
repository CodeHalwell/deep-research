# Advanced Features - Deep Research Workflow System

This document covers the advanced features added to make the Deep Research Workflow System production-ready.

## Table of Contents

1. [REST API Server](#rest-api-server)
2. [Error Recovery & Retry Logic](#error-recovery--retry-logic)
3. [SQLite Database](#sqlite-database)
4. [Advanced MCP Servers](#advanced-mcp-servers)
5. [Testing Suite](#testing-suite)
6. [Performance Optimization](#performance-optimization)

---

## REST API Server

### Overview

The REST API provides a complete HTTP interface for workflow management, allowing you to:
- Submit research workflows
- Monitor progress
- Retrieve results
- Manage workflow history
- Download reports

### Starting the API Server

```bash
# Using Python directly
python api_server.py

# Using uvicorn directly
uvicorn api_server:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with interactive documentation at `/docs`.

### Endpoints

#### Health Check
```bash
GET /health
```

Returns server health status.

#### Submit Workflow
```bash
POST /workflows
Content-Type: application/json

{
  "topic": "Your research topic here",
  "config_path": ".config/config.yaml"
}
```

Response:
```json
{
  "workflow_id": "uuid-here",
  "status": "submitted",
  "created_at": "2024-01-01T12:00:00"
}
```

#### Get Workflow Status
```bash
GET /workflows/{workflow_id}
```

Returns current status of a workflow.

#### List All Workflows
```bash
GET /workflows
```

Returns all workflows in history with basic info.

#### Get Workflow Result
```bash
GET /workflows/{workflow_id}/result
```

Returns complete workflow data (only when completed).

#### Download Report
```bash
GET /workflows/{workflow_id}/report
```

Download the generated HTML/PDF report.

#### Get Statistics
```bash
GET /workflows/{workflow_id}/statistics
```

Returns workflow statistics:
- Number of iterations
- Number of research notes
- Number of searches performed
- Number of approvals recorded

#### Delete Workflow
```bash
DELETE /workflows/{workflow_id}
```

Mark workflow for deletion (data can be archived first).

### Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Submit workflow
response = requests.post(f"{BASE_URL}/workflows", json={
    "topic": "Quantum computing applications in cryptography"
})
workflow_id = response.json()["workflow_id"]

# Poll for completion
import time
while True:
    status = requests.get(f"{BASE_URL}/workflows/{workflow_id}").json()
    print(f"Status: {status['status']}")

    if status['status'] == 'completed':
        break

    time.sleep(5)

# Get results
result = requests.get(f"{BASE_URL}/workflows/{workflow_id}/result").json()
print(f"Summary: {result['summary'][:200]}...")

# Download report
report = requests.get(f"{BASE_URL}/workflows/{workflow_id}/report")
with open("report.html", "wb") as f:
    f.write(report.content)
```

---

## Error Recovery & Retry Logic

### Overview

The error recovery system provides intelligent handling of failures with:
- Exponential backoff retry logic
- Error categorization and severity assessment
- Fallback operation support
- Resilient operation wrapping

### Error Categories

The system automatically categorizes errors:

| Category | Examples | Recoverable |
|----------|----------|-------------|
| `API_ERROR` | API failures, auth errors | Yes |
| `NETWORK_ERROR` | Connection issues | Yes |
| `TIMEOUT_ERROR` | Operation timeout | Yes |
| `VALIDATION_ERROR` | Invalid input | No |
| `RESOURCE_ERROR` | Out of memory, disk full | No |
| `UNKNOWN_ERROR` | Unclassified errors | Yes |

### Using Retry Logic

#### Basic Retry
```python
from error_recovery import retry_with_backoff

async def risky_operation():
    # Some operation that might fail
    return await some_async_function()

# Execute with automatic retry
result = await retry_with_backoff(
    risky_operation,
    max_retries=3,
    initial_delay=1.0,  # Start with 1 second
    max_delay=60.0,     # Max 60 second delay
)
```

#### Resilient Operation Wrapper
```python
from error_recovery import ResilientOperation

operation = ResilientOperation(
    my_async_function,
    max_retries=3,
    timeout=30.0  # 30 second timeout
)

# Execute with retry
result = await operation.execute_with_retry(arg1, arg2)

# Check error history
if operation.error_history:
    print(f"Encountered {len(operation.error_history)} errors")
```

#### Fallback Operations
```python
from error_recovery import with_fallback

result = await with_fallback(
    primary_search_function,
    fallback_search_function,
    query="research topic"
)
```

### Error Handling in Workflows

The workflow system automatically uses error recovery:

```python
from deepresearch import DeepResearchWorkflow

workflow = DeepResearchWorkflow()

try:
    result = await workflow.execute("Your research topic")
except Exception as e:
    print(f"Workflow failed: {e}")
    # Check database for partial results
```

### Configuring Retry Behavior

Set environment variables to customize retry behavior:

```bash
# Maximum iterations before escalation
export MAX_ITERATIONS=5

# Research operation timeout (seconds)
export RESEARCH_TIMEOUT=120

# Enable advanced error recovery
export ENABLE_ERROR_RECOVERY=true
```

---

## SQLite Database

### Overview

The database provides persistent storage for:
- Workflow execution history
- Research notes and sources
- Iteration tracking
- User approvals
- Search history
- Workflow statistics

### Initialization

The database is automatically created on first use:

```python
from database import get_database

db = get_database("deepresearch.db")  # Default path
```

### Database Schema

#### Workflows Table
Stores workflow metadata and results:
- `workflow_id`: Unique identifier
- `user_prompt`: Research topic
- `created_at`: Start time
- `completed_at`: Completion time
- `status`: 'in_progress', 'completed', 'failed'
- `research_plan`: Generated plan
- `draft_report`: Initial draft
- `final_report`: Final version
- `summary`: Executive summary
- `output_path`: Report file location
- `error_message`: Error details if failed

#### Research Notes Table
- `workflow_id`: Associated workflow
- `source_url`: URL of information source
- `source_title`: Title of source
- `note_content`: The note text
- `category`: Note category
- `created_at`: When note was created

#### Iterations Table
Tracks revisions and improvements:
- `workflow_id`: Associated workflow
- `iteration_number`: Revision number
- `stage`: Workflow stage (planning, writing, etc.)
- `input_content`: Content before stage
- `output_content`: Content after stage
- `feedback`: Review feedback

#### Approvals Table
Records user approval decisions:
- `workflow_id`: Associated workflow
- `approval_type`: 'plan', 'revision', etc.
- `content`: What was approved
- `approved`: True/False
- `notes`: User's comments

#### Search History Table
Tracks all searches performed:
- `workflow_id`: Associated workflow
- `search_type`: 'web', 'scholar', 'arxiv', etc.
- `query`: Search query text
- `results_count`: Number of results
- `created_at`: Timestamp

### Common Operations

#### Save a Workflow
```python
db.save_workflow(
    workflow_id="uuid-here",
    user_prompt="Research topic",
    status="in_progress"
)
```

#### Update Progress
```python
db.update_workflow(
    workflow_id="uuid-here",
    status="completed",
    final_report="Report text...",
    output_path="/path/to/report.html"
)
```

#### Add Research Notes
```python
db.add_research_note(
    workflow_id="uuid-here",
    note_content="Important finding...",
    source_url="https://example.com",
    source_title="Example Article",
    category="methodology"
)
```

#### Record Iteration
```python
db.record_iteration(
    workflow_id="uuid-here",
    iteration_number=1,
    stage="review",
    input_content="First draft...",
    output_content="Revised draft...",
    feedback="Needs better structure"
)
```

#### Record Approval
```python
db.record_approval(
    workflow_id="uuid-here",
    approval_type="plan",
    content="Research plan text...",
    approved=True,
    notes="Plan looks good, proceed"
)
```

#### Get Workflow History
```python
history = db.get_workflow_history()
for workflow in history:
    print(f"{workflow['workflow_id']}: {workflow['status']}")
```

#### Get Statistics
```python
stats = db.get_statistics("workflow_id")
print(f"Iterations: {stats['iterations']}")
print(f"Research notes: {stats['notes']}")
print(f"Searches: {stats['searches']}")
print(f"Approvals: {stats['approvals']}")
```

---

## Advanced MCP Servers

### Research Server

Provides research and data gathering tools via MCP protocol.

#### Available Tools

1. **scrape(url)** - Scrape website content
   ```
   url: String - Website URL to scrape
   ```

2. **ddg_search(query, max_results)** - DuckDuckGo web search
   ```
   query: String - Search query
   max_results: Integer - Results to return (default: 5)
   ```

3. **tavily_search(query, max_results)** - Advanced Tavily search
   ```
   query: String - Search query
   max_results: Integer - Results to return (default: 5)
   ```

4. **scholar_search(query, max_results)** - Google Scholar via SerpAPI
   ```
   query: String - Research query
   max_results: Integer - Results to return (default: 5)
   ```

5. **arxiv_search(query, max_results)** - Search arXiv papers
   ```
   query: String - Research query
   max_results: Integer - Results to return (default: 5)
   ```

6. **semantic_scholar_search(query, max_results)** - Semantic Scholar API
   ```
   query: String - Research query
   max_results: Integer - Results to return (default: 5)
   ```

### Document Server

Provides document processing tools via MCP protocol.

#### Available Tools

1. **format_citation(author, title, source, year, style)** - Format citations
   ```
   author: String - Author name(s)
   title: String - Citation title
   source: String - Publication source
   year: String - Publication year
   style: String - Style (apa, mla, chicago)
   ```

2. **validate_document(content)** - Check document quality
   ```
   content: String - Document text
   Returns: Metrics and validation results
   ```

3. **generate_toc(content)** - Create table of contents
   ```
   content: String - Document text with headings
   Returns: Markdown TOC
   ```

4. **format_as_html(title, content, style)** - Convert to HTML
   ```
   title: String - Document title
   content: String - Markdown content
   style: String - HTML style (professional, minimal, academic)
   ```

5. **extract_metadata(content)** - Extract document statistics
   ```
   content: String - Document text
   Returns: Word count, paragraphs, sentences, etc.
   ```

---

## Testing Suite

### Running Tests

```bash
# Run all tests
pytest test/ -v

# Run specific test class
pytest test/test_integration.py::TestWorkflowState -v

# Run with coverage report
pytest test/ --cov=. --cov-report=html

# Run specific test
pytest test/test_integration.py::TestWorkflowState::test_state_initialization -v
```

### Test Coverage

The test suite includes:

- **WorkflowState Tests** - State management and serialization
- **Agent Tests** - Agent initialization and configuration
- **Tool Registry Tests** - Tool registration and discovery
- **Configuration Tests** - Config loading and validation
- **Document Generation Tests** - HTML/PDF output
- **Workflow Integration Tests** - End-to-end workflow execution
- **Error Handling Tests** - Error tracking and recovery
- **Document Tools Tests** - Citation, validation, HTML conversion
- **Async Tests** - Async/await operations
- **Persistence Tests** - JSON serialization
- **Performance Tests** - Speed benchmarks

### Writing Custom Tests

```python
import pytest
from deepresearch import DeepResearchWorkflow

@pytest.mark.asyncio
async def test_custom_workflow():
    """Test custom workflow behavior."""
    workflow = DeepResearchWorkflow()

    # Perform some operation
    result = await workflow._generate_plan("Test topic")

    # Assert results
    assert result is not None
    assert len(result) > 0
```

---

## Performance Optimization

### Caching

Enable caching for frequently used operations:

```python
from utils.cache import cache_result
import functools

@cache_result(ttl=3600)  # Cache for 1 hour
async def expensive_search(query):
    # Perform expensive search
    return results
```

### Parallel Execution

Where safe, execute operations in parallel:

```python
import asyncio

async def parallel_searches(queries):
    """Execute multiple searches in parallel."""
    tasks = [
        perform_search(q)
        for q in queries
    ]

    results = await asyncio.gather(*tasks)
    return results
```

### Batch Processing

Process multiple items efficiently:

```python
from error_recovery import partial_recovery

urls = ["url1", "url2", "url3", ...]

successful, failed = await partial_recovery(
    urls,
    scrape_url,
    fail_on_count=5  # Stop after 5 failures
)
```

### Resource Management

```python
# Limit concurrent operations
semaphore = asyncio.Semaphore(5)

async def rate_limited_operation():
    async with semaphore:
        # Only 5 concurrent operations
        return await operation()
```

---

## Monitoring & Logging

### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
python run_workflow.py "Your topic"
```

### Accessing Logs

Logs are saved to:
- `deepresearch_*.log` - Main application logs
- `research_server.log` - Research server logs
- `document_server.log` - Document server logs
- `error_recovery.log` - Error recovery logs

### Monitoring Production Deployments

When running the API server:

```python
# Monitor workflow status
from database import get_database

db = get_database()

# Get all active workflows
active = [
    w for w in db.get_workflow_history()
    if w['status'] == 'in_progress'
]

# Get statistics
for workflow_id in active:
    stats = db.get_statistics(workflow_id)
    print(f"Workflow {workflow_id}: {stats}")
```

---

## Integration Examples

### Integrate with Existing Applications

```python
# In your Django/Flask app
from deepresearch import DeepResearchWorkflow
import asyncio

def generate_research_report(topic):
    """Generate a research report for a topic."""
    workflow = DeepResearchWorkflow()
    result = asyncio.run(workflow.execute(topic))
    return result['output_path']
```

### Scheduled Workflow Execution

```python
from APScheduler.schedulers.background import BackgroundScheduler
from deepresearch import DeepResearchWorkflow
import asyncio

scheduler = BackgroundScheduler()

def run_scheduled_research(topic):
    """Run research on a schedule."""
    workflow = DeepResearchWorkflow()
    asyncio.run(workflow.execute(topic))

# Run every day at 2 AM
scheduler.add_job(
    run_scheduled_research,
    'cron',
    hour=2,
    args=['Daily research topic']
)

scheduler.start()
```

---

## Troubleshooting

### API Server Won't Start

```bash
# Check if port is already in use
lsof -i :8000

# Use a different port
python api_server.py --port 8001
```

### Database Issues

```bash
# Reset database (WARNING: Deletes all data)
rm deepresearch.db

# The database will be recreated on next run
python run_workflow.py "topic"
```

### Tests Failing

```bash
# Run with verbose output
pytest test/ -vv

# Show print statements
pytest test/ -s

# Run only failed tests from last run
pytest test/ --lf
```

---

## Next Steps

For more information, see:
- [USAGE.md](USAGE.md) - User guide
- [IMPLEMENTATION_NOTES.md](IMPLEMENTATION_NOTES.md) - Technical details
- [README.md](README.md) - Project overview

For support or issues, open an issue on GitHub or contact the development team.
