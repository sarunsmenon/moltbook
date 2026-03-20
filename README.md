---
title: Moltbook Agent Dashboard
emoji: 🦞
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 6.9.0
app_file: app.py
pinned: false
license: mit
---

# Moltbook 🦞

An AI agent for the [Moltbook](https://www.moltbook.com) social network - built with Python and managed with `uv`.

## 🚀 Quick Start

### Prerequisites

- Python 3.13 or higher
- `uv` package manager (recommended) or `pip`

### Installation with uv (Recommended)

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone <your-repo-url>
cd moltbook

# Sync dependencies (creates .venv automatically)
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

### Installation with pip (Traditional)

```bash
# Clone the repository
git clone <your-repo-url>
cd moltbook

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies from pyproject.toml
pip install -e .

# Set up environment variables
cp .env.example .env
# Edit .env with your credentials
```

## 📋 Environment Variables

Create a `.env` file with the following variables:

```bash
MOLTBOOK_API_KEY=your_moltbook_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here  # Optional, for AI responses
```

## 🎯 Usage

### Run Gradio Dashboard (HuggingFace Spaces App)

```bash
# With uv
uv run python app.py

# With pip
python app.py
```

Then open http://localhost:7860 in your browser.

### Run Daily Workflow

```bash
# With uv
uv run python run_daily_workflow.py

# With pip
python run_daily_workflow.py
```

### Run Main Script

```bash
# With uv
uv run python main.py

# With pip
python main.py
```

## 🏗️ Project Structure

```
moltbook/
├── src/                      # Core application modules
│   ├── moltbook_client.py    # API client for Moltbook
│   ├── gandalf_poster.py     # Daily posting logic
│   ├── response_generator.py # AI response generation
│   ├── workflow_tasks.py     # Automated workflow tasks
│   └── data_archiver.py      # Data archival utilities
├── utils/                    # Utility modules
│   ├── gradio_utils.py       # Gradio UI helpers
│   ├── rate_limiter.py       # Rate limiting utilities
│   └── state_manager.py      # State management
├── config/                   # Configuration
│   └── settings.py           # App settings
├── data/                     # Data storage
│   ├── state/                # Application state
│   └── archives/             # Archived interactions
├── docs/                     # Documentation
├── app.py                    # Gradio web dashboard
├── main.py                   # Main entry point
├── run_daily_workflow.py     # Daily automation script
├── pyproject.toml            # Project metadata & dependencies
├── uv.lock                   # Lock file for reproducible installs
└── .python-version           # Python version for uv
```

## 🔧 Development

### Using uv

```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Run tests
uv run pytest

# Format code
uv run black .

# Lint code
uv run ruff check .
```

### Using pip

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Lint code
ruff check .
```

## 🚢 Deployment

### HuggingFace Spaces

This project is configured for deployment on HuggingFace Spaces:

1. Create a new Space on [HuggingFace](https://huggingface.co/spaces)
2. Set the Space SDK to "Gradio"
3. Add environment variables as Secrets:
   - `MOLTBOOK_API_KEY`
   - `OPENROUTER_API_KEY` (optional)
4. Push your code to the Space repository

HuggingFace Spaces will automatically detect and install dependencies from `pyproject.toml`.

See [README_HF_SPACE.md](README_HF_SPACE.md) for more details.

## 📦 Package Management with uv

This project uses `uv` for fast, reliable Python package management:

- **Fast**: 10-100x faster than pip
- **Reliable**: Deterministic dependency resolution with `uv.lock`
- **Compatible**: Works alongside pip and existing tools
- **Modern**: Based on Rust, following PEP 621

### Why uv?

- ⚡ **Speed**: Instant dependency resolution and installation
- 🔒 **Reproducibility**: Lock file ensures consistent environments
- 🎯 **Simplicity**: One tool for package management and virtual environments
- 🔄 **Compatibility**: Drop-in replacement for pip/pip-tools

### uv Commands Cheat Sheet

```bash
uv sync              # Install dependencies from lock file
uv add requests      # Add a dependency
uv remove requests   # Remove a dependency
uv lock              # Update lock file
uv run python app.py # Run a command in the virtual environment
uv pip list          # List installed packages
```

## 📚 Documentation

- [Moltbook Guide](docs/MOLTBOOK_GUIDE.md)
- [Automated Workflow](docs/AUTOMATED_COMMENT_RESPONSE_WORKFLOW.md)
- [HuggingFace Spaces Setup](README_HF_SPACE.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Moltbook](https://www.moltbook.com) - The social network for AI agents
- [uv Documentation](https://docs.astral.sh/uv/) - Learn more about uv
- [Gradio Documentation](https://gradio.app/docs/) - Build ML web interfaces

## ⚡ About uv

This project is powered by [uv](https://github.com/astral-sh/uv), an extremely fast Python package installer and resolver written in Rust. It's designed as a drop-in replacement for pip and pip-tools, offering:

- 10-100x faster installation
- Compatible with the Python ecosystem
- Supports Python 3.8+
- Cross-platform (Linux, macOS, Windows)

To learn more, visit: https://docs.astral.sh/uv/
