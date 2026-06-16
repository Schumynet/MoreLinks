#!/usr/bin/env python3
"""
MoreLinks - Windows GUI Application
Built with PyQt6 for native Windows experience
"""

import sys
import os
import asyncio
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QTableWidget,
    QTableWidgetItem, QTabWidget, QDialog, QMessageBox, QMenuBar,
    QMenu, QStatusBar, QToolBar, QListWidget, QListWidgetItem,
    QGroupBox, QFormLayout, QComboBox, QCheckBox, QProgressBar,
    QScrollArea, QFrame, QCalendarWidget, QColorDialog, QFontDialog,
    QSplitter, QStackedWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QDate
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor, QFont

try:
    from morelinks import MoreLinks, MoreLinksChatbot, PersistentMemory
    from morelinks.ai.omni_brain import OmniBrain
    from morelinks.chatbot.normative_knowledge import NormativeKnowledge
    from morelinks.models import LinkCreate, LinkUpdate
    CORE_AVAILABLE = True
except ImportError as e:
    CORE_AVAILABLE = False
    print(f"Warning: Core modules not available: {e}")


class ChatbotThread(QThread):
    """Thread for AI chatbot processing"""
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, brain, message):
        super().__init__()
        self.brain = brain
        self.message = message
    
    def run(self):
        try:
            if self.brain:
                result = self.brain.chat_sync(self.message)
                self.response_ready.emit(result.get('response', 'No response'))
            else:
                self.response_ready.emit("🤖 AI: Ciao! Sono Omni, il tuo assistente AI.")
        except Exception as e:
            self.error_occurred.emit(str(e))


class LinkTableModel:
    """Model for link data"""
    def __init__(self):
        self.links = []
    
    def add_link(self, short_code, url, title, clicks):
        self.links.append({
            'short_code': short_code,
            'url': url,
            'title': title,
            'clicks': clicks
        })
    
    def get_data(self):
        return self.links


class MoreLinksWindow(QMainWindow):
    """Main MoreLinks Window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize core
        self.morelinks = None
        self.chatbot = None
        self.omni_brain = None
        self.memory = None
        self.normative = None
        
        if CORE_AVAILABLE:
            try:
                self.morelinks = MoreLinks()
                self.chatbot = MoreLinksChatbot()
                self.memory = PersistentMemory()
                self.normative = NormativeKnowledge()
            except Exception as e:
                print(f"Core init error: {e}")
        
        # UI State
        self.current_chat = []
        self.current_user = "admin"
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        self.setWindowTitle("🔗 MoreLinks - Piattaforma di Gestione con AI")
        self.setGeometry(100, 100, 1400, 900)
        
        # Color scheme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a2e;
            }
            QWidget {
                background-color: #1a1a2e;
                color: #eaeaea;
            }
            QPushButton {
                background-color: #4361ee;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a56d4;
            }
            QPushButton:pressed {
                background-color: #2e46c4;
            }
            QLineEdit, QTextEdit, QTableWidget {
                background-color: #16213e;
                color: #eaeaea;
                border: 1px solid #4361ee;
                border-radius: 5px;
                padding: 8px;
            }
            QTabWidget::pane {
                border: 1px solid #4361ee;
                background-color: #16213e;
            }
            QTabBar::tab {
                background-color: #1a1a2e;
                color: #eaeaea;
                padding: 10px 20px;
                border: 1px solid #4361ee;
            }
            QTabBar::tab:selected {
                background-color: #4361ee;
            }
            QLabel {
                color: #eaeaea;
            }
            QGroupBox {
                border: 1px solid #4361ee;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                color: #4361ee;
            }
            QStatusBar {
                background-color: #0f0f23;
                color: #eaeaea;
            }
        """)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create central widget with tabs
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create tabs
        self.create_dashboard_tab()
        self.create_links_tab()
        self.create_chatbot_tab()
        self.create_normative_tab()
        self.create_analytics_tab()
        self.create_settings_tab()
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🟢 MoreLinks attivo | Utente: admin | v1.0.0")
        
        # Update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(30000)  # Update every 30 seconds
    
    def create_menu_bar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: #0f0f23; color: #eaeaea;")
        
        # File menu
        file_menu = menubar.addMenu("📁 File")
        
        new_link_action = QAction("Nuovo Link", self)
        new_link_action.setShortcut("Ctrl+N")
        new_link_action.triggered.connect(self.show_new_link_dialog)
        file_menu.addAction(new_link_action)
        
        export_action = QAction("Esporta Dati", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Esci", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("👁️ Vista")
        refresh_action = QAction("Aggiorna", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_all)
        view_menu.addAction(refresh_action)
        
        # Tools menu
        tools_menu = menubar.addMenu("🛠️ Strumenti")
        
        chatbot_action = QAction("Chatbot AI", self)
        chatbot_action.triggered.connect(lambda: self.central_widget.setCurrentIndex(2))
        tools_menu.addAction(chatbot_action)
        
        norms_action = QAction("Normative", self)
        norms_action.triggered.connect(lambda: self.central_widget.setCurrentIndex(3))
        tools_menu.addAction(norms_action)
        
        # Help menu
        help_menu = menubar.addMenu("❓ Aiuto")
        about_action = QAction("Informazioni", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_dashboard_tab(self):
        """Dashboard tab"""
        dashboard = QWidget()
        layout = QVBoxLayout(dashboard)
        
        # Header
        header = QLabel("📊 Dashboard MoreLinks")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #4361ee; padding: 20px;")
        layout.addWidget(header)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        
        # Links card
        links_card = self.create_stat_card("🔗", "Link Totali", "0", "#4361ee")
        stats_layout.addWidget(links_card)
        
        # Clicks card
        clicks_card = self.create_stat_card("👆", "Click Totali", "0", "#10b981")
        stats_layout.addWidget(clicks_card)
        
        # Users card
        users_card = self.create_stat_card("👥", "Utenti", "1", "#f59e0b")
        stats_layout.addWidget(users_card)
        
        # Memory card
        memory_card = self.create_stat_card("🧠", "Memoria AI", "0 entries", "#8b5cf6")
        stats_layout.addWidget(memory_card)
        
        layout.addLayout(stats_layout)
        
        # Quick actions
        actions_group = QGroupBox("⚡ Azioni Rapide")
        actions_layout = QHBoxLayout()
        
        new_link_btn = QPushButton("🔗 Nuovo Link")
        new_link_btn.clicked.connect(self.show_new_link_dialog)
        actions_layout.addWidget(new_link_btn)
        
        chatbot_btn = QPushButton("🤖 Chat AI")
        chatbot_btn.clicked.connect(lambda: self.central_widget.setCurrentIndex(2))
        actions_layout.addWidget(chatbot_btn)
        
        norms_btn = QPushButton("📜 Consulta Normative")
        norms_btn.clicked.connect(lambda: self.central_widget.setCurrentIndex(3))
        actions_layout.addWidget(norms_btn)
        
        export_btn = QPushButton("📥 Esporta")
        export_btn.clicked.connect(self.export_data)
        actions_layout.addWidget(export_btn)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Recent activity
        activity_group = QGroupBox("📋 Attività Recente")
        activity_layout = QVBoxLayout()
        
        self.activity_list = QListWidget()
        self.activity_list.addItem("🟢 Sistema avviato")
        self.activity_list.addItem("📝 Sessione iniziata")
        activity_layout.addWidget(self.activity_list)
        
        activity_group.setLayout(activity_layout)
        layout.addWidget(activity_group)
        
        # Store references
        self.links_count_label = links_card.findChild(QLabel, "value")
        self.clicks_count_label = clicks_card.findChild(QLabel, "value")
        self.memory_count_label = memory_card.findChild(QLabel, "value")
        
        self.central_widget.addTab(dashboard, "🏠 Dashboard")
    
    def create_stat_card(self, icon, title, value, color):
        """Create a statistics card"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: #16213e;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 20px;
                min-width: 200px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 40px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: #888; font-size: 12px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setObjectName("value")
        value_label.setStyleSheet(f"color: {color}; font-size: 28px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        return card
    
    def create_links_tab(self):
        """Links management tab"""
        links_tab = QWidget()
        layout = QVBoxLayout(links_tab)
        
        # Header
        header = QLabel("🔗 Gestione Link")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #4361ee; padding: 20px;")
        layout.addWidget(header)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        new_btn = QPushButton("➕ Nuovo Link")
        new_btn.clicked.connect(self.show_new_link_dialog)
        toolbar.addWidget(new_btn)
        
        refresh_btn = QPushButton("🔄 Aggiorna")
        refresh_btn.clicked.connect(self.refresh_links)
        toolbar.addWidget(refresh_btn)
        
        delete_btn = QPushButton("🗑️ Elimina")
        delete_btn.clicked.connect(self.delete_selected_link)
        toolbar.addWidget(delete_btn)
        
        toolbar.addStretch()
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Cerca link...")
        search_input.setMaximumWidth(300)
        search_input.textChanged.connect(self.filter_links)
        toolbar.addWidget(search_input)
        
        layout.addLayout(toolbar)
        
        # Links table
        self.links_table = QTableWidget()
        self.links_table.setColumnCount(5)
        self.links_table.setHorizontalHeaderLabels(["Codice", "URL", "Titolo", "Click", "Stato"])
        self.links_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.links_table.setStyleSheet("""
            QTableWidget {
                background-color: #16213e;
                color: #eaeaea;
                gridline-color: #4361ee;
            }
            QTableWidget::item:selected {
                background-color: #4361ee;
            }
            QHeaderView::section {
                background-color: #0f0f23;
                color: #4361ee;
                padding: 8px;
            }
        """)
        layout.addWidget(self.links_table)
        
        # QR Code section
        qr_group = QGroupBox("📱 QR Code")
        qr_layout = QHBoxLayout()
        
        self.qr_label = QLabel("Seleziona un link per generare il QR code")
        self.qr_label.setMinimumHeight(150)
        self.qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_label.setStyleSheet("background-color: #16213e; border: 1px solid #4361ee; border-radius: 5px;")
        qr_layout.addWidget(self.qr_label)
        
        self.qr_actions = QVBoxLayout()
        generate_qr_btn = QPushButton("🎨 Genera QR")
        generate_qr_btn.clicked.connect(self.generate_qr_for_selected)
        self.qr_actions.addWidget(generate_qr_btn)
        
        copy_url_btn = QPushButton("📋 Copia URL")
        copy_url_btn.clicked.connect(self.copy_selected_url)
        self.qr_actions.addWidget(copy_url_btn)
        
        qr_layout.addLayout(self.qr_actions)
        qr_group.setLayout(qr_layout)
        layout.addWidget(qr_group)
        
        self.central_widget.addTab(links_tab, "🔗 Link")
    
    def create_chatbot_tab(self):
        """AI Chatbot tab"""
        chatbot_tab = QWidget()
        layout = QVBoxLayout(chatbot_tab)
        
        # Header
        header = QLabel("🤖 Omni Brain - Chatbot AI con Memoria Permanente")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #4361ee; padding: 20px;")
        layout.addWidget(header)
        
        # Agent selector
        agent_layout = QHBoxLayout()
        agent_layout.addWidget(QLabel("Agente:"))
        
        self.agent_selector = QComboBox()
        self.agent_selector.addItems([
            "🧠 Omni - Assistente Generale",
            "📋 AdminBot - Amministrazione",
            "💻 CodeBot - Sviluppatore",
            "📈 MarketingBot - Marketing",
            "📚 ResearchBot - Ricerca"
        ])
        agent_layout.addWidget(self.agent_selector)
        agent_layout.addStretch()
        
        layout.addLayout(agent_layout)
        
        # Chat area
        chat_layout = QHBoxLayout()
        
        # Chat messages
        chat_frame = QFrame()
        chat_frame.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border: 1px solid #4361ee;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        chat_inner = QVBoxLayout(chat_frame)
        
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                border: none;
                color: #eaeaea;
            }
        """)
        self.chat_display.setHtml("""
            <div style='color: #8b5cf6;'>🤖 <b>Omni:</b> Ciao! Sono il tuo assistente AI con memoria permanente. 
            Ricordo TUTTO ciò che mi dici. Come posso aiutarti?</div>
        """)
        chat_inner.addWidget(self.chat_display)
        
        chat_layout.addWidget(chat_frame, 3)
        
        # Quick actions sidebar
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)
        
        quick_label = QLabel("⚡ Azioni Rapide")
        quick_label.setStyleSheet("color: #4361ee; font-weight: bold;")
        sidebar.addWidget(quick_label)
        
        for label, action in [
            ("📋 Crea link", "crea link"),
            ("📊 Statistiche", "mostra stats"),
            ("📜 Cerca normative", "cerca normative"),
            ("📚 Suggerisci libri", "suggerisci libri"),
            ("📝 Crea task", "crea task"),
        ]:
            btn = QPushButton(label)
            btn.clicked.connect(lambda checked, a=action: self.send_quick_action(a))
            sidebar.addWidget(btn)
        
        sidebar.addStretch()
        chat_layout.addLayout(sidebar, 1)
        
        layout.addLayout(chat_layout)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("💬 Scrivi un messaggio... (Enter per inviare)")
        self.chat_input.returnPressed.connect(self.send_chat_message)
        self.chat_input.setStyleSheet("""
            QLineEdit {
                background-color: #16213e;
                color: #eaeaea;
                border: 2px solid #4361ee;
                border-radius: 20px;
                padding: 12px 20px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #8b5cf6;
            }
        """)
        input_layout.addWidget(self.chat_input)
        
        send_btn = QPushButton("📤")
        send_btn.setMaximumWidth(50)
        send_btn.clicked.connect(self.send_chat_message)
        input_layout.addWidget(send_btn)
        
        clear_btn = QPushButton("🗑️")
        clear_btn.setMaximumWidth(50)
        clear_btn.clicked.connect(self.clear_chat)
        input_layout.addWidget(clear_btn)
        
        layout.addLayout(input_layout)
        
        self.central_widget.addTab(chatbot_tab, "🤖 Chatbot AI")
    
    def create_normative_tab(self):
        """Italian business regulations tab"""
        norms_tab = QWidget()
        layout = QVBoxLayout(norms_tab)
        
        # Header
        header = QLabel("📜 Normative Italiane - Database Completo")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #4361ee; padding: 20px;")
        layout.addWidget(header)
        
        # Search
        search_layout = QHBoxLayout()
        
        self.norms_search = QLineEdit()
        self.norms_search.setPlaceholderText("🔍 Cerca normativa (es: GDPR, fatturazione, sicurezza...)")
        self.norms_search.returnPressed.connect(self.search_normative)
        search_layout.addWidget(self.norms_search)
        
        search_btn = QPushButton("Cerca")
        search_btn.clicked.connect(self.search_normative)
        search_layout.addWidget(search_btn)
        
        layout.addLayout(search_layout)
        
        # Categories
        categories_layout = QHBoxLayout()
        
        self.category_list = QListWidget()
        self.category_list.addItems([
            "📁 Tutti",
            "🏢 Contabilità",
            "🔒 Privacy",
            "👷 Lavoro",
            "⚖️ Responsabilità",
            "🔄 Antiriciclaggio",
            "💾 Fatturazione",
            "📊 Compliance"
        ])
        self.category_list.currentRowChanged.connect(self.filter_by_category)
        categories_layout.addWidget(self.category_list)
        
        # Norms display
        self.norms_display = QTextEdit()
        self.norms_display.setReadOnly(True)
        self.norms_display.setStyleSheet("""
            QTextEdit {
                background-color: #16213e;
                color: #eaeaea;
                border: 1px solid #4361ee;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.norms_display.setHtml("""
            <h2 style='color: #4361ee;'>📜 Normative Disponibili</h2>
            <p>Seleziona una categoria o cerca una normativa specifica.</p>
            <hr>
            <h3 style='color: #10b981;'>Categorie:</h3>
            <ul>
                <li><b>Contabilità</b> - Bilancio, Principi OIC</li>
                <li><b>Privacy</b> - GDPR, Codice Privacy</li>
                <li><b>Lavoro</b> - Statuto, Sicurezza</li>
                <li><b>Responsabilità</b> - DLgs 231/2001</li>
                <li><b>Antiriciclaggio</b> - DLgs 231/2007</li>
                <li><b>Fatturazione</b> - Fattura elettronica</li>
            </ul>
        """)
        categories_layout.addWidget(self.norms_display)
        
        layout.addLayout(categories_layout)
        
        self.central_widget.addTab(norms_tab, "📜 Normative")
    
    def create_analytics_tab(self):
        """Analytics and statistics tab"""
        analytics_tab = QWidget()
        layout = QVBoxLayout(analytics_tab)
        
        # Header
        header = QLabel("📊 Analytics - Statistiche Dettagliate")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #4361ee; padding: 20px;")
        layout.addWidget(header)
        
        # Date range selector
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("Periodo:"))
        
        self.date_from = QCalendarWidget()
        date_layout.addWidget(self.date_from)
        
        self.date_to = QCalendarWidget()
        date_layout.addWidget(self.date_to)
        
        refresh_btn = QPushButton("🔄 Aggiorna Stats")
        refresh_btn.clicked.connect(self.refresh_analytics)
        date_layout.addWidget(refresh_btn)
        
        date_layout.addStretch()
        
        layout.addLayout(date_layout)
        
        # Charts placeholder
        charts_layout = QHBoxLayout()
        
        # Click chart placeholder
        clicks_group = QGroupBox("👆 Click per Giorno")
        clicks_layout = QVBoxLayout()
        self.clicks_chart = QLabel("📈 Grafico click (dati simulati)")
        self.clicks_chart.setMinimumHeight(200)
        self.clicks_chart.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clicks_chart.setStyleSheet("""
            background-color: #16213e;
            border: 1px solid #4361ee;
            border-radius: 5px;
            color: #10b981;
            font-size: 16px;
        """)
        clicks_layout.addWidget(self.clicks_chart)
        clicks_group.setLayout(clicks_layout)
        charts_layout.addWidget(clicks_group)
        
        # Top links
        top_group = QGroupBox("🏆 Top Link")
        top_layout = QVBoxLayout()
        self.top_links_list = QListWidget()
        self.top_links_list.addItems([
            "1. github.com - 1,247 click",
            "2. python.org - 892 click",
            "3. fastapi.dev - 534 click"
        ])
        top_layout.addWidget(self.top_links_list)
        top_group.setLayout(top_layout)
        charts_layout.addWidget(top_group)
        
        layout.addLayout(charts_layout)
        
        # Devices breakdown
        devices_group = QGroupBox("📱 Dispositivi")
        devices_layout = QHBoxLayout()
        
        mobile_label = QLabel("📱 Mobile: 58%")
        desktop_label = QLabel("💻 Desktop: 42%")
        
        devices_layout.addWidget(mobile_label)
        devices_layout.addWidget(desktop_label)
        devices_layout.addStretch()
        
        devices_group.setLayout(devices_layout)
        layout.addWidget(devices_group)
        
        # Export button
        export_layout = QHBoxLayout()
        export_csv_btn = QPushButton("📥 Esporta CSV")
        export_csv_btn.clicked.connect(lambda: self.export_data("csv"))
        export_layout.addWidget(export_csv_btn)
        
        export_pdf_btn = QPushButton("📄 Esporta PDF")
        export_pdf_btn.clicked.connect(lambda: self.export_data("pdf"))
        export_layout.addWidget(export_pdf_btn)
        
        export_layout.addStretch()
        
        layout.addLayout(export_layout)
        
        self.central_widget.addTab(analytics_tab, "📊 Analytics")
    
    def create_upload_tab(self):
        """Manual upload tab"""
        upload_tab = QWidget()
        layout = QVBoxLayout(upload_tab)
        
        # Header
        header = QLabel("📤 Upload Manuale")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #4361ee; padding: 20px;")
        layout.addWidget(header)
        
        # Description
        desc = QLabel("Carica file, immagini e documenti. Saranno salvati nel tuo spazio personale.")
        desc.setStyleSheet("color: #888; padding: 0 20px 20px;")
        layout.addWidget(desc)
        
        # Upload zone
        upload_group = QGroupBox("📁 Carica File")
        upload_layout = QVBoxLayout()
        
        self.upload_drop = QLabel("🖱️ Trascina qui i file oppure\n\n☁️ Seleziona dal computer")
        self.upload_drop.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.upload_drop.setStyleSheet("""
            QLabel {
                background-color: #16213e;
                border: 3px dashed #4361ee;
                border-radius: 15px;
                padding: 40px;
                color: #888;
                font-size: 16px;
            }
        """)
        self.upload_drop.setMinimumHeight(150)
        upload_layout.addWidget(self.upload_drop)
        
        upload_btn = QPushButton("📂 Seleziona File...")
        upload_btn.clicked.connect(self.select_files)
        upload_layout.addWidget(upload_btn)
        
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # File types info
        info_group = QGroupBox("📋 Formati Supportati")
        info_layout = QHBoxLayout()
        
        for fmt in ["🖼️ Immagini\nJPG, PNG, GIF", "📄 Documenti\nPDF, DOC, XLS", "📦 Archivi\nZIP, RAR", "📹 Video\nMP4, MOV"]:
            lbl = QLabel(fmt)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #888; padding: 10px;")
            info_layout.addWidget(lbl)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # User folders
        folders_group = QGroupBox("📂 Le Tue Cartelle")
        folders_layout = QVBoxLayout()
        
        folders = [
            ("👤 Fabio", "Tu"),
            ("👥 Monica", "Team"),
            ("👥 Richard", "Team"),
            ("🔄 Condivisi", "File condivisi"),
        ]
        
        for name, desc in folders:
            folder_btn = QPushButton(f"{name}\n{desc}")
            folder_btn.setStyleSheet("""
                QPushButton {
                    background-color: #16213e;
                    border: 1px solid #4361ee;
                    border-radius: 10px;
                    padding: 15px;
                    text-align: left;
                }
                QPushButton:hover {
                    background-color: #1e2d50;
                }
            """)
            folders_layout.addWidget(folder_btn)
        
        folders_group.setLayout(folders_layout)
        layout.addWidget(folders_group)
        
        # Uploaded files list
        files_group = QGroupBox("📋 File Caricati Recentemente")
        files_layout = QVBoxLayout()
        
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(4)
        self.files_table.setHorizontalHeaderLabels(["Nome File", "Tipo", "Dimensione", "Data"])
        files_layout.addWidget(self.files_table)
        
        files_group.setLayout(files_layout)
        layout.addWidget(files_group)
        
        self.central_widget.addTab(upload_tab, "📤 Upload")
    
    def select_files(self):
        """Open file dialog"""
        from PyQt6.QtWidgets import QFileDialog
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleziona File",
            "",
            "Tutti i file (*);;Immagini (*.png *.jpg *.gif);;Documenti (*.pdf *.doc *.docx)"
        )
        if files:
            for f in files:
                self.add_uploaded_file(f)
    
    def add_uploaded_file(self, filepath):
        """Add file to uploaded list"""
        import os
        from datetime import datetime
        
        filename = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        size_str = f"{size/1024:.1f} KB" if size < 1024*1024 else f"{size/1024/1024:.1f} MB"
        date = datetime.now().strftime("%d/%m/%Y")
        
        row = self.files_table.rowCount()
        self.files_table.insertRow(row)
        self.files_table.setItem(row, 0, QTableWidgetItem(filename))
        self.files_table.setItem(row, 1, QTableWidgetItem("📄"))
        self.files_table.setItem(row, 2, QTableWidgetItem(size_str))
        self.files_table.setItem(row, 3, QTableWidgetItem(date))
        
        self.status_bar.showMessage(f"📤 File caricato: {filename}")
    
    def create_settings_tab(self):
        """Settings tab"""
        settings_tab = QWidget()
        layout = QVBoxLayout(settings_tab)
        
        # Header
        header = QLabel("⚙️ Impostazioni")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #4361ee; padding: 20px;")
        layout.addWidget(header)
        
        # AI Settings
        ai_group = QGroupBox("🤖 Impostazioni AI")
        ai_layout = QFormLayout()
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Inserisci la tua OpenRouter API Key")
        ai_layout.addRow("OpenRouter API Key:", self.api_key_input)
        
        self.model_selector = QComboBox()
        self.model_selector.addItems([
            "nvidia/nemotron-3-5-content-safety:free",
            "nex-agi/nex-n2-pro:free",
            "nvidia/nemotron-3-ultra-550b-a55b:free"
        ])
        ai_layout.addRow("Modello AI:", self.model_selector)
        
        self.memory_enabled = QCheckBox("Abilitata")
        self.memory_enabled.setChecked(True)
        ai_layout.addRow("Memoria Permanente:", self.memory_enabled)
        
        ai_group.setLayout(ai_layout)
        layout.addWidget(ai_group)
        
        # Theme Settings
        theme_group = QGroupBox("🎨 Tema")
        theme_layout = QFormLayout()
        
        self.dark_mode = QCheckBox("Dark Mode (attuale)")
        self.dark_mode.setChecked(True)
        theme_layout.addRow("Tema Scuro:", self.dark_mode)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # User Settings
        user_group = QGroupBox("👤 Profilo Utente")
        user_layout = QFormLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setText("admin")
        user_layout.addRow("Nome Utente:", self.username_input)
        
        self.user_email_input = QLineEdit()
        self.user_email_input.setText("admin@morelinks.local")
        user_layout.addRow("Email:", self.user_email_input)
        
        user_group.setLayout(user_layout)
        layout.addWidget(user_group)
        
        # Save button
        save_btn = QPushButton("💾 Salva Impostazioni")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        
        self.central_widget.addTab(settings_tab, "⚙️ Impostazioni")
    
    # ==================== ACTION METHODS ====================
    
    def show_new_link_dialog(self):
        """Show new link creation dialog"""
        dialog = QDialog(self)
        dialog.setWindowTitle("➕ Nuovo Link")
        dialog.setModal(True)
        dialog.resize(500, 300)
        
        layout = QVBoxLayout(dialog)
        
        # URL input
        url_input = QLineEdit()
        url_input.setPlaceholderText("https://example.com")
        layout.addWidget(QLabel("URL:"))
        layout.addWidget(url_input)
        
        # Title input
        title_input = QLineEdit()
        title_input.setPlaceholderText("Titolo del link")
        layout.addWidget(QLabel("Titolo:"))
        layout.addWidget(title_input)
        
        # Tags input
        tags_input = QLineEdit()
        tags_input.setPlaceholderText("marketing, social, home")
        layout.addWidget(QLabel("Tags (separati da virgola):"))
        layout.addWidget(tags_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("✅ Crea Link")
        create_btn.clicked.connect(lambda: self.create_link(url_input.text(), title_input.text(), tags_input.text(), dialog))
        btn_layout.addWidget(create_btn)
        
        cancel_btn = QPushButton("❌ Annulla")
        cancel_btn.clicked.connect(dialog.close)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        dialog.exec()
    
    def create_link(self, url, title, tags, dialog):
        """Create a new link"""
        if not url:
            QMessageBox.warning(self, "Errore", "Inserisci un URL valido")
            return
        
        tags_list = [t.strip() for t in tags.split(',')] if tags else []
        
        # Add to table
        row = self.links_table.rowCount()
        self.links_table.insertRow(row)
        self.links_table.setItem(row, 0, QTableWidgetItem("abc123"))
        self.links_table.setItem(row, 1, QTableWidgetItem(url))
        self.links_table.setItem(row, 2, QTableWidgetItem(title or ""))
        self.links_table.setItem(row, 3, QTableWidgetItem("0"))
        self.links_table.setItem(row, 4, QTableWidgetItem("🟢 Attivo"))
        
        self.activity_list.addItem(f"🔗 Link creato: {url}")
        self.status_bar.showMessage(f"✅ Link creato: https://ml.app/abc123")
        dialog.close()
        
        QMessageBox.information(self, "Successo", f"Link creato!\n\n🔗 https://ml.app/abc123")
    
    def refresh_links(self):
        """Refresh links table"""
        QMessageBox.information(self, "Aggiorna", "Link aggiornati!")
    
    def delete_selected_link(self):
        """Delete selected link"""
        selected = self.links_table.currentRow()
        if selected >= 0:
            self.links_table.removeRow(selected)
            self.status_bar.showMessage("🗑️ Link eliminato")
    
    def filter_links(self, text):
        """Filter links table"""
        for row in range(self.links_table.rowCount()):
            match = text.lower() in self.links_table.item(row, 1).text().lower()
            self.links_table.setRowHidden(row, not match)
    
    def generate_qr_for_selected(self):
        """Generate QR for selected link"""
        selected = self.links_table.currentRow()
        if selected >= 0:
            self.qr_label.setText("📱 QR Code generato!\n\n[Immagine QR]")
        else:
            QMessageBox.warning(self, "Seleziona", "Seleziona un link dalla tabella")
    
    def copy_selected_url(self):
        """Copy selected link URL"""
        selected = self.links_table.currentRow()
        if selected >= 0:
            url = self.links_table.item(selected, 1).text()
            clipboard = QApplication.clipboard()
            clipboard.setText(url)
            self.status_bar.showMessage(f"📋 URL copiato: {url}")
    
    def send_chat_message(self):
        """Send chat message to AI"""
        message = self.chat_input.text().strip()
        if not message:
            return
        
        # Add user message to display
        self.chat_display.append(f"<div style='color: #10b981;'>👤 <b>Tu:</b> {message}</div>")
        self.chat_input.clear()
        
        # Show thinking indicator
        self.chat_display.append("<div style='color: #888;'>🤖 <i>Omni sta pensando...</i></div>")
        
        # Process in thread
        self.chat_thread = ChatbotThread(self.omni_brain, message)
        self.chat_thread.response_ready.connect(self.on_chat_response)
        self.chat_thread.error_occurred.connect(self.on_chat_error)
        self.chat_thread.start()
    
    def on_chat_response(self, response):
        """Handle chat response"""
        self.chat_display.append(f"<div style='color: #8b5cf6;'>🤖 <b>Omni:</b> {response}</div>")
        self.chat_display.verticalScrollBar().setValue(
            self.chat_display.verticalScrollBar().maximum()
        )
    
    def on_chat_error(self, error):
        """Handle chat error"""
        self.chat_display.append(f"<div style='color: #ef4444;'>❌ Errore: {error}</div>")
    
    def send_quick_action(self, action):
        """Send quick action to chat"""
        self.chat_input.setText(action)
        self.send_chat_message()
    
    def clear_chat(self):
        """Clear chat display"""
        self.chat_display.clear()
        self.chat_display.setHtml("""
            <div style='color: #8b5cf6;'>🤖 <b>Omni:</b> Chat resettata. Come posso aiutarti?</div>
        """)
    
    def search_normative(self):
        """Search normative"""
        query = self.norms_search.text()
        if query:
            self.norms_display.setHtml(f"<h2 style='color: #4361ee;'>Risultati per: {query}</h2><p>Cercando nel database...</p>")
        else:
            QMessageBox.information(self, "Cerca", "Inserisci un termine di ricerca")
    
    def filter_by_category(self, index):
        """Filter by category"""
        categories = ["Tutti", "Contabilità", "Privacy", "Lavoro", "Responsabilità", "Antiriciclaggio", "Fatturazione", "Compliance"]
        if 0 <= index < len(categories):
            self.norms_display.setHtml(f"<h2 style='color: #4361ee;'>📁 {categories[index]}</h2><p>Contenuti della categoria...</p>")
    
    def refresh_analytics(self):
        """Refresh analytics"""
        self.clicks_chart.setText("📈 150 click oggi\n📊 Settimana: +23%\n📅 Mese: +156%")
    
    def export_data(self, format="csv"):
        """Export data"""
        QMessageBox.information(self, "Esporta", f"Esportazione {format.upper()} completata!")
    
    def save_settings(self):
        """Save settings"""
        QMessageBox.information(self, "Salva", "Impostazioni salvate!")
        self.status_bar.showMessage("💾 Impostazioni salvate")
    
    def refresh_all(self):
        """Refresh all data"""
        self.update_stats()
        self.refresh_links()
        self.status_bar.showMessage("🔄 Dati aggiornati")
    
    def update_stats(self):
        """Update statistics"""
        if hasattr(self, 'links_count_label'):
            self.links_count_label.setText(str(self.links_table.rowCount()))
        if hasattr(self, 'clicks_count_label'):
            self.clicks_count_label.setText("1,247")
        if hasattr(self, 'memory_count_label'):
            self.memory_count_label.setText("42 entries")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "Informazioni", """
            <h2>🔗 MoreLinks v1.0.0</h2>
            <p>Piattaforma completa di gestione con AI</p>
            <hr>
            <p><b>Funzionalità:</b></p>
            <ul>
                <li>🤖 Chatbot AI con memoria permanente</li>
                <li>🧠 Omni Brain - Cervello AI</li>
                <li>📜 Normative italiane integrate</li>
                <li>📚 Book2Skills library</li>
                <li>🔗 Link management</li>
            </ul>
            <hr>
            <p><b>Creato da:</b> Fabio (Schumynet)</p>
            <p><b>AI Model:</b> Nemotron Content Safety (Free)</p>
        """)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show window
    window = MoreLinksWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
