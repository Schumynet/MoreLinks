#!/usr/bin/env python3
"""
MoreLinks - Mac/Linux GUI Application
Built with Tkinter for native experience
Run: python gui/mac/app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Theme colors
COLORS = {
    'bg': '#1a1a2e',
    'bg2': '#16213e',
    'primary': '#4361ee',
    'secondary': '#8b5cf6',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'text': '#eaeaea',
    'muted': '#888888'
}


class MoreLinksApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔗 MoreLinks - Piattaforma AI")
        self.root.geometry("1200x800")
        self.root.configure(bg=COLORS['bg'])
        
        # Data
        self.links = []
        self.files = []
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the UI"""
        # Header
        header = tk.Frame(self.root, bg=COLORS['bg2'], pady=15)
        header.pack(fill='x')
        
        tk.Label(header, text="🔗 MoreLinks", font=('Helvetica', 24, 'bold'), 
                bg=COLORS['bg2'], fg=COLORS['primary']).pack(side='left', padx=20)
        
        tk.Label(header, text="Piattaforma AI con Memoria Permanente", 
                font=('Helvetica', 10), bg=COLORS['bg2'], fg=COLORS['muted']).pack(side='left', padx=10)
        
        # Main container
        main = tk.Frame(self.root, bg=COLORS['bg'])
        main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left sidebar
        sidebar = tk.Frame(main, bg=COLORS['bg2'], width=200)
        sidebar.pack(side='left', fill='y', padx=(0, 20))
        sidebar.pack_propagate(False)
        
        nav_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("🔗 Link", self.show_links),
            ("📤 Upload", self.show_upload),
            ("🤖 Chatbot AI", self.show_chatbot),
            ("📜 Normative", self.show_normative),
            ("📊 Analytics", self.show_analytics),
            ("⚙️ Impostazioni", self.show_settings),
        ]
        
        for i, (text, cmd) in enumerate(nav_items):
            btn = tk.Button(sidebar, text=text, font=('Helvetica', 12), 
                          bg=COLORS['bg2'], fg=COLORS['text'], 
                          activebackground=COLORS['primary'], activeforeground='white',
                          bd=0, anchor='w', padx=20, pady=12, command=cmd)
            btn.pack(fill='x', pady=1)
        
        # Content area
        self.content = tk.Frame(main, bg=COLORS['bg'])
        self.content.pack(side='left', fill='both', expand=True)
        
        self.show_dashboard()
    
    def clear_content(self):
        """Clear content area"""
        for widget in self.content.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Dashboard view"""
        self.clear_content()
        
        # Title
        tk.Label(self.content, text="📊 Dashboard", font=('Helvetica', 24, 'bold'),
                bg=COLORS['bg'], fg=COLORS['primary']).pack(anchor='w', pady=(0, 20))
        
        # Stats cards
        stats_frame = tk.Frame(self.content, bg=COLORS['bg'])
        stats_frame.pack(fill='x', pady=(0, 20))
        
        stats = [
            ("🔗 Link Totali", "0", COLORS['primary']),
            ("👆 Click Totali", "0", COLORS['success']),
            ("📁 File", "0", COLORS['warning']),
            ("🧠 Memoria AI", "42", COLORS['secondary']),
        ]
        
        for text, value, color in stats:
            card = tk.Frame(stats_frame, bg=COLORS['bg2'], padx=30, pady=20)
            card.pack(side='left', padx=10, ipadx=20)
            tk.Label(card, text=text, font=('Helvetica', 10), 
                    bg=COLORS['bg2'], fg=COLORS['muted']).pack()
            tk.Label(card, text=value, font=('Helvetica', 28, 'bold'), 
                    bg=COLORS['bg2'], fg=color).pack()
        
        # Quick actions
        tk.Label(self.content, text="⚡ Azioni Rapide", font=('Helvetica', 16, 'bold'),
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(20, 10))
        
        actions = [
            ("🔗 Nuovo Link", self.show_links),
            ("📤 Carica File", self.show_upload),
            ("🤖 Chat AI", self.show_chatbot),
        ]
        
        for text, cmd in actions:
            btn = tk.Button(self.content, text=text, font=('Helvetica', 12),
                           bg=COLORS['primary'], fg='white', padx=30, pady=10,
                           command=cmd, bd=0)
            btn.pack(anchor='w', pady=5)
    
    def show_links(self):
        """Links management view"""
        self.clear_content()
        
        # Header
        header = tk.Frame(self.content, bg=COLORS['bg'])
        header.pack(fill='x', pady=(0, 20))
        
        tk.Label(header, text="🔗 Gestione Link", font=('Helvetica', 24, 'bold'),
                bg=COLORS['bg'], fg=COLORS['primary']).pack(side='left')
        
        tk.Button(header, text="➕ Nuovo Link", font=('Helvetica', 12),
                bg=COLORS['primary'], fg='white', padx=20, pady=5,
                command=self.add_new_link, bd=0).pack(side='right')
        
        # Links list
        list_frame = tk.Frame(self.content, bg=COLORS['bg2'])
        list_frame.pack(fill='both', expand=True)
        
        # Table header
        headers = ["Codice", "Titolo", "URL", "Click", "Azioni"]
        for i, h in enumerate(headers):
            tk.Label(list_frame, text=h, font=('Helvetica', 10, 'bold'),
                    bg=COLORS['bg2'], fg=COLORS['primary']).grid(row=0, column=i, padx=10, pady=10)
        
        # Sample data
        sample_links = [
            ("gh1234", "GitHub", "https://github.com", "1,247", "📱 QR"),
            ("py9876", "Python", "https://python.org", "892", "📱 QR"),
            ("fa5432", "FastAPI", "https://fastapi.tiangolo.com", "534", "📱 QR"),
        ]
        
        for r, row in enumerate(sample_links, 1):
            for c, val in enumerate(row):
                tk.Label(list_frame, text=val, bg=COLORS['bg2'], fg=COLORS['text']).grid(row=r, column=c, padx=10, pady=5)
    
    def add_new_link(self):
        """Add new link dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Nuovo Link")
        dialog.geometry("400x300")
        dialog.configure(bg=COLORS['bg2'])
        
        tk.Label(dialog, text="🔗 Nuovo Link", font=('Helvetica', 16, 'bold'),
                bg=COLORS['bg2'], fg=COLORS['primary']).pack(pady=20)
        
        tk.Label(dialog, text="URL:", bg=COLORS['bg2'], fg=COLORS['text']).pack(anchor='w', padx=40)
        url_entry = tk.Entry(dialog, width=40)
        url_entry.pack(pady=5, padx=40)
        
        tk.Label(dialog, text="Titolo:", bg=COLORS['bg2'], fg=COLORS['text']).pack(anchor='w', padx=40)
        title_entry = tk.Entry(dialog, width=40)
        title_entry.pack(pady=5, padx=40)
        
        tk.Button(dialog, text="✅ Crea Link", bg=COLORS['success'], fg='white',
                 command=lambda: self.create_link(url_entry.get(), title_entry.get(), dialog),
                 padx=20, pady=10, bd=0).pack(pady=20)
    
    def create_link(self, url, title, dialog):
        """Create new link"""
        if url:
            messagebox.showinfo("Successo", f"✅ Link creato!\n\n🔗 https://ml.app/abc123")
            dialog.destroy()
            self.show_links()
    
    def show_upload(self):
        """Upload files view"""
        self.clear_content()
        
        tk.Label(self.content, text="📤 Upload Manuale", font=('Helvetica', 24, 'bold'),
                bg=COLORS['bg'], fg=COLORS['primary']).pack(anchor='w', pady=(0, 20))
        
        # Upload zone
        upload_zone = tk.Frame(self.content, bg=COLORS['bg2'], height=200)
        upload_zone.pack(fill='x', pady=(0, 20))
        upload_zone.pack_propagate(False)
        
        tk.Label(upload_zone, text="🖱️ Trascina qui i file\n\noppure", font=('Helvetica', 14),
                bg=COLORS['bg2'], fg=COLORS['muted']).pack(expand=True)
        
        tk.Button(self.content, text="📂 Seleziona File...", bg=COLORS['primary'], fg='white',
                 command=self.select_files, padx=30, pady=10, bd=0).pack()
        
        # User folders
        tk.Label(self.content, text="📂 Le Tue Cartelle", font=('Helvetica', 16, 'bold'),
                bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w', pady=(20, 10))
        
        folders = ["👤 Fabio", "👥 Monica", "👥 Richard", "🔄 Condivisi"]
        for folder in folders:
            tk.Button(self.content, text=folder, bg=COLORS['bg2'], fg=COLORS['text'],
                     anchor='w', padx=20, pady=10, bd=0).pack(fill='x', pady=2)
    
    def select_files(self):
        """Select files to upload"""
        files = filedialog.askopenfilenames()
        if files:
            for f in files:
                self.files.append(os.path.basename(f))
            messagebox.showinfo("Upload", f"✅ {len(files)} file caricati!")
    
    def show_chatbot(self):
        """Chatbot AI view"""
        self.clear_content()
        
        tk.Label(self.content, text="🤖 Omni Brain - Chatbot AI", font=('Helvetica', 24, 'bold'),
                bg=COLORS['bg'], fg=COLORS['primary']).pack(anchor='w', pady=(0, 10))
        
        tk.Label(self.content, text="🧠 Memoria Permanente Attiva - Ricordo TUTTO!",
                bg=COLORS['bg'], fg=COLORS['success']).pack(anchor='w', pady=(0, 20))
        
        # Chat display
        chat_frame = tk.Frame(self.content, bg=COLORS['bg2'], height=400)
        chat_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        tk.Label(chat_frame, text="👋 Ciao! Sono Omni, il tuo assistente AI con memoria permanente.\nCome posso aiutarti?",
                bg=COLORS['bg2'], fg=COLORS['secondary'], justify='left').pack(anchor='w', padx=20, pady=20)
        
        # Input
        input_frame = tk.Frame(self.content, bg=COLORS['bg'])
        input_frame.pack(fill='x')
        
        self.chat_entry = tk.Entry(input_frame, font=('Helvetica', 12), bg=COLORS['bg2'], fg=COLORS['text'])
        self.chat_entry.pack(side='left', fill='x', expand=True, ipady=10)
        self.chat_entry.insert(0, "Scrivi un messaggio...")
        
        tk.Button(input_frame, text="📤", bg=COLORS['primary'], fg='white',
                 command=lambda: self.send_chat(), padx=20, bd=0).pack(side='right')
    
    def send_chat(self):
        """Send chat message"""
        msg = self.chat_entry.get()
        if msg and msg != "Scrivi un messaggio...":
            self.chat_entry.delete(0, 'end')
            messagebox.showinfo("AI", f"🤖 Ho ricevuto: {msg}\n\n(Risposta AI simulata)")
    
    def show_normative(self):
        """Normative view"""
        self.clear_content()
        
        tk.Label(self.content, text="📜 Normative Italiane", font=('Helvetica', 24, 'bold'),
                bg=COLORS['bg'], fg=COLORS['primary']).pack(anchor='w', pady=(0, 20))
        
        # Search
        tk.Entry(self.content, width=50, bg=COLORS['bg2'], fg=COLORS['text']).pack(fill='x', pady=(0, 20))
        
        # Categories
        norms = [
            ("🏢 Contabilità", "Codice Civile, Principi OIC"),
            ("🔒 Privacy", "GDPR, Codice Privacy"),
            ("👷 Lavoro", "Statuto, Sicurezza"),
            ("⚖️ Responsabilità", "DLgs 231/2001"),
            ("🔄 Antiriciclaggio", "DLgs 231/2007"),
        ]
        
        for icon, desc in norms:
            frame = tk.Frame(self.content, bg=COLORS['bg2'])
            frame.pack(fill='x', pady=5)
            tk.Label(frame, text=icon, font=('Helvetica', 14), bg=COLORS['bg2']).pack(side='left', padx=15)
            tk.Label(frame, text=desc, bg=COLORS['bg2'], fg=COLORS['text']).pack(side='left')
    
    def show_analytics(self):
        """Analytics view"""
        self.clear_content()
        
        tk.Label(self.content, text="📊 Analytics", font=('Helvetica', 24, 'bold'),
                bg=COLORS['bg'], fg=COLORS['primary']).pack(anchor='w', pady=(0, 20))
        
        tk.Label(self.content, text="📈 Statistiche in sviluppo...",
                bg=COLORS['bg'], fg=COLORS['muted']).pack()
    
    def show_settings(self):
        """Settings view"""
        self.clear_content()
        
        tk.Label(self.content, text="⚙️ Impostazioni", font=('Helvetica', 24, 'bold'),
                bg=COLORS['bg'], fg=COLORS['primary']).pack(anchor='w', pady=(0, 20))
        
        # API Key
        tk.Label(self.content, text="🤖 OpenRouter API Key:", bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w')
        tk.Entry(self.content, width=50, show='*', bg=COLORS['bg2'], fg=COLORS['text']).pack(pady=(5, 20))
        
        tk.Label(self.content, text="🧠 Memoria Permanente:", bg=COLORS['bg'], fg=COLORS['text']).pack(anchor='w')
        tk.Checkbutton(self.content, text="Attivata", bg=COLORS['bg'], fg=COLORS['success'],
                     selectcolor=COLORS['bg2']).pack(anchor='w')


def main():
    root = tk.Tk()
    app = MoreLinksApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
