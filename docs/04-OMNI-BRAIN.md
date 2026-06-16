# 🧠 Guida Omni Brain

## 1. Cos'è Omni Brain?

**Omni Brain** è il cervello AI centrale di MoreLinks. È il sistema che:

- 🤖 Gestisce le conversazioni con AI
- 🧠 Mantiene memoria permanente
- 🔧 Esegue azioni (Python, Bash, API)
- 📚 Ha accesso a Book2Skills
- 📜 Conosce le normative italiane

## 2. Architettura

```
┌──────────────────────────────────────────────────────────────┐
│                       OMNI BRAIN                             │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐                                            │
│  │   Chat      │◄──── User Message                          │
│  │   Input     │                                            │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────┐                                            │
│  │  Intent     │ ◄─── Parse Message                         │
│  │  Detection  │                                            │
│  └──────┬──────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                     │    │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐           │    │
│  │  │ Memory  │  │  Norms  │  │ Tasks   │           │    │
│  │  │ System  │  │ Search  │  │ Manager │           │    │
│  │  └─────────┘  └─────────┘  └─────────┘           │    │
│  │                                                     │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        │                                     │
│                        ▼                                     │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                                                     │    │
│  │              OpenRouter API                          │    │
│  │         (Nemotron / Nex-N2-Pro)                     │    │
│  │                                                     │    │
│  └─────────────────────┬───────────────────────────────┘    │
│                        │                                     │
│                        ▼                                     │
│                 AI Response                                  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

## 3. Configurazione

### 3.1 Modelli Disponibili (GRATIS)

```python
# src/morelinks/config.py

FREE_MODELS = {
    "nemotron_safety": "nvidia/nemotron-3-5-content-safety:free",
    "nemotron_ultra": "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nex_n2_pro": "nex-agi/nex-n2-pro:free"
}

# Modello default
DEFAULT_MODEL = "nvidia/nemotron-3-5-content-safety:free"
```

### 3.2 Inizializzazione

```python
from morelinks.ai.omni_brain import OmniBrain

# Configurazione base
brain = OmniBrain(
    api_key="sk-or-v1-your-key",
    model="nvidia/nemotron-3-5-content-safety:free"
)

# Con GitHub sync
brain = OmniBrain(
    api_key="sk-or-v1-your-key",
    github_token="ghp_your_token",
    github_repo="username/morelinks-memory"
)
```

## 4. Utilizzo Base

### 4.1 Chat Semplice

```python
# Chat sincrono
response = brain.chat_sync("Ciao! Mi chiamo Marco")
print(response['response'])

# Chat asincrono
import asyncio

async def chat():
    result = await brain.chat("Ciao!")
    print(result['response'])

asyncio.run(chat())
```

### 4.2 Risposta Completa

```python
result = brain.chat_sync("Ciao!")

# Risposta
print(result['response'])

# Info
print(f"Agente: {result['agent']}")
print(f"Modello: {result['model']}")
print(f"Token usati: {result['tokens_used']}")
print(f"Azioni eseguite: {result['actions_executed']}")
```

## 5. Sistema Agenti

### 5.1 Agenti Disponibili

```python
# Lista agenti
agents = brain.get_agents()

for agent in agents:
    print(f"{agent.id}: {agent.name}")
    print(f"  Ruolo: {agent.role}")
    print(f"  Capabilities: {', '.join(agent.capabilities)}")
```

| Agente | ID | Ruolo |
|--------|-----|-------|
| Omni | `omni` | Assistente generale |
| AdminBot | `admin` | Amministrazione e normative |
| CodeBot | `coder` | Sviluppo Python |
| MarketingBot | `marketer` | Marketing digitale |
| ResearchBot | `researcher` | Ricerca e libri |

### 5.2 Usare Agente Specifico

```python
# Chat con agente specifico
result = brain.chat_sync(
    message="Come funziona il GDPR?",
    agent_id="admin"  # AdminBot
)
```

## 6. Sistema Azioni

### 6.1 Azioni Predefinite

```python
# Azioni disponibili
actions = brain.actions.keys()
print(list(actions))

# Output:
# ['create_link', 'list_links', 'get_stats', 
#  'remember', 'recall', 'search_norms', 
#  'search_books', 'create_task']
```

### 6.2 Eseguire Azioni

```python
import asyncio

async def demo_actions():
    # Lista link
    result = await brain.execute_action("list_links")
    print(result)
    
    # Crea task
    result = await brain.execute_action("create_task", {
        "title": "Report mensile",
        "priority": "high"
    })
    print(result)

asyncio.run(demo_actions())
```

### 6.3 Azioni con Approvazione

```python
# Azioni che richiedono approvazione
result = await brain.execute_action(
    "execute_python",
    {"code": "print('Hello')"},
    approved=False  # Richiede conferma
)

# Output:
# {'success': False, 'error': 'Action requires approval', 
#  'requires_approval': True}
```

## 7. Memoria

### 7.1 Ricordare

```python
# Ricorda manualmente
memory_id = brain.remember(
    content="La mia azienda si chiama TestCorp",
    category="company",
    importance=0.8
)
print(f"Memory ID: {memory_id}")
```

### 7.2 Ricordare/Recall

```python
# Cerca memorie
memories = brain.recall("azienda")
for m in memories:
    print(f"{m['content']} (importance: {m['importance']})")
```

### 7.3 Auto-Learning

```python
# Omni Brain impara automaticamente da conversazioni
brain.chat_sync("Mi chiamo Giovanni")
brain.chat_sync("La mia azienda è WebDev")
brain.chat_sync("Il mio email è giovanni@webdev.com")

# Le info vengono salvate automaticamente in memoria
```

## 8. GitHub Sync

### 8.1 Configurazione

```python
brain = OmniBrain(
    github_token="ghp_your_token",
    github_repo="username/morelinks-memory"
)
```

### 8.2 Sincronizzazione

```python
# Sync locale → GitHub
brain._sync_memory_to_github(memory_id, content, category)

# Sync GitHub → locale
brain.sync_from_github()
```

## 9. Statistiche

```python
# Statistiche Omni Brain
stats = brain.get_stats()

print(f"""
🧠 Omni Brain Stats:
- Modello: {stats['model']}
- Agenti: {stats['agents']}
- Azioni: {stats['actions']}
- Memorie: {stats['total_memories']}
- Conversazioni: {stats['total_conversations']}
- Azioni riuscite: {stats['successful_actions']}
- Skills: {stats['total_skills']}
- GitHub Sync: {'✓' if stats['github_sync'] else '✗'}
""")
```

## 10. Skills

### 10.1 Learn Skill

```python
# Impara una nuova skill
skill_id = brain.learn_skill(
    name="Send Email",
    description="Invia email con Python",
    code="""
import smtplib
def send_email(to, subject, body):
    # Implementation
    pass
""",
    category="communication"
)
```

### 10.2 Get Skills

```python
# Tutte le skills
skills = brain.get_skills()

# Skills per categoria
skills = brain.get_skills(category="communication")
```

## 11. Integrazione Book2Skills

```python
# Cerca libri
result = brain.execute_action("search_books", {
    "query": "productivity"
})
print(result)

# Output:
# {'success': True, 'books': [...]}
```

## 12. Esempio Completo

```python
from morelinks.ai.omni_brain import create_omni_brain

def main():
    # Crea Omni Brain
    brain = create_omni_brain(
        api_key="sk-or-v1-xxx",
        github_token="ghp-xxx"
    )
    
    # Mostra stats
    stats = brain.get_stats()
    print(f"🧠 Omni Brain ready!")
    print(f"   Model: {stats['model']}")
    
    # Conversazione
    print("\n💬 Chat Demo:")
    
    result = brain.chat_sync("Ciao! Mi chiamo Luca")
    print(f"   Tu: Ciao! Mi chiamo Luca")
    print(f"   AI: {result['response'][:100]}...")
    
    result = brain.chat_sync("Come mi chiamo?")
    print(f"   Tu: Come mi chiamo?")
    print(f"   AI: {result['response']}")
    
    # Azione
    print("\n🔧 Action Demo:")
    import asyncio
    result = asyncio.run(brain.execute_action("get_stats"))
    print(f"   Result: {result}")
    
    # Cleanup
    brain.close()

if __name__ == "__main__":
    main()
```

## 13. Troubleshooting

### 13.1 API Error

```python
# Se l'API dà errore
result = await brain.chat("Ciao")

if "API Error" in result['response']:
    print("❌ API non raggiungibile")
    print("Verifica API key e connessione internet")
```

### 13.2 Rate Limit

```python
# Se superi rate limit
import time
time.sleep(60)  # Aspetta 1 minuto
```

---

*Omni Brain - MoreLinks*
