"""
MoreLinks Data Models
"""

from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID, uuid4


class LinkStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    EXPIRED = "expired"
    ARCHIVED = "archived"


class UserPlan(str, Enum):
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class DeviceType(str, Enum):
    DESKTOP = "desktop"
    MOBILE = "mobile"
    TABLET = "tablet"
    OTHER = "other"


# === User Models ===
class UserBase(BaseModel):
    email: str
    plan: UserPlan = UserPlan.FREE


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID = Field(default_factory=uuid4)
    api_key: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UserInDB(User):
    password_hash: str


# === Link Models ===
class LinkBase(BaseModel):
    original_url: HttpUrl
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class LinkCreate(LinkBase):
    short_code: Optional[str] = None
    branded_domain: Optional[str] = None
    expires_at: Optional[datetime] = None
    password: Optional[str] = None


class LinkUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None
    expires_at: Optional[datetime] = None
    password: Optional[str] = None


class Link(LinkBase):
    id: UUID = Field(default_factory=uuid4)
    short_code: str
    branded_domain: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None
    is_active: bool = True
    click_count: int = 0
    user_id: Optional[UUID] = None

    @property
    def short_url(self) -> str:
        domain = self.branded_domain or "morelinks.app"
        return f"https://{domain}/{self.short_code}"


class LinkWithAnalytics(Link):
    analytics: List["Analytics"] = Field(default_factory=list)


# === Analytics Models ===
class AnalyticsBase(BaseModel):
    link_id: UUID
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    referrer: Optional[str] = None
    country: Optional[str] = None
    device: DeviceType = DeviceType.OTHER
    browser: Optional[str] = None
    os: Optional[str] = None


class AnalyticsCreate(AnalyticsBase):
    pass


class Analytics(AnalyticsBase):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class AnalyticsSummary(BaseModel):
    total_clicks: int
    unique_visitors: int
    top_countries: dict
    top_devices: dict
    top_referrers: dict
    clicks_by_day: dict


# === Template Models ===
class TemplateBase(BaseModel):
    name: str
    slug: str
    content: dict


class TemplateCreate(TemplateBase):
    pass


class Template(TemplateBase):
    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# === Campaign Models ===
class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class CampaignBase(BaseModel):
    name: str
    description: Optional[str] = None
    link_ids: List[UUID] = Field(default_factory=list)


class CampaignCreate(CampaignBase):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class Campaign(CampaignBase):
    id: UUID = Field(default_factory=uuid4)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: CampaignStatus = CampaignStatus.DRAFT
    created_at: datetime = Field(default_factory=datetime.utcnow)


# === QR Code Models ===
class QRCodeConfig(BaseModel):
    size: int = Field(default=300, ge=100, le=1000)
    foreground_color: str = "#000000"
    background_color: str = "#FFFFFF"
    logo: Optional[str] = None
    error_correction: str = "H"  # L, M, Q, H


class QRCodeResponse(BaseModel):
    link_id: UUID
    qr_code_base64: str
    download_url: str
