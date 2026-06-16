# 📜 Guida Normative Italiane

## 1. Database Normative

MoreLinks include un **database completo** di normative italiane per le imprese.

## 2. Utilizzo Base

```python
from morelinks import NormativeKnowledge

nk = NormativeKnowledge()

# Cerca normativa
results = nk.search("privacy")
for r in results:
    print(f"📜 {r.title}")
    print(f"   {r.category}")

# Dettagli completa
norm = nk.get("gdpr")
print(f"""
Normativa: {norm.title}
Categoria: {norm.category}
Descrizione: {norm.description}

Obblighi:
{chr(10).join(f"• {o}" for o in norm.obligations)}

Sanzioni: {norm.penalties}
""")
```

## 3. Lista Normative

### 3.1 Privacy

| Codice | Nome | Obblighi Principali |
|--------|------|---------------------|
| GDPR | Reg. UE 679/2016 | Protezione dati, DPO, Notifiche |
| COD_PRIVACY | DLgs 196/2003 | Codice Privacy Italiano |

### 3.2 Responsabilità

| Codice | Nome | Obblighi Principali |
|--------|------|---------------------|
| 231_2001 | DLgs 231/2001 | Modello 231, OdV, Whistleblowing |

### 3.3 Lavoro

| Codice | Nome | Obblighi Principali |
|--------|------|---------------------|
| 81_2008 | DLgs 81/2008 | Sicurezza, DVR, RSPP |
| STATUTO | L. 300/1970 | Statuto Lavoratori |

### 3.4 Contabilità

| Codice | Nome | Obblighi Principali |
|--------|------|---------------------|
| 2423_CC | Art. 2423 CC | Bilancio, Principi OIC |
| TUIR | DPR 917/1986 | Imposte redditi |

### 3.5 Fatturazione

| Codice | Nome | Obblighi Principali |
|--------|------|---------------------|
| FE | DLgs 127/2015 | Fattura elettronica SDI |

### 3.6 Antiriciclaggio

| Codice | Nome | Obblighi Principali |
|--------|------|---------------------|
| AR | DLgs 231/2007 | KYC, SOS, Conservazione 10 anni |

## 4. Esempio GDPR

```python
norm = nk.get("gdpr")

print(f"""
══════════════════════════════════════════
📜 {norm.title}
══════════════════════════════════════════

📋 Descrizione:
{norm.description}

⚖️ OBBLIGHI:
""")

for i, obbligo in enumerate(norm.obligations, 1):
    print(f"   {i}. {obbligo}")

print(f"""
⚠️ SANZIONI:
{norm.penalties}

📅 AGGIORNAMENTO:
{norm.last_updated}
""")
```

## 5. Obblighi per Dimensione

```python
# Micro impresa (< 10 dipendenti)
micro = nk.get_for_size("micro", "gdpr")

# Piccola media (≥ 10 dipendenti)
pmi = nk.get_for_size("pmi", "gdpr")

# Grande (> 250 dipendenti)
grande = nk.get_for_size("grande", "gdpr")
```

## 6. Checklist Compliance

```python
# Genera checklist per compliance
checklist = nk.generate_checklist("231_2001")

print("CHECKLIST DLgs 231/2001:")
for item in checklist:
    status = "✅" if item.compliant else "⬜"
    print(f"   {status} {item.description}")
```

---

*Normative Italiane - MoreLinks*
