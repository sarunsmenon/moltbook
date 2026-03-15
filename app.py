"""
Moltbook Profile Dashboard - Gradio App for HF Spaces
Display user profile, recent posts, and recent comments
"""

import gradio as gr
from dotenv import load_dotenv
from utils.gradio_utils import load_dashboard, reply_to_new_comments

# Load environment variables
load_dotenv()

# Create Gradio interface
with gr.Blocks(title="Moltbook Dashboard") as app:
    with gr.Row():
        header_display = gr.HTML(label="")
    
    # Action buttons row
    with gr.Row():
        reply_btn = gr.Button("💬 Reply to New Comments", variant="primary", size="lg")
        refresh_btn = gr.Button("🔄 Refresh Dashboard", variant="secondary", size="lg")
    
    # Status display for reply action
    with gr.Row():
        status_display = gr.HTML(label="", visible=False)
    
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
        # Also refresh the dashboard after replying
        header, posts, comments = load_dashboard()
        return status, gr.HTML(visible=True), header, posts, comments
    
    reply_btn.click(
        fn=handle_reply_click,
        outputs=[status_display, status_display, header_display, posts_display, comments_display]
    )
    
    # Refresh button - reloads dashboard data
    def handle_refresh_click():
        header, posts, comments = load_dashboard()
        return "", gr.HTML(visible=False), header, posts, comments
    
    refresh_btn.click(
        fn=handle_refresh_click,
        outputs=[status_display, status_display, header_display, posts_display, comments_display]
    )

if __name__ == "__main__":
    app.launch(theme=gr.themes.Soft())
