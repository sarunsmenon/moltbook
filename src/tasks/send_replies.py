"""Task 4: send generated replies back to Moltbook."""

import logging
from typing import Dict, List

from src.core.moltbook_client import MoltbookClient
from utils import RateLimiter, StateManager

logger = logging.getLogger(__name__)


class SendRepliesTask:
    """Post generated responses while honoring rate limits and state."""

    def __init__(
        self,
        client: MoltbookClient,
        state_manager: StateManager,
        rate_limiter: RateLimiter,
    ):
        self.client = client
        self.state = state_manager
        self.rate_limiter = rate_limiter

    def run(self, comments_with_responses: List[Dict], dry_run: bool = False) -> Dict[str, int]:
        """Send replies and return success and failure counts."""
        logger.info("=" * 80)
        logger.info("TASK 4: Sending replies to comments")
        logger.info("=" * 80)

        if dry_run:
            logger.info("DRY RUN MODE - Not actually posting replies")

        results = {'success': 0, 'failed': 0}

        for comment in comments_with_responses:
            comment_id = comment['comment_id']
            post_id = comment['post_id']
            response_text = comment['generated_response']

            logger.info(f"Posting reply to comment {comment_id}...")

            if dry_run:
                logger.info(f"Would post: {response_text}")
                results['success'] += 1
                continue

            if not self.rate_limiter.wait_if_needed():
                logger.error("Daily comment limit reached")
                results['failed'] += 1
                continue

            response = self.client.post_comment(
                post_id=post_id,
                content=response_text,
                parent_id=comment_id,
            )

            if response:
                self.rate_limiter.record_comment()
                self.state.mark_processed(comment_id)
                results['success'] += 1
            else:
                results['failed'] += 1

        logger.info(
            f"✓ Task 4 Complete: {results['success']} successful, {results['failed']} failed"
        )
        return results
