"""
FastAPI server for Deep Research Workflow System.

Provides REST API endpoints for:
- Submitting research workflows
- Checking workflow status
- Retrieving results
- Managing workflow history
"""

import asyncio
import uuid
from typing import Optional, List
from datetime import datetime

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from fastapi.responses import FileResponse

from deepresearch import DeepResearchWorkflow, WorkflowState
from database import get_database

# Initialize app
app = FastAPI(
    title="Deep Research Workflow API",
    description="REST API for automated research and report generation",
    version="0.1.0",
)

# Database
db = get_database()


# Request/Response models


class WorkflowRequest(BaseModel):
    """Request to start a research workflow."""

    topic: str = Field(..., description="Research topic or question", min_length=10)
    config_path: Optional[str] = Field(
        default=".config/config.yaml", description="Path to config file"
    )


class WorkflowResponse(BaseModel):
    """Response after workflow submission."""

    workflow_id: str = Field(..., description="Unique workflow identifier")
    status: str = Field(default="submitted", description="Workflow status")
    created_at: datetime = Field(..., description="Creation timestamp")


class WorkflowStatus(BaseModel):
    """Workflow status information."""

    workflow_id: str
    status: str
    user_prompt: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    output_path: Optional[str] = None
    error_message: Optional[str] = None


class WorkflowStatistics(BaseModel):
    """Statistics for a workflow."""

    workflow_id: str
    iterations: int
    research_notes: int
    searches: int
    approvals: int


class WorkflowResult(BaseModel):
    """Complete workflow result."""

    workflow_id: str
    user_prompt: str
    research_plan: Optional[str]
    draft_report: Optional[str]
    final_report: Optional[str]
    summary: Optional[str]
    output_path: Optional[str]
    status: str


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str = "0.1.0"
    timestamp: datetime


# Background tasks


def execute_workflow_background(workflow_id: str, topic: str):
    """Execute workflow in background."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        workflow = DeepResearchWorkflow()
        result = loop.run_until_complete(workflow.execute(topic))

        # Update database with results
        db.update_workflow(
            workflow_id,
            status="completed",
            final_report=result.get("summary", ""),
            output_path=result.get("output_path", ""),
        )

    except Exception as e:
        # Record error in database
        db.update_workflow(
            workflow_id,
            status="failed",
            error_message=str(e),
        )


# Routes


@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {
        "message": "Deep Research Workflow API",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health():
    """Health check endpoint."""
    return HealthResponse(timestamp=datetime.now())


@app.post(
    "/workflows",
    response_model=WorkflowResponse,
    tags=["Workflows"],
    summary="Submit a research workflow",
    description="Start a new research workflow with the given topic",
)
async def submit_workflow(
    request: WorkflowRequest,
    background_tasks: BackgroundTasks,
):
    """
    Submit a new research workflow.

    Args:
        request: WorkflowRequest with topic and optional config path
        background_tasks: Background task manager

    Returns:
        WorkflowResponse with workflow_id and status
    """
    # Generate unique workflow ID
    workflow_id = str(uuid.uuid4())

    # Save to database
    db.save_workflow(
        workflow_id=workflow_id,
        user_prompt=request.topic,
        status="submitted",
    )

    # Schedule background execution
    background_tasks.add_task(
        execute_workflow_background,
        workflow_id,
        request.topic,
    )

    return WorkflowResponse(
        workflow_id=workflow_id,
        status="submitted",
        created_at=datetime.now(),
    )


@app.get(
    "/workflows/{workflow_id}",
    response_model=WorkflowStatus,
    tags=["Workflows"],
    summary="Get workflow status",
    description="Get the current status of a workflow",
)
async def get_workflow_status(workflow_id: str):
    """
    Get workflow status.

    Args:
        workflow_id: Workflow identifier

    Returns:
        WorkflowStatus with current information

    Raises:
        HTTPException: If workflow not found
    """
    workflow = db.get_workflow(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return WorkflowStatus(
        workflow_id=workflow["workflow_id"],
        status=workflow["status"],
        user_prompt=workflow["user_prompt"],
        created_at=datetime.fromisoformat(workflow["created_at"]),
        completed_at=(
            datetime.fromisoformat(workflow["completed_at"])
            if workflow["completed_at"]
            else None
        ),
        output_path=workflow["output_path"],
        error_message=workflow["error_message"],
    )


@app.get(
    "/workflows/{workflow_id}/result",
    response_model=WorkflowResult,
    tags=["Workflows"],
    summary="Get workflow result",
    description="Get the complete result of a completed workflow",
)
async def get_workflow_result(workflow_id: str):
    """
    Get workflow result.

    Args:
        workflow_id: Workflow identifier

    Returns:
        WorkflowResult with all workflow data

    Raises:
        HTTPException: If workflow not found or not completed
    """
    workflow = db.get_workflow(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if workflow["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Workflow not completed. Current status: {workflow['status']}",
        )

    return WorkflowResult(
        workflow_id=workflow["workflow_id"],
        user_prompt=workflow["user_prompt"],
        research_plan=workflow["research_plan"],
        draft_report=workflow["draft_report"],
        final_report=workflow["final_report"],
        summary=workflow["summary"],
        output_path=workflow["output_path"],
        status=workflow["status"],
    )


@app.get(
    "/workflows/{workflow_id}/report",
    tags=["Workflows"],
    summary="Download report",
    description="Download the generated report file",
)
async def download_report(workflow_id: str):
    """
    Download generated report.

    Args:
        workflow_id: Workflow identifier

    Returns:
        Report file

    Raises:
        HTTPException: If workflow not found or no report available
    """
    workflow = db.get_workflow(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if not workflow["output_path"]:
        raise HTTPException(
            status_code=400,
            detail="No report available for this workflow",
        )

    return FileResponse(
        path=workflow["output_path"],
        filename=f"report_{workflow_id}.html",
    )


@app.get(
    "/workflows/{workflow_id}/statistics",
    response_model=WorkflowStatistics,
    tags=["Workflows"],
    summary="Get workflow statistics",
    description="Get statistics about a workflow (iterations, notes, searches)",
)
async def get_workflow_statistics(workflow_id: str):
    """
    Get workflow statistics.

    Args:
        workflow_id: Workflow identifier

    Returns:
        WorkflowStatistics with various metrics

    Raises:
        HTTPException: If workflow not found
    """
    workflow = db.get_workflow(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    stats = db.get_statistics(workflow_id)

    return WorkflowStatistics(
        workflow_id=workflow_id,
        iterations=stats["iterations"],
        research_notes=stats["notes"],
        searches=stats["searches"],
        approvals=stats["approvals"],
    )


@app.get(
    "/workflows",
    tags=["Workflows"],
    summary="List all workflows",
    description="Get a list of all workflows in history",
)
async def list_workflows():
    """
    List all workflows.

    Returns:
        List of workflows with basic information
    """
    workflows = db.get_workflow_history()

    return {
        "count": len(workflows),
        "workflows": workflows,
    }


@app.delete(
    "/workflows/{workflow_id}",
    tags=["Workflows"],
    summary="Delete workflow",
    description="Delete a workflow and its associated data",
)
async def delete_workflow(workflow_id: str):
    """
    Delete workflow.

    Args:
        workflow_id: Workflow identifier

    Returns:
        Confirmation message

    Raises:
        HTTPException: If workflow not found
    """
    workflow = db.get_workflow(workflow_id)

    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    # In a production system, you'd delete from database
    # For now, just return confirmation
    return {
        "message": f"Workflow {workflow_id} marked for deletion",
        "workflow_id": workflow_id,
    }


# Error handlers


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return HTTPException(status_code=400, detail=str(exc))


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return HTTPException(status_code=500, detail="Internal server error")


# Startup/Shutdown events


@app.on_event("startup")
async def startup_event():
    """Run on server startup."""
    print("Deep Research Workflow API started")
    print("API Documentation: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on server shutdown."""
    db.close()
    print("Deep Research Workflow API stopped")


# CLI entry point


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )
