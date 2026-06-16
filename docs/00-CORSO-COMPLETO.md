# 🎓 Corso MoreLinks - Corso Completo di Formazione

Benvenuto nel corso completo su **MoreLinks**! Questa guida ti insegnerà tutto, dall'installazione alle funzionalità avanzate.

---

## 📋 Indice del Corso

1. [Introduzione](#1-introduzione)
2. [Installazione](#2-installazione)
3. [Architettura del Sistema](#3-architettura-del-sistema)
4. [Modulo Link Management](#4-modulo-link-management)
5. [Modulo Chatbot AI](#5-modulo-chatbot-ai)
6. [Omni Brain](#6-omni-brain)
7. [Book2Skills](#7-book2skills)
8. [Normative Italiane](#8-normative-italiane)
9. [GUI e UI](#9-gui-e-ui)
10. [Integrazioni](#10-integrazioni)
11. [Sviluppo Avanzato](#11-sviluppo-avanzato)

---

## 1. Introduzione

### 1.1 Cos'è MoreLinks?

**MoreLinks** è una piattaforma completa che unisce:

| Funzionalità | Descrizione |
|--------------|-------------|
| 🔗 **Link Management** | Come Linktree - gestisci tutti i tuoi link |
| 🏢 **Gestionale Business** | Come Pienissimo - gestisci la tua azienda |
| 🤖 **Chatbot AI** | Assistente virtuale con memoria permanente |
| 📚 **Book2Skills** | 5000+ libri trasformati in competenze |
| 🧠 **Omni Brain** | Cervello AI centrale per automazioni |

### 1.2 Perché MoreLinks?

```
Pienissimo + Linktree + Chatbot AI = MoreLinks
```

**Vantaggi:**
- ✅ Tutto in uno (link + business + AI)
- ✅ Memoria permanente (ricorda TUTTO)
- ✅ Modelli AI gratuiti (Nex-N2-Pro, Nemotron)
- ✅ Normative italiane integrate
- ✅ Multi-piattaforma (Windows, Mac, Android, Web)

### 1.3 Requisiti di Sistema

| Componente | Requisito Minimo |
|------------|------------------|
| Python | 3.11+ |
| RAM | 4 GB |
| Spazio Disco | 100 MB |
| OS | Windows 10+, macOS 11+, Linux |

---

## 2. Installazione

### 2.1 Clona il Repository

```bash
git clone https://github.com/Schumynet/MoreLinks.git
cd MoreLinks
```

### 2.2 Crea Virtual Environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 2.3 Installa Dipendenze

```bash
pip install -r requirements.txt
```

### 2.4 File requirements.txt

```txt
# Core
aiohttp>=3.9.0
sqlite3 (built-in)

# AI
openai>=1.0.0

# GUI (opzionali)
PyQt6>=6.6.0     # Windows
streamlit>=1.30.0 # Web

# Utils
python-dotenv>=1.0.0
qrcode>=7.4.0
```

### 2.5 Configurazione API Key

Crea file `.env`:

```env
# OpenRouter API (per Omni Brain AI)
OPENROUTER_API_KEY=sk-or-v1-your-key-here

# GitHub Token (per memoria sync)
GITHUB_TOKEN=ghp_your_token
```

### 2.6 Primo Avvio

```bash
# CLI
python cli/app.py

# GUI Windows
python gui/windows/app.py

# Web
streamlit run gui/web/app.py
```

---

## 3. Architettura del Sistema

### 3.1 Diagramma Architettura

```
┌─────────────────────────────────────────────────────────────┐
│                      MORE LINKS                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  Link Mgmt  │  │   Chatbot   │  │   Book2Skills │
│  │             │  │             │  │             │        │
│  │  • ShortURL │  │  • Memory   │  │  • 5000+    │        │
│  │  • QR Code  │  │  • Norme    │  │    Libri    │        │
│  │  • Analytics│  │  • Tasks    │  │  • Skills   │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │
│         └────────────────┼────────────────┘                │
│                          │                                  │
│                   ┌──────▼──────┐                          │
│                   │  OMNI BRAIN │                          │
│                   │             │                          │
│                   │  • AI Chat  │                          │
│                   │  • Actions  │                          │
│                   │  • Memory   │                          │
│                   └──────┬──────┘                          │
│                          │                                  │
│         ┌────────────────┼────────────────┐               │
│         │                │                │               │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐        │
│  │  SQLite DB  │  │   GitHub    │  │  OpenRouter │        │
│  │  (Locale)   │  │   (Cloud)   │  │    (AI)     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Struttura Directory

```
MoreLinks/
├── src/morelinks/           # Core Package
│   ├── __init__.py
│   ├── models.py            # Modelli dati (Pydantic)
│   ├── database.py          # Database SQLite
│   ├── config.py            # Configurazione
│   │
│   ├── ai/                  # AI Module
│   │   └── omni_brain.py   # Omni Brain AI
│   │
│   ├── chatbot/             # Chatbot Module
│   │   ├── chatbot.py       # Chatbot principale
│   │   ├── memory.py        # Memoria persistente
│   │   └── normative_knowledge.py  # Normative
│   │
│   ├── core/                # Core Features
│   │   ├── morelinks.py     # Gestione link
│   │   └── version.py       # Versione
│   │
│   └── book2skills/         # Book2Skills Module
│       └── book2skills.py    # Library libri
│
├── cli/                     # CLI Application
│   └── app.py
│
├── gui/                     # GUI Applications
│   ├── windows/app.py       # Windows (PyQt6)
│   ├── mac/app.py           # Mac (Tkinter)
│   ├── linux/app.py         # Linux (Tkinter)
│   ├── android/pwa/         # Android (PWA)
│   └── web/app.py           # Web (Streamlit)
│
├── docs/                    # Documentazione
│   ├── 00-CORSO-COMPLETO.md
│   ├── 01-INSTALLazione.md
│   ├── 02-LINK-MANAGEMENT.md
│   └── ...
│
├── tests/                   # Test
│   ├── test_chatbot.py
│   ├── test_omni_brain.py
│   └── test_database.py
│
├── Book2Skills/             # Repository separato
│   └── book2skills.py
│
├── SPEC.md                  # Specifiche tecniche
├── README.md                # Readme principale
└── requirements.txt         # Dipendenze
```

### 3.3 Flusso Dati

```
┌──────────────────────────────────────────────────────────────┐
│                      FLUSSO DATI                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Utente ──► GUI/CLI ──► Omni Brain ──► AI (OpenRouter)     │
│                    │           │                            │
│                    │           ▼                            │
│                    │     ┌─────────────┐                    │
│                    │     │   Memory    │                    │
│                    │     │   SQLite    │                    │
│                    │     └──────┬──────┘                    │
│                    │            │                          │
│                    ▼            ▼                           │
│              ┌─────────────┐  ┌─────────────┐               │
│              │   Links DB  │  │ GitHub Sync │               │
│              │   SQLite    │  │   (Cloud)   │               │
│              └─────────────┘  └─────────────┘               │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 4. Modulo Link Management

### 4.1 Introduzione

Il modulo **Link Management** permette di:
- ✅ Creare short URL personalizzati
- ✅ Generare QR Code automatici
- ✅ Statistiche click in tempo reale
- ✅ Gestione campaign

### 4.2 Modello Dati

```python
# src/morelinks/models.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Link(BaseModel):
    """Modello Link"""
    id: int
    short_code: str              # es: "abc123"
    original_url: str            # URL completo
    title: Optional[str] = None  # Titolo descrittivo
    description: Optional[str] = None
    click_count: int = 0         # Contatore click
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    expires_at: Optional[datetime] = None
    tags: list[str] = []
    user_id: str = "default"

class LinkCreate(BaseModel):
    """Schema creazione link"""
    original_url: str
    title: Optional[str] = None
    custom_code: Optional[str] = None  # Codice personalizzato
    tags: list[str] = []
```

### 4.3 Database Schema

```sql
-- Tabella links
CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    short_code TEXT UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    title TEXT,
    description TEXT,
    click_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    expires_at TIMESTAMP,
    user_id TEXT DEFAULT 'default',
    tags TEXT DEFAULT '[]'
);

-- Tabella clicks (analytics)
CREATE TABLE clicks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    link_id INTEGER REFERENCES links(id),
    ip_address TEXT,
    user_agent TEXT,
    referrer TEXT,
    country TEXT,
    device_type TEXT,
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4.4 Utilizzo Base

```python
from morelinks import MoreLinks

# Crea istanza
db = MoreLinks()

# Crea link
link = db.create_link(
    original_url="https://example.com",
    title="Il mio sito"
)
print(f"Link creato: {link.short_url}")

# Lista link
links = db.list_links()
for link in links:
    print(f"{link.short_code}: {link.click_count} click")

# Statistiche
stats = db.get_analytics_summary()
print(f"Total click: {stats.total_clicks}")
```

### 4.5 QR Code

```python
import qrcode
from io import BytesIO

def generate_qr(short_code: str) -> bytes:
    """Genera QR code per un link"""
    url = f"https://ml.app/{short_code}"
    
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()
```

---

## 5. Modulo Chatbot AI

### 5.1 Architettura Chatbot

```
┌─────────────────────────────────────────────────────────────┐
│                      CHATBOT AI                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Utente ──► Parser ──► Intent Detection ──► Action Router  │
│                │              │                   │         │
│                ▼              ▼                   ▼         │
│         ┌──────────┐    ┌──────────┐       ┌──────────┐    │
│         │  Memory  │    │  Norme   │       │  Tasks   │    │
│         │ (Recall) │    │ (Search) │       │ (CRUD)   │    │
│         └──────────┘    └──────────┘       └──────────┘    │
│                              │                             │
│                              ▼                             │
│                    ┌──────────────────┐                    │
│                    │    AI Response   │                    │
│                    │  (OpenRouter)    │                    │
│                    └──────────────────┘                    │
│                              │                             │
│                              ▼                             │
│                      ┌──────────────┐                      │
│                      │   Memory     │                      │
│                      │  (Remember)  │                      │
│                      └──────────────┘                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Intent Detection

```python
# Intent predefiniti
INTENTS = {
    "link_create": ["crea link", "nuovo link", "aggiungi link"],
    "link_list": ["mostra link", "lista link", "i miei link"],
    "link_stats": ["statistiche", "stats", "quanti click"],
    "memory_save": ["ricorda", "memorizza", "non dimenticare"],
    "memory_recall": ["cosa sai", "ricordi", "hai salvato"],
    "norm_search": ["normativa", "legge", "regolamento"],
    "task_create": ["crea task", "nuovo task", "promemoria"],
    "task_list": ["mostra task", "cose da fare"],
    "greeting": ["ciao", "salve", "buongiorno"],
}
```

### 5.3 Utilizzo Chatbot

```python
from morelinks import MoreLinksChatbot

# Crea chatbot
bot = MoreLinksChatbot()

# Chat
response = bot.process("Ciao! Mi chiamo Fabio")
print(response.message)
# Output: "Ciao Fabio! Piacere di conoscerti. Come posso aiutarti?"

# Chat con memoria
bot.process("La mia azienda si chiama TestCorp")
bot.process("Come si chiama la mia azienda?")
# Output: "La tua azienda si chiama TestCorp!"
```

### 5.4 Risposte Contestuali

```python
# Risposte predefinite per contesto
CONTEXT_RESPONSES = {
    "link_created": "✅ Link creato con successo!\n\n🔗 {short_url}\n\nClicca per copiare.",
    "link_not_found": "❌ Link non trovato. Prova a creare un nuovo link!",
    "memory_saved": "🧠 Informazione salvata nella memoria permanente!",
    "memory_recalled": "📋 Ecco cosa ho trovato:\n\n{memories}",
    "norm_found": "📜 Ho trovato:\n\n**{title}**\n\n{summary}\n\nVuoi approfondire?",
}
```

---

## 6. Omni Brain

### 6.1 Cos'è Omni Brain?

**Omni Brain** è il cervello AI centrale di MoreLinks:

| Caratteristica | Descrizione |
|----------------|-------------|
| 🤖 **Modello** | NVIDIA Nemotron / Nex-N2-Pro (GRATIS) |
| 🧠 **Memoria** | SQLite + GitHub Sync |
| 🔧 **Azioni** | Python, Bash, API execution |
| 📚 **Knowledge** | Book2Skills + Normative |
| 🎯 **Agents** | 5 agent specializzati |

### 6.2 Configurazione

```python
# src/morelinks/config.py

# Modelli gratuiti disponibili
FREE_MODELS = {
    "nemotron": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nex-n2-pro": "nex-agi/nex-n2-pro:free", 
    "safety": "nvidia/nemotron-3-5-content-safety:free"
}

# Default
DEFAULT_MODEL = "nvidia/nemotron-3-5-content-safety:free"
```

### 6.3 Utilizzo Omni Brain

```python
from morelinks.ai.omni_brain import create_omni_brain

# Crea Omni Brain
brain = create_omni_brain(
    api_key="sk-or-v1-your-key",
    github_token="ghp_your_token"
)

# Chat
result = brain.chat_sync("Ciao! Mi chiamo Fabio")
print(result['response'])

# Azioni
import asyncio
action_result = asyncio.run(
    brain.execute_action("list_links")
)
print(action_result)
```

### 6.4 Sistema Agenti

```python
AGENTS = [
    {
        "id": "omni",
        "name": "Omni",
        "role": "Assistente Generale",
        "capabilities": ["all"],
        "instructions": "Aiuta con qualsiasi richiesta"
    },
    {
        "id": "admin",
        "name": "AdminBot",
        "role": "Amministrazione",
        "capabilities": ["norms", "compliance", "tasks"],
        "instructions": "Specializzato in normative italiane"
    },
    {
        "id": "coder",
        "name": "CodeBot",
        "role": "Sviluppatore",
        "capabilities": ["coding", "python", "debugging"],
        "instructions": "Scrive e corregge codice"
    },
    {
        "id": "marketer",
        "name": "MarketingBot",
        "role": "Marketing",
        "capabilities": ["seo", "content", "social"],
        "instructions": "Specializzato in marketing digitale"
    },
    {
        "id": "researcher",
        "name": "ResearchBot",
        "role": "Ricerca",
        "capabilities": ["books", "knowledge", "learning"],
        "instructions": "Accesso a 5000+ libri Book2Skills"
    },
]
```

### 6.5 Azioni Disponibili

```python
# Azioni predefinite
ACTIONS = {
    "create_link": {
        "description": "Crea short link",
        "params": {"url": "str", "title": "str"},
        "type": "python"
    },
    "list_links": {
        "description": "Lista tutti i link",
        "params": {},
        "type": "python"
    },
    "remember": {
        "description": "Salva in memoria",
        "params": {"content": "str", "category": "str"},
        "type": "python"
    },
    "recall": {
        "description": "Cerca memorie",
        "params": {"query": "str"},
        "type": "python"
    },
    "search_norms": {
        "description": "Cerca normative",
        "params": {"query": "str"},
        "type": "python"
    },
    "create_task": {
        "description": "Crea task",
        "params": {"title": "str", "priority": "str"},
        "type": "python"
    },
}
```

---

## 7. Book2Skills

### 7.1 Introduzione

**Book2Skills** è una library che trasforma 5000+ libri in competenze azionabili.

### 7.2 Struttura Database

```python
# Categorie principali
CATEGORIES = [
    "Business & Management",
    "Technology & Programming",
    "Psychology & Self-Help",
    "Sales & Negotiation",
    "Entrepreneurship",
    "Marketing & Advertising",
    "Creativity & Design",
    "Habits & Mindset",
    "Leadership & Management",
    "Mindfulness & Spirituality",
    "Productivity & Time Management",
    # ... 30+ categorie
]

# Schema libro
class Book:
    id: int
    title: str
    author: str
    category: str
    year: int
    summary: str
    skills: list[str]      # Competenze acquisibili
    key_takeaways: list[str]
    chapters: list[str]
```

### 7.3 Utilizzo

```python
from book2skills import Book2SkillsLibrary

lib = Book2SkillsLibrary()

# Cerca libri
results = lib.search_books("productivity")
for book in results:
    print(f"📖 {book.title}")
    print(f"   Autore: {book.author}")
    print(f"   Skills: {', '.join(book.skills[:3])}")

# Filtra per categoria
lib.set_category("Business & Management")
books = lib.get_books()

# Suggerimenti basati su interessi
suggestions = lib.get_suggestions(["marketing", "sales"])
```

### 7.4 Esempio Skills

```
📚 Libro: "Atomic Habits" - James Clear

Skills acquisibili:
• 🎯 Habit Formation
• 🎯 Identity-Based Habits  
• 🔄 Habit Stacking
• 📊 Habit Tracking
• 🎮 Variable Rewards

Takeaways:
1. Piccoli miglioramenti = grandi risultati
2. Cambia il tuo ambiente
3. Il 2% migliora ogni giorno
```

---

## 8. Normative Italiane

### 8.1 Database Normative

```python
# Normative integrate
NORMATIVES = {
    "gdpr": {
        "title": "GDPR - Regolamento UE 679/2016",
        "category": "Privacy",
        "description": "Protezione dati personali",
        "obligations": [
            "Protezione dati personali",
            "Nomina DPO (se richiesto)",
            "Registro trattamenti",
            "Notifica violazioni entro 72h",
            "Informativa agli interessati"
        ],
        "penalties": "Fino a €20M o 4% fatturato"
    },
    "231_2001": {
        "title": "DLgs 231/2001",
        "category": "Responsabilità Enti",
        "description": "Responsabilità amministrativa",
        "obligations": [
            "Adozione Modello Organizzativo",
            "Nomina Organismo di Vigilanza",
            "Codice Etico",
            "Whistleblowing",
            "Formazione personale"
        ],
        "penalties": "Sanzioni fino a €1.5M + interdittive"
    },
    # ... altre normative
}
```

### 8.2 Utilizzo

```python
from morelinks import NormativeKnowledge

nk = NormativeKnowledge()

# Cerca normativa
results = nk.search("privacy")
for norm in results:
    print(f"📜 {norm.title}")
    print(f"   Obblighi: {len(norm.obligations)}")

# Dettagli
norm = nk.get("gdpr")
print(f"""
Normativa: {norm.title}
Categoria: {norm.category}

Obblighi:
{chr(10).join(f"• {o}" for o in norm.obligations)}

Sanzioni: {norm.penalties}
""")
```

### 8.3 Lista Normative Complete

| Codice | Nome | Categoria |
|--------|------|-----------|
| GDPR | Reg. UE 679/2016 | Privacy |
| 231_2001 | DLgs 231/2001 | Responsabilità |
| 81_2008 | DLgs 81/2008 | Sicurezza Lavoro |
| 127_2015 | DLgs 127/2015 | Fatturazione |
| 196_2003 | Codice Privacy | Privacy |
| 300_1970 | Statuto Lavoratori | Lavoro |
| 231_2007 | DLgs 231/2007 | Antiriciclaggio |
| 917_1986 | TUIR | Contabilità |

---

## 9. GUI e UI

### 9.1 Panoramica GUI

| Piattaforma | Framework | Tecnologia |
|-------------|-----------|------------|
| Windows | PyQt6 | Desktop nativo |
| Mac | Tkinter | Desktop nativo |
| Linux | Tkinter | Desktop nativo |
| Android | PWA | HTML5/CSS3/JS |
| Web/Chromebook | Streamlit | Python + Web |

### 9.2 Windows GUI (PyQt6)

```python
# gui/windows/app.py

from PyQt6.QtWidgets import QApplication, QMainWindow

class MoreLinksWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MoreLinks")
        # ... UI setup
    
    def create_tabs(self):
        """Crea tabs principali"""
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_dashboard(), "🏠 Dashboard")
        self.tabs.addTab(self.create_links(), "🔗 Link")
        self.tabs.addTab(self.create_chatbot(), "🤖 Chatbot")
        self.tabs.addTab(self.create_upload(), "📤 Upload")
```

### 9.3 Android PWA

```html
<!-- gui/android/pwa/index.html -->

<!-- PWA con design moderno -->
<div class="bottom-nav">
    <div class="nav-item active">
        <span class="icon">🏠</span>
        <span class="label">Home</span>
    </div>
    <div class="nav-item">
        <span class="icon">🔗</span>
        <span class="label">Link</span>
    </div>
</div>

<!-- Chat integrato -->
<div class="chat-container">
    <div class="message user">Ciao!</div>
    <div class="message ai">Ciao, sono Omni!</div>
</div>
```

### 9.4 Web Streamlit

```python
# gui/web/app.py

import streamlit as st

st.title("🔗 MoreLinks")

# Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Link", len(links))
col2.metric("Click", total_clicks)
col3.metric("Memoria", memory_count)

# Chat
if prompt := st.chat_input("Scrivi..."):
    st.chat_message("user").write(prompt)
    response = brain.chat_sync(prompt)
    st.chat_message("assistant").write(response)
```

---

## 10. Integrazioni

### 10.1 OpenRouter Integration

```python
import aiohttp

async def call_ai(messages: list, model: str):
    """Chiama OpenRouter API"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": 2000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        ) as resp:
            return await resp.json()
```

### 10.2 GitHub Sync

```python
# Sincronizza memoria su GitHub
def sync_to_github(memory: dict):
    """Salva memoria su repo GitHub"""
    # Push to GitHub repo
    pass

def sync_from_github():
    """Leggi memorie da GitHub"""
    # Pull from GitHub repo
    pass
```

### 10.3 QR Code Generation

```python
import qrcode
from PIL import Image

def create_qr_with_logo(url: str, logo_path: str = None):
    """Crea QR con logo opzionale"""
    qr = qrcode.QRCode(version=3)
    qr.add_data(url)
    qr.make()
    
    img = qr.make_image()
    
    if logo_path:
        logo = Image.open(logo_path)
        logo = logo.resize((50, 50))
        
        pos = (
            (img.size[0] - logo.size[0]) // 2,
            (img.size[1] - logo.size[1]) // 2
        )
        img.paste(logo, pos)
    
    return img
```

---

## 11. Sviluppo Avanzato

### 11.1 Testing

```python
# tests/test_chatbot.py

import pytest
from morelinks import MoreLinksChatbot

@pytest.fixture
def bot():
    return MoreLinksChatbot()

def test_greeting(bot):
    response = bot.process("Ciao")
    assert "ciao" in response.message.lower()

def test_memory(bot):
    bot.process("Mi chiamo Test")
    response = bot.process("Come mi chiamo?")
    assert "test" in response.message.lower()
```

### 11.2 Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "gui/web/app.py"]
```

### 11.3 CI/CD

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest tests/
```

---

## 🎓 Esercizi Pratici

### Esercizio 1: Crea il tuo primo Link
```python
# Crea un link per il tuo sito
link = db.create_link(
    original_url="https://tuosito.com",
    title="Il mio sito"
)
print(f"Short URL: {link.short_url}")
```

### Esercizio 2: Usa il Chatbot
```python
# Prova il chatbot
bot = MoreLinksChatbot()
bot.process("Ciao! Mi chiamo Mario")
bot.process("La mia azienda si chiama TechCorp")
print(bot.process("Come mi chiamo?"))  # Dovrebbe ricordare!
```

### Esercizio 3: Cerca Normative
```python
# Trova normative su privacy
nk = NormativeKnowledge()
results = nk.search("privacy")
for r in results:
    print(f"📜 {r.title}")
```

---

## 📚 Risorse Aggiuntive

- [SPEC.md](./SPEC.md) - Specifiche tecniche complete
- [README.md](../README.md) - Guida rapida
- [Repository GitHub](https://github.com/Schumynet/MoreLinks)

---

## ✅ Checklist Competenze

Dopo questo corso, saprai:

- [ ] Installare e configurare MoreLinks
- [ ] Creare e gestire short link
- [ ] Usare il chatbot AI con memoria
- [ ] Configurare Omni Brain
- [ ] Cercare normative italiane
- [ ] Usare Book2Skills
- [ ] Distribuire su diverse piattaforme

---

*Corso MoreLinks v1.0 - Creato da Fabio (Schumynet)*
