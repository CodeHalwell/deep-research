"""
Deep Research Workflow System - Streamlit Web Application

Interactive web frontend for submitting research workflows,
monitoring progress, and viewing results.
"""

import streamlit as st
import requests
import json
import time
from datetime import datetime
from pathlib import Path
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Deep Research Workflow",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# App header
st.markdown(
    """
    # 🔬 Deep Research Workflow System
    Automated research and professional report generation powered by AI
    """
)

# Initialize session state
if "api_url" not in st.session_state:
    st.session_state.api_url = "http://localhost:8000"

if "workflows" not in st.session_state:
    st.session_state.workflows = []

if "current_workflow" not in st.session_state:
    st.session_state.current_workflow = None


# Helper functions
def check_api_connection():
    """Check if API server is running."""
    try:
        response = requests.get(f"{st.session_state.api_url}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def submit_workflow(topic: str):
    """Submit a new research workflow."""
    try:
        response = requests.post(
            f"{st.session_state.api_url}/workflows",
            json={"topic": topic},
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Error submitting workflow: {str(e)}")
        return None


def get_workflow_status(workflow_id: str):
    """Get the status of a workflow."""
    try:
        response = requests.get(
            f"{st.session_state.api_url}/workflows/{workflow_id}",
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def get_workflow_result(workflow_id: str):
    """Get the result of a completed workflow."""
    try:
        response = requests.get(
            f"{st.session_state.api_url}/workflows/{workflow_id}/result",
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def get_workflow_statistics(workflow_id: str):
    """Get statistics for a workflow."""
    try:
        response = requests.get(
            f"{st.session_state.api_url}/workflows/{workflow_id}/statistics",
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def list_workflows():
    """List all workflows."""
    try:
        response = requests.get(
            f"{st.session_state.api_url}/workflows",
            timeout=10,
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("workflows", [])
        return []
    except:
        return []


def download_report(workflow_id: str):
    """Download a report file."""
    try:
        response = requests.get(
            f"{st.session_state.api_url}/workflows/{workflow_id}/report",
            timeout=30,
        )
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None


# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")

    # API Configuration
    st.markdown("### API Configuration")
    api_url = st.text_input(
        "API Server URL",
        value=st.session_state.api_url,
        help="URL of the Deep Research API server",
    )

    if api_url != st.session_state.api_url:
        st.session_state.api_url = api_url

    # Check API status
    if check_api_connection():
        st.success("✅ API Server Connected")
    else:
        st.error(
            "❌ Cannot connect to API Server\n\n"
            "Make sure to start the API server:\n"
            "`python api_server.py`"
        )

    st.markdown("---")

    # Help section
    st.markdown("### 📚 Help")
    with st.expander("How to use this app"):
        st.markdown(
            """
            1. **Submit Research** - Enter a research topic
            2. **Monitor Progress** - Watch the workflow status
            3. **View Results** - Access the generated report
            4. **Download Report** - Export as HTML or PDF

            Each workflow includes:
            - Automated research plan generation
            - Comprehensive data gathering
            - Professional report writing
            - Quality review and revision
            - Executive summary generation
            """
        )

    with st.expander("System Requirements"):
        st.markdown(
            """
            - Python 3.12+
            - FastAPI server running
            - OpenAI API key configured
            - 5-15 minutes per workflow
            """
        )


# Main content
tab1, tab2, tab3, tab4 = st.tabs(
    ["📝 Submit Research", "📊 Monitor", "📋 History", "ℹ️ About"]
)

# Tab 1: Submit Research
with tab1:
    st.markdown("## Submit New Research Workflow")

    col1, col2 = st.columns([3, 1])

    with col1:
        research_topic = st.text_area(
            "Research Topic or Question",
            placeholder="e.g., 'Quantum computing applications in cryptography'",
            height=100,
            help="Enter the topic you want researched",
        )

    with col2:
        st.markdown("### Topic Tips")
        st.info(
            """
            • Be specific
            • Use 2-10 words
            • Include key terms
            • Avoid questions
            """
        )

    if st.button("🚀 Start Research Workflow", type="primary", use_container_width=True):
        if not research_topic.strip():
            st.error("Please enter a research topic")
        elif not check_api_connection():
            st.error("Cannot connect to API server. Please check your connection.")
        else:
            with st.spinner("Submitting workflow..."):
                result = submit_workflow(research_topic)

            if result:
                st.session_state.current_workflow = result["workflow_id"]
                st.success(f"✅ Workflow submitted successfully!")
                st.json(result)

                # Show next steps
                st.markdown("### Next Steps")
                st.info(
                    f"""
                    Your workflow ID: `{result['workflow_id']}`

                    1. Go to the **Monitor** tab to track progress
                    2. Workflow typically takes 5-15 minutes
                    3. Check back later for your report
                    """
                )

            else:
                st.error("Failed to submit workflow. Please try again.")

    # Quick examples
    st.markdown("---")
    st.markdown("### 📌 Example Topics")

    col1, col2, col3 = st.columns(3)

    examples = [
        "Artificial Intelligence in healthcare",
        "Climate change mitigation strategies",
        "Renewable energy technologies",
        "Blockchain applications",
        "Space exploration missions",
        "Biotechnology advances",
    ]

    for i, example in enumerate(examples):
        col = [col1, col2, col3][i % 3]
        with col:
            if st.button(example, use_container_width=True):
                st.session_state.research_topic = example


# Tab 2: Monitor
with tab2:
    st.markdown("## Monitor Workflow Progress")

    col1, col2 = st.columns([3, 1])

    with col1:
        workflow_id = st.text_input(
            "Workflow ID",
            placeholder="Enter or paste workflow ID",
            help="The ID returned when you submit a workflow",
        )

    with col2:
        refresh = st.button("🔄 Refresh", use_container_width=True)

    if workflow_id:
        if refresh or st.session_state.current_workflow == workflow_id:
            status = get_workflow_status(workflow_id)

            if status:
                # Status overview
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Status", status["status"].upper())

                with col2:
                    st.metric("Created", status["created_at"][:10])

                with col3:
                    if status["completed_at"]:
                        st.metric("Completed", status["completed_at"][:10])
                    else:
                        st.metric("Completed", "In Progress")

                with col4:
                    st.metric("Has Report", "✅" if status["output_path"] else "⏳")

                # Topic
                st.markdown(f"**Research Topic:** {status['user_prompt']}")

                # Status details
                st.markdown("---")
                st.markdown("### Workflow Status")

                if status["status"] == "in_progress":
                    st.info(
                        "⏳ Workflow is currently running. "
                        "This typically takes 5-15 minutes."
                    )
                    st.progress(0.5)

                elif status["status"] == "completed":
                    st.success("✅ Workflow completed successfully!")
                    st.progress(1.0)

                    # Show statistics
                    stats = get_workflow_statistics(workflow_id)
                    if stats:
                        st.markdown("#### Workflow Statistics")
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric("Iterations", stats["iterations"])

                        with col2:
                            st.metric("Research Notes", stats["research_notes"])

                        with col3:
                            st.metric("Searches", stats["searches"])

                        with col4:
                            st.metric("Approvals", stats["approvals"])

                    # Result section
                    st.markdown("---")
                    st.markdown("### Workflow Results")

                    result = get_workflow_result(workflow_id)
                    if result:
                        with st.expander("📋 Research Plan"):
                            st.text_area(
                                "Research Plan",
                                value=result["research_plan"] or "N/A",
                                disabled=True,
                                height=150,
                            )

                        with st.expander("📝 Summary"):
                            st.text_area(
                                "Executive Summary",
                                value=result["summary"] or "N/A",
                                disabled=True,
                                height=200,
                            )

                        with st.expander("📄 Draft Report"):
                            if result["draft_report"]:
                                st.text_area(
                                    "Draft Report",
                                    value=result["draft_report"][:1000] + "...",
                                    disabled=True,
                                    height=200,
                                )
                            else:
                                st.info("No draft report available")

                        # Download button
                        st.markdown("---")
                        if result["output_path"]:
                            report_data = download_report(workflow_id)
                            if report_data:
                                st.download_button(
                                    label="📥 Download Report",
                                    data=report_data,
                                    file_name=f"report_{workflow_id}.html",
                                    mime="text/html",
                                    use_container_width=True,
                                )

                elif status["status"] == "failed":
                    st.error("❌ Workflow failed")
                    if status["error_message"]:
                        st.error(f"Error: {status['error_message']}")

            else:
                st.error("Workflow not found. Please check the workflow ID.")

    else:
        st.info("Enter a workflow ID to monitor its progress")


# Tab 3: History
with tab3:
    st.markdown("## Workflow History")

    if st.button("📥 Load Workflow History", use_container_width=True):
        workflows = list_workflows()

        if workflows:
            # Convert to DataFrame for display
            df_data = []
            for w in workflows:
                df_data.append(
                    {
                        "Workflow ID": w["workflow_id"][:8] + "...",
                        "Topic": w["user_prompt"][:50],
                        "Status": w["status"],
                        "Created": w["created_at"][:10],
                        "Full ID": w["workflow_id"],
                    }
                )

            df = pd.DataFrame(df_data)

            # Display table
            st.dataframe(df[["Workflow ID", "Topic", "Status", "Created"]], use_container_width=True)

            # Selection
            st.markdown("---")
            selected_id = st.selectbox(
                "Select workflow to view",
                options=[w["Full ID"] for w in df_data],
                format_func=lambda x: [d["Topic"] for d in df_data if d["Full ID"] == x][0],
            )

            if selected_id:
                st.session_state.current_workflow = selected_id
                st.rerun()

        else:
            st.info("No workflows found. Start a new research workflow to get started!")


# Tab 4: About
with tab4:
    st.markdown("## About Deep Research Workflow System")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            ### 🎯 Purpose
            Automated research and professional report generation using AI agents.

            ### 🔍 What It Does
            - Generates research plans
            - Conducts web searches
            - Accesses academic databases
            - Synthesizes information
            - Writes professional reports
            - Performs quality reviews
            - Creates executive summaries

            ### ⚡ Features
            - **9-Stage Pipeline** - Complete research workflow
            - **8 AI Agents** - Specialized for each stage
            - **Multiple Sources** - Web, academic, knowledge bases
            - **Quality Control** - Human-in-the-loop approvals
            - **Professional Output** - HTML and PDF reports
            """
        )

    with col2:
        st.markdown(
            """
            ### 📊 How Long Does It Take?
            - Planning: 30-60 seconds
            - Research: 1-5 minutes
            - Writing: 1-2 minutes
            - Review: 2-5 minutes
            - **Total: 5-15 minutes**

            ### 💰 Cost Estimate
            - Simple topic: $0.05-$0.10
            - Medium topic: $0.15-$0.30
            - Complex topic: $0.50-$1.00

            ### 🚀 Getting Started
            1. Install dependencies
            2. Set up API keys
            3. Start API server
            4. Submit research topic
            5. Monitor progress
            6. Download report
            """
        )

    st.markdown("---")

    st.markdown("### 🛠️ Technology Stack")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            **Backend**
            - FastAPI
            - SQLite
            - Python 3.12+
            """
        )

    with col2:
        st.markdown(
            """
            **AI & Research**
            - OpenAI GPT-4
            - Web search APIs
            - Academic databases
            """
        )

    with col3:
        st.markdown(
            """
            **Frontend**
            - Streamlit
            - REST API
            - Interactive UI
            """
        )

    st.markdown("---")

    st.markdown("### 📚 Documentation")
    st.markdown(
        """
        - **README.md** - Project overview
        - **USAGE.md** - User guide
        - **ADVANCED_FEATURES.md** - Advanced documentation
        - **IMPLEMENTATION_NOTES.md** - Technical details
        """
    )


# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Deep Research Workflow System v0.1.0</p>
        <p>Automated Research & Report Generation</p>
    </div>
    """,
    unsafe_allow_html=True,
)
