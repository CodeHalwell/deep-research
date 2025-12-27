# Frontend Guide - Deep Research Workflow System

This guide covers both frontend options for the Deep Research Workflow System.

## 📋 Table of Contents

1. [Frontend Options](#frontend-options)
2. [Streamlit Web App](#streamlit-web-app)
3. [Web Dashboard](#web-dashboard)
4. [Installation & Setup](#installation--setup)
5. [Usage Guide](#usage-guide)
6. [API Integration](#api-integration)

---

## Frontend Options

The Deep Research Workflow System provides two frontend options:

### 1. **Streamlit Web App** (Recommended for ease of use)
- Interactive Python web application
- Real-time status monitoring
- Workflow history and statistics
- Download reports directly
- Responsive design
- Requires: Python 3.12+, Streamlit

### 2. **Web Dashboard** (Pure HTML/CSS/JavaScript)
- Standalone HTML file
- No server-side dependencies
- Works offline after loading
- Modern, responsive design
- API integration
- Suitable for all users

---

## Streamlit Web App

### What It Is

A modern web application built with Streamlit that provides an intuitive interface for managing research workflows.

### Starting the Streamlit App

```bash
# Install dependencies (if not already done)
uv sync

# Start the Streamlit app
streamlit run streamlit_app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

### Features

#### 📝 Submit Research Tab
- Enter research topic
- Quick examples for inspiration
- Real-time API connection status
- Workflow ID display upon submission

#### 📊 Monitor Tab
- Track workflow progress in real-time
- View workflow statistics:
  - Number of iterations
  - Research notes collected
  - Searches performed
  - Approvals recorded
- Expand sections to view:
  - Research plan
  - Executive summary
  - Draft report
- Download report button when completed

#### 📋 History Tab
- Browse all previous workflows
- Click on any workflow to view details
- Search and filter workflows
- View completion status and dates

#### ℹ️ About Tab
- System information
- Technology stack
- Quick start guide
- Performance metrics
- Documentation links

### Streamlit Configuration

Optional: Create `~/.streamlit/config.toml` for customization:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#333333"
font = "sans serif"

[client]
showErrorDetails = true

[logger]
level = "info"
```

---

## Web Dashboard

### What It Is

A single HTML file that provides a modern, responsive dashboard for managing research workflows. No installation required - just open in a browser.

### Starting the Dashboard

#### Option 1: Direct File Open
```bash
# Open in your default browser
open dashboard.html  # macOS
start dashboard.html # Windows
xdg-open dashboard.html # Linux
```

#### Option 2: Local Web Server
```bash
# Using Python
python -m http.server 8000

# Then visit: http://localhost:8000/dashboard.html
```

### Features

#### 📝 Submit Research Section
- API server URL configuration
- Connection status indicator
- Research topic input area
- Quick example topics
- Status notifications

#### 📊 Monitor Workflow Section
- Workflow ID input
- Status checking
- Progress bar visualization
- Statistics display:
  - Iterations count
  - Research notes count
  - Searches performed
  - Approvals recorded

#### 📋 Results Section
- Executive summary display
- Report download button
- Result preview

#### 📚 Workflow History Section
- Load and display all workflows
- Click to select and monitor
- Status indicators
- Creation timestamps

### Dashboard Tips

1. **API URL**: Ensure the API server is running at the configured URL
2. **Real-time Updates**: Manually refresh status or use browser auto-refresh
3. **Report Download**: Works when workflow is completed
4. **Offline Mode**: Dashboard works offline, but API calls require connection

---

## Installation & Setup

### Prerequisites

```bash
# Check Python version (3.12+ required)
python --version

# Check if pip/uv is available
pip --version
# or
uv --version
```

### Step 1: Install Dependencies

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

### Step 2: Create Environment File

```bash
# Copy template
cp .env.example .env

# Edit .env and add your API keys
# OPENAI_API_KEY=your_key_here
# TAVILY_API_KEY=your_key_here
# SERPAPI_API_KEY=your_key_here
```

### Step 3: Start the API Server

In one terminal:

```bash
python api_server.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 4: Start the Frontend

#### For Streamlit:
```bash
streamlit run streamlit_app.py
```

#### For Web Dashboard:
Simply open `dashboard.html` in your browser.

---

## Usage Guide

### Typical Workflow

1. **Submit a Research Request**
   - Enter your research topic
   - Click submit
   - Copy the workflow ID (for tracking)

2. **Monitor Progress**
   - Use the workflow ID to check status
   - Monitor the progress bar
   - View real-time statistics

3. **Review Results**
   - Wait for "completed" status
   - Read executive summary
   - Download the full report

4. **Manage History**
   - View all past workflows
   - Compare research topics and results
   - Track research patterns

### Best Practices

1. **Topic Quality**
   - Be specific (2-10 words)
   - Include key terms
   - Avoid questions
   - Example: "Quantum computing applications" (good)
   - Example: "What is quantum computing?" (less ideal)

2. **Monitoring**
   - Initial workflows take 5-15 minutes
   - Check status periodically
   - Don't close browser/terminal while workflow runs

3. **Report Quality**
   - Review executive summary first
   - Check research plan for completeness
   - Download report for offline reading
   - Share HTML/PDF with others

### Keyboard Shortcuts (Streamlit)

- `C` - Clear all cache
- `R` - Rerun app
- `S` - Save to cloud (if configured)

---

## API Integration

### REST API Endpoints

All frontends communicate with these REST API endpoints:

#### Health Check
```bash
GET /health
```

#### Submit Workflow
```bash
POST /workflows
Content-Type: application/json

{
  "topic": "Your research topic",
  "config_path": ".config/config.yaml"
}

Returns:
{
  "workflow_id": "uuid",
  "status": "submitted",
  "created_at": "2024-01-01T12:00:00"
}
```

#### Get Workflow Status
```bash
GET /workflows/{workflow_id}

Returns:
{
  "workflow_id": "uuid",
  "status": "in_progress|completed|failed",
  "user_prompt": "topic",
  "created_at": "timestamp",
  "completed_at": "timestamp|null",
  "output_path": "/path/to/report",
  "error_message": null
}
```

#### Get Workflow Results
```bash
GET /workflows/{workflow_id}/result

Returns:
{
  "workflow_id": "uuid",
  "user_prompt": "topic",
  "research_plan": "...",
  "draft_report": "...",
  "final_report": "...",
  "summary": "...",
  "output_path": "/path",
  "status": "completed"
}
```

#### Get Workflow Statistics
```bash
GET /workflows/{workflow_id}/statistics

Returns:
{
  "workflow_id": "uuid",
  "iterations": 2,
  "research_notes": 15,
  "searches": 8,
  "approvals": 3
}
```

#### Download Report
```bash
GET /workflows/{workflow_id}/report

Returns: HTML or PDF file
```

#### List All Workflows
```bash
GET /workflows

Returns:
{
  "count": 5,
  "workflows": [
    {
      "workflow_id": "uuid",
      "user_prompt": "topic",
      "created_at": "timestamp",
      "status": "completed",
      "output_path": "/path"
    }
  ]
}
```

### Making Custom API Calls

#### Using Python
```python
import requests

API_URL = "http://localhost:8000"

# Submit workflow
response = requests.post(f"{API_URL}/workflows", json={
    "topic": "Your research topic"
})
workflow_id = response.json()["workflow_id"]

# Check status
status = requests.get(f"{API_URL}/workflows/{workflow_id}").json()
print(f"Status: {status['status']}")

# Download report
if status['status'] == 'completed':
    report = requests.get(f"{API_URL}/workflows/{workflow_id}/report")
    with open("report.html", "wb") as f:
        f.write(report.content)
```

#### Using JavaScript (Fetch)
```javascript
const API_URL = "http://localhost:8000";

// Submit workflow
const response = await fetch(`${API_URL}/workflows`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ topic: 'Your topic' })
});

const { workflow_id } = await response.json();

// Check status
const status = await fetch(`${API_URL}/workflows/${workflow_id}`);
const data = await status.json();
console.log(`Status: ${data.status}`);
```

#### Using cURL
```bash
# Submit workflow
curl -X POST http://localhost:8000/workflows \
  -H "Content-Type: application/json" \
  -d '{"topic": "Your research topic"}'

# Check status
curl http://localhost:8000/workflows/{workflow_id}

# Download report
curl http://localhost:8000/workflows/{workflow_id}/report > report.html
```

---

## Troubleshooting

### Streamlit Issues

#### Port Already in Use
```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

#### Module Not Found
```bash
# Reinstall dependencies
uv sync --upgrade

# Or use pip
pip install streamlit>=1.30.0
```

#### Slow Loading
- Clear cache: Press `C` in browser
- Restart app: Press `R`
- Check API server connection

### Web Dashboard Issues

#### Cannot Connect to API
1. Ensure API server is running: `python api_server.py`
2. Check API URL is correct
3. Verify no firewall blocking port 8000
4. Check browser console (F12) for errors

#### Report Won't Download
- Ensure workflow is completed
- Try different browser
- Check CORS settings in API server

#### API Server Issues

#### Cannot Start API Server
```bash
# Check if port 8000 is in use
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Use different port
python api_server.py --port 8001
```

#### Database Errors
```bash
# Reset database (WARNING: Deletes data)
rm deepresearch.db

# Restart API server to recreate database
python api_server.py
```

### Network Issues

#### CORS Errors
- Ensure API server allows CORS
- Check origin URL matches configuration
- For Streamlit, ensure both apps on same network

#### Timeout Errors
- Workflows take 5-15 minutes
- Don't close application during workflow
- Check internet connection stability

---

## Customization

### Streamlit Theming

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#667eea"     # Main color
backgroundColor = "#ffffff"   # Background
secondaryBackgroundColor = "#f0f2f6"  # Secondary
textColor = "#333333"        # Text color
font = "sans serif"          # Font family
```

### Web Dashboard Styling

Edit `dashboard.html`, modify CSS variables:

```css
/* Main color gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Card styling */
box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);

/* Button styling */
border-radius: 5px;
padding: 12px 25px;
```

### API Configuration

Edit `api_server.py`:

```python
# Change host/port
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",  # Or "127.0.0.1" for local only
        port=8000,
        log_level="info"
    )
```

---

## Performance Tips

### For Streamlit
1. Use cache: `@st.cache_data`
2. Limit API calls
3. Lazy load content with expanders
4. Compress images in reports

### For Web Dashboard
1. Minimize JavaScript
2. Use local storage for user preferences
3. Debounce API calls
4. Cache API responses in localStorage

### For API Server
1. Enable database indexes
2. Use connection pooling
3. Implement rate limiting
4. Add response caching

---

## Advanced Usage

### Batch Processing

```python
# Script to process multiple topics
topics = [
    "Artificial Intelligence",
    "Quantum Computing",
    "Renewable Energy"
]

for topic in topics:
    result = requests.post(
        "http://localhost:8000/workflows",
        json={"topic": topic}
    ).json()
    print(f"Started: {result['workflow_id']}")
```

### Scheduled Research

```python
# Using APScheduler
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()

def run_daily_research():
    requests.post("http://localhost:8000/workflows",
                 json={"topic": "Daily AI News"})

scheduler.add_job(run_daily_research, 'cron', hour=2)
scheduler.start()
```

### Custom Report Processing

```python
# After workflow completes
import requests
from bs4 import BeautifulSoup

workflow_id = "..."
report = requests.get(
    f"http://localhost:8000/workflows/{workflow_id}/report"
).text

soup = BeautifulSoup(report, 'html.parser')
summary = soup.find('div', {'class': 'summary'}).text

# Process summary further...
```

---

## Support

For issues or questions:

1. Check the logs:
   - Streamlit: Browser console (F12)
   - Dashboard: Browser console (F12)
   - API: Terminal output

2. Review documentation:
   - USAGE.md
   - ADVANCED_FEATURES.md
   - IMPLEMENTATION_NOTES.md

3. Verify setup:
   - API server running
   - Environment variables set
   - Database accessible
   - Network connectivity

---

## Next Steps

- [View Complete Documentation](README.md)
- [Check Advanced Features](ADVANCED_FEATURES.md)
- [Review Technical Details](IMPLEMENTATION_NOTES.md)
- [Explore API Endpoints](ADVANCED_FEATURES.md#rest-api-server)

---

**Happy researching! 🔬**
