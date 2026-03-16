"""
Moltbook Profile Dashboard - Gradio App for HF Spaces
Display user profile, recent posts, and recent comments
"""

import sys
from pathlib import Path

# Add project root to path for proper imports
sys.path.insert(0, str(Path(__file__).parent))

import gradio as gr
from dotenv import load_dotenv
from utils.gradio_utils import load_dashboard, reply_to_new_comments, post_gandalf_quote

# Load environment variables
load_dotenv()

# Create Gradio interface
with gr.Blocks(title="Moltbook Dashboard") as app:
    with gr.Row():
        header_display = gr.HTML(label="")
    
    # Action buttons row
    with gr.Row():
        reply_btn = gr.Button("💬 Reply to New Comments", variant="primary", size="lg")
        gandalf_btn = gr.Button("🧙 Post Gandalf Quote", variant="primary", size="lg")
        refresh_btn = gr.Button("🔄 Refresh Dashboard", variant="secondary", size="lg")
    
    # Status display for actions
    with gr.Row():
        status_display = gr.HTML(label="", visible=True)
    
    # Main content
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Recent Posts")
            posts_display = gr.HTML(label="")
        
        with gr.Column(scale=1):
            gr.Markdown("### 💬 Recent Comments")
            comments_display = gr.HTML(label="")
    
    # Load initial data
    app.load(
        fn=load_dashboard,
        outputs=[header_display, posts_display, comments_display]
    )
    
    # Reply button - calls the workflow and shows status
    def handle_reply_click():
        status = reply_to_new_comments()
        # Show status without auto-refresh to avoid API rate limits
        # User can click Refresh button manually
        return status
    
    reply_btn.click(
        fn=handle_reply_click,
        outputs=status_display
    )
    
    # Gandalf button - posts a Gandalf quote to /m/lotr
    def handle_gandalf_click():
        status = post_gandalf_quote()
        # Show status without auto-refresh to avoid API rate limits
        # User can click Refresh button manually
        return status
    
    gandalf_btn.click(
        fn=handle_gandalf_click,
        outputs=status_display
    )
    
    # Refresh button - reloads dashboard data
    def handle_refresh_click():
        header, posts, comments = load_dashboard()
        return header, posts, comments
    
    refresh_btn.click(
        fn=handle_refresh_click,
        outputs=[header_display, posts_display, comments_display]
    )

if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft())
