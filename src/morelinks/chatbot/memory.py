"""
MoreLinks Chatbot - Persistent Memory System
Never forgets anything - True Administrative AI Assistant
"""

import sqlite3
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from uuid import uuid4
from pathlib import Path


@dataclass
class ConversationEntry:
    """A single conversation entry"""
    id: str
    session_id: str
    user_id: str
    role: str  # 'user', 'assistant', 'system'
    message: str
    intent: str
    entities: Dict[str, Any]
    action_taken: str
    result_data: Optional[Dict]
    timestamp: str
    context: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None  # For semantic search


@dataclass
class UserProfile:
    """Complete user profile with memory"""
    id: str
    name: str
    email: str
    phone: Optional[str]
    company: Optional[str]
    role: str  # 'admin', 'user', 'guest'
    preferences: Dict[str, Any]
    created_at: str
    last_seen: str
    conversation_count: int
    total_messages: int


@dataclass
class ContextWindow:
    """Rolling context window for conversations"""
    recent_messages: List[Dict]
    active_topics: List[str]
    pending_tasks: List[Dict]
    user_preferences: Dict[str, Any]
    knowledge_base_updates: List[str]


class PersistentMemory:
    """
    Permanent Memory System - NEVER FORGETS ANYTHING
    
    Stores everything forever in SQLite with full-text search
    and semantic similarity for context retrieval.
    """
    
    def __init__(self, db_path: str = "morelinks_memory.db"):
        self.db_path = db_path
        self.conn = None
        self._init_memory_db()
    
    def _init_memory_db(self):
        """Initialize persistent memory database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Conversations - ALL messages stored forever
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                intent TEXT DEFAULT '',
                entities TEXT DEFAULT '{}',
                action_taken TEXT DEFAULT '',
                result_data TEXT,
                timestamp TEXT NOT NULL,
                context TEXT DEFAULT '{}'
            )
        """)
        
        # User profiles with memory
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                company TEXT,
                role TEXT DEFAULT 'user',
                preferences TEXT DEFAULT '{}',
                created_at TEXT NOT NULL,
                last_seen TEXT NOT NULL,
                conversation_count INTEGER DEFAULT 0,
                total_messages INTEGER DEFAULT 0,
                metadata TEXT DEFAULT '{}'
            )
        """)
        
        # Facts - Things the AI learned about the user
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_facts (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                category TEXT NOT NULL,
                fact_key TEXT NOT NULL,
                fact_value TEXT NOT NULL,
                confidence REAL DEFAULT 1.0,
                source TEXT DEFAULT 'conversation',
                timestamp TEXT NOT NULL,
                verified INTEGER DEFAULT 0
            )
        """)
        
        # Tasks and reminders
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending',
                priority TEXT DEFAULT 'medium',
                due_date TEXT,
                completed_at TEXT,
                created_at TEXT NOT NULL,
                metadata TEXT DEFAULT '{}'
            )
        """)
        
        # Topics discussed
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                topic TEXT NOT NULL,
                message_count INTEGER DEFAULT 1,
                last_discussed TEXT NOT NULL,
                sentiment TEXT DEFAULT 'neutral',
                metadata TEXT DEFAULT '{}'
            )
        """)
        
        # Links and URLs mentioned
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mentioned_links (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                url TEXT NOT NULL,
                context TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # Full-text search virtual table
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts 
            USING fts5(message, content='conversations', content_rowid='rowid')
        """)
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_user ON conversations(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_timestamp ON conversations(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_facts_user ON learned_facts(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tasks_user ON tasks(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_topics_user ON topics(user_id)")
        
        self.conn.commit()
    
    # ==================== CONVERSATION STORAGE ====================
    
    def save_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        message: str,
        intent: str = "",
        entities: Dict = None,
        action_taken: str = "",
        result_data: Dict = None,
        context: Dict = None
    ) -> str:
        """Save a message to permanent memory - NEVER DELETES"""
        msg_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO conversations (id, session_id, user_id, role, message, intent, 
                                     entities, action_taken, result_data, timestamp, context)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            msg_id,
            session_id,
            user_id,
            role,
            message,
            intent,
            json.dumps(entities or {}),
            action_taken,
            json.dumps(result_data) if result_data else None,
            timestamp,
            json.dumps(context or {})
        ))
        
        # Update FTS index
        cursor.execute("""
            INSERT INTO messages_fts (rowid, message) 
            SELECT rowid, message FROM conversations WHERE id = ?
        """, (msg_id,))
        
        # Update user stats
        cursor.execute("""
            UPDATE user_profiles 
            SET last_seen = ?, total_messages = total_messages + 1
            WHERE id = ?
        """, (timestamp, user_id))
        
        self.conn.commit()
        return msg_id
    
    def get_conversation_history(
        self,
        user_id: str,
        session_id: str = None,
        limit: int = 1000,
        offset: int = 0
    ) -> List[Dict]:
        """Get full conversation history"""
        cursor = self.conn.cursor()
        
        if session_id:
            cursor.execute("""
                SELECT * FROM conversations 
                WHERE user_id = ? AND session_id = ?
                ORDER BY timestamp ASC
                LIMIT ? OFFSET ?
            """, (user_id, session_id, limit, offset))
        else:
            cursor.execute("""
                SELECT * FROM conversations 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """, (user_id, limit, offset))
        
        return [self._row_to_message(row) for row in cursor.fetchall()]
    
    def search_conversations(
        self,
        user_id: str,
        query: str,
        limit: int = 50
    ) -> List[Dict]:
        """Full-text search in conversations"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT c.* FROM conversations c
            JOIN messages_fts fts ON c.rowid = fts.rowid
            WHERE c.user_id = ? AND messages_fts MATCH ?
            ORDER BY c.timestamp DESC
            LIMIT ?
        """, (user_id, query, limit))
        
        return [self._row_to_message(row) for row in cursor.fetchall()]
    
    def get_context_for_response(
        self,
        user_id: str,
        max_messages: int = 20
    ) -> Dict[str, Any]:
        """Get relevant context for generating responses"""
        cursor = self.conn.cursor()
        
        # Get recent messages
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (user_id, max_messages))
        recent = [self._row_to_message(row) for row in cursor.fetchall()][::-1]  # Reverse to chronological
        
        # Get learned facts
        cursor.execute("""
            SELECT * FROM learned_facts 
            WHERE user_id = ? AND verified = 1
            ORDER BY timestamp DESC
        """, (user_id,))
        facts = [dict(row) for row in cursor.fetchall()]
        
        # Get active topics
        cursor.execute("""
            SELECT * FROM topics 
            WHERE user_id = ?
            ORDER BY message_count DESC
            LIMIT 10
        """, (user_id,))
        topics = [dict(row) for row in cursor.fetchall()]
        
        # Get pending tasks
        cursor.execute("""
            SELECT * FROM tasks 
            WHERE user_id = ? AND status = 'pending'
            ORDER BY priority DESC, due_date ASC
            LIMIT 10
        """, (user_id,))
        tasks = [dict(row) for row in cursor.fetchall()]
        
        # Get user profile
        cursor.execute("SELECT * FROM user_profiles WHERE id = ?", (user_id,))
        profile_row = cursor.fetchone()
        profile = dict(profile_row) if profile_row else None
        
        return {
            "recent_messages": recent,
            "learned_facts": facts,
            "active_topics": topics,
            "pending_tasks": tasks,
            "user_profile": profile
        }
    
    # ==================== USER PROFILE ====================
    
    def create_or_update_profile(
        self,
        user_id: str,
        name: str = None,
        email: str = None,
        phone: str = None,
        company: str = None,
        role: str = "user",
        preferences: Dict = None
    ) -> UserProfile:
        """Create or update user profile"""
        timestamp = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_profiles WHERE id = ?", (user_id,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing
            updates = []
            params = []
            if name:
                updates.append("name = ?"); params.append(name)
            if email:
                updates.append("email = ?"); params.append(email)
            if phone:
                updates.append("phone = ?"); params.append(phone)
            if company:
                updates.append("company = ?"); params.append(company)
            updates.append("last_seen = ?"); params.append(timestamp)
            if preferences:
                updates.append("preferences = ?"); params.append(json.dumps(preferences))
            
            params.append(user_id)
            cursor.execute(f"UPDATE user_profiles SET {', '.join(updates)} WHERE id = ?", params)
        else:
            # Create new
            cursor.execute("""
                INSERT INTO user_profiles (id, name, email, phone, company, role, preferences, created_at, last_seen)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, name or "Unknown", email or f"{user_id}@morelinks.local",
                phone, company, role, json.dumps(preferences or {}), timestamp, timestamp
            ))
        
        self.conn.commit()
        
        # Return updated profile
        cursor.execute("SELECT * FROM user_profiles WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return self._row_to_profile(row)
    
    def learn_fact(
        self,
        user_id: str,
        category: str,
        fact_key: str,
        fact_value: str,
        confidence: float = 1.0,
        source: str = "conversation"
    ) -> str:
        """Learn a new fact about the user"""
        fact_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        
        # Check if fact already exists
        cursor.execute("""
            SELECT id FROM learned_facts 
            WHERE user_id = ? AND fact_key = ?
        """, (user_id, fact_key))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing fact
            cursor.execute("""
                UPDATE learned_facts SET fact_value = ?, confidence = ?, timestamp = ?
                WHERE id = ?
            """, (fact_value, confidence, timestamp, existing["id"]))
            fact_id = existing["id"]
        else:
            # Insert new fact
            cursor.execute("""
                INSERT INTO learned_facts (id, user_id, category, fact_key, fact_value, confidence, source, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (fact_id, user_id, category, fact_key, fact_value, confidence, source, timestamp))
        
        self.conn.commit()
        return fact_id
    
    def get_learned_facts(self, user_id: str, category: str = None) -> List[Dict]:
        """Get all learned facts about a user"""
        cursor = self.conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT * FROM learned_facts 
                WHERE user_id = ? AND category = ?
                ORDER BY timestamp DESC
            """, (user_id, category))
        else:
            cursor.execute("""
                SELECT * FROM learned_facts 
                WHERE user_id = ?
                ORDER BY category, timestamp DESC
            """, (user_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # ==================== TASKS ====================
    
    def create_task(
        self,
        user_id: str,
        title: str,
        description: str = None,
        priority: str = "medium",
        due_date: str = None
    ) -> str:
        """Create a new task"""
        task_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO tasks (id, user_id, title, description, status, priority, due_date, created_at)
            VALUES (?, ?, ?, ?, 'pending', ?, ?, ?)
        """, (task_id, user_id, title, description, priority, due_date, timestamp))
        
        self.conn.commit()
        return task_id
    
    def complete_task(self, task_id: str) -> bool:
        """Mark task as completed"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE tasks SET status = 'completed', completed_at = ?
            WHERE id = ?
        """, (datetime.utcnow().isoformat(), task_id))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get_tasks(self, user_id: str, status: str = None) -> List[Dict]:
        """Get user tasks"""
        cursor = self.conn.cursor()
        
        if status:
            cursor.execute("""
                SELECT * FROM tasks WHERE user_id = ? AND status = ?
                ORDER BY priority DESC, due_date ASC
            """, (user_id, status))
        else:
            cursor.execute("""
                SELECT * FROM tasks WHERE user_id = ?
                ORDER BY status, priority DESC, due_date ASC
            """, (user_id,))
        
        return [dict(row) for row in cursor.fetchall()]
    
    # ==================== TOPICS ====================
    
    def track_topic(self, user_id: str, topic: str, sentiment: str = "neutral"):
        """Track topics discussed"""
        timestamp = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id FROM topics WHERE user_id = ? AND topic = ?
        """, (user_id, topic.lower()))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("""
                UPDATE topics SET message_count = message_count + 1, last_discussed = ?, sentiment = ?
                WHERE id = ?
            """, (timestamp, sentiment, existing["id"]))
        else:
            cursor.execute("""
                INSERT INTO topics (id, user_id, topic, message_count, last_discussed, sentiment)
                VALUES (?, ?, ?, 1, ?, ?)
            """, (str(uuid4()), user_id, topic.lower(), timestamp, sentiment))
        
        self.conn.commit()
    
    # ==================== STATS ====================
    
    def get_memory_stats(self, user_id: str = None) -> Dict[str, Any]:
        """Get memory statistics"""
        cursor = self.conn.cursor()
        
        if user_id:
            cursor.execute("SELECT COUNT(*) as c FROM conversations WHERE user_id = ?", (user_id,))
            total_messages = cursor.fetchone()["c"]
            
            cursor.execute("SELECT COUNT(*) as c FROM learned_facts WHERE user_id = ?", (user_id,))
            total_facts = cursor.fetchone()["c"]
            
            cursor.execute("SELECT COUNT(*) as c FROM tasks WHERE user_id = ? AND status = 'pending'", (user_id,))
            pending_tasks = cursor.fetchone()["c"]
            
            cursor.execute("SELECT COUNT(*) as c FROM topics WHERE user_id = ?", (user_id,))
            total_topics = cursor.fetchone()["c"]
            
            return {
                "user_id": user_id,
                "total_messages": total_messages,
                "total_facts_learned": total_facts,
                "pending_tasks": pending_tasks,
                "topics_discussed": total_topics,
                "memory_active": True
            }
        else:
            cursor.execute("SELECT COUNT(*) as c FROM conversations")
            total_messages = cursor.fetchone()["c"]
            
            cursor.execute("SELECT COUNT(*) as c FROM user_profiles")
            total_users = cursor.fetchone()["c"]
            
            return {
                "total_messages_stored": total_messages,
                "total_users": total_users,
                "memory_persistent": True
            }
    
    def _row_to_message(self, row: sqlite3.Row) -> Dict:
        """Convert row to message dict"""
        return {
            "id": row["id"],
            "session_id": row["session_id"],
            "user_id": row["user_id"],
            "role": row["role"],
            "message": row["message"],
            "intent": row["intent"],
            "entities": json.loads(row["entities"]) if row["entities"] else {},
            "action_taken": row["action_taken"],
            "result_data": json.loads(row["result_data"]) if row["result_data"] else None,
            "timestamp": row["timestamp"],
            "context": json.loads(row["context"]) if row["context"] else {}
        }
    
    def _row_to_profile(self, row: sqlite3.Row) -> UserProfile:
        """Convert row to profile"""
        return UserProfile(
            id=row["id"],
            name=row["name"],
            email=row["email"],
            phone=row["phone"],
            company=row["company"],
            role=row["role"],
            preferences=json.loads(row["preferences"]) if row["preferences"] else {},
            created_at=row["created_at"],
            last_seen=row["last_seen"],
            conversation_count=row["conversation_count"],
            total_messages=row["total_messages"]
        )
    
    def close(self):
        """Close connection"""
        if self.conn:
            self.conn.close()


class AdministrativeMemory:
    """
    Specialized memory for administrative/business context
    Remembers EVERYTHING about the user's business
    """
    
    def __init__(self, memory: PersistentMemory):
        self.memory = memory
    
    def store_business_info(self, user_id: str, category: str, key: str, value: Any):
        """Store business-related information"""
        fact_categories = {
            "company": "Informazioni azienda",
            "contacts": "Contatti",
            "preferences": "Preferenze",
            "compliance": "Compliance e normative",
            "links": "Link gestiti",
            "tasks": "Task e progetti",
            "meetings": "Appuntamenti",
            "finances": "Informazioni finanziarie",
            "marketing": "Marketing e campaign",
            "leads": "Lead e clienti"
        }
        
        category_name = fact_categories.get(category, category)
        self.memory.learn_fact(
            user_id=user_id,
            category=category,
            fact_key=key,
            fact_value=json.dumps(value) if isinstance(value, (dict, list)) else str(value),
            source="business_context"
        )
    
    def get_business_summary(self, user_id: str) -> Dict[str, Any]:
        """Get complete business summary for user"""
        facts = self.memory.get_learned_facts(user_id)
        
        summary = {
            "company_info": {},
            "contacts": {},
            "preferences": {},
            "compliance_status": {},
            "active_links": [],
            "pending_tasks": [],
            "recent_activities": []
        }
        
        for fact in facts:
            category = fact["category"]
            key = fact["fact_key"]
            value = fact["fact_value"]
            
            try:
                parsed_value = json.loads(value)
            except:
                parsed_value = value
            
            if category == "company":
                summary["company_info"][key] = parsed_value
            elif category == "contacts":
                summary["contacts"][key] = parsed_value
            elif category == "preferences":
                summary["preferences"][key] = parsed_value
            elif category == "compliance":
                summary["compliance_status"][key] = parsed_value
            elif category == "links":
                summary["active_links"].append(parsed_value)
            elif category == "tasks":
                summary["pending_tasks"].append(parsed_value)
        
        # Get pending tasks
        summary["pending_tasks"] = self.memory.get_tasks(user_id, status="pending")
        
        # Get recent conversations
        recent = self.memory.get_conversation_history(user_id, limit=10)
        summary["recent_activities"] = [r["message"][:100] for r in recent[-5:]]
        
        return summary
    
    def remember_contact(
        self,
        user_id: str,
        name: str,
        email: str = None,
        phone: str = None,
        company: str = None,
        notes: str = None,
        tags: List[str] = None
    ):
        """Remember a contact with full details"""
        contact_id = str(uuid4())
        contact_data = {
            "id": contact_id,
            "name": name,
            "email": email,
            "phone": phone,
            "company": company,
            "notes": notes,
            "tags": tags or []
        }
        
        self.store_business_info(user_id, "contacts", contact_id, contact_data)
        self.store_business_info(user_id, "contacts", f"{name}_id", contact_id)
        
        return contact_id
    
    def get_contact(self, user_id: str, identifier: str) -> Optional[Dict]:
        """Retrieve contact by name or ID"""
        facts = self.memory.get_learned_facts(user_id, category="contacts")
        
        for fact in facts:
            if identifier.lower() in fact["fact_key"].lower():
                try:
                    return json.loads(fact["fact_value"])
                except:
                    return None
        
        return None
    
    def create_reminder(
        self,
        user_id: str,
        title: str,
        description: str = None,
        due_date: str = None,
        priority: str = "medium"
    ) -> str:
        """Create a reminder/task"""
        return self.memory.create_task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )
    
    def get_compliance_reminders(self, user_id: str) -> List[Dict]:
        """Get compliance-related reminders"""
        # This integrates with normative knowledge
        from .normative_knowledge import NormativeKnowledge
        
        norms = NormativeKnowledge()
        deadlines = norms.get_upcoming_deadlines(30)
        
        reminders = []
        for dl in deadlines:
            reminders.append({
                "title": f"Scadenza: {dl['name']}",
                "description": f"{dl['regulation']}",
                "due_date": dl["when"],
                "priority": "high",
                "category": "compliance"
            })
        
        return reminders
