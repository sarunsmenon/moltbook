"""
Configuration settings for Moltbook workflow.

This module manages all configuration settings including API keys,
file paths, and workflow parameters.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables from .env file at repo root
repo_root = Path(__file__).parent.parent
dotenv_path = repo_root / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)


def _load_yaml_config() -> Dict[str, Any]:
    """Load configuration from YAML file."""
    config_file = Path(__file__).parent / "config.yaml"
    if config_file.exists():
        with open(config_file, 'r') as f:
            return yaml.safe_load(f) or {}
    return {}


def _get_config_value(config: Dict[str, Any], *keys, default=None):
    """
    Get a configuration value from nested dict.
    
    Args:
        config: Configuration dictionary
        *keys: Nested keys to traverse
        default: Default value if key not found
    
    Returns:
        Configuration value or default
    """
    value = config
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
            if value is None:
                return default
        else:
            return default
    return value


# Load YAML configuration once at module level
_CONFIG = _load_yaml_config()


class Settings:
    """Central configuration for Moltbook workflow."""
    
    # Base directories
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    LOGS_DIR = BASE_DIR / "logs"
    CONFIG_DIR = BASE_DIR / "config"
    
    # Data subdirectories
    ARCHIVES_DIR = DATA_DIR / "archives"
    STATE_DIR = DATA_DIR / "state"
    
    # State Files
    PROCESSED_COMMENTS_FILE = STATE_DIR / "processed_comments.json"
    GANDALF_STATE_FILE = STATE_DIR / "gandalf_state.json"
    
    # API Configuration (from YAML)
    MOLTBOOK_BASE_URL = _get_config_value(_CONFIG, 'api', 'moltbook_base_url', 
                                           default="https://www.moltbook.com/api/v1")
    MOLTBOOK_WEB_BASE = _get_config_value(_CONFIG, 'api', 'moltbook_web_base', 
                                           default="https://www.moltbook.com")
    OPENROUTER_BASE_URL = _get_config_value(_CONFIG, 'api', 'openrouter_base_url', 
                                             default="https://openrouter.ai/api/v1")
    REQUEST_TIMEOUT = _get_config_value(_CONFIG, 'api', 'request_timeout', default=30)
    
    # API Keys (from environment variables - NOT in YAML for security)
    MOLTBOOK_API_KEY = os.getenv("MOLTBOOK_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # LLM Models (from YAML)
    OPENAI_MODEL = _get_config_value(_CONFIG, 'llm', 'openai', 'model', 
                                     default="gpt-5.3-chat")
    ANTHROPIC_MODEL = _get_config_value(_CONFIG, 'llm', 'anthropic', 'model', 
                                        default="claude-3-5-sonnet-20241022")
    OPENROUTER_GANDALF_MODEL = _get_config_value(_CONFIG, 'llm', 'openrouter', 'gandalf_model', 
                                                  default="anthropic/claude-3.5-sonnet")
    OPENROUTER_RESPONSE_MODEL_OPENAI = _get_config_value(_CONFIG, 'llm', 'openrouter', 'response_model_openai', 
                                                          default="openai/gpt-4-turbo")
    OPENROUTER_RESPONSE_MODEL_ANTHROPIC = _get_config_value(_CONFIG, 'llm', 'openrouter', 'response_model_anthropic', 
                                                             default="anthropic/claude-3.5-sonnet")
    
    # Response Generation Settings (from YAML)
    RESPONSE_MAX_TOKENS = _get_config_value(_CONFIG, 'response_generation', 'max_tokens', default=200)
    RESPONSE_TEMPERATURE = _get_config_value(_CONFIG, 'response_generation', 'temperature', default=0.8)
    RESPONSE_SYSTEM_PROMPT = _get_config_value(_CONFIG, 'response_generation', 'system_prompt', 
                                                default="You are a witty AI agent on Moltbook. Respond naturally and engagingly to comments.")
    
    # Gandalf Settings (from YAML)
    GANDALF_MAX_TOKENS = _get_config_value(_CONFIG, 'gandalf', 'max_tokens', default=300)
    GANDALF_TEMPERATURE = _get_config_value(_CONFIG, 'gandalf', 'temperature', default=0.9)
    GANDALF_SUBMOLT = _get_config_value(_CONFIG, 'gandalf', 'submolt', default="lotr")
    GANDALF_THEMES = _get_config_value(_CONFIG, 'gandalf', 'themes', default=[
        "about courage and bravery",
        "about wisdom and knowledge",
        "about hope in dark times"
    ])
    GANDALF_SOURCES = _get_config_value(_CONFIG, 'gandalf', 'sources', default=[
        "The Hobbit",
        "The Fellowship of the Ring",
        "The Two Towers",
        "The Return of the King"
    ])
    
    # Rate Limiting (from YAML)
    COMMENT_COOLDOWN_SECONDS = _get_config_value(_CONFIG, 'rate_limiting', 'comment_cooldown_seconds', default=20)
    DAILY_COMMENT_LIMIT = _get_config_value(_CONFIG, 'rate_limiting', 'daily_comment_limit', default=50)
    
    # Workflow Settings (from YAML)
    MAX_POSTS_TO_CHECK = _get_config_value(_CONFIG, 'workflow', 'max_posts_to_check', default=50)
    MAX_COMMENTS_PER_POST = _get_config_value(_CONFIG, 'workflow', 'max_comments_per_post', default=100)
    MAX_PAGES_TO_SEARCH = _get_config_value(_CONFIG, 'workflow', 'max_pages_to_search', default=10)
    POSTS_PER_PAGE = _get_config_value(_CONFIG, 'workflow', 'posts_per_page', default=25)
    
    # Logging (from YAML)
    LOG_LEVEL = _get_config_value(_CONFIG, 'logging', 'level', default="INFO")
    LOG_FORMAT = _get_config_value(_CONFIG, 'logging', 'format', 
                                    default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    LOG_FILE = LOGS_DIR / "daily_workflow.log"
    
    # Gradio Settings (from YAML)
    GRADIO_THEME = _get_config_value(_CONFIG, 'gradio', 'theme', default="soft")
    GRADIO_DEFAULT_LLM_PROVIDER = _get_config_value(_CONFIG, 'gradio', 'default_llm_provider', default="openai")
    GRADIO_REQUEST_TIMEOUT = _get_config_value(_CONFIG, 'gradio', 'request_timeout', default=20)
    GRADIO_MAX_POSTS_DISPLAY = _get_config_value(_CONFIG, 'gradio', 'max_posts_display', default=10)
    GRADIO_MAX_COMMENTS_DISPLAY = _get_config_value(_CONFIG, 'gradio', 'max_comments_display', default=10)
    GRADIO_POSTS_SCROLL_HEIGHT = _get_config_value(_CONFIG, 'gradio', 'posts_scroll_height', default=600)
    GRADIO_COMMENTS_SCROLL_HEIGHT = _get_config_value(_CONFIG, 'gradio', 'comments_scroll_height', default=600)
    GRADIO_COMMENT_CONTENT_TRUNCATE = _get_config_value(_CONFIG, 'gradio', 'comment_content_truncate', default=150)
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that all required settings are present.
        
        Returns:
            bool: True if all required settings are valid
        
        Raises:
            ValueError: If required settings are missing
        """
        if not cls.MOLTBOOK_API_KEY:
            raise ValueError("MOLTBOOK_API_KEY environment variable is required")
        
        if not cls.OPENAI_API_KEY and not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "At least one LLM API key is required: "
                "OPENAI_API_KEY or ANTHROPIC_API_KEY"
            )
        
        return True
    
    @classmethod
    def create_directories(cls):
        """Create all necessary directories if they don't exist."""
        for directory in [cls.DATA_DIR, cls.LOGS_DIR, cls.ARCHIVES_DIR, cls.STATE_DIR]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_headers(cls) -> dict:
        """
        Get HTTP headers for Moltbook API requests.
        
        Returns:
            dict: Headers including authorization
        """
        return {
            "Authorization": f"Bearer {cls.MOLTBOOK_API_KEY}",
            "Content-Type": "application/json"
        }
