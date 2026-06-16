"""
MoreLinks Core Module
"""

from .morelinks import MoreLinks, get_morelinks
from .version import __version__, VERSION, EDITION, is_demo, is_pro

__all__ = ["MoreLinks", "get_morelinks", "__version__", "VERSION", "EDITION", "is_demo", "is_pro"]
