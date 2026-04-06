"""Task 2: enrich new comments with thread context."""

import logging
from typing import Dict, List

from src.core.moltbook_client import MoltbookClient

logger = logging.getLogger(__name__)


class BuildContextTask:
    """Build conversation context for newly discovered comments."""

    def __init__(self, client: MoltbookClient):
        self.client = client

    def run(self, new_comments: List[Dict]) -> List[Dict]:
        """Return comments enriched with conversation thread metadata."""
        logger.info("=" * 80)
        logger.info("TASK 2: Understanding what posts are being replied to")
        logger.info("=" * 80)

        enriched_comments = []

        for comment_data in new_comments:
            post_id = comment_data['post_id']
            all_comments = self.client.get_comments_for_post(post_id)

            comment = next(
                (c for c in all_comments if c.get('id') == comment_data['comment_id']),
                None,
            )

            if not comment:
                logger.warning(f"Could not find comment {comment_data['comment_id']}")
                continue

            thread = self._build_thread(comment, all_comments)

            enriched = comment_data.copy()
            enriched['conversation_thread'] = thread
            enriched['is_direct_reply'] = comment_data['parent_id'] is None
            enriched['thread_depth'] = len(thread)
            enriched_comments.append(enriched)

            thread_description = (
                'Direct reply'
                if enriched['is_direct_reply']
                else f"Thread depth {enriched['thread_depth']}"
            )
            logger.debug(f"Comment {comment_data['comment_id']}: {thread_description}")

        logger.info(f"✓ Task 2 Complete: Built context for {len(enriched_comments)} comments")
        return enriched_comments

    def _build_thread(self, comment: Dict, all_comments: List[Dict]) -> List[Dict]:
        """Build the ancestor thread for a comment from oldest to newest."""
        thread = []
        current = comment

        while current:
            thread.insert(0, current)

            parent_id = current.get('parent_id')
            if not parent_id:
                break

            current = next((c for c in all_comments if c.get('id') == parent_id), None)

        return thread
