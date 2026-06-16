# 🤖 Guida Chatbot AI

## 1. Introduzione

Il **Chatbot AI** di MoreLinks è un assistente virtuale con **memoria permanente** che:
- Ricorda TUTTO ciò che dici
- Risponde in italiano
- Ha accesso a normative italiane
- Può eseguire azioni

## 2. Utilizzo Base

### 2.1 Creare Chatbot

```python
from morelinks import MoreLinksChatbot

# Crea istanza
bot = MoreLinksChatbot()
```

### 2.2 Inviare Messaggi

```python
# Chat base
response = bot.process("Ciao!")
print(response.message)
# Output: "Ciao! Sono il tuo assistente AI. Come posso aiutarti?"

# Chat con contesto
response = bot.process("Mi chiamo Marco")
response = bot.process("Come mi chiamo?")
# Output: "Ti chiami Marco!"
```

## 3. Memória Permanente

### 3.1 Come Funziona

```
┌─────────────────────────────────────────────┐
│            SISTEMA MEMORIA                  │
├─────────────────────────────────────────────┤
│                                              │
│  Tu dici: "La mia azienda è TestCorp"      │
│                    │                         │
│                    ▼                         │
│         ┌──────────────────┐                │
│         │   Parser & Save  │                │
│         └────────┬─────────┘                │
│                  │                          │
│                  ▼                          │
│         ┌──────────────────┐                │
│         │    SQLite DB     │                │
│         │  omni_memory.db  │                │
│         └────────┬─────────┘                │
│                  │                          │
│                  ▼                          │
│         ┌──────────────────┐                │
│         │   GitHub Sync    │ (opzionale)    │
│         └──────────────────┘                │
│                                              │
│  Tu chiedi: "Come si chiama la mia azienda?"│
│                    │                         │
│                    ▼                         │
│         ┌──────────────────┐                │
│         │   Memory Recall  │                │
│         └────────┬─────────┘                │
│                  │                          │
│                  ▼                          │
│         Output: "La tua azienda è TestCorp"│
│                                              │
└─────────────────────────────────────────────┘
```

### 3.2 Ricordare Informazioni

```python
# Ricorda automaticamente
bot.process("Mi chiamo Giovanni")
bot.process("La mia azienda si chiama TechSrl")
bot.process("Il mio email è giovanni@techsrl.com")

# Recupera
response = bot.process("Come mi chiamo?")
# Output: "Ti chiami Giovanni!"

response = bot.process("Email?")
# Output: "Il tuo email è giovanni@techsrl.com"
```

### 3.3 Ricerca Memoria

```python
from morelinks import PersistentMemory

memory = PersistentMemory()

# Cerca per categoria
results = memory.recall(category="personal")
for r in results:
    print(f"{r.content} (importanza: {r.importance})")

# Cerca per query
results = memory.recall(query="azienda")
```

## 4. Normative Italiane

### 4.1 Accedere alle Normative

```python
# Cerca normative
response = bot.process("Cosa dice il GDPR?")
# Output: "Il GDPR (Reg. UE 679/2016) stabilisce che..."

# Mostra obblighi
response = bot.process("Quali sono gli obblighi del DLgs 231?")
```

### 4.2 Database Normative

```python
from morelinks import NormativeKnowledge

nk = NormativeKnowledge()

# Ricerca
results = nk.search("privacy")
for r in results:
    print(f"📜 {r['title']}")
    print(f"   {r['description']}")

# Dettagli
norm = nk.get("gdpr")
print(f"""
Normativa: {norm.title}
Obblighi:
{chr(10).join(f"  • {o}" for o in norm.obligations)}
Sanzioni: {norm.penalties}
""")
```

## 5. Gestione Task

### 5.1 Creare Task

```python
# Tramite chatbot
bot.process("Crea un task: Preparare report mensile")
bot.process("Crea task: Chiamare cliente, priorità alta")

# Tramite API
memory = PersistentMemory()
task_id = memory.create_task(
    user_id="fabio",
    title="Report mensile",
    priority="high"
)
```

### 5.2 Lista Task

```python
# Mostra task
response = bot.process("Mostra i miei task")
# Output: Lista task pendenti

# API
tasks = memory.get_tasks("fabio")
for task in tasks:
    print(f"[{task.status}] {task.title}")
```

## 6. Comandi Chatbot

### 6.1 Comandi Base

| Comando | Descrizione | Esempio |
|---------|-------------|---------|
| `ciao` | Saluto | "Ciao!" |
| `aiuto` | Mostra help | "aiuto" |
| `crea link` | Crea short link | "crea link https://..." |
| `memoria` | Info memoria | "quante cose ricordi?" |
| `normativa` | Cerca norme | "cerca GDPR" |
| `task` | Gestione task | "mostra task" |

### 6.2 Esempi Conversazione

```
👤: Ciao!
🤖: Ciao! Sono Omni, il tuo assistente AI con memoria permanente.
    Ricordo TUTTO ciò che mi dici. Come posso aiutarti?

👤: Mi chiamo Luca e ho un'azienda chiamata WebDesign
🤖: Piacere Luca! Ho salvato che la tua azienda è WebDesign.

👤: Ricordi come mi chiamo?
🤖: Ti chiami Luca!

👤: E come si chiama la mia azienda?
🤖: La tua azienda si chiama WebDesign!

👤: Quali sono gli obblighi del GDPR?
🤖: Il GDPR prevede:
    • Protezione dati personali
    • Nomina DPO (se richiesto)
    • Registro trattamenti
    • Notifica violazioni entro 72h
    • Informativa agli interessati
```

## 7. Personalizzazione

### 7.1 Cambiare Agente

```python
# Agente Admin (normative)
bot = MoreLinksChatbot(agent_id="admin")

# Agente Marketing
bot = MoreLinksChatbot(agent_id="marketer")

# Agente Coder
bot = MoreLinksChatbot(agent_id="coder")
```

### 7.2 Configurare Risposte

```python
# Custom prompt
bot = MoreLinksChatbot(
    system_prompt="Sei un assistente amichevole italiano..."
)
```

## 8. API Chatbot

### 8.1 Endpoint

```
POST /api/chat     # Invia messaggio
GET  /api/history  # Cronologia
DEL  /api/history  # Pulisci cronologia
```

### 8.2 Esempio API

```python
import requests

# Invia messaggio
response = requests.post(
    "https://api.morelinks.app/api/chat",
    json={
        "message": "Ciao!",
        "user_id": "fabio",
        "session_id": "session_123"
    }
)

print(response.json())
# {'message': 'Ciao!', 'agent': 'omni', 'memory_saved': False}
```

---

## 9. Risoluzione Problemi

### 9.1 Chatbot non risponde

```python
# Verifica API key
import os
from morelinks.config import OPENROUTER_API_KEY
print(f"API Key: {OPENROUTER_API_KEY[:10]}...")

# Test connessione
import aiohttp
async def test():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://openrouter.ai/api/v1/models") as resp:
            print(await resp.json())

import asyncio
asyncio.run(test())
```

### 9.2 Memoria non funziona

```bash
# Verifica database
ls -la *.db

# Recrea database
rm omni_memory.db
python -c "from morelinks import PersistentMemory; PersistentMemory()"
```

---

## 10. Best Practices

### ✅ Fai

- Usa frasi complete per aiutare il parsing
- Specifica chiaramente informazioni importanti
- Chiedi conferma per azioni importanti

### ❌ Non Fare

- Non dare comandi contraddittori
- Non aspettarti che ricordi conversazioni chiuse
- Non confidare ciecamente nelle risposte (verifica normative)

---

*Chatbot AI - MoreLinks*
