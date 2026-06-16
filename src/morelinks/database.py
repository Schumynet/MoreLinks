"""
MoreLinks Database Layer
"""

import sqlite3
from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4
import json
from pathlib import Path

from .models import (
    Link, LinkCreate, LinkUpdate,
    Analytics, AnalyticsCreate, AnalyticsSummary,
    Campaign, CampaignCreate,
    Template, TemplateCreate,
    User, UserCreate, UserInDB,
    LinkStatus, CampaignStatus, DeviceType
)


class Database:
    def __init__(self, db_path: str = "morelinks.db"):
        self.db_path = db_path
        self.conn = None
        self._init_db()

    def _init_db(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        cursor = self.conn.cursor()

        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                api_key TEXT UNIQUE NOT NULL,
                plan TEXT DEFAULT 'free',
                created_at TEXT NOT NULL
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

        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_links_short_code ON links(short_code)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_links_user_id ON links(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_link_id ON analytics(link_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_timestamp ON analytics(timestamp)")

        self.conn.commit()

    # === User Operations ===
    def create_user(self, user_data: UserCreate) -> UserInDB:
        import hashlib
        import secrets
        
        user_id = str(uuid4())
        password_hash = hashlib.sha256(user_data.password.encode()).hexdigest()
        api_key = secrets.token_urlsafe(32)
        created_at = datetime.utcnow().isoformat()

        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO users (id, email, password_hash, api_key, plan, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, user_data.email, password_hash, api_key, user_data.plan.value, created_at))
        self.conn.commit()

        return UserInDB(
            id=UUID(user_id),
            email=user_data.email,
            api_key=api_key,
            plan=user_data.plan,
            created_at=datetime.fromisoformat(created_at)
        )

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return UserInDB(
                id=UUID(row["id"]),
                email=row["email"],
                password_hash=row["password_hash"],
                api_key=row["api_key"],
                plan=row["plan"],
                created_at=datetime.fromisoformat(row["created_at"])
            )
        return None

    # === Link Operations ===
    def create_link(self, link_data: LinkCreate, user_id: Optional[UUID] = None) -> Link:
        import random
        import string
        
        link_id = str(uuid4())
        short_code = link_data.short_code or ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        created_at = datetime.utcnow().isoformat()
        tags = json.dumps(link_data.tags or [])

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
            1, 0, link_data.password, str(user_id) if user_id else None
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
            user_id=user_id
        )

    def get_link(self, link_id: UUID) -> Optional[Link]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM links WHERE id = ?", (str(link_id),))
        row = cursor.fetchone()
        if row:
            return self._row_to_link(row)
        return None

    def get_link_by_short_code(self, short_code: str) -> Optional[Link]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM links WHERE short_code = ?", (short_code,))
        row = cursor.fetchone()
        if row:
            return self._row_to_link(row)
        return None

    def list_links(self, user_id: Optional[UUID] = None, tags: Optional[List[str]] = None,
                   limit: int = 100, offset: int = 0) -> List[Link]:
        cursor = self.conn.cursor()
        query = "SELECT * FROM links WHERE 1=1"
        params = []

        if user_id:
            query += " AND user_id = ?"
            params.append(str(user_id))

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        links = [self._row_to_link(row) for row in rows]

        if tags:
            links = [l for l in links if any(t in l.tags for t in tags)]

        return links

    def update_link(self, link_id: UUID, update_data: LinkUpdate) -> Optional[Link]:
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

        updates.append("updated_at = ?")
        params.append(datetime.utcnow().isoformat())
        params.append(str(link_id))

        query = f"UPDATE links SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, params)
        self.conn.commit()

        return self.get_link(link_id)

    def delete_link(self, link_id: UUID) -> bool:
        cursor = self.conn.cursor()
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

    # === Analytics Operations ===
    def track_click(self, link_id: UUID, analytics_data: AnalyticsCreate) -> Analytics:
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
            analytics_data.device.value, analytics_data.browser, analytics_data.os
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
            device=analytics_data.device,
            browser=analytics_data.browser,
            os=analytics_data.os
        )

    def get_analytics(self, link_id: UUID, days: int = 30) -> List[Analytics]:
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

    def get_analytics_summary(self, link_id: Optional[UUID] = None, days: int = 30) -> AnalyticsSummary:
        cursor = self.conn.cursor()
        
        where_clause = f"WHERE timestamp > datetime('now', '-{days} days')"
        if link_id:
            where_clause += f" AND link_id = '{link_id}'"

        # Total clicks
        cursor.execute(f"SELECT COUNT(*) as count FROM analytics {where_clause}")
        total_clicks = cursor.fetchone()["count"]

        # Unique visitors
        cursor.execute(f"SELECT COUNT(DISTINCT ip_address) as count FROM analytics {where_clause}")
        unique_visitors = cursor.fetchone()["count"]

        # Top countries
        cursor.execute(f"""
            SELECT country, COUNT(*) as count FROM analytics 
            {where_clause} AND country IS NOT NULL
            GROUP BY country ORDER BY count DESC LIMIT 5
        """)
        top_countries = {row["country"]: row["count"] for row in cursor.fetchall()}

        # Top devices
        cursor.execute(f"""
            SELECT device, COUNT(*) as count FROM analytics 
            {where_clause}
            GROUP BY device ORDER BY count DESC
        """)
        top_devices = {row["device"]: row["count"] for row in cursor.fetchall()}

        # Top referrers
        cursor.execute(f"""
            SELECT referrer, COUNT(*) as count FROM analytics 
            {where_clause} AND referrer IS NOT NULL
            GROUP BY referrer ORDER BY count DESC LIMIT 5
        """)
        top_referrers = {row["referrer"]: row["count"] for row in cursor.fetchall()}

        # Clicks by day
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

    # === Template Operations ===
    def create_template(self, template_data: TemplateCreate) -> Template:
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

    # === Campaign Operations ===
    def create_campaign(self, campaign_data: CampaignCreate) -> Campaign:
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

    def close(self):
        if self.conn:
            self.conn.close()
