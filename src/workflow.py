"""
Workflow orchestrator.

This module wires together all individual task classes into a single
facade that the entry-points (main.py, app.py, etc.) interact with.
"""

import logging
from typing import Dict, List

from src.core.moltbook_client import MoltbookClient
from src.tasks import (
    BuildContextTask,
    CheckNewCommentsTask,
    GenerateResponsesTask,
    PostGandalfQuoteTask,
    SendRepliesTask,
)
from utils import RateLimiter, StateManager

logger = logging.getLogger(__name__)


class WorkflowTasks:
    """Facade that orchestrates individual task classes."""

    def __init__(
        self,
        client: MoltbookClient,
        state_manager: StateManager,
        rate_limiter: RateLimiter
    ):
        """
        Initialize workflow tasks.

        Args:
            client: Moltbook API client
            state_manager: State manager for tracking processed comments
            rate_limiter: Rate limiter for API compliance
        """
        self.client = client
        self.state = state_manager
        self.rate_limiter = rate_limiter
        self.check_new_comments_task = CheckNewCommentsTask(client, state_manager)
        self.build_context_task = BuildContextTask(client)
        self.generate_responses_task = GenerateResponsesTask()
        self.send_replies_task = SendRepliesTask(client, state_manager, rate_limiter)
        self.post_gandalf_quote_task = PostGandalfQuoteTask(client)

    def task1_check_new_comments(self) -> List[Dict]:
        """Task 1 facade."""
        return self.check_new_comments_task.run()

    def task2_build_context(self, new_comments: List[Dict]) -> List[Dict]:
        """Task 2 facade."""
        return self.build_context_task.run(new_comments)

    def task3_generate_responses(
        self,
        enriched_comments: List[Dict],
        provider: str = "openai"
    ) -> List[Dict]:
        """Task 3 facade."""
        return self.generate_responses_task.run(enriched_comments, provider=provider)

    def task4_send_replies(
        self,
        comments_with_responses: List[Dict],
        dry_run: bool = False
    ) -> Dict[str, int]:
        """Task 4 facade."""
        return self.send_replies_task.run(comments_with_responses, dry_run=dry_run)

    def task7_post_gandalf_quote(self, dry_run: bool = False) -> bool:
        """Task 7 facade."""
        return self.post_gandalf_quote_task.run(dry_run=dry_run)
