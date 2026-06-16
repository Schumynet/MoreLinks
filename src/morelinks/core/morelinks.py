"""
MoreLinks Core Engine
Main class that orchestrates all functionality
"""

import os
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID, uuid4
import json
import hashlib
import secrets
import random
import string

from ..models import (
    Link, LinkCreate, LinkUpdate, LinkWithAnalytics,
    Analytics, AnalyticsCreate, AnalyticsSummary,
    Campaign, CampaignCreate,
    Template, TemplateCreate,
    User, UserCreate, UserInDB,
    DeviceType, CampaignStatus
)
from .version import (
    EDITION, Edition, is_demo, is_pro, is_enterprise,
    get_features, check_feature, get_limit, get_edition_info
)
from ..licensing import LicenseManager, validate_license, LicenseInfo


class MoreLinks:
    """
    Main MoreLinks Engine
    
    Args:
        db_path: Path to SQLite database file
        edition: Edition type (demo, pro, enterprise)
        license_key: License key for Pro/Enterprise
    """
    
    _instance = None
    
    def __init__(
        self,
        db_path: str = "morelinks.db",
        edition: str = None,
        license_key: str = None,
        demo_mode: bool = True
    ):
        self.db_path = db_path
        self.license: Optional[LicenseInfo] = None
        
        # Determine edition
        if edition:
            self.edition = edition
        elif demo_mode:
            self.edition = Edition.DEMO
        else:
            self.edition = Edition.DEMO
        
        # Validate license if pro/enterprise
        if license_key:
            self.license = validate_license(license_key)
            if self.license and self.license.is_valid:
                self.edition = self.license.edition
        
        # Override global edition
        global EDITION
        EDITION = self.edition
        
        self._init_database()
        self._create_demo_data_if_needed()
        
        # Singleton pattern
        MoreLinks._instance = self
    
    def _init_database(self):
        """Initialize database connection and tables"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
    
    def _create_tables(self):
        """Create all database tables"""
        cursor = self.conn.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                api_key TEXT UNIQUE NOT NULL,
                plan TEXT DEFAULT 'free',
                created_at TEXT NOT NULL,
                edition TEXT DEFAULT 'demo'
            )
        """)
        
        # Links table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS links (
                id TEXT PRIMARY KEY,
                original_url TEXT NOT NULL,
                short_code TEXT UNIQUE NOT NULL,
                branded_domain TEXT,
                title TEXT,
                description TEXT,
                tags TEXT DEFAULT '[]',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                expires_at TEXT,
                is_active INTEGER DEFAULT 1,
                click_count INTEGER DEFAULT 0,
                password TEXT,
                user_id TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Analytics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id TEXT PRIMARY KEY,
                link_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                ip_address TEXT,
                user_agent TEXT,
                referrer TEXT,
                country TEXT,
                device TEXT,
                browser TEXT,
                os TEXT,
                FOREIGN KEY (link_id) REFERENCES links(id)
            )
        """)
        
        # Templates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS templates (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT UNIQUE NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        
        # Campaigns table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS campaigns (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                link_ids TEXT DEFAULT '[]',
                start_date TEXT,
                end_date TEXT,
                status TEXT DEFAULT 'draft',
                created_at TEXT NOT NULL
            )
        """)
        
        # License table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS license (
                id INTEGER PRIMARY KEY,
                license_key TEXT,
                edition TEXT,
                activated_at TEXT,
                expires_at TEXT,
                user_email TEXT
            )
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_links_short_code ON links(short_code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_links_user_id ON links(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_link_id ON analytics(link_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON analytics(timestamp)")
        
        self.conn.commit()
    
    def _create_demo_data_if_needed(self):
        """Create demo user and sample data"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            # Create demo user
            demo_user = UserCreate(
                email="demo@morelinks.app",
                password="demo123",
                plan="free"
            )
            self.create_user(demo_user)
            
            # Create sample links
            sample_links = [
                ("https://github.com", "GitHub", "Social", "La piattaforma per condividere codice"),
                ("https://python.org", "Python", "Tech", "Linguaggio di programmazione"),
                ("https://fastapi.tiangolo.com", "FastAPI", "Tech", "Framework Python moderno"),
            ]
            
            for url, title, tag, desc in sample_links:
                self.create_link(
                    LinkCreate(
                        original_url=url,
                        title=title,
                        tags=[tag],
                        description=desc
                    ),
                    user_email="demo@morelinks.app"
                )
    
    # ==================== INFO ====================
    def info(self) -> Dict[str, Any]:
        """Get system information"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM links")
        total_links = cursor.fetchone()["count"]
        
        cursor.execute("SELECT SUM(click_count) as total FROM links")
        total_clicks = cursor.fetchone()["total"] or 0
        
        features = get_features()
        edition_info = get_edition_info()
        
        return {
            "name": "MoreLinks",
            "version": "1.0.0",
            "edition": self.edition,
            "edition_name": edition_info["name"],
            "edition_color": edition_info["color"],
            "is_demo": is_demo(),
            "is_pro": is_pro(),
            "is_enterprise": is_enterprise(),
            "features": features,
            "stats": {
                "total_links": total_links,
                "total_clicks": total_clicks,
            },
            "limits": {
                "max_links": get_limit("max_links"),
                "max_clicks": get_limit("max_clicks"),
            }
        }
    
    # ==================== USER ====================
    def create_user(self, user_data: UserCreate) -> UserInDB:
        """Create a new user"""
        user_id = str(uuid4())
        password_hash = hashlib.sha256(user_data.password.encode()).hexdigest()
        api_key = secrets.token_urlsafe(32)
        created_at = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, email, password_hash, api_key, plan, created_at, edition)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, user_data.email, password_hash, api_key, 
              user_data.plan.value, created_at, self.edition))
        self.conn.commit()
        
        return UserInDB(
            id=UUID(user_id),
            email=user_data.email,
            api_key=api_key,
            plan=user_data.plan,
            created_at=datetime.fromisoformat(created_at)
        )
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authenticate user and return user info"""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password_hash = ?", 
                      (email, password_hash))
        row = cursor.fetchone()
        
        if row:
            return User(
                id=UUID(row["id"]),
                email=row["email"],
                api_key=row["api_key"],
                plan=row["plan"],
                created_at=datetime.fromisoformat(row["created_at"])
            )
        return None
    
    # ==================== LINKS ====================
    def create_link(self, link_data: LinkCreate, user_email: str = None) -> Link:
        """Create a new shortened link"""
        # Check limits
        if is_demo():
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links WHERE user_id = (SELECT id FROM users WHERE email = ?)", 
                          (user_email,))
            count = cursor.fetchone()[0]
            if count >= get_limit("max_links"):
                raise ValueError(f"Demo limit reached: max {get_limit('max_links')} links")
        
        link_id = str(uuid4())
        short_code = link_data.short_code or self._generate_short_code()
        created_at = datetime.utcnow().isoformat()
        tags = json.dumps(link_data.tags or [])
        
        # Get user_id
        user_id = None
        if user_email:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
            row = cursor.fetchone()
            if row:
                user_id = row["id"]
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO links (id, original_url, short_code, branded_domain, title, 
                             description, tags, created_at, updated_at, expires_at, 
                             is_active, click_count, password, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            link_id, str(link_data.original_url), short_code, link_data.branded_domain,
            link_data.title, link_data.description, tags, created_at, created_at,
            link_data.expires_at.isoformat() if link_data.expires_at else None,
            1, 0, link_data.password, user_id
        ))
        self.conn.commit()
        
        return Link(
            id=UUID(link_id),
            original_url=link_data.original_url,
            short_code=short_code,
            branded_domain=link_data.branded_domain,
            title=link_data.title,
            description=link_data.description,
            tags=link_data.tags or [],
            created_at=datetime.fromisoformat(created_at),
            updated_at=datetime.fromisoformat(created_at),
            expires_at=link_data.expires_at,
            is_active=True,
            click_count=0,
            user_id=UUID(user_id) if user_id else None
        )
    
    def _generate_short_code(self, length: int = 6) -> str:
        """Generate a unique short code"""
        while True:
            code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links WHERE short_code = ?", (code,))
            if cursor.fetchone()[0] == 0:
                return code
    
    def get_link(self, link_id: UUID) -> Optional[Link]:
        """Get link by ID"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM links WHERE id = ?", (str(link_id),))
        row = cursor.fetchone()
        if row:
            return self._row_to_link(row)
        return None
    
    def get_link_by_short_code(self, short_code: str) -> Optional[Link]:
        """Get link by short code"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM links WHERE short_code = ?", (short_code,))
        row = cursor.fetchone()
        if row:
            return self._row_to_link(row)
        return None
    
    def list_links(self, user_email: str = None, tags: List[str] = None,
                   limit: int = 100, offset: int = 0) -> List[Link]:
        """List all links with optional filtering"""
        cursor = self.conn.cursor()
        
        if user_email:
            cursor.execute("SELECT id FROM users WHERE email = ?", (user_email,))
            row = cursor.fetchone()
            user_id = row["id"] if row else None
        else:
            user_id = None
        
        if user_id:
            cursor.execute("""
                SELECT * FROM links WHERE user_id = ? 
                ORDER BY created_at DESC LIMIT ? OFFSET ?
            """, (user_id, limit, offset))
        else:
            cursor.execute("""
                SELECT * FROM links ORDER BY created_at DESC LIMIT ? OFFSET ?
            """, (limit, offset))
        
        rows = cursor.fetchall()
        links = [self._row_to_link(row) for row in rows]
        
        if tags:
            links = [l for l in links if any(t in l.tags for t in tags)]
        
        return links
    
    def update_link(self, link_id: UUID, update_data: LinkUpdate) -> Optional[Link]:
        """Update a link"""
        cursor = self.conn.cursor()
        updates = []
        params = []
        
        if update_data.title is not None:
            updates.append("title = ?")
            params.append(update_data.title)
        if update_data.description is not None:
            updates.append("description = ?")
            params.append(update_data.description)
        if update_data.tags is not None:
            updates.append("tags = ?")
            params.append(json.dumps(update_data.tags))
        if update_data.is_active is not None:
            updates.append("is_active = ?")
            params.append(1 if update_data.is_active else 0)
        if update_data.expires_at is not None:
            updates.append("expires_at = ?")
            params.append(update_data.expires_at.isoformat())
        if update_data.password is not None:
            updates.append("password = ?")
            params.append(update_data.password)
        
        if updates:
            updates.append("updated_at = ?")
            params.append(datetime.utcnow().isoformat())
            params.append(str(link_id))
            
            query = f"UPDATE links SET {', '.join(updates)} WHERE id = ?"
            cursor.execute(query, params)
            self.conn.commit()
        
        return self.get_link(link_id)
    
    def delete_link(self, link_id: UUID) -> bool:
        """Delete a link"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM analytics WHERE link_id = ?", (str(link_id),))
        cursor.execute("DELETE FROM links WHERE id = ?", (str(link_id),))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def _row_to_link(self, row: sqlite3.Row) -> Link:
        return Link(
            id=UUID(row["id"]),
            original_url=row["original_url"],
            short_code=row["short_code"],
            branded_domain=row["branded_domain"],
            title=row["title"],
            description=row["description"],
            tags=json.loads(row["tags"]) if row["tags"] else [],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            expires_at=datetime.fromisoformat(row["expires_at"]) if row["expires_at"] else None,
            is_active=bool(row["is_active"]),
            click_count=row["click_count"],
            user_id=UUID(row["user_id"]) if row["user_id"] else None
        )
    
    # ==================== ANALYTICS ====================
    def track_click(self, link_id: UUID, analytics_data: AnalyticsCreate) -> Analytics:
        """Track a click on a link"""
        analytics_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO analytics (id, link_id, timestamp, ip_address, user_agent, 
                                 referrer, country, device, browser, os)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            analytics_id, str(link_id), timestamp,
            analytics_data.ip_address, analytics_data.user_agent,
            analytics_data.referrer, analytics_data.country,
            analytics_data.device.value if analytics_data.device else DeviceType.OTHER.value,
            analytics_data.browser, analytics_data.os
        ))
        
        cursor.execute("UPDATE links SET click_count = click_count + 1 WHERE id = ?", (str(link_id),))
        self.conn.commit()
        
        return Analytics(
            id=UUID(analytics_id),
            link_id=link_id,
            timestamp=datetime.fromisoformat(timestamp),
            ip_address=analytics_data.ip_address,
            user_agent=analytics_data.user_agent,
            referrer=analytics_data.referrer,
            country=analytics_data.country,
            device=analytics_data.device or DeviceType.OTHER,
            browser=analytics_data.browser,
            os=analytics_data.os
        )
    
    def get_analytics(self, link_id: UUID, days: int = 30) -> List[Analytics]:
        """Get analytics for a link"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM analytics 
            WHERE link_id = ? AND timestamp > datetime('now', ?)
            ORDER BY timestamp DESC
        """, (str(link_id), f"-{days} days"))
        rows = cursor.fetchall()
        
        analytics = []
        for row in rows:
            analytics.append(Analytics(
                id=UUID(row["id"]),
                link_id=UUID(row["link_id"]),
                timestamp=datetime.fromisoformat(row["timestamp"]),
                ip_address=row["ip_address"],
                user_agent=row["user_agent"],
                referrer=row["referrer"],
                country=row["country"],
                device=DeviceType(row["device"]) if row["device"] else DeviceType.OTHER,
                browser=row["browser"],
                os=row["os"]
            ))
        return analytics
    
    def get_analytics_summary(self, link_id: UUID = None, days: int = 30) -> AnalyticsSummary:
        """Get analytics summary"""
        cursor = self.conn.cursor()
        
        where_clause = f"WHERE timestamp > datetime('now', '-{days} days')"
        if link_id:
            where_clause += f" AND link_id = '{link_id}'"
        
        cursor.execute(f"SELECT COUNT(*) as count FROM analytics {where_clause}")
        total_clicks = cursor.fetchone()["count"]
        
        cursor.execute(f"SELECT COUNT(DISTINCT ip_address) as count FROM analytics {where_clause}")
        unique_visitors = cursor.fetchone()["count"]
        
        cursor.execute(f"""
            SELECT country, COUNT(*) as count FROM analytics 
            {where_clause} AND country IS NOT NULL
            GROUP BY country ORDER BY count DESC LIMIT 5
        """)
        top_countries = {row["country"]: row["count"] for row in cursor.fetchall()}
        
        cursor.execute(f"""
            SELECT device, COUNT(*) as count FROM analytics 
            {where_clause}
            GROUP BY device ORDER BY count DESC
        """)
        top_devices = {row["device"]: row["count"] for row in cursor.fetchall()}
        
        cursor.execute(f"""
            SELECT referrer, COUNT(*) as count FROM analytics 
            {where_clause} AND referrer IS NOT NULL
            GROUP BY referrer ORDER BY count DESC LIMIT 5
        """)
        top_referrers = {row["referrer"]: row["count"] for row in cursor.fetchall()}
        
        cursor.execute(f"""
            SELECT date(timestamp) as day, COUNT(*) as count FROM analytics 
            {where_clause}
            GROUP BY day ORDER BY day
        """)
        clicks_by_day = {row["day"]: row["count"] for row in cursor.fetchall()}
        
        return AnalyticsSummary(
            total_clicks=total_clicks,
            unique_visitors=unique_visitors,
            top_countries=top_countries,
            top_devices=top_devices,
            top_referrers=top_referrers,
            clicks_by_day=clicks_by_day
        )
    
    # ==================== TEMPLATES ====================
    def create_template(self, template_data: TemplateCreate) -> Template:
        """Create a new template"""
        template_id = str(uuid4())
        created_at = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO templates (id, name, slug, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (template_id, template_data.name, template_data.slug, 
              json.dumps(template_data.content), created_at))
        self.conn.commit()
        
        return Template(
            id=UUID(template_id),
            name=template_data.name,
            slug=template_data.slug,
            content=template_data.content,
            created_at=datetime.fromisoformat(created_at)
        )
    
    def list_templates(self) -> List[Template]:
        """List all templates"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM templates ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [Template(
            id=UUID(row["id"]),
            name=row["name"],
            slug=row["slug"],
            content=json.loads(row["content"]),
            created_at=datetime.fromisoformat(row["created_at"])
        ) for row in rows]
    
    # ==================== CAMPAIGNS ====================
    def create_campaign(self, campaign_data: CampaignCreate) -> Campaign:
        """Create a new campaign"""
        campaign_id = str(uuid4())
        created_at = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO campaigns (id, name, description, link_ids, start_date, end_date, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            campaign_id, campaign_data.name, campaign_data.description,
            json.dumps([str(lid) for lid in campaign_data.link_ids]),
            campaign_data.start_date.isoformat() if campaign_data.start_date else None,
            campaign_data.end_date.isoformat() if campaign_data.end_date else None,
            CampaignStatus.DRAFT.value, created_at
        ))
        self.conn.commit()
        
        return Campaign(
            id=UUID(campaign_id),
            name=campaign_data.name,
            description=campaign_data.description,
            link_ids=campaign_data.link_ids,
            start_date=campaign_data.start_date,
            end_date=campaign_data.end_date,
            status=CampaignStatus.DRAFT,
            created_at=datetime.fromisoformat(created_at)
        )
    
    def list_campaigns(self) -> List[Campaign]:
        """List all campaigns"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [Campaign(
            id=UUID(row["id"]),
            name=row["name"],
            description=row["description"],
            link_ids=[UUID(lid) for lid in json.loads(row["link_ids"])] if row["link_ids"] else [],
            start_date=datetime.fromisoformat(row["start_date"]) if row["start_date"] else None,
            end_date=datetime.fromisoformat(row["end_date"]) if row["end_date"] else None,
            status=CampaignStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"])
        ) for row in rows]
    
    # ==================== LICENSE ====================
    def activate_license(self, license_key: str, email: str = None) -> LicenseInfo:
        """Activate a license key"""
        license_info = validate_license(license_key)
        
        if license_info and license_info.is_valid:
            self.license = license_info
            self.edition = license_info.edition
            
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO license (id, license_key, edition, activated_at, expires_at, user_email)
                VALUES (1, ?, ?, ?, ?, ?)
            """, (
                license_key,
                license_info.edition,
                datetime.utcnow().isoformat(),
                license_info.expires_at.isoformat() if license_info.expires_at else None,
                email or "unknown"
            ))
            self.conn.commit()
        
        return license_info
    
    def get_license_info(self) -> Optional[LicenseInfo]:
        """Get current license info"""
        return self.license
    
    # ==================== QR CODE ====================
    def generate_qr(self, link: Link, size: int = 300) -> str:
        """Generate QR code for a link (returns base64)"""
        try:
            import qrcode
            import io
            import base64
            
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            qr.add_data(link.short_url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            img = img.resize((size, size))
            
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode()
        except ImportError:
            return None
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


# Singleton accessor
def get_morelinks() -> MoreLinks:
    """Get the singleton MoreLinks instance"""
    return MoreLinks._instance


# Factory function
def create_morelinks(
    db_path: str = "morelinks.db",
    edition: str = None,
    license_key: str = None,
    demo: bool = True
) -> MoreLinks:
    """Create a new MoreLinks instance"""
    return MoreLinks(
        db_path=db_path,
        edition=edition,
        license_key=license_key,
        demo_mode=demo
    )
