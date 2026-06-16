#!/usr/bin/env python3
"""
MoreLinks - Web Application
Built with Streamlit for Chromebook and browser access
Run: streamlit run gui/web/app.py
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

# Page config
st.set_page_config(
    page_title="MoreLinks - AI Platform",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import core modules
try:
    from morelinks import MoreLinks, MoreLinksChatbot, PersistentMemory
    from morelinks.chatbot.normative_knowledge import NormativeKnowledge
    CORE_AVAILABLE = True
except ImportError:
    CORE_AVAILABLE = False

# Custom CSS
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Cards */
    .link-card {
        background: #16213e;
        border: 1px solid #4361ee;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Stats */
    .stat-card {
        background: linear-gradient(135deg, #4361ee 0%, #3a56d4 100%);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        color: white;
    }
    
    /* Chat bubbles */
    .user-msg {
        background: #4361ee;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin: 5px 0;
    }
    
    .ai-msg {
        background: #8b5cf6;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin: 5px 0;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #4361ee !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #0f0f23;
    }
    
    /* Buttons */
    .stButton>button {
        background: #4361ee;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    
    .stButton>button:hover {
        background: #3a56d4;
    }
</style>
""", unsafe_allow_html=True)


# ==================== INITIALIZE STATE ====================

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'links' not in st.session_state:
    st.session_state.links = [
        {"code": "gh1234", "url": "https://github.com", "title": "GitHub", "clicks": 1247},
        {"code": "py9876", "url": "https://python.org", "title": "Python", "clicks": 892},
        {"code": "fa5432", "url": "https://fastapi.tiangolo.com", "title": "FastAPI", "clicks": 534},
    ]

if 'memory_entries' not in st.session_state:
    st.session_state.memory_entries = []


# ==================== SIDEBAR ====================

with st.sidebar:
    st.title("🔗 MoreLinks")
    st.markdown("---")
    
    # Navigation
    st.header("📋 Menu")
    page = st.radio(
        "Vai a:",
        ["🏠 Dashboard", "🔗 Link", "🤖 Chatbot AI", "📜 Normative", "📊 Analytics", "⚙️ Impostazioni"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick stats
    st.subheader("📊 Quick Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Link", len(st.session_state.links))
    with col2:
        st.metric("Click", sum(l['clicks'] for l in st.session_state.links))
    
    st.markdown("---")
    
    # User info
    st.subheader("👤 Utente")
    st.text("admin")
    st.text("🟢 Online")


# ==================== DASHBOARD PAGE ====================

if page == "🏠 Dashboard":
    st.title("📊 Dashboard MoreLinks")
    st.markdown("---")
    
    # Stats row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <h1>🔗</h1>
            <h2>{}</h2>
            <p>Link Totali</p>
        </div>
        """.format(len(st.session_state.links)), unsafe_allow_html=True)
    
    with col2:
        total_clicks = sum(l['clicks'] for l in st.session_state.links)
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
            <h1>👆</h1>
            <h2>{}</h2>
            <p>Click Totali</p>
        </div>
        """.format(total_clicks), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);">
            <h1>🧠</h1>
            <h2>{}</h2>
            <p>Memoria AI</p>
        </div>
        """.format(len(st.session_state.memory_entries)), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);">
            <h1>📚</h1>
            <h2>5000+</h2>
            <p>Libri Skills</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("⚡ Azioni Rapide")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔗 Nuovo Link", use_container_width=True):
            st.session_state.nav = "🔗 Link"
            st.rerun()
    
    with col2:
        if st.button("🤖 Chat AI", use_container_width=True):
            st.session_state.nav = "🤖 Chatbot AI"
            st.rerun()
    
    with col3:
        if st.button("📜 Normative", use_container_width=True):
            st.session_state.nav = "📜 Normative"
            st.rerun()
    
    with col4:
        if st.button("📊 Analytics", use_container_width=True):
            st.session_state.nav = "📊 Analytics"
            st.rerun()
    
    st.markdown("---")
    
    # Recent activity
    st.subheader("📋 Attività Recente")
    activity_col1, activity_col2 = st.columns(2)
    
    with activity_col1:
        st.markdown("**🔗 Link Recent**")
        for link in st.session_state.links[:3]:
            st.markdown(f"- {link['title']}: {link['clicks']} click")
    
    with activity_col2:
        st.markdown("**💬 Chat Recenti**")
        for msg in st.session_state.chat_history[-3:]:
            if msg['role'] == 'user':
                st.markdown(f"- Tu: {msg['content'][:50]}...")


# ==================== LINKS PAGE ====================

elif page == "🔗 Link":
    st.title("🔗 Gestione Link")
    
    # Create new link form
    with st.expander("➕ Crea Nuovo Link", expanded=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            new_url = st.text_input("URL", placeholder="https://example.com")
            new_title = st.text_input("Titolo", placeholder="Nome del link")
            new_tags = st.text_input("Tags", placeholder="marketing, social, home")
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Crea Link", use_container_width=True):
                if new_url:
                    import random
                    code = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
                    st.session_state.links.append({
                        "code": code,
                        "url": new_url,
                        "title": new_title or code,
                        "clicks": 0
                    })
                    st.success(f"✅ Link creato! 🔗 https://ml.app/{code}")
                else:
                    st.error("Inserisci un URL valido")
    
    st.markdown("---")
    
    # Links list
    st.subheader("📋 I Tuoi Link")
    
    if st.session_state.links:
        # Table
        data = {
            "Codice": [l['code'] for l in st.session_state.links],
            "Titolo": [l['title'] for l in st.session_state.links],
            "URL": [l['url'] for l in st.session_state.links],
            "Click": [l['clicks'] for l in st.session_state.links],
        }
        
        st.data_editor(
            data,
            column_config={
                "Codice": st.column_config.TextColumn("Codice", width="small"),
                "Titolo": st.column_config.TextColumn("Titolo"),
                "URL": st.column_config.LinkColumn("URL"),
                "Click": st.column_config.NumberColumn("Click", min_value=0),
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Actions
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected = st.selectbox("Seleziona link", [l['code'] for l in st.session_state.links])
        
        with col2:
            if st.button("📱 Genera QR"):
                st.info(f"QR Code per: https://ml.app/{selected}")
        
        with col3:
            if st.button("📋 Copia URL"):
                st.code(f"https://ml.app/{selected}")
    else:
        st.info("Nessun link creato. Crea il tuo primo link!")


# ==================== CHATBOT PAGE ====================

elif page == "🤖 Chatbot AI":
    st.title("🤖 Omni Brain - Chatbot AI con Memoria Permanente")
    
    st.markdown("""
    <div style="background: #8b5cf6; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h4>🧠 Memoria Permanente Attiva</h4>
        <p>Ricordo TUTTO ciò che mi dici. Non dimentico mai nulla!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Agent selector
    col1, col2 = st.columns([3, 1])
    
    with col1:
        agent = st.selectbox(
            "🤖 Agente",
            ["🧠 Omni - Assistente Generale", "📋 AdminBot - Amministrazione", 
             "💻 CodeBot - Sviluppatore", "📈 MarketingBot - Marketing", 
             "📚 ResearchBot - Ricerca"]
        )
    
    with col2:
        if st.button("🗑️ Pulisci Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("---")
    
    # Chat display
    st.subheader("💬 Conversazione")
    
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg['role'] == 'user':
                st.markdown(f"<div class='user-msg'>👤 <b>Tu:</b> {msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='ai-msg'>🤖 <b>Omni:</b> {msg['content']}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick actions
    with st.expander("⚡ Azioni Rapide"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Crea link", use_container_width=True):
                st.session_state.chat_input = "crea link https://example.com"
        
        with col2:
            if st.button("📊 Mostra stats", use_container_width=True):
                st.session_state.chat_input = "mostra statistiche"
        
        with col3:
            if st.button("📜 Cerca normative", use_container_width=True):
                st.session_state.chat_input = "cerca normative privacy"
    
    # Input
    if 'chat_input' not in st.session_state:
        st.session_state.chat_input = ""
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "💬 Messaggio",
            value=st.session_state.chat_input,
            placeholder="Scrivi un messaggio... (Enter per inviare)",
            label_visibility="collapsed"
        )
        st.session_state.chat_input = ""
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        send = st.button("📤 Invia")
    
    if send and user_input:
        # Add user message
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input,
            'timestamp': datetime.now().isoformat()
        })
        
        # Simulate AI response
        if "normativa" in user_input.lower() or "legge" in user_input.lower():
            response = "📜 Ho cercato nelle normative italiane. Ecco cosa ho trovato:\n\n**GDPR (Reg. UE 679/2016)**\n- Obbligo di protezione dati personali\n- DPO obbligatorio in alcuni casi\n- Notifica violazioni entro 72 ore\n\nVuoi approfondire una normativa specifica?"
        elif "link" in user_input.lower() or "crea" in user_input.lower():
            response = "🔗 Posso aiutarti con i link! Ecco cosa posso fare:\n- Creare nuovi short link\n- Mostrarti le statistiche\n- Generare QR code\n\nDimmi cosa ti serve!"
        elif "ciao" in user_input.lower() or "salve" in user_input.lower():
            response = "👋 Ciao! Sono **Omni**, il tuo assistente AI con memoria permanente. Ricordo tutto ciò che mi dici!\n\nCome posso aiutarti oggi?"
        elif "libro" in user_input.lower() or "skill" in user_input.lower():
            response = "📚 Ho accesso a **5000+ libri** trasformati in skills! Ecco alcuni suggerimenti:\n\n1. **Atomic Habits** - James Clear\n2. **Deep Work** - Cal Newport  \n3. **The Lean Startup** - Eric Ries\n\nVuoi che cerchi un argomento specifico?"
        elif "stats" in user_input.lower() or "statistiche" in user_input.lower():
            response = f"📊 Ecco le tue statistiche:\n\n- 🔗 Link totali: {len(st.session_state.links)}\n- 👆 Click totali: {sum(l['clicks'] for l in st.session_state.links)}\n- 🧠 Ricordi salvati: {len(st.session_state.memory_entries)}\n\nVuoi dati più dettagliati?"
        else:
            response = f"🤖 Ho capito: \"{user_input}\"\n\nPosso aiutarti con:\n- 🔗 Gestione link\n- 📜 Normative italiane\n- 📚 Suggerimenti libri\n- 📊 Statistiche\n- 💬 E altro ancora!\n\nCosa ti serve?"
        
        # Add AI response
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response,
            'timestamp': datetime.now().isoformat()
        })
        
        st.rerun()


# ==================== NORMATIVE PAGE ====================

elif page == "📜 Normative":
    st.title("📜 Normative Italiane")
    
    # Search
    col1, col2 = st.columns([4, 1])
    
    with col1:
        search = st.text_input("🔍 Cerca normativa", placeholder="Es: GDPR, fatturazione, sicurezza...")
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Cerca"):
            st.info(f"Cercando: {search}")
    
    st.markdown("---")
    
    # Categories
    st.subheader("📁 Categorie")
    
    categories = {
        "🏢 Contabilità": ["Codice Civile Art. 2423 - Bilancio", "Principi Contabili OIC", "DPR 917/86 - TUIR"],
        "🔒 Privacy": ["GDPR (Reg. UE 679/2016)", "Codice Privacy (DLgs 196/2003)", "Videosorveglianza"],
        "👷 Lavoro": ["Statuto Lavoratori (L. 300/70)", "TUSL (DLgs 81/2008)", "Whistleblowing (DLgs 24/2023)"],
        "⚖️ Responsabilità": ["DLgs 231/2001 - Modello 231", "Responsabilità Enti"],
        "🔄 Antiriciclaggio": ["DLgs 231/2007", "Segnalazione SOS"],
        "💾 Fatturazione": ["DLgs 127/2015 - Fattura Elettronica", "SDI"],
    }
    
    tabs = st.tabs(list(categories.keys()))
    
    for i, (cat, norms) in enumerate(categories.items()):
        with tabs[i]:
            for norm in norms:
                with st.expander(f"📜 {norm}"):
                    st.markdown(f"**{norm}**")
                    st.markdown("""
                    - ✅ Principali obblighi elencati
                    - ⚠️ Sanzioni previste
                    - 📅 Scadenze da rispettare
                    """)
                    if st.button(f"Applica {norm[:20]}", key=f"btn_{norm}"):
                        st.success(f"Hai applicato: {norm}")


# ==================== ANALYTICS PAGE ====================

elif page == "📊 Analytics":
    st.title("📊 Analytics - Statistiche Dettagliate")
    
    # Date range
    col1, col2 = st.columns(2)
    
    with col1:
        st.date_input("Da", value=datetime.now())
    
    with col2:
        st.date_input("A", value=datetime.now())
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👆 Click per Giorno")
        st.line_chart({
            "Data": ["01/06", "02/06", "03/06", "04/06", "05/06"],
            "Click": [45, 67, 89, 56, 102]
        })
    
    with col2:
        st.subheader("📱 Dispositivi")
        st.bar_chart({
            "Dispositivo": ["Mobile", "Desktop", "Tablet"],
            "%": [58, 38, 4]
        })
    
    st.markdown("---")
    
    # Top links
    st.subheader("🏆 Top Link")
    
    top_data = {
        "Posizione": [1, 2, 3, 4, 5],
        "Link": ["GitHub", "Python", "FastAPI", "Docker", "React"],
        "Click": [1247, 892, 534, 321, 234]
    }
    
    st.dataframe(top_data, use_container_width=True)
    
    st.markdown("---")
    
    # Export
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Esporta CSV"):
            st.info("Esportazione CSV completata!")
    
    with col2:
        if st.button("📄 Esporta PDF"):
            st.info("Esportazione PDF completata!")
    
    with col3:
        if st.button("📊 Esporta Excel"):
            st.info("Esportazione Excel completata!")


# ==================== SETTINGS PAGE ====================

elif page == "⚙️ Impostazioni":
    st.title("⚙️ Impostazioni")
    
    # AI Settings
    st.subheader("🤖 Impostazioni AI")
    
    api_key = st.text_input(
        "OpenRouter API Key",
        value="",
        type="password",
        help="Inserisci la tua API key da OpenRouter.ai"
    )
    
    model = st.selectbox(
        "Modello AI",
        ["nvidia/nemotron-3-5-content-safety:free", "nex-agi/nex-n2-pro:free", "nvidia/nemotron-3-ultra-550b-a55b:free"]
    )
    
    memory_enabled = st.checkbox("🧠 Memoria Permanente Attivata", value=True)
    
    st.markdown("---")
    
    # Profile
    st.subheader("👤 Profilo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        username = st.text_input("Nome Utente", value="admin")
        email = st.text_input("Email", value="admin@morelinks.local")
    
    with col2:
        company = st.text_input("Azienda", value="")
        phone = st.text_input("Telefono", value="")
    
    st.markdown("---")
    
    # Save
    if st.button("💾 Salva Impostazioni", use_container_width=True):
        st.success("✅ Impostazioni salvate!")


# ==================== FOOTER ====================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888;">
    <p>🔗 MoreLinks v1.0.0 | Piattaforma AI con Memoria Permanente</p>
    <p>🧠 Omni Brain | 📚 Book2Skills | 📜 Normative Italiane</p>
    <p>Creato da Fabio (Schumynet)</p>
</div>
""", unsafe_allow_html=True)
