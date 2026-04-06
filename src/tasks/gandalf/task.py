"""Task 7: generate and post a Gandalf quote."""

import logging

from src.core.moltbook_client import MoltbookClient
from .poster import GandalfPoster

logger = logging.getLogger(__name__)


class PostGandalfQuoteTask:
    """Generate and optionally publish a Gandalf quote to Moltbook."""

    def __init__(self, client: MoltbookClient):
        self.client = client

    def run(self, dry_run: bool = False) -> bool:
        """Generate and post the daily Gandalf quote."""
        logger.info("=" * 80)
        logger.info("TASK 7: Posting Gandalf quote to /m/lotr")
        logger.info("=" * 80)

        if dry_run:
            logger.info("DRY RUN MODE - Not actually posting quote")

        try:
            gandalf = GandalfPoster()

            if dry_run:
                quote_data = gandalf.generate_gandalf_quote()
                if not quote_data:
                    logger.warning("✗ Task 7 Failed: Could not generate Gandalf quote")
                    return False

                logger.info(f"Would post: {quote_data['title']}")
                logger.info(f"Content: {quote_data['content'][:200]}...")
                logger.info("✓ Task 7 Complete: Successfully generated Gandalf quote (dry run)")
                return True

            success = gandalf.post_gandalf_quote(self.client)

            if success:
                logger.info("✓ Task 7 Complete: Successfully posted Gandalf quote")
            else:
                logger.warning("✗ Task 7 Failed: Could not post Gandalf quote")

            return success

        except Exception as e:
            logger.error(f"✗ Task 7 Failed with error: {e}", exc_info=True)
            return False
