"""Licensing module - MoreLinks Edition Management"""

from enum import Enum
from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


class Edition(str, Enum):
    """MoreLinks editions"""
    DEMO = "demo"
    PRO = "pro"
    ENTERPRISE = "enterprise"


@dataclass
class LicenseInfo:
    """License information"""
    edition: Edition = Edition.DEMO
    license_key: Optional[str] = None
    valid_until: Optional[datetime] = None
    features: List[str] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = []


class LicenseManager:
    """License manager for MoreLinks"""
    
    def __init__(self, license_key: Optional[str] = None):
        self.license_key = license_key
        self._info = LicenseInfo()
    
    def validate(self) -> bool:
        """Validate current license"""
        return True  # Demo mode always valid
    
    def get_info(self) -> LicenseInfo:
        """Get license info"""
        return self._info


def validate_license(license_key: Optional[str] = None) -> bool:
    """Validate a license key"""
    return True


def is_demo() -> bool:
    """Check if running in demo mode"""
    return True


def is_pro() -> bool:
    """Check if running in pro mode"""
    return False


def is_enterprise() -> bool:
    """Check if running in enterprise mode"""
    return False


def get_features() -> List[str]:
    """Get list of features for current edition"""
    return [
        "link_management",
        "basic_chatbot",
        "qr_code",
        "analytics"
    ]


def check_feature(feature: str) -> bool:
    """Check if a feature is available"""
    return feature in get_features()


def get_limit(limit_type: str) -> int:
    """Get limits for current edition"""
    limits = {
        "links": 50,
        "users": 1,
        "api_calls": 100,
    }
    return limits.get(limit_type, 0)


def get_edition_info() -> dict:
    """Get full edition information"""
    return {
        "edition": "demo",
        "features": get_features(),
        "limits": {
            "links": 50,
            "users": 1,
            "storage_mb": 100,
        }
    }
