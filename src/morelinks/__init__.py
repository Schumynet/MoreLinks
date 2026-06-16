"""
MoreLinks - Complete Management Platform with AI Assistant
Pienissimo + Linktree + Chatbot with Persistent Memory
Business Admin + Lead Gen + DM Automation
"""

__version__ = "1.0.0"
__author__ = "Fabio (Schumynet)"

# Core
from .core.morelinks import MoreLinks, create_morelinks
from .database import Database

# Chatbot with Persistent Memory
from .chatbot.chatbot import MoreLinksChatbot, ActionResult, ChatIntent
from .chatbot.memory import PersistentMemory, AdministrativeMemory
from .chatbot.normative_knowledge import NormativeKnowledge, RegulationExpert

# Models
from .models import (
    Link, LinkCreate, LinkUpdate,
    Analytics, AnalyticsCreate, AnalyticsSummary,
    Campaign, CampaignCreate,
    Template, TemplateCreate,
    User, UserCreate, UserInDB,
    DeviceType, CampaignStatus
)

__all__ = [
    # Core
    "MoreLinks",
    "create_morelinks",
    "Database",
    
    # Chatbot
    "MoreLinksChatbot",
    "ActionResult",
    "ChatIntent",
    "PersistentMemory",
    "AdministrativeMemory",
    "NormativeKnowledge",
    "RegulationExpert",
    
    # Models
    "Link",
    "LinkCreate", 
    "LinkUpdate",
    "Analytics",
    "AnalyticsCreate",
    "AnalyticsSummary",
    "Campaign",
    "CampaignCreate",
    "Template",
    "TemplateCreate",
    "User",
    "UserCreate",
    "UserInDB",
    "DeviceType",
    "CampaignStatus",
    
    # Version
    "__version__",
]
