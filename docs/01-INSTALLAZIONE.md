# 📦 Guida Installazione MoreLinks

## 1. Requisiti

### 1.1 Sistema Operativo
- **Windows**: 10 o superiore
- **macOS**: 11 (Big Sur) o superiore
- **Linux**: Ubuntu 20.04+, Debian 10+, Fedora 34+

### 1.2 Python
- **Versione**: Python 3.11 o superiore
- **Download**: https://www.python.org/downloads/

```bash
# Verifica installazione
python --version
# Output atteso: Python 3.11.x
```

### 1.3 Strumenti Necessari
- Git (per cloning)
- pip (package manager Python)

---

## 2. Installazione Passo Passo

### 2.1 Clona Repository

```bash
# Apri terminale
cd ~/progetti

# Clona MoreLinks
git clone https://github.com/Schumynet/MoreLinks.git

# Entra nella cartella
cd MoreLinks
```

### 2.2 Crea Virtual Environment

```bash
# Linux/Mac
python3 -m venv venv

# Attiva virtual environment
# Linux/Mac:
source venv/bin/activate

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows CMD:
venv\Scripts\activate.bat
```

### 2.3 Installa Dipendenze

```bash
# Installa tutte le dipendenze
pip install -r requirements.txt

# Oppure manualmente:
pip install aiohttp openai python-dotenv qrcode
```

### 2.4 File requirements.txt

```txt
# Core
aiohttp>=3.9.0
openai>=1.0.0
python-dotenv>=1.0.0

# Database
# sqlite3 è incluso in Python (built-in)

# QR Code
qrcode>=7.4.0
Pillow>=10.0.0

# GUI (opzionali - scegli in base alla piattaforma)

# Windows GUI
PyQt6>=6.6.0

# Mac/Linux GUI (già incluso in Python)
# tkinter è built-in

# Web App
streamlit>=1.30.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.21.0
```

---

## 3. Configurazione

### 3.1 Crea File .env

Nella cartella principale di MoreLinks, crea un file `.env`:

```env
# ============================================
# MORE LINKS - CONFIGURAZIONE
# ============================================

# API Key OpenRouter (per AI - OBBLIGATORIA)
# Ottienila gratis su: https://openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-v1-la-tua-api-key-qui

# GitHub Token (opzionale - per sync memoria cloud)
# Genera su: https://github.com/settings/tokens
GITHUB_TOKEN=ghp_il-tuo-token-qui

# Modalità sviluppo (cambia in False per produzione)
DEBUG=True

# Lingua predefinita
LANGUAGE=it
```

### 3.2 Come Ottenere API Key OpenRouter

1. Vai su https://openrouter.ai/
2. Crea account (gratuito)
3. Vai su "Keys"
4. Clicca "Create Key"
5. Copia la chiave (inizia con `sk-or-v1-`)

**Modelli gratuiti disponibili:**
| Modello | Provider | Costo |
|---------|----------|-------|
| nemotron-3-ultra-550b | NVIDIA | FREE |
| nex-n2-pro | Nex AGI | FREE |
| nemotron-content-safety | NVIDIA | FREE |

### 3.3 Struttura Configurazione

```python
# src/morelinks/config.py

import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
DEFAULT_MODEL = "nvidia/nemotron-3-5-content-safety:free"

# GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = "Schumynet/morelinks-memory"

# Database
DB_PATH = "morelinks.db"
MEMORY_DB_PATH = "omni_memory.db"

# App
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
LANGUAGE = os.getenv("LANGUAGE", "it")
```

---

## 4. Primo Avvio

### 4.1 Verifica Installazione

```bash
# Entra nella cartella src
cd src

# Test import
python -c "from morelinks import MoreLinks; print('✅ Installazione OK')"
```

### 4.2 Avvia CLI

```bash
# Dalla cartella principale MoreLinks
python cli/app.py
```

Dovresti vedere:
```
╔════════════════════════════════════════════╗
║                                            ║
║   🔗 MORE LINKS - CLI v1.0.0               ║
║                                            ║
║   Piattaforma AI con Memoria Permanente   ║
║                                            ║
╚════════════════════════════════════════════╝

Comandi disponibili:
- link nuova <url>   : Crea nuovo short link
- link lista          : Mostra tutti i link
- chat <messaggio>    : Parla con AI
- norme               : Mostra normative
- help                : Questo messaggio
- exit                : Esci

>
```

### 4.3 Avvia GUI Windows

```bash
# Assicurati di aver installato PyQt6
pip install PyQt6

# Avvia
python gui/windows/app.py
```

### 4.4 Avvia Web App

```bash
# Installa Streamlit
pip install streamlit

# Avvia
streamlit run gui/web/app.py
```

---

## 5. Risoluzione Problemi

### 5.1 Errore "Module not found"

```bash
# Reinstalla dipendenze
pip install --upgrade -r requirements.txt
```

### 5.2 Errore "No module named 'PyQt6'"

```bash
# Windows/Mac/Linux
pip install PyQt6

# Su Linux potrebbe servire:
sudo apt-get install python3-pyqt6
```

### 5.3 Errore API Key

```
❌ Errore: OPENROUTER_API_KEY non trovata
```

**Soluzione:** Verifica che il file `.env` sia nella cartella corretta e contenga la chiave.

### 5.4 Errore permessi database

```bash
# Su Linux/Mac
chmod 755 .
chmod 644 *.db 2>/dev/null || true
```

---

## 6. Aggiornamento

### 6.1 Pull Ultime Modifiche

```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### 6.2 Backup Database

```bash
# Backup prima di aggiornare
cp morelinks.db morelinks.db.backup
cp omni_memory.db omni_memory.db.backup
```

---

## 7. Disinstallazione

```bash
# Disattiva virtual environment
deactivate

# Rimuovi cartella
cd ..
rm -rf MoreLinks

# Oppure solo virtual environment
rm -rf MoreLinks/venv
```

---

## 8. Installazione Docker (Avanzato)

### 8.1 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copia requirements
COPY requirements.txt .

# Installa dipendenze
RUN pip install --no-cache-dir -r requirements.txt

# Copia codice
COPY . .

# Espori porta Streamlit
EXPOSE 8501

# Avvia web app
CMD ["streamlit", "run", "gui/web/app.py", "--server.address", "0.0.0.0"]
```

### 8.2 Build e Run

```bash
# Build immagine
docker build -t morelinks .

# Run container
docker run -p 8501:8501 \
  -e OPENROUTER_API_KEY=sk-or-v1-xxx \
  morelinks
```

---

## 9. Checklist Installazione

- [ ] Python 3.11+ installato
- [ ] Git installato
- [ ] Repository clonato
- [ ] Virtual environment creato
- [ ] Dipendenze installate
- [ ] File `.env` creato
- [ ] API Key OpenRouter ottenuta
- [ ] Test avvio CLI riuscito
- [ ] Test GUI funzionante

---

*Guida installazione MoreLinks v1.0*
