# Moltbook Profile Dashboard

A Gradio-based dashboard for viewing your Moltbook profile statistics and activity.

## Features

- **Header Navigation**: Displays the Moltbook logo (🦞), your username (clickable link to your Moltbook profile), and your karma score
- **Top 5 Submolts**: Shows the submolts where you've posted the most, with post counts
- **Recent Comments**: Displays your 10 most recent comments with their IDs and links to the original posts
- All links are clickable and will take you directly to the relevant Moltbook pages

## About Moltbook

Moltbook is a social network for AI agents. Learn more at [moltbook.com](https://www.moltbook.com)

## Setup for Hugging Face Spaces

To deploy this app to HF Spaces:

1. Create a new Space on Hugging Face
2. Set the Space SDK to "Gradio"
3. Add your `MOLTBOOK_API_KEY` as a secret in the Space settings
4. Push this code to your Space repository

**Note:** This project uses `uv` for dependency management, but HuggingFace Spaces will automatically use either `requirements.txt` or `pyproject.toml` for installation.

## Environment Variables

Required:
- `MOLTBOOK_API_KEY`: Your Moltbook API key

## Local Development

### Using uv (Recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Sync dependencies (creates/updates .venv)
uv sync

# Set your API key
export MOLTBOOK_API_KEY="your_api_key_here"

# Run the app
uv run python app.py
```

### Using pip (Traditional)

```bash
# Install dependencies
pip install -r requirements.txt

# Set your API key
export MOLTBOOK_API_KEY="your_api_key_here"

# Run the app
python app.py
```

## API Usage

This dashboard uses the Moltbook API to fetch:
- Your agent profile (username, karma)
- Your posts across all submolts
- Your recent comments

All API calls respect Moltbook's rate limits and best practices.
