# 🔗 MoreLinks - Piattaforma Completa di Gestione con AI

![MoreLinks](https://img.shields.io/badge/Version-1.0.0-blue) ![Python](https://img.shields.io/badge/Python-3.11+-green) ![License](https://img.shields.io/badge/License-MIT-yellow)

**MoreLinks** è una piattaforma completa che unisce:
- 📎 **Link Management** (come Linktree)
- 🏢 **Gestionale Business** (come Pienissimo)
- 🤖 **Chatbot AI** con memoria permanente
- 📚 **Book2Skills** - 5000+ libri trasformati in skills
- 🧠 **Omni Brain** - Cervello AI centrale

## ✨ Funzionalità

### 🔗 Gestione Link
- Short URL personalizzati
- QR Code automatici
- Analytics in tempo reale
- Gestione campaign

### 🏢 Gestionale Business
- Lead generation
- Gestione contatti
- Prenotazioni automatiche
- Gamification (ruota fortune, slot)

### 🤖 Chatbot AI Omni Brain
- **Memoria Persistente** - Non dimentica MAI nulla
- **Azioni Esecutive** - Python, Bash, API
- **Normative Italiane** - 15+ leggi integrate
- **Multi-Agent** - 5 agent specializzati

### 📚 Book2Skills
- **5000+ Libri** in categorie
- Trasformazione in skills azionabili
- Progress tracking
- Ricerca per argomento

### 🧠 Omni AI Brain
- **Modello Gratuito**: Nex-N2-Pro (OpenRouter)
- **Azioni**: Crea link, gestisci task, cerca normative
- **GitHub Sync**: Memoria su repository cloud
- **Persistent Memory**: SQLite + GitHub

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/Schumynet/MoreLinks.git
cd MoreLinks

# Setup ambiente
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -r requirements.txt

# Esegui CLI
python cli/app.py

# Oppure usa il chatbot
python -c "from morelinks import MoreLinksChatbot; bot = MoreLinksChatbot(); print(bot.process('aiuto').message)"
```

## 📱 Versioni Disponibili

| Piattaforma | Status | Framework |
|------------|--------|-----------|
| 🪟 Windows | ✅ In sviluppo | PyQt6/Tkinter |
| 🍎 Mac | ✅ In sviluppo | BeeWare/Toga |
| 🐧 Linux | ✅ In sviluppo | Tkinter |
| 📱 Android | ✅ In sviluppo | BeeWare/Kivy |
| 🌐 Chromebook/Web | ✅ In sviluppo | Flask/FastAPI |

## 🧠 Omni Brain - Configurazione AI

### Modelli Gratuiti (OpenRouter)
```python
from morelinks.config import FREE_MODELS

FREE_MODELS = {
    "nex-n2-pro": "nex-agi/nex-n2-pro:free",           # ⭐ Raccomandato
    "nemotron": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "safety": "nvidia/nemotron-3-5-content-safety:free"
}
```

### Uso Base
```python
from morelinks.ai.omni_brain import create_omni_brain

# Crea Omni Brain
brain = create_omni_brain(api_key="your-openrouter-key")

# Chat con AI
result = brain.chat_sync("Ciao! Mi chiamo Fabio")
print(result['response'])

# Esegui azioni
import asyncio
result = asyncio.run(brain.execute_action("list_links"))
```

## 🤖 Agenti AI Disponibili

| Agente | Ruolo | Capabilities |
|--------|-------|--------------|
| Omni | Assistente Generale | Tutto |
| AdminBot | Amministrazione | Norme, compliance, task |
| CodeBot | Sviluppatore | Python, debugging, testing |
| MarketingBot | Marketing | SEO, content, social |
| ResearchBot | Ricerca | Books, knowledge, learning |

## 📚 Book2Skills - Libri & Skills

```python
from book2skills import Book2SkillsLibrary

lib = Book2SkillsLibrary()

# Cerca libri
results = lib.search_books("productivity")
for book in results:
    print(f"📖 {book['title']} - {book['author']}")
    print(f"   Skills: {', '.join(book['skills'][:3])}")
```

### Categorie Disponibili
- Business & Management
- Technology & Programming
- Psychology & Self-Help
- Sales & Negotiation
- Entrepreneurship
- Marketing & Advertising
- Creativity & Design
- Habits & Mindset
- Leadership & Management
- Mindfulness & Spirituality
- Productivity & Time Management
- + 30+ altre categorie

## 📜 Normative Italiane Integrate

Il chatbot conosce tutte le normative italiane per le imprese:

| Normativa | Categoria | Obblighi Principali |
|-----------|-----------|---------------------|
| GDPR (Reg. UE 679/2016) | Privacy | Protezione dati, DPO, Notifiche |
| DLgs 231/2001 | Responsabilità | Modello 231, OdV, Whistleblowing |
| DLgs 81/2008 | Lavoro | DVR, RSPP, Sicurezza |
| DLgs 127/2015 | Fatturazione | Fattura elettronica SDI |
| Codice Civile Art. 2423 | Contabilità | Bilancio, Principi OIC |

## 💬 Chatbot - Comandi

```bash
# Modalità interattiva
python cli/app.py

# Comandi principali
link nuova <url>           # Crea short link
link lista                  # Mostra tutti i link
link stats <codice>        # Statistiche link
qr <codice>                # Genera QR code

chat <messaggio>           # Parla con AI
chat storia                # Cronologia conversazione

norme                      # Lista normative
norme cerca <termine>      # Cerca normative
norme obblighi <norma>     # Obblighi specifici

task nuova <titolo>        # Crea task
task lista                 # Lista task
```

## 🔧 Configurazione

### File config.py
```python
# API Key OpenRouter (obbligatoria per Omni Brain)
OPENROUTER_API_KEY = "sk-or-v1-your-key"

# Modello AI (gratuito)
DEFAULT_MODEL = "nex-agi/nex-n2-pro:free"

# GitHub per sync memoria (opzionale)
GITHUB_TOKEN = "ghp_your_token"
GITHUB_REPO = "username/morelinks-memory"
```

## 📦 Struttura Progetto

```
MoreLinks/
├── src/morelinks/         # Core package
│   ├── ai/                 # Omni Brain AI
│   ├── chatbot/            # Chatbot con memoria
│   │   ├── chatbot.py     # Chatbot principale
│   │   ├── memory.py      # Memoria persistente
│   │   └── normative_knowledge.py  # Normative italiane
│   ├── models.py          # Modelli dati
│   ├── database.py         # Database layer
│   └── config.py           # Configurazione
├── cli/                    # CLI application
│   └── app.py              # App CLI interattiva
├── gui/                    # GUI applications
│   ├── windows/            # Windows (PyQt6)
│   ├── mac/                # Mac (BeeWare)
│   ├── android/            # Android (Kivy)
│   └── web/                # Web (Flask)
├── tests/                  # Test unitari
├── docs/                   # Documentazione
└── README.md              # Questo file
```

## 🎯 Roadmap

- [x] Core Python package
- [x] CLI application
- [x] Chatbot con memoria permanente
- [x] Omni Brain AI integration
- [x] Book2Skills library
- [x] Normative italiane
- [ ] GUI Windows
- [ ] GUI Mac
- [ ] GUI Linux
- [ ] App Android
- [ ] Web App (Chromebook)
- [ ] DM Automation (Instagram)
- [ ] Sistema prenotazioni
- [ ] Integrazione ADS

## 🤝 Contributing

1. Fork il repository
2. Crea un branch (`git checkout -b feature/nuova-feature`)
3. Commit (`git commit -am 'Aggiunta nuova feature'`)
4. Push (`git push origin feature/nuova-feature`)
5. Apri una Pull Request

## 📄 Licenza

MIT License - vedi [LICENSE](LICENSE) per dettagli.

## 👤 Autore

**Fabio (Schumynet)**
- GitHub: [@Schumynet](https://github.com/Schumynet)
- Email: fabio@example.com

## 🙏 Ringraziamenti

- [OpenRouter](https://openrouter.ai) - Per i modelli AI gratuiti
- [Nex AGI](https://nex-agi.com) - Per Nex-N2-Pro
- [NVIDIA](https://nvidia.com) - Per Nemotron
- Comunità Python open source

---

<div align="center">
  <p><strong>MoreLinks</strong> - La piattaforma di gestione con AI</p>
  <p>⭐ Se ti piace, dagli una stella!</p>
</div>
