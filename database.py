"""
Database layer for Deep Research Workflow System.

Provides SQLite-based persistence for:
- Workflow execution history
- Research notes and sources
- Report versions and iterations
- User approvals and feedback
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger("database")


class WorkflowDatabase:
    """SQLite database for workflow persistence."""

    def __init__(self, db_path: str = "deepresearch.db"):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = Path(db_path)
        self.connection = None
        self._initialize()

    def _initialize(self):
        """Initialize database schema."""
        self.connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()
        logger.info(f"Database initialized: {self.db_path}")

    def _create_tables(self):
        """Create database tables if they don't exist."""
        cursor = self.connection.cursor()

        # Workflows table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS workflows (
                workflow_id TEXT PRIMARY KEY,
                user_prompt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                status TEXT DEFAULT 'in_progress',
                research_plan TEXT,
                draft_report TEXT,
                final_report TEXT,
                summary TEXT,
                output_path TEXT,
                error_message TEXT
            )
            """
        )

        # Research notes table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS research_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_id TEXT NOT NULL,
                source_url TEXT,
                source_title TEXT,
                note_content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                category TEXT,
                FOREIGN KEY (workflow_id) REFERENCES workflows(workflow_id)
            )
            """
        )

        # Iterations table (for tracking revisions)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS iterations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_id TEXT NOT NULL,
                iteration_number INTEGER,
                stage TEXT,
                input_content TEXT,
                output_content TEXT,
                feedback TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (workflow_id) REFERENCES workflows(workflow_id)
            )
            """
        )

        # User approvals table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS approvals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_id TEXT NOT NULL,
                approval_type TEXT,
                content TEXT NOT NULL,
                approved BOOLEAN,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                FOREIGN KEY (workflow_id) REFERENCES workflows(workflow_id)
            )
            """
        )

        # Search history table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_id TEXT NOT NULL,
                search_type TEXT,
                query TEXT NOT NULL,
                results_count INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (workflow_id) REFERENCES workflows(workflow_id)
            )
            """
        )

        self.connection.commit()
        logger.debug("Database tables created/verified")

    def save_workflow(
        self,
        workflow_id: str,
        user_prompt: str,
        status: str = "in_progress",
    ):
        """
        Save workflow to database.

        Args:
            workflow_id: Unique workflow identifier
            user_prompt: User's research prompt
            status: Workflow status
        """
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO workflows
            (workflow_id, user_prompt, status)
            VALUES (?, ?, ?)
            """,
            (workflow_id, user_prompt, status),
        )

        self.connection.commit()
        logger.info(f"Workflow saved: {workflow_id}")

    def update_workflow(
        self,
        workflow_id: str,
        status: str = None,
        research_plan: str = None,
        draft_report: str = None,
        final_report: str = None,
        summary: str = None,
        output_path: str = None,
        error_message: str = None,
    ):
        """
        Update workflow information.

        Args:
            workflow_id: Workflow identifier
            status: New status
            research_plan: Research plan content
            draft_report: Draft report content
            final_report: Final report content
            summary: Executive summary
            output_path: Path to output file
            error_message: Error message if failed
        """
        cursor = self.connection.cursor()

        updates = []
        values = []

        if status is not None:
            updates.append("status = ?")
            values.append(status)

        if research_plan is not None:
            updates.append("research_plan = ?")
            values.append(research_plan)

        if draft_report is not None:
            updates.append("draft_report = ?")
            values.append(draft_report)

        if final_report is not None:
            updates.append("final_report = ?")
            values.append(final_report)

        if summary is not None:
            updates.append("summary = ?")
            values.append(summary)

        if output_path is not None:
            updates.append("output_path = ?")
            values.append(output_path)

        if error_message is not None:
            updates.append("error_message = ?")
            values.append(error_message)

        if status == "completed":
            updates.append("completed_at = CURRENT_TIMESTAMP")

        if updates:
            values.append(workflow_id)
            query = f"UPDATE workflows SET {', '.join(updates)} WHERE workflow_id = ?"
            cursor.execute(query, values)
            self.connection.commit()
            logger.info(f"Workflow updated: {workflow_id}")

    def get_workflow(self, workflow_id: str) -> Optional[Dict]:
        """
        Retrieve workflow information.

        Args:
            workflow_id: Workflow identifier

        Returns:
            Workflow data or None
        """
        cursor = self.connection.cursor()

        cursor.execute("SELECT * FROM workflows WHERE workflow_id = ?", (workflow_id,))
        row = cursor.fetchone()

        if row:
            return dict(row)

        return None

    def add_research_note(
        self,
        workflow_id: str,
        note_content: str,
        source_url: Optional[str] = None,
        source_title: Optional[str] = None,
        category: Optional[str] = None,
    ):
        """
        Add a research note.

        Args:
            workflow_id: Workflow identifier
            note_content: Note content
            source_url: Source URL
            source_title: Source title
            category: Note category
        """
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO research_notes
            (workflow_id, note_content, source_url, source_title, category)
            VALUES (?, ?, ?, ?, ?)
            """,
            (workflow_id, note_content, source_url, source_title, category),
        )

        self.connection.commit()
        logger.debug(f"Research note added for workflow: {workflow_id}")

    def get_research_notes(self, workflow_id: str) -> List[Dict]:
        """
        Retrieve research notes for a workflow.

        Args:
            workflow_id: Workflow identifier

        Returns:
            List of research notes
        """
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT * FROM research_notes WHERE workflow_id = ? ORDER BY created_at",
            (workflow_id,),
        )

        return [dict(row) for row in cursor.fetchall()]

    def record_iteration(
        self,
        workflow_id: str,
        iteration_number: int,
        stage: str,
        input_content: str,
        output_content: str,
        feedback: Optional[str] = None,
    ):
        """
        Record an iteration step.

        Args:
            workflow_id: Workflow identifier
            iteration_number: Iteration number
            stage: Workflow stage
            input_content: Input to this stage
            output_content: Output from this stage
            feedback: Any feedback provided
        """
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO iterations
            (workflow_id, iteration_number, stage, input_content, output_content, feedback)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                workflow_id,
                iteration_number,
                stage,
                input_content,
                output_content,
                feedback,
            ),
        )

        self.connection.commit()
        logger.debug(f"Iteration recorded: {workflow_id}, stage: {stage}")

    def record_approval(
        self,
        workflow_id: str,
        approval_type: str,
        content: str,
        approved: bool,
        notes: Optional[str] = None,
    ):
        """
        Record a user approval decision.

        Args:
            workflow_id: Workflow identifier
            approval_type: Type of approval (plan, revision, etc.)
            content: Content being approved
            approved: Whether it was approved
            notes: User notes
        """
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO approvals
            (workflow_id, approval_type, content, approved, notes)
            VALUES (?, ?, ?, ?, ?)
            """,
            (workflow_id, approval_type, content, approved, notes),
        )

        self.connection.commit()
        logger.info(
            f"Approval recorded: {workflow_id}, "
            f"type: {approval_type}, approved: {approved}"
        )

    def record_search(
        self,
        workflow_id: str,
        search_type: str,
        query: str,
        results_count: int,
    ):
        """
        Record a search operation.

        Args:
            workflow_id: Workflow identifier
            search_type: Type of search (web, scholar, etc.)
            query: Search query
            results_count: Number of results
        """
        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO search_history
            (workflow_id, search_type, query, results_count)
            VALUES (?, ?, ?, ?)
            """,
            (workflow_id, search_type, query, results_count),
        )

        self.connection.commit()
        logger.debug(
            f"Search recorded: {search_type} - {query[:50]} "
            f"({results_count} results)"
        )

    def get_workflow_history(self) -> List[Dict]:
        """
        Get all workflows in history.

        Returns:
            List of all workflows
        """
        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT workflow_id, user_prompt, created_at, status, output_path
            FROM workflows
            ORDER BY created_at DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    def get_statistics(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get statistics about a workflow.

        Args:
            workflow_id: Workflow identifier

        Returns:
            Dictionary with workflow statistics
        """
        cursor = self.connection.cursor()

        # Get iteration count
        cursor.execute(
            "SELECT COUNT(*) as count FROM iterations WHERE workflow_id = ?",
            (workflow_id,),
        )
        iteration_count = cursor.fetchone()["count"]

        # Get note count
        cursor.execute(
            "SELECT COUNT(*) as count FROM research_notes WHERE workflow_id = ?",
            (workflow_id,),
        )
        note_count = cursor.fetchone()["count"]

        # Get search count
        cursor.execute(
            "SELECT COUNT(*) as count FROM search_history WHERE workflow_id = ?",
            (workflow_id,),
        )
        search_count = cursor.fetchone()["count"]

        # Get approval count
        cursor.execute(
            "SELECT COUNT(*) as count FROM approvals WHERE workflow_id = ?",
            (workflow_id,),
        )
        approval_count = cursor.fetchone()["count"]

        return {
            "iterations": iteration_count,
            "notes": note_count,
            "searches": search_count,
            "approvals": approval_count,
        }

    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")


# Global database instance
_db_instance: Optional[WorkflowDatabase] = None


def get_database(db_path: str = "deepresearch.db") -> WorkflowDatabase:
    """
    Get or create global database instance.

    Args:
        db_path: Path to database file

    Returns:
        WorkflowDatabase instance
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = WorkflowDatabase(db_path)

    return _db_instance
