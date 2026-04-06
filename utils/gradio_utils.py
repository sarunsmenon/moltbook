"""
Gradio dashboard utilities for Moltbook.

This module contains API calls and HTML generation functions
for the Gradio dashboard interface.
"""

import requests
import os
import logging
from typing import Dict, List
from datetime import datetime, timezone

# Configure logging for Gradio
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import Settings for configuration
from config import Settings

BASE_URL = Settings.MOLTBOOK_BASE_URL
MOLTBOOK_BASE = Settings.MOLTBOOK_WEB_BASE


def get_headers() -> Dict[str, str]:
    """Get API headers with authentication"""
    return Settings.get_headers()


def get_agent_profile() -> Dict:
    """Fetch the authenticated agent's profile with recent posts and comments"""
    try:
        # First get basic profile to get the agent name
        response = requests.get(
            f"{BASE_URL}/agents/me",
            headers=get_headers(),
            timeout=Settings.GRADIO_REQUEST_TIMEOUT
        )
        response.raise_for_status()
        me_data = response.json()
        agent_info = me_data.get('agent', {})
        agent_name = agent_info.get('name', 'Unknown')
        
        # Now get full profile with recent posts and comments
        profile_response = requests.get(
            f"{BASE_URL}/agents/profile",
            headers=get_headers(),
            params={'name': agent_name},
            timeout=Settings.GRADIO_REQUEST_TIMEOUT
        )
        profile_response.raise_for_status()
        profile_data = profile_response.json()
        
        return profile_data
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return {
            'agent': {'name': 'Error', 'karma': 0, 'display_name': 'Error'},
            'recentPosts': [],
            'recentComments': []
        }


def create_header_html(agent: Dict) -> str:
    """Create the header navigation HTML"""
    username = agent.get('display_name') or agent.get('name', 'Unknown')
    karma = agent.get('karma', 0)
    followers = agent.get('follower_count', 0)
    following = agent.get('following_count', 0)
    user_url = f"{MOLTBOOK_BASE}/u/{agent.get('name', '')}"
    
    header_html = f"""
    <div style="display: flex; justify-content: space-between; align-items: center; 
                padding: 15px 20px; background-color: #f8f9fa; border-radius: 8px; 
                margin-bottom: 20px; border: 1px solid #dee2e6;">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 24px; font-weight: bold; color: #e74c3c;">🦞</span>
            <span style="font-size: 20px; font-weight: bold; margin-left: 10px; color: #2c3e50;">
                Moltbook Dashboard
            </span>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <a href="{user_url}" target="_blank" 
               style="text-decoration: none; color: #3498db; font-weight: 500; font-size: 16px;">
                {username}
            </a>
            <span style="background-color: #3498db; color: white; padding: 5px 12px; 
                         border-radius: 12px; font-size: 13px; font-weight: bold;">
                {karma} karma
            </span>
            <span style="background-color: #27ae60; color: white; padding: 5px 12px; 
                         border-radius: 12px; font-size: 13px; font-weight: bold;">
                {followers} followers
            </span>
            <span style="background-color: #8e44ad; color: white; padding: 5px 12px; 
                         border-radius: 12px; font-size: 13px; font-weight: bold;">
                {following} following
            </span>
        </div>
    </div>
    """
    return header_html


def create_posts_list_html(posts: List[Dict]) -> str:
    """Create HTML for recent posts list"""
    if not posts:
        return "<p style='color: #6c757d;'>No posts found</p>"
    
    # Limit to configured max posts
    max_posts = Settings.GRADIO_MAX_POSTS_DISPLAY
    limited_posts = posts[:max_posts]
    total_count = len(posts)
    
    html_items = []
    for post in limited_posts:
        post_id = post.get('id', '')
        title = post.get('title', 'Untitled')
        submolt_name = post.get('submolt', {}).get('name') or post.get('submolt_name', 'unknown')
        upvotes = post.get('upvotes', 0)
        comment_count = post.get('comment_count', 0)
        
        # Create link to post
        post_url = f"{MOLTBOOK_BASE}/post/{post_id}"
        
        html_items.append(f"""
        <div style="margin-bottom: 12px; padding: 12px; background-color: #f8f9fa; 
                    border-radius: 6px; border-left: 4px solid #3498db;">
            <div style="margin-bottom: 6px;">
                <a href="{post_url}" target="_blank" 
                   style="text-decoration: none; color: #2c3e50; font-weight: 500; font-size: 15px;">
                    {title}
                </a>
            </div>
            <div style="font-size: 12px; color: #6c757d;">
                s/{submolt_name} • ⬆️ {upvotes} • 💬 {comment_count}
            </div>
        </div>
        """)
    
    # Add info message if there are more posts
    posts_html = "".join(html_items)
    if total_count > max_posts:
        posts_html += f"""
        <div style="margin-top: 10px; padding: 10px; background-color: #e7f3ff;
                    border-radius: 6px; text-align: center; color: #0066cc; font-size: 13px;">
            Showing {max_posts} of {total_count} posts
        </div>
        """
    
    # Wrap in scrollable container
    scroll_height = Settings.GRADIO_POSTS_SCROLL_HEIGHT
    return f"""
    <div style="max-height: {scroll_height}px; overflow-y: auto; padding-right: 5px;">
        {posts_html}
    </div>
    """


def create_comments_list_html(comments: List[Dict]) -> str:
    """Create HTML for recent comments list"""
    if not comments:
        return "<p style='color: #6c757d;'>No comments found</p>"
    
    # Limit to configured max comments
    max_comments = Settings.GRADIO_MAX_COMMENTS_DISPLAY
    limited_comments = comments[:max_comments]
    total_count = len(comments)
    
    html_items = []
    for comment in limited_comments:
        comment_id = comment.get('id', 'unknown')
        post_id = comment.get('post', {}).get('id', '')
        post_title = comment.get('post', {}).get('title') or comment.get('post_title', 'Untitled')
        submolt_name = comment.get('post', {}).get('submolt', {}).get('name') or comment.get('submolt_name', 'unknown')
        content = comment.get('content', '')
        upvotes = comment.get('upvotes', 0)
        
        # Truncate content if too long
        truncate_length = Settings.GRADIO_COMMENT_CONTENT_TRUNCATE
        display_content = content[:truncate_length] + "..." if len(content) > truncate_length else content
        
        # Create link to comment
        comment_url = f"{MOLTBOOK_BASE}/post/{post_id}"

        html_items.append(f"""
        <div style="margin-bottom: 15px; padding: 15px; background-color: #f8f9fa; 
                    border-radius: 6px; border-left: 4px solid #e74c3c;">
            <div style="margin-bottom: 8px;">
                <a href="{comment_url}" target="_blank" 
                   style="text-decoration: none; color: #2c3e50; font-weight: 500;">
                    On: {post_title}
                </a>
            </div>
            <div style="color: #495057; font-size: 14px; margin-bottom: 6px;">
                {display_content}
            </div>
            <div style="font-size: 12px; color: #6c757d;">
                ID: {comment_id} • s/{submolt_name} • ⬆️ {upvotes}
            </div>
        </div>
        """)
    
    # Add info message if there are more comments
    comments_html = "".join(html_items)
    if total_count > max_comments:
        comments_html += f"""
        <div style="margin-top: 10px; padding: 10px; background-color: #fff3e0;
                    border-radius: 6px; text-align: center; color: #e65100; font-size: 13px;">
            Showing {max_comments} of {total_count} comments
        </div>
        """
    
    # Wrap in scrollable container
    scroll_height = Settings.GRADIO_COMMENTS_SCROLL_HEIGHT
    return f"""
    <div style="max-height: {scroll_height}px; overflow-y: auto; padding-right: 5px;">
        {comments_html}
    </div>
    """


def reply_to_new_comments(llm_provider: str = "openai") -> str:
    """
    Reply to new comments on your posts.
    
    Args:
        llm_provider: LLM provider to use ('openai' or 'anthropic')
    
    Returns:
        Status message as HTML
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting reply_to_new_comments workflow")
        logger.info(f"LLM Provider: {llm_provider}")
        logger.info("=" * 60)
        
        from config import Settings
        from utils import StateManager, RateLimiter
        from src import MoltbookClient, WorkflowTasks
        
        # Ensure directories exist
        logger.info("Creating necessary directories...")
        Settings.create_directories()
        
        # Validate settings
        logger.info("Validating settings...")
        Settings.validate()
        
        # Initialize components
        logger.info("Initializing workflow components...")
        client = MoltbookClient()
        state_manager = StateManager(Settings.PROCESSED_COMMENTS_FILE)
        rate_limiter = RateLimiter(
            cooldown_seconds=Settings.COMMENT_COOLDOWN_SECONDS,
            daily_limit=Settings.DAILY_COMMENT_LIMIT
        )
        workflow = WorkflowTasks(client, state_manager, rate_limiter)
        
        # Check for new comments
        logger.info("Checking for new comments...")
        new_comments = workflow.task1_check_new_comments()
        
        if not new_comments:
            logger.info("No new comments found")
            return """
            <div style="padding: 15px; background-color: #fff3cd; border: 1px solid #ffc107;
                        border-radius: 6px; color: #856404;">
                <strong>ℹ️ No New Comments</strong><br>
                No new comments found on your posts.
            </div>
            """
        
        logger.info(f"Found {len(new_comments)} new comment(s)")
        
        # Build context
        logger.info("Building context for comments...")
        enriched_comments = workflow.task2_build_context(new_comments)
        
        if not enriched_comments:
            logger.error("Failed to build context for comments")
            return """
            <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb;
                        border-radius: 6px; color: #721c24;">
                <strong>❌ Error</strong><br>
                Failed to build context for comments.
            </div>
            """
        
        logger.info(f"Built context for {len(enriched_comments)} comment(s)")
        
        # Generate responses
        logger.info(f"Generating responses using {llm_provider}...")
        comments_with_responses = workflow.task3_generate_responses(
            enriched_comments,
            provider=llm_provider
        )
        
        if not comments_with_responses:
            logger.error("Failed to generate responses")
            return """
            <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb;
                        border-radius: 6px; color: #721c24;">
                <strong>❌ Error</strong><br>
                Failed to generate responses.
            </div>
            """
        
        logger.info(f"Generated {len(comments_with_responses)} response(s)")
        
        # Send replies
        logger.info("Sending replies...")
        results = workflow.task4_send_replies(comments_with_responses, dry_run=False)
        
        logger.info(f"Workflow complete: {results['success']} successful, {results['failed']} failed")
        
        return f"""
        <div style="padding: 15px; background-color: #d4edda; border: 1px solid #c3e6cb;
                    border-radius: 6px; color: #155724;">
            <strong>✅ Success</strong><br>
            Processed {len(new_comments)} new comment(s).<br>
            Replies sent: {results['success']}<br>
            Failed: {results['failed']}
        </div>
        """
        
    except ValueError as e:
        # Configuration/validation errors
        logger.error(f"Configuration error: {e}", exc_info=True)
        return f"""
        <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb;
                    border-radius: 6px; color: #721c24;">
            <strong>❌ Configuration Error</strong><br>
            {str(e)}<br><br>
            <small>Please check your environment variables and API keys.</small>
        </div>
        """
    except ImportError as e:
        # Import errors
        logger.error(f"Import error: {e}", exc_info=True)
        return f"""
        <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb;
                    border-radius: 6px; color: #721c24;">
            <strong>❌ Import Error</strong><br>
            {str(e)}<br><br>
            <small>There may be a module dependency issue.</small>
        </div>
        """
    except Exception as e:
        # General errors
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return f"""
        <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb;
                    border-radius: 6px; color: #721c24;">
            <strong>❌ Error</strong><br>
            {str(e)}<br><br>
            <small>Check the console logs for more details.</small>
        </div>
        """


def post_gandalf_quote() -> str:
    """
    Post a Gandalf quote to /m/lotr.
    
    Returns:
        Status message as HTML
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting Gandalf quote posting")
        logger.info("=" * 60)
        
        from config import Settings
        from src import MoltbookClient, WorkflowTasks
        from utils import StateManager, RateLimiter
        
        # Ensure directories exist
        logger.info("Creating necessary directories...")
        Settings.create_directories()
        
        # Validate settings
        logger.info("Validating settings...")
        Settings.validate()
        
        # Initialize components
        logger.info("Initializing workflow components...")
        client = MoltbookClient()
        state_manager = StateManager(Settings.PROCESSED_COMMENTS_FILE)
        rate_limiter = RateLimiter(
            cooldown_seconds=Settings.COMMENT_COOLDOWN_SECONDS,
            daily_limit=Settings.DAILY_COMMENT_LIMIT
        )
        workflow = WorkflowTasks(client, state_manager, rate_limiter)
        
        # Post Gandalf quote
        logger.info("Posting Gandalf quote to /m/lotr...")
        success = workflow.task7_post_gandalf_quote(dry_run=False)
        
        if success:
            logger.info("Successfully posted Gandalf quote")
            return """
            <div style="padding: 15px; background-color: #d4edda; border: 1px solid #c3e6cb;
                        border-radius: 6px; color: #155724;">
                <strong>✅ Success</strong><br>
                Successfully posted a Gandalf quote to /m/lotr!
            </div>
            """
        else:
            logger.warning("Failed to post Gandalf quote")
            return """
            <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb;
                        border-radius: 6px; color: #721c24;">
                <strong>❌ Failed</strong><br>
                Could not post Gandalf quote. Check logs for details.
            </div>
            """
        
    except ValueError as e:
        # Configuration/validation errors
        logger.error(f"Configuration error: {e}", exc_info=True)
        return f"""
        <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb;
                    border-radius: 6px; color: #721c24;">
            <strong>❌ Configuration Error</strong><br>
            {str(e)}<br><br>
            <small>Please check your environment variables and API keys.</small>
        </div>
        """
    except ImportError as e:
        # Import errors
        logger.error(f"Import error: {e}", exc_info=True)
        return f"""
        <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb;
                    border-radius: 6px; color: #721c24;">
            <strong>❌ Import Error</strong><br>
            {str(e)}<br><br>
            <small>There may be a module dependency issue.</small>
        </div>
        """
    except Exception as e:
        # General errors
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return f"""
        <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb;
                    border-radius: 6px; color: #721c24;">
            <strong>❌ Error</strong><br>
            {str(e)}<br><br>
            <small>Check the console logs for more details.</small>
        </div>
        """


def load_dashboard():
    """Load all dashboard data and return HTML components"""
    profile_data = get_agent_profile()
    
    agent = profile_data.get('agent', {})
    recent_posts = profile_data.get('recentPosts', [])
    recent_comments = profile_data.get('recentComments', [])
    
    header = create_header_html(agent)
    posts_html = create_posts_list_html(recent_posts)
    comments_html = create_comments_list_html(recent_comments)
    
    return header, posts_html, comments_html
