"""Task 3: generate LLM responses for enriched comments."""

import logging
from datetime import datetime, timezone
from typing import Dict, List

from .response_generator import ResponseGenerator

logger = logging.getLogger(__name__)


class GenerateResponsesTask:
    """Generate contextual replies for comments."""

    def run(self, enriched_comments: List[Dict], provider: str = "openai") -> List[Dict]:
        """Return enriched comments with generated response data attached."""
        logger.info("=" * 80)
        logger.info("TASK 3: Generating contextual responses")
        logger.info("=" * 80)

        generator = ResponseGenerator(provider=provider)
        comments_with_responses = []

        for comment in enriched_comments:
            logger.info(f"Generating response for comment {comment['comment_id']}...")
            response_text = generator.generate_response(comment)

            if not response_text:
                logger.warning(f"Failed to generate response for {comment['comment_id']}")
                continue

            comment_with_response = comment.copy()
            comment_with_response['generated_response'] = response_text
            comment_with_response['generated_by'] = f"{provider}:{generator.model}"
            comment_with_response['generated_at'] = datetime.now(timezone.utc).isoformat()
            comments_with_responses.append(comment_with_response)

            logger.info(f"Generated: {response_text[:100]}...")

        logger.info(f"✓ Task 3 Complete: Generated {len(comments_with_responses)} responses")
        return comments_with_responses
