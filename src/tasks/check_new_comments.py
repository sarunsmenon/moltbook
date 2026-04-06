"""Task 1: discover new comments on the agent's posts."""

import logging
from typing import Dict, List

from src.core.moltbook_client import MoltbookClient
from utils import StateManager

logger = logging.getLogger(__name__)


class CheckNewCommentsTask:
    """Find unprocessed comments on the authenticated agent's posts."""

    def __init__(self, client: MoltbookClient, state_manager: StateManager):
        self.client = client
        self.state = state_manager

    def run(self) -> List[Dict]:
        """Return newly discovered comments with post metadata."""
        logger.info("=" * 80)
        logger.info("TASK 1: Checking for new comments on your posts")
        logger.info("=" * 80)

        my_posts = self.client.get_my_posts()
        new_comments = []

        for post in my_posts:
            post_id = post.get('id')
            post_title = post.get('title', '')
            post_content = post.get('content', '')
            submolt = post.get('submolt', {})
            submolt_name = submolt.get('name') if isinstance(submolt, dict) else str(submolt)

            comments = self.client.get_comments_for_post(post_id)

            for comment in comments:
                comment_id = comment.get('id')
                author = comment.get('author', {})
                author_name = author.get('name') if isinstance(author, dict) else str(author)

                if author_name == self.client.agent_name:
                    continue

                if self.state.is_processed(comment_id):
                    continue

                new_comments.append({
                    'comment_id': comment_id,
                    'comment_content': comment.get('content', ''),
                    'comment_author': author_name,
                    'parent_id': comment.get('parent_id'),
                    'post_id': post_id,
                    'post_title': post_title,
                    'post_content': post_content,
                    'submolt_name': submolt_name,
                    'created_at': comment.get('created_at'),
                    'upvotes': comment.get('upvotes', 0),
                })

        logger.info(f"✓ Task 1 Complete: Found {len(new_comments)} new comments")
        return new_comments
