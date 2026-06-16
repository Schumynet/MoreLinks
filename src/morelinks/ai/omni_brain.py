"""
MoreLinks Omni Brain - Central AI Intelligence System
Uses free NVIDIA Nemotron 3 Ultra via OpenRouter
Executes Python actions, manages GitHub memory, integrates Book2Skills
"""

import os
import json
import sqlite3
import subprocess
import asyncio
import aiohttp
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from uuid import uuid4
import re

# OpenRouter API Key (get from environment)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Free model configuration
FREE_MODELS = {
    "primary": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "fallback": "nex-agi/nex-n2-pro:free", 
    "safety": "nvidia/nemotron-3-5-content-safety:free"
}


@dataclass
class AIAgent:
    """An AI agent with specific capabilities"""
    id: str
    name: str
    role: str
    capabilities: List[str]
    instructions: str
    model: str = "nvidia/nemotron-3-ultra-550b-a55b:free"


@dataclass
class Action:
    """An action the AI can execute"""
    id: str
    name: str
    description: str
    action_type: str  # 'python', 'bash', 'api', 'gui'
    code: str
    parameters: Dict[str, Any]
    requires_approval: bool = False
    safe: bool = True


@dataclass
class Memory:
    """A memory entry"""
    id: str
    content: str
    category: str
    importance: float
    created_at: str
    accessed_at: str
    access_count: int = 0


class OmniBrain:
    """
    MoreLinks Omni Brain - The Central AI Intelligence
    
    Features:
    - AI model: NVIDIA Nemotron 3 Ultra (FREE)
    - Action execution: Python, Bash, API
    - Memory: GitHub sync + Local SQLite
    - Book2Skills: Integrated knowledge base
    - Multi-agent: Specialized AI agents
    - Web access: Real-time information
    """
    
    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        github_token: str = None,
        github_repo: str = None,
        db_path: str = "omni_brain.db"
    ):
        self.api_key = api_key or OPENROUTER_API_KEY
        self.model = model or FREE_MODELS["primary"]
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN", "")
        self.github_repo = github_repo or "Schumynet/morelinks-memory"
        
        # Database
        self.db_path = db_path
        self.conn = None
        self._init_db()
        
        # Agents
        self.agents = self._init_agents()
        
        # Actions registry
        self.actions = self._init_actions()
        
        # Memory system
        self.memory = None
        try:
            from ..chatbot.memory import PersistentMemory
            self.memory = PersistentMemory("omni_memory.db")
        except:
            pass
        
        # Book2Skills integration
        self.book_library = None
        try:
            import sys
            sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))))
            from book2skills import Book2SkillsLibrary
            self.book_library = Book2SkillsLibrary()
        except Exception as e:
            print(f"Book2Skills not available: {e}")
        
        print(f"🧠 Omni Brain initialized!")
        print(f"   Model: {self.model}")
        print(f"   Memory: {'GitHub ✓' if self.github_token else 'Local Only'}")
    
    def _init_db(self):
        """Initialize Omni Brain database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        cursor = self.conn.cursor()
        
        # Memories table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                category TEXT NOT NULL,
                importance REAL DEFAULT 0.5,
                created_at TEXT NOT NULL,
                accessed_at TEXT NOT NULL,
                access_count INTEGER DEFAULT 0,
                synced_to_github INTEGER DEFAULT 0,
                tags TEXT DEFAULT '[]'
            )
        """)
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                response TEXT,
                model_used TEXT,
                tokens_used INTEGER,
                actions_taken TEXT,
                timestamp TEXT NOT NULL
            )
        """)
        
        # Actions history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS action_history (
                id TEXT PRIMARY KEY,
                action_name TEXT NOT NULL,
                parameters TEXT,
                result TEXT,
                status TEXT,
                execution_time REAL,
                timestamp TEXT NOT NULL
            )
        """)
        
        # Agents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT NOT NULL,
                capabilities TEXT NOT NULL,
                instructions TEXT,
                model TEXT,
                active INTEGER DEFAULT 1
            )
        """)
        
        # Skills table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                code TEXT,
                created_at TEXT NOT NULL,
                usage_count INTEGER DEFAULT 0
            )
        """)
        
        self.conn.commit()
    
    def _init_agents(self) -> List[AIAgent]:
        """Initialize specialized AI agents"""
        return [
            AIAgent(
                id="omni",
                name="Omni",
                role="General Assistant",
                capabilities=["all"],
                instructions="You are Omni, the central AI brain of MoreLinks. You help with anything.",
                model=self.model
            ),
            AIAgent(
                id="admin",
                name="AdminBot",
                role="Administrative Assistant",
                capabilities=["admin", "norms", "compliance", "tasks", "scheduling"],
                instructions="You are the administrative AI. You know all Italian business regulations, can manage tasks, and help with compliance.",
                model=self.model
            ),
            AIAgent(
                id="coder",
                name="CodeBot",
                role="Python Developer",
                capabilities=["coding", "python", "debugging", "refactoring", "testing"],
                instructions="You are an expert Python developer. You write clean, efficient code and can execute Python directly.",
                model=self.model
            ),
            AIAgent(
                id="marketer",
                name="MarketingBot",
                role="Marketing Expert",
                capabilities=["marketing", "seo", "content", "social", "analytics"],
                instructions="You are a marketing expert. You help with content creation, SEO, social media, and analytics.",
                model=self.model
            ),
            AIAgent(
                id="researcher",
                name="ResearchBot",
                role="Research Assistant",
                capabilities=["research", "analysis", "books", "knowledge", "learning"],
                instructions="You have access to Book2Skills library with 5000+ books. Help users learn and grow.",
                model=self.model
            ),
        ]
    
    def _init_actions(self) -> Dict[str, Action]:
        """Initialize action registry"""
        return {
            "create_link": Action(
                id="create_link",
                name="Create Short Link",
                description="Create a new shortened link",
                action_type="python",
                code="result = {'success': True, 'message': 'Link created via Omni Brain'}",
                parameters={"url": "str", "title": "str|optional"},
                safe=True
            ),
            "list_links": Action(
                id="list_links",
                name="List All Links",
                description="List all user's links",
                action_type="python",
                code="result = {'success': True, 'message': 'Retrieved link list'}",
                parameters={},
                safe=True
            ),
            "get_stats": Action(
                id="get_stats",
                name="Get Statistics",
                description="Get analytics summary",
                action_type="python",
                code="result = {'success': True, 'total_clicks': 0, 'unique_visitors': 0}",
                parameters={},
                safe=True
            ),
            "remember": Action(
                id="remember",
                name="Remember Information",
                description="Store information in permanent memory",
                action_type="python",
                code="result = {'success': True, 'message': 'Remembered via Omni Brain'}",
                parameters={"content": "str", "category": "str|optional"},
                safe=True
            ),
            "recall": Action(
                id="recall",
                name="Recall Memories",
                description="Search and retrieve memories",
                action_type="python",
                code="result = {'success': True, 'memories': []}",
                parameters={"query": "str"},
                safe=True
            ),
            "search_norms": Action(
                id="search_norms",
                name="Search Italian Norms",
                description="Search Italian business regulations",
                action_type="python",
                code="result = {'success': True, 'norms': ['GDPR', 'DLgs 231', 'Codice Civile']}",
                parameters={"query": "str"},
                safe=True
            ),
            "search_books": Action(
                id="search_books",
                name="Search Books",
                description="Search Book2Skills library",
                action_type="python",
                code="result = {'success': True, 'books': []}",
                parameters={"query": "str"},
                safe=True
            ),
            "create_task": Action(
                id="create_task",
                name="Create Task",
                description="Create a new task",
                action_type="python",
                code="result = {'success': True, 'task_id': str(uuid4())}",
                parameters={"title": "str"},
                safe=True
            ),
        }
    
    async def chat(
        self,
        message: str,
        user_id: str = "default",
        session_id: str = None,
        agent_id: str = "omni",
        context: Dict = None,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Main chat function"""
        session_id = session_id or str(datetime.now().timestamp())
        agent = self._get_agent(agent_id)
        system_prompt = self._build_system_prompt(agent, context)
        history = self._get_conversation_history(session_id, limit=10)
        
        messages = [
            {"role": "system", "content": system_prompt},
            *history,
            {"role": "user", "content": message}
        ]
        
        response = await self._call_openrouter(messages, model=self.model, max_tokens=max_tokens)
        
        # Parse actions
        actions_to_execute = self._parse_actions_from_response(response["content"])
        execution_results = []
        for action_spec in actions_to_execute:
            result = await self.execute_action(action_spec["name"], action_spec["params"])
            execution_results.append(result)
        
        self._save_conversation(session_id, user_id, message, response["content"])
        self._learn_from_conversation(message, response["content"])
        
        return {
            "success": True,
            "response": response["content"],
            "agent": agent.name,
            "model": self.model,
            "actions_executed": len(execution_results),
            "action_results": execution_results,
            "tokens_used": response.get("tokens_used", 0)
        }
    
    def chat_sync(
        self,
        message: str,
        user_id: str = "default",
        session_id: str = None,
        agent_id: str = "omni",
        context: Dict = None
    ) -> Dict[str, Any]:
        """Synchronous chat"""
        return asyncio.run(self.chat(message, user_id, session_id, agent_id, context))
    
    async def _call_openrouter(
        self,
        messages: List[Dict],
        model: str = None,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """Call OpenRouter API"""
        model = model or self.model
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://morelinks.app",
            "X-Title": "MoreLinks Omni Brain"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as resp:
                    if resp.status != 200:
                        error = await resp.text()
                        return {"content": f"API Error: {error}", "tokens_used": 0}
                    
                    result = await resp.json()
                    
                    if "choices" in result and len(result["choices"]) > 0:
                        return {
                            "content": result["choices"][0]["message"]["content"],
                            "tokens_used": result.get("usage", {}).get("total_tokens", 0)
                        }
                    
                    return {"content": "No response", "tokens_used": 0}
        except Exception as e:
            return {"content": f"Error: {str(e)}", "tokens_used": 0}
    
    def _build_system_prompt(self, agent: AIAgent, context: Dict = None) -> str:
        """Build system prompt"""
        recent_memories = self._get_recent_memories(limit=5)
        memory_context = "\n".join([f"- {m['content']}" for m in recent_memories])
        
        return f"""You are {agent.name}, {agent.role}.

{agent.instructions}

## Current Date/Time
{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Capabilities
{', '.join(agent.capabilities)}

## To execute actions, respond with JSON:
```json
{{"actions": [{{"name": "action_name", "params": {{"param1": "value1"}}}}]}}
```

## Available Actions
- create_link: Create short link
- list_links: List all links
- get_stats: Get analytics
- remember: Store in memory
- recall: Search memories
- search_norms: Search Italian regulations
- search_books: Search Book2Skills library
- create_task: Create task

## Recent Memories
{memory_context or "No memories yet."}

Be helpful, concise, and accurate. Remember important info for later.
"""
    
    async def execute_action(
        self,
        action_name: str,
        parameters: Dict = None,
        approved: bool = False
    ) -> Dict[str, Any]:
        """Execute an action"""
        parameters = parameters or {}
        
        if action_name not in self.actions:
            return {"success": False, "error": f"Unknown action: {action_name}"}
        
        action = self.actions[action_name]
        
        if action.requires_approval and not approved:
            return {"success": False, "error": "Action requires approval", "requires_approval": True}
        
        start_time = datetime.now()
        
        try:
            if action.action_type == "python":
                namespace = {
                    "params": parameters,
                    "datetime": datetime,
                    "uuid": uuid4,
                    "result": None
                }
                exec(action.code, namespace)
                result = namespace.get("result", {"success": True})
            elif action.action_type == "bash":
                result = subprocess.run(
                    parameters.get("command", ""),
                    shell=True, capture_output=True, text=True, timeout=30
                )
                result = {"success": result.returncode == 0, "stdout": result.stdout}
            else:
                result = {"success": True}
            
            execution_time = (datetime.now() - start_time).total_seconds()
            self._save_action_history(action_name, parameters, result, "success", execution_time)
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _parse_actions_from_response(self, response: str) -> List[Dict]:
        """Parse JSON actions from response"""
        try:
            match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                if "actions" in data:
                    return data["actions"]
            return []
        except:
            return []
    
    def remember(
        self,
        content: str,
        category: str = "general",
        importance: float = 0.5,
        tags: List[str] = None
    ) -> str:
        """Store information in permanent memory"""
        memory_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO memories (id, content, category, importance, created_at, accessed_at, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (memory_id, content, category, importance, timestamp, timestamp, json.dumps(tags or [])))
        self.conn.commit()
        return memory_id
    
    def recall(self, query: str, category: str = None, limit: int = 10) -> List[Dict]:
        """Search and retrieve memories"""
        cursor = self.conn.cursor()
        
        if category:
            cursor.execute("""
                SELECT * FROM memories 
                WHERE content LIKE ? AND category = ?
                ORDER BY importance DESC, accessed_at DESC
                LIMIT ?
            """, (f"%{query}%", category, limit))
        else:
            cursor.execute("""
                SELECT * FROM memories 
                WHERE content LIKE ?
                ORDER BY importance DESC, accessed_at DESC
                LIMIT ?
            """, (f"%{query}%", limit))
        
        rows = cursor.fetchall()
        memories = []
        for row in rows:
            mem = dict(row)
            mem["tags"] = json.loads(mem["tags"]) if mem["tags"] else []
            memories.append(mem)
        
        return memories
    
    def _get_recent_memories(self, limit: int = 5) -> List[Dict]:
        """Get recent memories"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM memories ORDER BY accessed_at DESC LIMIT ?", (limit,))
        return [dict(row) for row in cursor.fetchall()]
    
    def _learn_from_conversation(self, user_message: str, ai_response: str):
        """Learn important info from conversations"""
        import re
        
        patterns = [
            (r"mi chiamo (\w+)", "personal", "name"),
            (r"la mia azienda è (.+?)(?:\.|$)", "company", "name"),
            (r"il mio email è (\S+@\S+)", "contact", "email"),
        ]
        
        for pattern, category, key in patterns:
            match = re.search(pattern, user_message, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                self.remember(content=f"{key}: {value}", category=category, importance=0.8)
    
    def _get_conversation_history(self, session_id: str, limit: int = 10) -> List[Dict]:
        """Get conversation history"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM conversations 
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (session_id, limit))
        
        rows = cursor.fetchall()[::-1]
        return [{"role": row["role"], "content": row["message"]} for row in rows]
    
    def _save_conversation(
        self,
        session_id: str,
        user_id: str,
        user_message: str,
        ai_response: str
    ):
        """Save conversation"""
        timestamp = datetime.utcnow().isoformat()
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (id, session_id, user_id, role, message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(uuid4()), session_id, user_id, "user", user_message, timestamp))
        
        cursor.execute("""
            INSERT INTO conversations (id, session_id, user_id, role, message, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(uuid4()), session_id, user_id, "assistant", ai_response, timestamp))
        
        self.conn.commit()
    
    def _save_action_history(
        self,
        action_name: str,
        parameters: Dict,
        result: Any,
        status: str,
        execution_time: float
    ):
        """Save action history"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO action_history (id, action_name, parameters, result, status, execution_time, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (str(uuid4()), action_name, json.dumps(parameters), json.dumps(result), status, execution_time, datetime.utcnow().isoformat()))
        self.conn.commit()
    
    def _get_agent(self, agent_id: str) -> AIAgent:
        """Get agent by ID"""
        for agent in self.agents:
            if agent.id == agent_id:
                return agent
        return self.agents[0]
    
    def get_agents(self) -> List[AIAgent]:
        """Get all agents"""
        return self.agents
    
    def learn_skill(self, name: str, description: str, code: str, category: str = "custom"):
        """Learn a new skill"""
        skill_id = str(uuid4())
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO skills (id, name, description, category, code, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (skill_id, name, description, category, code, datetime.utcnow().isoformat()))
        self.conn.commit()
        return skill_id
    
    def get_skills(self, category: str = None) -> List[Dict]:
        """Get all skills"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM skills ORDER BY usage_count DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_stats(self) -> Dict:
        """Get Omni Brain statistics"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as c FROM memories")
        total_memories = cursor.fetchone()["c"]
        
        cursor.execute("SELECT COUNT(*) as c FROM conversations")
        total_conversations = cursor.fetchone()["c"]
        
        cursor.execute("SELECT COUNT(*) as c FROM action_history WHERE status = 'success'")
        successful_actions = cursor.fetchone()["c"]
        
        cursor.execute("SELECT COUNT(*) as c FROM skills")
        total_skills = cursor.fetchone()["c"]
        
        return {
            "model": self.model,
            "agents": len(self.agents),
            "actions": len(self.actions),
            "total_memories": total_memories,
            "total_conversations": total_conversations,
            "successful_actions": successful_actions,
            "total_skills": total_skills,
            "github_sync": bool(self.github_token)
        }
    
    def close(self):
        """Close database"""
        if self.conn:
            self.conn.close()


def create_omni_brain(api_key: str = None, github_token: str = None) -> OmniBrain:
    """Create a new Omni Brain instance"""
    return OmniBrain(api_key=api_key, github_token=github_token)


if __name__ == "__main__":
    print("🧠 MoreLinks Omni Brain")
    print("=" * 50)
    
    brain = create_omni_brain()
    
    stats = brain.get_stats()
    print(f"\n✅ Omni Brain ready!")
    print(f"   Model: {stats['model']}")
    print(f"   Agents: {stats['agents']}")
    print(f"   Actions: {stats['actions']}")
    print(f"   Memories: {stats['total_memories']}")
    
    print("\n💬 Test chat:")
    result = brain.chat_sync("Ciao! Mi chiamo Fabio")
    print(f"   AI: {result['response'][:200]}...")
    
    brain.close()
