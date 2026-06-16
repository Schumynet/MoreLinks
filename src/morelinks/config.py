"""
MoreLinks Configuration
Update with your API keys
"""

# OpenRouter API Key (get from environment or .env file)
import os
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Default AI Model (FREE) - Nemotron Content Safety
DEFAULT_MODEL = "nvidia/nemotron-3-5-content-safety:free"

# Alternative free models
FREE_MODELS = {
    "nex-n2-pro": "nex-agi/nex-n2-pro:free",
    "nemotron": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "safety": "nvidia/nemotron-3-5-content-safety:free"
}

# GitHub Configuration
GITHUB_TOKEN = ""  # Set your GitHub token for memory sync
GITHUB_REPO = "Schumynet/morelinks-memory"

# MoreLinks Configuration
MORELINKS_CONFIG = {
    "app_name": "MoreLinks",
    "version": "1.0.0",
    "max_links_demo": 10,
    "max_clicks_demo": 1000,
}

# Database paths
DB_PATHS = {
    "main": "morelinks.db",
    "memory": "omni_memory.db",
    "brain": "omni_brain.db"
}
