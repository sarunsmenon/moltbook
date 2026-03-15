"""
Gradio dashboard utilities for Moltbook.

This module contains API calls and HTML generation functions
for the Gradio dashboard interface.
"""

import requests
import os
from typing import Dict, List

BASE_URL = "https://www.moltbook.com/api/v1"
MOLTBOOK_BASE = "https://www.moltbook.com"


def get_headers() -> Dict[str, str]:
    """Get API headers with authentication"""
    api_key = os.getenv('MOLTBOOK_API_KEY')
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


def get_agent_profile() -> Dict:
    """Fetch the authenticated agent's profile with recent posts and comments"""
    try:
        # First get basic profile to get the agent name
        response = requests.get(
            f"{BASE_URL}/agents/me",
            headers=get_headers(),
            timeout=10
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
            timeout=10
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
    
    html_items = []
    for post in posts:
        post_id = post.get('id', '')
        title = post.get('title', 'Untitled')
        submolt_name = post.get('submolt', {}).get('name') or post.get('submolt_name', 'unknown')
        upvotes = post.get('upvotes', 0)
        comment_count = post.get('comment_count', 0)
        
        # Create link to post
        post_url = f"{MOLTBOOK_BASE}/s/{submolt_name}/comments/{post_id}"
        
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
    
    return "".join(html_items)


def create_comments_list_html(comments: List[Dict]) -> str:
    """Create HTML for recent comments list"""
    if not comments:
        return "<p style='color: #6c757d;'>No comments found</p>"
    
    html_items = []
    for comment in comments:
        comment_id = comment.get('id', 'unknown')
        post_id = comment.get('post_id', '')
        post_title = comment.get('post', {}).get('title') or comment.get('post_title', 'Untitled')
        submolt_name = comment.get('post', {}).get('submolt', {}).get('name') or comment.get('submolt_name', 'unknown')
        content = comment.get('content', '')
        upvotes = comment.get('upvotes', 0)
        
        # Truncate content if too long
        display_content = content[:150] + "..." if len(content) > 150 else content
        
        # Create link to comment
        comment_url = f"{MOLTBOOK_BASE}/s/{submolt_name}/comments/{post_id}#{comment_id}"
        
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
    
    return "".join(html_items)


def reply_to_new_comments(llm_provider: str = "openai") -> str:
    """
    Reply to new comments on your posts.
    
    Args:
        llm_provider: LLM provider to use ('openai' or 'anthropic')
    
    Returns:
        Status message as HTML
    """
    try:
        from pathlib import Path
        from config import Settings
        from utils import StateManager, RateLimiter
        from src import MoltbookClient, WorkflowTasks
        
        # Initialize components
        client = MoltbookClient()
        state_manager = StateManager(Settings.PROCESSED_COMMENTS_FILE)
        rate_limiter = RateLimiter(
            cooldown_seconds=Settings.COMMENT_COOLDOWN_SECONDS,
            daily_limit=Settings.DAILY_COMMENT_LIMIT
        )
        workflow = WorkflowTasks(client, state_manager, rate_limiter)
        
        # Check for new comments
        new_comments = workflow.task1_check_new_comments()
        
        if not new_comments:
            return """
            <div style="padding: 15px; background-color: #fff3cd; border: 1px solid #ffc107; 
                        border-radius: 6px; color: #856404;">
                <strong>ℹ️ No New Comments</strong><br>
                No new comments found on your posts.
            </div>
            """
        
        # Build context
        enriched_comments = workflow.task2_build_context(new_comments)
        
        if not enriched_comments:
            return """
            <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb; 
                        border-radius: 6px; color: #721c24;">
                <strong>❌ Error</strong><br>
                Failed to build context for comments.
            </div>
            """
        
        # Generate responses
        comments_with_responses = workflow.task3_generate_responses(
            enriched_comments,
            provider=llm_provider
        )
        
        if not comments_with_responses:
            return """
            <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb; 
                        border-radius: 6px; color: #721c24;">
                <strong>❌ Error</strong><br>
                Failed to generate responses.
            </div>
            """
        
        # Send replies
        results = workflow.task4_send_replies(comments_with_responses, dry_run=False)
        
        return f"""
        <div style="padding: 15px; background-color: #d4edda; border: 1px solid #c3e6cb; 
                    border-radius: 6px; color: #155724;">
            <strong>✅ Success</strong><br>
            Processed {len(new_comments)} new comment(s).<br>
            Replies sent: {results['success']}<br>
            Failed: {results['failed']}
        </div>
        """
        
    except Exception as e:
        return f"""
        <div style="padding: 15px; background-color: #f8d7da; border: 1px solid #f5c6cb; 
                    border-radius: 6px; color: #721c24;">
            <strong>❌ Error</strong><br>
            {str(e)}
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
