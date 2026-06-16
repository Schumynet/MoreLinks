# MoreLinks - Specifica Tecnica Completa

## 🎯 Panoramica Progetto

**MoreLinks** è un software enterprise per la gestione, brandizzazione e analytics di link URL con automazione avanzata.

### Caratteristiche Principali
- ✅ Generazione e brandizzazione URL personalizzati
- ✅ Dashboard analytics in tempo reale
- ✅ Automazione "Bulldozer" per operazioni bulk
- ✅ Supporto multi-piattaforma (Windows, Mac, Android)
- ✅ API RESTful per integrazioni
- ✅ Sistema di template per campagne marketing
- ✅ QR Code generation integrato
- ✅ Esportazione dati avanzata (CSV, JSON, PDF)

---

## 🏗️ Architettura Sistema

### Stack Tecnologico

| Componente | Tecnologia | Versione |
|------------|-----------|----------|
| **Backend** | Python | 3.11+ |
| **API** | FastAPI | 0.104+ |
| **Database** | SQLite / PostgreSQL | 15+ |
| **CLI** | Click | 8.1+ |
| **GUI Windows** | PyQt6 / Tkinter | 6.4+ |
| **GUI Mac** | BeeWare/Toga | 0.3+ |
| **Android** | BeeWare/Toga + Kivy | 2.2+ |
| **Automazione** | Selenium/Playwright | Latest |
| **Testing** | pytest | 7.4+ |

### Diagramma Architettura

```
┌─────────────────────────────────────────────────────────┐
│                    MoreLinks System                      │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Windows   │  │     Mac     │  │   Android   │    │
│  │    GUI      │  │    GUI      │  │     GUI      │    │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘    │
│         │                │                │            │
│  ┌──────┴────────────────┴────────────────┴──────┐     │
│  │              CLI / BULDIZER                    │     │
│  │         (Automazione Bulk Operations)          │     │
│  └──────────────────────┬─────────────────────────┘     │
│                         │                               │
│  ┌──────────────────────┴─────────────────────────┐     │
│  │                 REST API (FastAPI)              │     │
│  │  - Links CRUD                                    │     │
│  │  - Analytics                                     │     │
│  │  - Templates                                     │     │
│  │  - Campaigns                                     │     │
│  └──────────────────────┬─────────────────────────┘     │
│                         │                               │
│  ┌──────────────────────┴─────────────────────────┐     │
│  │              Database Layer                    │     │
│  │  - SQLite (Local) / PostgreSQL (Cloud)         │     │
│  │  - Redis (Cache)                               │     │
│  └───────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 Modello Dati

### Entità Principali

```sql
-- Links
links (
    id: UUID (PK)
    original_url: TEXT
    short_code: TEXT (UNIQUE)
    branded_domain: TEXT
    title: TEXT
    description: TEXT
    tags: JSON
    created_at: TIMESTAMP
    updated_at: TIMESTAMP
    expires_at: TIMESTAMP (nullable)
    is_active: BOOLEAN
    click_count: INTEGER
    user_id: UUID (FK)
)

-- Analytics
analytics (
    id: UUID (PK)
    link_id: UUID (FK)
    timestamp: TIMESTAMP
    ip_address: TEXT
    user_agent: TEXT
    referrer: TEXT
    country: TEXT
    device: TEXT
    browser: TEXT
    os: TEXT
)

-- Templates
templates (
    id: UUID (PK)
    name: TEXT
    slug: TEXT
    content: JSON
    created_at: TIMESTAMP
)

-- Campaigns
campaigns (
    id: UUID (PK)
    name: TEXT
    description: TEXT
    links: JSON (array of link_ids)
    start_date: DATE
    end_date: DATE
    status: ENUM
)

-- Users
users (
    id: UUID (PK)
    email: TEXT (UNIQUE)
    password_hash: TEXT
    api_key: TEXT (UNIQUE)
    plan: ENUM (free/pro/enterprise)
    created_at: TIMESTAMP
)
```

---

## 🚀 Funzionalità Core

### 1. Gestione Link

| Feature | Descrizione |
|---------|-------------|
| URL Shortening | Genera short URL personalizzati |
| Custom Branded | Usa domini personalizzati (es. go.miosito.com) |
| UTM Builder | Genera URL con parametri UTM automatici |
| Bulk Import | Importa centinaia di URL da CSV/Excel |
| QR Code | Genera QR code per ogni link |
| Expiration | Imposta data scadenza link |
| Password Protection | Proteggi link con password |
| Geo Targeting | Reindirizza in base alla posizione |

### 2. Analytics Dashboard

- **Click in tempo reale** con WebSocket
- **Geolocalizzazione** dettagliata
- **Dispositivo/Browser/OS** breakdown
- **Trend temporali** (giornaliero/settimanale/mensile)
- **A/B testing** tra link
- **Funnel visualization**

### 3. Automazione Bulldozer

Sistema di automazione GUI per:
- Operazioni bulk (crea/aggiorna/elimina centinaia di link)
- Scheduling automatico
- Integrazione con browser ( Selenium/Playwright)
- Macro recorder per azioni ripetitive
- API chaining per workflow complessi

### 4. Template System

Template predefiniti per:
- Social media posts
- Email campaigns
- SMS marketing
- Landing pages
- Affiliate links

---

## 🖥️ Interfacce Utente

### CLI (Command Line Interface)

```bash
# Gestione link
morelinks create --url "https://example.com" --title "Example"
morelinks list --filter "tag=marketing"
morelinks update --id <uuid> --title "New Title"
morelinks delete --id <uuid>

# Bulk operations
morelinks bulk import --file links.csv
morelinks bulk export --format csv --date-range "2024-01-01:2024-12-31"

# Analytics
morelinks stats --link <short_code>
morelinks analytics --dashboard

# Bulldozer
morelinks bulldozer run --script automate.py
morelinks bulldozer record
morelinks bulldozer schedule --cron "0 9 * * *"
```

### GUI Windows (PyQt6)

- Main window con sidebar navigation
- Dashboard analytics interattiva con grafici
- Link manager con drag-drop
- QR code preview
- Bulk editor
- Settings panel

### GUI Mac (BeeWare/Toga)

- Design nativo macOS
- Menu bar integration
- System notifications
- Shortcuts globali

### Android App (BeeWare)

- UI nativa Android Material Design
- Widget per home screen
- NFC tag writing
- Share intent receiver

---

## 🔌 API REST

### Endpoints

```
Authentication:
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
GET    /api/v1/auth/me

Links:
GET    /api/v1/links
POST   /api/v1/links
GET    /api/v1/links/{id}
PUT    /api/v1/links/{id}
DELETE /api/v1/links/{id}
POST   /api/v1/links/bulk

Analytics:
GET    /api/v1/analytics/{link_id}
GET    /api/v1/analytics/overview
GET    /api/v1/analytics/realtime

Templates:
GET    /api/v1/templates
POST   /api/v1/templates
GET    /api/v1/templates/{id}
PUT    /api/v1/templates/{id}

Campaigns:
GET    /api/v1/campaigns
POST   /api/v1/campaigns
GET    /api/v1/campaigns/{id}
PUT    /api/v1/campaigns/{id}
POST   /api/v1/campaigns/{id}/launch

QR Codes:
GET    /api/v1/qr/{link_id}
POST   /api/v1/qr/generate
```

---

## 🛠️ Sistema Bulldozer

### Concept
Automazione GUI che simula interazioni utente per operazioni bulk e testing.

### Features

1. **Macro Recorder**
   - Registra azioni GUI
   - Genera script Python автоматически
   - Playback con velocità configurabile

2. **Bulk Operations Engine**
   - Processa migliaia di link in parallelo
   - Rate limiting configurabile
   - Retry logic con backoff esponenziale

3. **Browser Automation**
   - Selenium WebDriver integration
   - Playwright support
   - Headless mode

4. **Scheduling**
   - Cron expressions
   - Event-based triggers
   - Queue system

### Esempio Script Bulldozer

```python
from morelinks.bulldozer import Task, Pipeline

pipeline = Pipeline(name="Create 1000 Links")

# Step 1: Read CSV
pipeline.add_step(
    Task("read_csv", 
         source="leads.csv",
         columns=["name", "url", "tag"])
)

# Step 2: Transform
pipeline.add_step(
    Task("transform",
         mapper=lambda row: {
             "original_url": row["url"],
             "title": row["name"],
             "tags": [row["tag"]]
         })
)

# Step 3: Create Links
pipeline.add_step(
    Task("create_links",
         parallel=10,
         rate_limit=100)  # 100 links/minute
)

# Step 4: Generate QR
pipeline.add_step(
    Task("generate_qr",
         output_dir="qrcodes/")
)

# Step 5: Export Report
pipeline.add_step(
    Task("export",
         format="csv",
         destination="report.csv")
)

# Execute
pipeline.run()
```

---

## 📱 Roadmap Sviluppo

### Fase 1: Core (Settimana 1-2)
- [x] SPEC.md
- [ ] Backend FastAPI con database
- [ ] CLI base con Click
- [ ] CRUD link completo

### Fase 2: Analytics (Settimana 3-4)
- [ ] Dashboard analytics
- [ ] Tracking click
- [ ] Grafici e visualizzazioni
- [ ] Export CSV/PDF

### Fase 3: Automazione (Settimana 5-6)
- [ ] Sistema Bulldozer
- [ ] Bulk operations
- [ ] Macro recorder
- [ ] Scheduling

### Fase 4: GUI Windows (Settimana 7-8)
- [ ] PyQt6 interface
- [ ] Native look
- [ ] System tray
- [ ] Notifications

### Fase 5: Mac & Android (Settimana 9-10)
- [ ] BeeWare setup
- [ ] macOS app
- [ ] Android app
- [ ] Widgets

### Fase 6: Enterprise (Settimana 11-12)
- [ ] Multi-tenant
- [ ] Team management
- [ ] SSO/SAML
- [ ] White-label

---

## 📦 Packaging

### Windows
- PyInstaller per .exe
- Inno Setup per installer
- MSIX per Microsoft Store

### Mac
- Briefcase per .app
- DMG distribution
- Homebrew formula

### Android
- Buildozer per APK
- Google Play publish
- F-Droid alternative

---

## 🔒 Sicurezza

- OAuth 2.0 / JWT authentication
- Rate limiting per API
- Input sanitization
- SQL injection prevention
- XSS protection
- Audit logging
- Data encryption at rest

---

## 📄 Licenza

MIT License - vedi LICENSE file

---

**Creato:** 2026-06-16  
**Versione:** 0.1.0  
**Autore:** Fabio (Schumynet)
