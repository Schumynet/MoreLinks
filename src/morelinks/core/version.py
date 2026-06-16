"""
MoreLinks Version Configuration
Defines Demo vs Pro/Enterprise editions
"""

__version__ = "1.0.0"
VERSION = __version__

# Edition types
class Edition:
    DEMO = "demo"
    PRO = "pro"
    ENTERPRISE = "enterprise"

# Current edition - can be overridden
EDITION = Edition.DEMO

def is_demo() -> bool:
    return EDITION == Edition.DEMO

def is_pro() -> bool:
    return EDITION in (Edition.PRO, Edition.ENTERPRISE)

def is_enterprise() -> bool:
    return EDITION == Edition.ENTERPRISE

# Feature flags by edition
FEATURES = {
    Edition.DEMO: {
        "max_links": 10,
        "max_clicks": 1000,
        "max_campaigns": 1,
        "custom_domain": False,
        "api_access": False,
        "bulk_operations": False,
        "qr_code": True,
        "analytics": True,
        "export": "csv",
        "team_members": 1,
        "support": "community",
        "branded_qr": False,
        "utm_builder": True,
        "password_protection": False,
        "expiration": False,
        "geo_targeting": False,
        "automations": False,
        "bulldozer": False,
        "templates": 3,
    },
    Edition.PRO: {
        "max_links": 1000,
        "max_clicks": 100000,
        "max_campaigns": 50,
        "custom_domain": True,
        "api_access": True,
        "bulk_operations": True,
        "qr_code": True,
        "analytics": True,
        "export": "csv,json,pdf",
        "team_members": 5,
        "support": "email",
        "branded_qr": True,
        "utm_builder": True,
        "password_protection": True,
        "expiration": True,
        "geo_targeting": False,
        "automations": True,
        "bulldozer": True,
        "templates": 50,
    },
    Edition.ENTERPRISE: {
        "max_links": -1,  # Unlimited
        "max_clicks": -1,
        "max_campaigns": -1,
        "custom_domain": True,
        "api_access": True,
        "bulk_operations": True,
        "qr_code": True,
        "analytics": True,
        "export": "csv,json,pdf,excel",
        "team_members": -1,
        "support": "dedicated",
        "branded_qr": True,
        "utm_builder": True,
        "password_protection": True,
        "expiration": True,
        "geo_targeting": True,
        "automations": True,
        "bulldozer": True,
        "templates": -1,
    }
}

def get_features(edition: str = None) -> dict:
    """Get feature flags for specified edition"""
    if edition is None:
        edition = EDITION
    return FEATURES.get(edition, FEATURES[Edition.DEMO])

def check_feature(feature: str, edition: str = None) -> bool:
    """Check if a feature is enabled for the edition"""
    features = get_features(edition)
    return features.get(feature, False)

def get_limit(limit_name: str, edition: str = None) -> int:
    """Get a numeric limit for the edition"""
    features = get_features(edition)
    return features.get(limit_name, 0)

# Edition metadata
EDITION_INFO = {
    Edition.DEMO: {
        "name": "MoreLinks Demo",
        "description": "Prova gratuita - Perfetta per testare le funzionalità",
        "color": "#6B7280",  # Gray
        "badge": "FREE",
        "price": 0,
        "trial_days": None,
    },
    Edition.PRO: {
        "name": "MoreLinks Pro",
        "description": "Per professionisti e piccole team",
        "color": "#3B82F6",  # Blue
        "badge": "PRO",
        "price": 29,
        "trial_days": 14,
    },
    Edition.ENTERPRISE: {
        "name": "MoreLinks Enterprise",
        "description": "Per aziende con esigenze avanzate",
        "color": "#8B5CF6",  # Purple
        "badge": "ENTERPRISE",
        "price": 99,
        "trial_days": 30,
    }
}

def get_edition_info(edition: str = None) -> dict:
    """Get edition metadata"""
    if edition is None:
        edition = EDITION
    return EDITION_INFO.get(edition, EDITION_INFO[Edition.DEMO])
