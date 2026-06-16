# 📚 Guida Book2Skills

## 1. Introduzione

**Book2Skills** è una library che trasforma **5000+ libri** in competenze azionabili.

## 2. Utilizzo Base

```python
from book2skills import Book2SkillsLibrary

# Crea istanza
lib = Book2SkillsLibrary()

# Cerca libri
results = lib.search_books("productivity")
for book in results:
    print(f"📖 {book.title}")
    print(f"   Autore: {book.author}")
    print(f"   Skills: {', '.join(book.skills[:3])}")

lib.close()
```

## 3. Categorie

```python
# Categorie disponibili
categories = lib.get_categories()
print(categories)
# Output:
# - Business & Management
# - Technology & Programming
# - Psychology & Self-Help
# - Sales & Negotiation
# - Entrepreneurship
# - Marketing & Advertising
# - Creativity & Design
# - Habits & Mindset
# - Leadership & Management
# - Productivity & Time Management
# - ...

# Filtra per categoria
lib.set_category("Business & Management")
books = lib.get_books()
```

## 4. Schema Dati

```python
class Book:
    id: int
    title: str
    author: str
    category: str
    year: int
    rating: float
    summary: str
    skills: list[str]         # Competenze
    key_takeaways: list[str] # Punti chiave
    chapters: list[str]       # Capitoli
    related_books: list[int]  # Libri correlati
```

## 5. Suggerimenti

```python
# Suggerimenti basati su interessi
suggestions = lib.get_suggestions(["marketing", "sales", "productivity"])

for book in suggestions:
    print(f"📖 {book.title}")
    print(f"   Match: {book.match_score}%")
```

## 6. Esempio Output

```
📚 LIBRO: Atomic Habits
   Autore: James Clear
   Categoria: Habits & Mindset
   Anno: 2018
   Rating: 4.8/5

🎯 SKILLS ACQUISIBILI:
   • Habit Formation
   • Identity-Based Habits
   • Habit Stacking
   • Compounding Habits
   • Environment Design

📌 KEY TAKEAWAYS:
   1. Piccoli miglioramenti = grandi risultati
   2. Il 2% migliora ogni giorno = 37x meglio in un anno
   3. Cambia il tuo ambiente
   4. Abitudini = Riuscire + Ripetere
   5. Non focalizzarti sugli obiettivi, sui sistemi

📑 CAPITOLI:
   1. I fondamenti
   2. La prima legge: Evidente
   3. La seconda legge: Attraente
   4. La terza legge: Facile
   5. La quarta legge: Soddisfacente
```

---

*Book2Skills - MoreLinks*
