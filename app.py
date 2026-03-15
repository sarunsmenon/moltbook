"""
Moltbook Profile Dashboard - Gradio App for HF Spaces
Display user profile, top submolts, and recent comments
"""

import gradio as gr
import requests
import os
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from collections import Counter

# Load environment variables
load_dotenv()

MOLTBOOK_API_KEY = os.getenv('MOLTBOOK_API_KEY')
BASE_URL = "https://www.moltbook.com/api/v1"
MOLTBOOK_BASE = "https://www.moltbook.com"

def get_headers():
    """Get API headers with authentication"""
    return {
        "Authorization": f"Bearer {MOLTBOOK_API_KEY}",
        "Content-Type": "application/json"
    }

def get_agent_profile() -> Dict:
    """Fetch the authenticated agent's profile"""
    try:
        response = requests.get(
            f"{BASE_URL}/agents/me",
            headers=get_headers(),
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        agent_info = data.get('agent', {})
        return {
            'name': agent_info.get('name', 'Unknown'),
            'karma': agent_info.get('karma', 0),
            'display_name': agent_info.get('display_name', agent_info.get('name', 'Unknown'))
        }
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return {'name': 'Error', 'karma': 0, 'display_name': 'Error'}

def get_my_posts(limit: int = 100) -> List[Dict]:
    """Fetch user's posts"""
    try:
        # Get agent name first
        profile = get_agent_profile()
        agent_name = profile['name']
        
        posts = []
        cursor = None
        max_pages = 5
        pages_checked = 0
        
        while len(posts) < limit and pages_checked < max_pages:
            params = {'sort': 'new', 'limit': 25}
            if cursor:
                params['cursor'] = cursor
            
            response = requests.get(
                f"{BASE_URL}/posts",
                headers=get_headers(),
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            all_posts = data.get('posts', [])
            
            # Filter for user's posts
            my_posts = [
                p for p in all_posts
                if p.get('author', {}).get('name') == agent_name
            ]
            
            posts.extend(my_posts)
            pages_checked += 1
            
            cursor = data.get('next_cursor')
            if not cursor:
                break
        
        return posts[:limit]
    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []

def get_recent_comments(limit: int = 10) -> List[Dict]:
    """Fetch user's recent comments by checking /home endpoint"""
    try:
        response = requests.get(
            f"{BASE_URL}/home",
            headers=get_headers(),
            timeout=10
        )
        response.raise_for_status()
        home_data = response.json()
        
        # Get activity on your posts to find your comments
        # Note: The API doesn't have a direct "my comments" endpoint,
        # so we'll fetch from your posts
        profile = get_agent_profile()
        agent_name = profile['name']
        
        comments = []
        posts = get_my_posts(limit=20)
        
        for post in posts:
            post_id = post.get('id')
            if not post_id:
                continue
            
            # Get comments on this post
            try:
                comment_response = requests.get(
                    f"{BASE_URL}/posts/{post_id}/comments",
                    headers=get_headers(),
                    params={'sort': 'new', 'limit': 50},
                    timeout=10
                )
                comment_response.raise_for_status()
                comment_data = comment_response.json()
                post_comments = comment_data.get('comments', [])
                
                # Filter for your comments
                my_comments = [
                    c for c in post_comments
                    if c.get('author', {}).get('name') == agent_name
                ]
                
                # Add post context to each comment
                for comment in my_comments:
                    comment['post_title'] = post.get('title', 'Untitled')
                    comment['post_id'] = post_id
                    comment['submolt_name'] = post.get('submolt', {}).get('name', 'unknown')
                
                comments.extend(my_comments)
                
                if len(comments) >= limit:
                    break
            except Exception as e:
                print(f"Error fetching comments for post {post_id}: {e}")
                continue
        
        # Sort by created_at (most recent first)
        comments.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return comments[:limit]
    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []

def get_top_submolts(posts: List[Dict], limit: int = 5) -> List[Tuple[str, int]]:
    """Get top submolts by post count"""
    submolt_names = [
        post.get('submolt', {}).get('name') or post.get('submolt_name', 'unknown')
        for post in posts
    ]
    
    counter = Counter(submolt_names)
    return counter.most_common(limit)

def create_header_html(profile: Dict) -> str:
    """Create the header navigation HTML"""
    username = profile['display_name']
    karma = profile['karma']
    user_url = f"{MOLTBOOK_BASE}/u/{profile['name']}"
    
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
        <div style="display: flex; align-items: center; gap: 15px;">
            <a href="{user_url}" target="_blank" 
               style="text-decoration: none; color: #3498db; font-weight: 500; font-size: 16px;">
                {username}
            </a>
            <span style="background-color: #3498db; color: white; padding: 5px 12px; 
                         border-radius: 12px; font-size: 14px; font-weight: bold;">
                {karma} karma
            </span>
        </div>
    </div>
    """
    return header_html

def create_submolt_list_html(submolts: List[Tuple[str, int]]) -> str:
    """Create HTML for top submolts list"""
    if not submolts:
        return "<p style='color: #6c757d;'>No posts found</p>"
    
    html_items = []
    for submolt_name, count in submolts:
        submolt_url = f"{MOLTBOOK_BASE}/s/{submolt_name}"
        html_items.append(f"""
        <div style="margin-bottom: 12px; padding: 12px; background-color: #f8f9fa; 
                    border-radius: 6px; border-left: 4px solid #3498db;">
            <a href="{submolt_url}" target="_blank" 
               style="text-decoration: none; color: #2c3e50; font-weight: 500; font-size: 16px;">
                s/{submolt_name}
            </a>
            <span style="color: #6c757d; margin-left: 10px; font-size: 14px;">
                ({count} post{"s" if count != 1 else ""})
            </span>
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
        post_title = comment.get('post_title', 'Untitled')
        submolt_name = comment.get('submolt_name', 'unknown')
        content = comment.get('content', '')
        
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
                ID: {comment_id} • s/{submolt_name}
            </div>
        </div>
        """)
    
    return "".join(html_items)

def load_dashboard():
    """Load all dashboard data"""
    profile = get_agent_profile()
    posts = get_my_posts(limit=100)
    comments = get_recent_comments(limit=10)
    top_submolts = get_top_submolts(posts, limit=5)
    
    header = create_header_html(profile)
    submolts_html = create_submolt_list_html(top_submolts)
    comments_html = create_comments_list_html(comments)
    
    return header, submolts_html, comments_html

# Create Gradio interface
with gr.Blocks(title="Moltbook Dashboard") as app:
    with gr.Row():
        header_display = gr.HTML(label="")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🔥 Top 5 Submolts")
            submolt_display = gr.HTML(label="")
        
        with gr.Column(scale=1):
            gr.Markdown("### 💬 Recent Comments")
            comments_display = gr.HTML(label="")
    
    with gr.Row():
        refresh_btn = gr.Button("🔄 Refresh Dashboard", variant="primary")
    
    # Load initial data
    app.load(
        fn=load_dashboard,
        outputs=[header_display, submolt_display, comments_display]
    )
    
    # Refresh button
    refresh_btn.click(
        fn=load_dashboard,
        outputs=[header_display, submolt_display, comments_display]
    )

if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft())
