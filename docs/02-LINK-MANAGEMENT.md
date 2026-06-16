# 🔗 Guida Link Management

## 1. Introduzione

Il modulo **Link Management** di MoreLinks permette di:
- Creare short URL personalizzati
- Generare QR Code automatici
- Tracciare click e analytics
- Gestire campaign

## 2. Utilizzo Base

### 2.1 Creare un Link

```python
from morelinks import MoreLinks

db = MoreLinks()

# Link semplice
link = db.create_link(
    original_url="https://example.com/pagina-lunga"
)
print(f"Short URL: {link.short_url}")
# Output: Short URL: https://ml.app/abc123
```

### 2.2 Link con Opzioni

```python
# Link con titolo e tags
link = db.create_link(
    original_url="https://example.com",
    title="Sito Principale",
    tags=["home", "principale"]
)

# Link personalizzato
link = db.create_link(
    original_url="https://example.com",
    custom_code="miosito"  # Diventa: https://ml.app/miosito
)
```

### 2.3 Lista Link

```python
# Tutti i link
links = db.list_links()

# Link di uno specifico utente
links = db.list_links(user_id="fabio")

# Link attivi/inattivi
links = db.list_links(only_active=True)
```

## 3. QR Code

### 3.1 Generazione Base

```python
import qrcode

url = "https://ml.app/abc123"

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)
qr.add_data(url)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr_code.png")
```

### 3.2 QR con Logo

```python
from PIL import Image

def generate_qr_with_logo(url, logo_path):
    qr = qrcode.QRCode(version=3)
    qr.add_data(url)
    qr.make()
    
    img = qr.make_image().convert('RGB')
    
    # Aggiungi logo
    logo = Image.open(logo_path)
    logo = logo.resize((60, 60))
    
    pos = ((img.size[0] - logo.size[0]) // 2,
           (img.size[1] - logo.size[1]) // 2)
    
    img.paste(logo, pos)
    return img
```

## 4. Analytics

### 4.1 Statistiche Link

```python
# Click totali
link = db.get_link("abc123")
print(f"Click: {link.click_count}")

# Analytics dettagliate
stats = db.get_link_analytics("abc123")
print(f"Paese: {stats.country}")
print(f"Dispositivo: {stats.device_type}")
```

### 4.2 Analytics Aggregate

```python
summary = db.get_analytics_summary()

print(f"""
📊 Riepilogo Analytics:
- Link Totali: {summary.total_links}
- Click Totali: {summary.total_clicks}
- Visitatori Unici: {summary.unique_visitors}
- Click Oggi: {summary.clicks_today}
""")
```

## 5. API REST (Web)

### 5.1 Endpoint

```
POST /api/links          # Crea link
GET  /api/links          # Lista link
GET  /api/links/<code>   # Dettaglio link
PUT  /api/links/<code>   # Aggiorna link
DEL  /api/links/<code>   # Elimina link
GET  /api/links/<code>/qr   # QR code
GET  /api/links/<code>/stats # Statistiche
```

### 5.2 Esempio cURL

```bash
# Crea link
curl -X POST https://api.morelinks.app/links \
  -H "Content-Type: application/json" \
  -d '{"original_url": "https://example.com"}'

# Risposta:
# {"short_url": "https://ml.app/xyz789", "code": "xyz789"}
```

---

## 6. Database Schema

```sql
-- Tabella links
CREATE TABLE links (
    id INTEGER PRIMARY KEY,
    short_code TEXT UNIQUE,
    original_url TEXT NOT NULL,
    title TEXT,
    click_count INTEGER DEFAULT 0,
    created_at TIMESTAMP,
    is_active BOOLEAN DEFAULT 1,
    user_id TEXT DEFAULT 'default'
);

-- Tabella clicks
CREATE TABLE clicks (
    id INTEGER PRIMARY KEY,
    link_id INTEGER REFERENCES links(id),
    ip_address TEXT,
    user_agent TEXT,
    referrer TEXT,
    country TEXT,
    device_type TEXT,
    clicked_at TIMESTAMP
);
```

---

## 7. Comandi CLI

```bash
# CLI di MoreLinks

# Crea link
> link nuova https://example.com

# Lista link
> link lista

# Statistiche
> link stats abc123

# QR code
> qr abc123

# Elimina
> link elimina abc123
```

---

*Link Management - MoreLinks*
