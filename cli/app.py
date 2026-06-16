#!/usr/bin/env python3
"""
MoreLinks - Complete Management Platform
CLI Application with Persistent Memory Chatbot
"""

import sys
import os
import cmd
import json
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from morelinks import (
    MoreLinks, MoreLinksChatbot, ActionResult,
    PersistentMemory, AdministrativeMemory,
    NormativeKnowledge, Database,
    LinkCreate, LinkUpdate
)


class MoreLinksCLI(cmd.Cmd):
    """
    MoreLinks Command Line Interface
    Interactive chatbot with persistent memory
    """
    
    intro = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███╗   ███╗███████╗███████╗████████╗ ██████╗██╗      ██╗ ║
║   ████╗ ████║██╔════╝██╔════╝╚══██╔══╝██╔════╝██║      ██║ ║
║   ██╔████╔██║█████╗  █████╗     ██║   ██║     ██║█████╗██║ ║
║   ██║╚██╔╝██║██╔══╝  ██╔══╝     ██║   ██║     ██║╚════╝██║ ║
║   ██║ ╚═╝ ██║███████╗███████╗   ██║   ╚██████╗██║      ██║ ║
║   ╚═╝     ╚═╝╚══════╝╚══════╝   ╚═╝    ╚═════╝╚═╝      ╚═╝ ║
║                                                              ║
║   Piattaforma Completa di Gestione con Chatbot AI             ║
║   Memoria Persistente - Non Dimentica Mai!                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🤖 Benvenuto! Sono il tuo assistente AI con memoria permanente.
📋 Ricordo TUTTO ciò che mi dici - non dimenticherò mai nulla!

Scrivi 'aiuto' per vedere tutti i comandi disponibili.
Scrivi 'chat' per iniziare una conversazione con il chatbot.
Scrivi 'norme' per consultare le normative italiane.

"""
    
    prompt = "(MoreLinks) "
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.db = Database("morelinks.db")
        self.ml = MoreLinks(db_path="morelinks.db")
        self.memory = PersistentMemory("morelinks_memory.db")
        self.admin_memory = AdministrativeMemory(self.memory)
        self.chatbot = MoreLinksChatbot(database=self.db)
        self.normative = NormativeKnowledge(self.db)
        
        # Session info
        self.session_id = str(datetime.now().timestamp())
        self.user_id = "admin_default"
        self.user_name = "Admin"
        self.is_chat_mode = False
        
        # Create default admin profile
        self.memory.create_or_update_profile(
            user_id=self.user_id,
            name=self.user_name,
            email="admin@morelinks.local",
            role="admin"
        )
        
        print(f"\n✅ Sistema inizializzato!")
        print(f"📊 Link nel database: {len(self.db.list_links())}")
        print(f"💾 Messaggi salvati: {self.memory.get_memory_stats(self.user_id)['total_messages']}")
        print()
    
    # ==================== GENERAL COMMANDS ====================
    
    def do_aiuto(self, arg):
        """Mostra l'elenco completo dei comandi"""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║                    COMANDI DISPONIBILI                        ║
╚══════════════════════════════════════════════════════════════╝

🎯 GESTIONE LINK:
   link nuova <url>           - Crea un nuovo short link
   link lista                 - Mostra tutti i link
   link stats <codice>       - Statistiche di un link
   link elimina <codice>      - Elimina un link
   link aggiorna <codice>     - Aggiorna un link
   qr <codice>                - Genera QR code

📊 ANALYTICS:
   stats                      - Dashboard completa
   top                        - Top link per click
   analytics                  - Report dettagliato

💬 CHATBOT (usa 'chat' per modalità conversazione):
   chat <messaggio>           - Parla con l'AI
   chat storia                - Mostra cronologia
   chat cerca <query>         - Cerca nella memoria
   chat dimentica            - Pulisci schermo

📚 NORMATIVE:
   norme                      - Lista normative
   norme cerca <termine>      - Cerca normative
   norme obblighi <norma>    - Obblighi specifici
   norme sanzioni <norma>     - Sanzioni per violazioni
   norme scadenze             - Prossime scadenze

👤 PROFILO:
   profile                    - Il tuo profilo
   profile aggiorna <campo>   - Aggiorna profilo

📋 TASK:
   task nuova <titolo>        - Crea task
   task lista                 - Lista task
   task completa <id>         - Completa task

💼 BUSINESS:
   business info              - Info azienda
   business contatti          - Contatti salvati
   business ricorda <info>    - Salva informazione

🔧 SISTEMA:
   status                     - Stato sistema
   memoria                    - Statistiche memoria
   chiudi                     - Esci

"""
        print(help_text)
    
    def do_aiuto(self, arg):
        """Mostra l'elenco dei comandi (alias di aiuto)"""
        self.do_aiuto(arg)
    
    def do_help(self, arg):
        """Mostra l'aiuto"""
        self.do_aiuto("")
    
    # ==================== LINK MANAGEMENT ====================
    
    def do_link(self, arg):
        """Gestione link - link <azione> [parametri]"""
        args = arg.split(maxsplit=2)
        if not args:
            print("Uso: link <nuova|lista|stats|elimina|aggiorna> [parametri]")
            return
        
        action = args[0].lower()
        
        if action == "nuova" and len(args) > 1:
            url = args[1]
            title = args[2] if len(args) > 2 else None
            
            try:
                link_data = LinkCreate(original_url=url, title=title)
                link = self.db.create_link(link_data)
                
                self.memory.save_message(
                    session_id=self.session_id,
                    user_id=self.user_id,
                    role="assistant",
                    message=f"Link creato: {link.short_url}",
                    action_taken="create_link"
                )
                
                print(f"\n✅ Link creato con successo!")
                print(f"🔗 URL: {link.short_url}")
                print(f"📌 Titolo: {title or 'N/A'}")
                print(f"👆 Click: {link.click_count}")
                
                # Save to memory
                self.admin_memory.store_business_info(
                    self.user_id, "links", link.short_code,
                    {"url": str(link.original_url), "title": title, "created": str(link.created_at)}
                )
                
            except Exception as e:
                print(f"❌ Errore: {e}")
        
        elif action == "lista":
            links = self.db.list_links(limit=50)
            
            if not links:
                print("\n📭 Nessun link trovato. Creane uno con 'link nuova <url>'")
                return
            
            print("\n📋 I TUOI LINK:\n")
            print(f"{'#':<3} {'Codice':<10} {'URL':<40} {'Click':<8} {'Titolo'}")
            print("-" * 80)
            
            for i, link in enumerate(links, 1):
                title = (link.title or link.short_code)[:20]
                url = str(link.original_url)[:38]
                print(f"{i:<3} {link.short_code:<10} {url:<40} {link.click_count:<8} {title}")
            
            print()
        
        elif action == "stats" and len(args) > 1:
            short_code = args[1]
            link = self.db.get_link(short_code=short_code)
            
            if not link:
                print(f"❌ Link '{short_code}' non trovato")
                return
            
            summary = self.db.get_analytics_summary(link.id)
            
            print(f"\n📊 STATS - {short_code}:\n")
            print(f"🔗 URL: {link.short_url}")
            print(f"📌 Titolo: {link.title or 'N/A'}")
            print(f"👆 Click totali: {summary.total_clicks}")
            print(f"👥 Visitatori unici: {summary.unique_visitors}")
            print(f"📅 Creato: {link.created_at.strftime('%d/%m/%Y %H:%M')}")
            print(f"🌍 Top paesi: {', '.join(summary.top_countries.keys()) or 'N/A'}")
            print()
        
        elif action == "elimina" and len(args) > 1:
            short_code = args[1]
            link = self.db.get_link(short_code=short_code)
            
            if not link:
                print(f"❌ Link '{short_code}' non trovato")
                return
            
            self.db.delete_link(link.id)
            print(f"🗑️ Link '{short_code}' eliminato!")
        
        elif action == "aggiorna" and len(args) > 1:
            parts = ' '.join(args[1:]).split('titolo:')
            short_code = parts[0].strip()
            new_title = parts[1].strip() if len(parts) > 1 else None
            
            if not new_title:
                print("Uso: link aggiorna <codice> titolo:<nuovo titolo>")
                return
            
            link = self.db.get_link(short_code=short_code)
            if not link:
                print(f"❌ Link '{short_code}' non trovato")
                return
            
            updated = self.db.update_link(link.id, LinkUpdate(title=new_title))
            print(f"✅ Link aggiornato! Nuovo titolo: {new_title}")
        
        else:
            print("Uso: link <nuova|lista|stats|elimina|aggiorna> [parametri]")
    
    def do_qr(self, arg):
        """Genera QR code per un link"""
        if not arg:
            print("Uso: qr <codice>")
            return
        
        short_code = arg.strip()
        link = self.db.get_link(short_code=short_code)
        
        if not link:
            print(f"❌ Link '{short_code}' non trovato")
            return
        
        print(f"\n📱 QR CODE per {short_code}:\n")
        print(f"🔗 URL: {link.short_url}")
        print("""
    ██████████████████████████████
    ██ ████  ██ ████  ████  ██ ██
    ██ ████  ██ ████  ████  ██ ██
    ██    ██    ████    ██     ██
    ██ ████  ██ ████  ████  ██ ██
    ██ ████  ██ ████  ████  ██ ██
    ██    ██    ████    ██     ██
    ██ ████  ██ ████  ████  ██ ██
    ██ ████  ██ ████  ████  ██ ██
    ██████████████████████████████
""")
        print(f"💾 Scarica l'immagine QR dalla dashboard!")
    
    # ==================== CHATBOT MODE ====================
    
    def do_chat(self, arg):
        """Modalità chat con il chatbot AI"""
        args = arg.strip()
        
        if not args:
            print("\n💬 Modalità chat attivata!")
            print("   Scrivi 'exit' per tornare al prompt normale")
            print("   Scrivi 'aiuto' per vedere i comandi chatbot\n")
            self.is_chat_mode = True
            self.prompt = "(💬) "
            return
        
        # Special commands
        if args.lower() == "storia":
            history = self.memory.get_conversation_history(self.user_id, limit=20)
            print("\n📜 ULTIME CONVERSAZIONI:\n")
            for msg in history[-10:]:
                role = "👤" if msg["role"] == "user" else "🤖"
                print(f"{role} [{msg['timestamp'][:16]}] {msg['message'][:100]}")
            print()
            return
        
        if args.lower() == "cerca" and len(args.split()) > 1:
            query = ' '.join(args.split()[1:])
            results = self.memory.search_conversations(self.user_id, query)
            print(f"\n🔍 Risultati per '{query}':")
            for r in results[:5]:
                print(f"   - {r['message'][:80]}...")
            print()
            return
        
        if args.lower() == "dimentica":
            print("🧹 La memoria è PERMANENTE - non posso dimenticare!")
            print("   Ma posso mostraroti cosa ricordo...")
            stats = self.memory.get_memory_stats(self.user_id)
            print(f"\n📊 Ho salvato: {stats['total_messages']} messaggi")
            print(f"   Ho imparato: {stats['total_facts_learned']} fatti su di te")
            return
        
        # Process with chatbot
        result = self.chatbot.process(args, self.user_id)
        
        # Save to persistent memory
        self.memory.save_message(
            session_id=self.session_id,
            user_id=self.user_id,
            role="user",
            message=args,
            intent=result.action_type,
            action_taken=result.action_type
        )
        
        self.memory.save_message(
            session_id=self.session_id,
            user_id=self.user_id,
            role="assistant",
            message=result.message,
            intent=result.action_type,
            action_taken=result.action_type,
            result_data=result.data
        )
        
        print(f"\n🤖 {result.message}")
        
        # Learn facts from conversation
        if "mi chiamo" in args.lower():
            name = args.lower().split("mi chiamo")[-1].strip().split()[0]
            self.memory.learn_fact(self.user_id, "personal", "name", name)
            self.user_name = name.capitalize()
            self.memory.create_or_update_profile(self.user_id, name=self.user_name)
    
    def do_norme(self, arg):
        """Consulta le normative italiane"""
        args = arg.strip()
        
        if not args:
            categories = self.normative.get_categories()
            print("\n📚 NORMATIVE ITALIANE:\n")
            for cat in categories:
                norms = self.normative.get_by_category(cat)
                print(f"📁 {cat} ({len(norms)})")
            print("\nUsa 'norme cerca <termine>' per cercare normative specifiche")
            return
        
        parts = args.split(maxsplit=1)
        action = parts[0].lower()
        query = parts[1] if len(parts) > 1 else ""
        
        if action == "cerca":
            results = self.normative.search(query)
            print(f"\n🔍 Risultati per '{query}':\n")
            for r in results[:5]:
                print(f"📌 {r['title']}")
                print(f"   {r['description'][:100]}...")
                print()
        
        elif action == "obblighi":
            results = self.normative.search(query)
            if results:
                norm = results[0]
                print(f"\n⚠️ OBBLIGHI - {norm['title']}:\n")
                for i, obl in enumerate(norm.get('obligations', [])[:10], 1):
                    print(f"{i}. {obl}")
                print()
        
        elif action == "sanzioni":
            results = self.normative.search(query)
            if results:
                norm = results[0]
                print(f"\n⚖️ SANZIONI - {norm['title']}:\n")
                print(norm.get('penalties', 'Consulta il testo ufficiale'))
                print()
        
        elif action == "scadenze":
            deadlines = self.normative.get_upcoming_deadlines(30)
            print("\n📅 PROSSIME SCADENZE:\n")
            for dl in deadlines[:10]:
                print(f"⏰ {dl['name']}")
                print(f"   {dl['when']} - {dl['regulation']}")
                print()
    
    # ==================== STATS & ANALYTICS ====================
    
    def do_stats(self, arg):
        """Mostra statistiche generali"""
        summary = self.db.get_analytics_summary()
        
        print("""
╔══════════════════════════════════════════════════════════════╗
║                    📊 DASHBOARD MORELINKS                    ║
╚══════════════════════════════════════════════════════════════╝
""")
        print(f"👆 Click totali: {summary.total_clicks}")
        print(f"👥 Visitatori unici: {summary.unique_visitors}")
        print(f"\n🌍 Top paesi:")
        for country, count in list(summary.top_countries.items())[:5]:
            print(f"   • {country}: {count}")
        print(f"\n📱 Dispositivi:")
        for device, count in list(summary.top_devices.items())[:3]:
            print(f"   • {device}: {count}")
        print()
    
    def do_top(self, arg):
        """Top link per click"""
        links = self.db.list_links(limit=20)
        sorted_links = sorted(links, key=lambda x: x.click_count, reverse=True)
        
        print("\n🏆 TOP LINK:\n")
        medals = ["🥇", "🥈", "🥉", "4.", "5."]
        
        for i, link in enumerate(sorted_links[:5], 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            print(f"{medal} {link.title or link.short_code}: {link.click_count} click")
        
        print()
    
    # ==================== PROFILE & TASKS ====================
    
    def do_profile(self, arg):
        """Gestione profilo"""
        args = arg.split(maxsplit=1)
        
        if not args or args[0] != "aggiorna":
            profile = self.memory.create_or_update_profile(self.user_id, name=self.user_name)
            facts = self.memory.get_learned_facts(self.user_id)
            stats = self.memory.get_memory_stats(self.user_id)
            
            print(f"\n👤 PROFILO:\n")
            print(f"   Nome: {profile.name}")
            print(f"   Email: {profile.email}")
            print(f"   ID: {profile.id}")
            print(f"   Ruolo: {profile.role}")
            print(f"   Creato: {profile.created_at[:10]}")
            print(f"   Ultimo accesso: {profile.last_seen[:16]}")
            print(f"\n📊 STATISTICHE:")
            print(f"   Messaggi salvati: {stats['total_messages']}")
            print(f"   Fatti appresi: {stats['total_facts_learned']}")
            print(f"   Task pendenti: {stats['pending_tasks']}")
            print()
            return
        
        # Update profile
        if len(args) > 1:
            field = args[1]
            self.memory.create_or_update_profile(self.user_id, name=field)
            print(f"✅ Profilo aggiornato: {field}")
    
    def do_task(self, arg):
        """Gestione task"""
        args = arg.split(maxsplit=2)
        if not args:
            tasks = self.memory.get_tasks(self.user_id)
            print("\n📋 TASK:\n")
            for t in tasks[:10]:
                status = "✅" if t["status"] == "completed" else "⏳"
                print(f"{status} [{t['id'][:8]}] {t['title']}")
                if t.get('due_date'):
                    print(f"   📅 Scadenza: {t['due_date']}")
            print()
            return
        
        action = args[0].lower()
        
        if action == "nuova" and len(args) > 1:
            title = args[1]
            desc = args[2] if len(args) > 2 else None
            task_id = self.memory.create_task(self.user_id, title, desc)
            print(f"✅ Task creata: {title}")
        
        elif action == "completa" and len(args) > 1:
            task_id = args[1]
            self.memory.complete_task(task_id)
            print(f"✅ Task completata!")
    
    # ==================== BUSINESS FEATURES ====================
    
    def do_business(self, arg):
        """Funzioni business"""
        args = arg.strip()
        
        if args == "info":
            summary = self.admin_memory.get_business_summary(self.user_id)
            print("\n💼 INFO AZIENDA:\n")
            print(f"   Link attivi: {len(summary['active_links'])}")
            print(f"   Contatti salvati: {len(summary['contacts'])}")
            print(f"   Task pendenti: {len(summary['pending_tasks'])}")
            print()
        
        elif args == "contatti":
            contacts = self.memory.get_learned_facts(self.user_id, "contacts")
            print("\n👥 CONTATTI SALVATI:\n")
            for c in contacts[:10]:
                try:
                    data = json.loads(c['fact_value'])
                    print(f"   📱 {data.get('name', 'N/A')} - {data.get('email', 'N/A')}")
                except:
                    print(f"   • {c['fact_key']}")
            print()
        
        elif args.startswith("ricorda"):
            info = args.replace("ricorda", "").strip()
            if info:
                self.admin_memory.store_business_info(self.user_id, "general", "note", info)
                print(f"✅ Ricordato: {info}")
    
    # ==================== SYSTEM ====================
    
    def do_status(self, arg):
        """Stato sistema"""
        info = self.ml.info()
        stats = self.memory.get_memory_stats(self.user_id)
        
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                      🔧 STATO SISTEMA                         ║
╠══════════════════════════════════════════════════════════════╣
║  MoreLinks Version: {info['version']:<42} ║
║  Edition: {info['edition_name']:<46} ║
║  Database: ✅ Connesso                                        ║
║  Chatbot: ✅ Attivo                                          ║
║  Memoria: ✅ Persistente                                    ║
╠══════════════════════════════════════════════════════════════╣
║  Link totali: {info['stats']['total_links']:<45} ║
║  Click totali: {info['stats']['total_clicks']:<43} ║
║  Messaggi salvati: {stats['total_messages']:<41} ║
║  Fatti appresi: {stats['total_facts_learned']:<43} ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    def do_memoria(self, arg):
        """Statistiche memoria"""
        stats = self.memory.get_memory_stats(self.user_id)
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    💾 STATISTICHE MEMORIA                     ║
╠══════════════════════════════════════════════════════════════╣
║  📝 Messaggi totali: {stats['total_messages']:<40} ║
║  📚 Fatti appresi: {stats['total_facts_learned']:<41} ║
║  📋 Task pendenti: {stats['pending_tasks']:<42} ║
║  💭 Topic discussi: {stats['topics_discussed']:<41} ║
╠══════════════════════════════════════════════════════════════╣
║  🧠 La memoria è PERMANENTE - Non dimentico MAI nulla!       ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    def do_chiudi(self, arg):
        """Chiudi l'applicazione"""
        print("\n👋 Arrivederci! La memoria è stata salvata permanentemente.")
        print("   Ci vediamo presto!\n")
        self.db.close()
        self.memory.close()
        return True
    
    def do_exit(self, arg):
        """Alias per chiudi"""
        return self.do_chiudi("")
    
    def do_quit(self, arg):
        """Alias per chiudi"""
        return self.do_chiudi("")
    
    # ==================== SHORTCUTS ====================
    
    def do_stato(self, arg):
        """Alias per status"""
        self.do_status("")
    
    def do_info(self, arg):
        """Alias per status"""
        self.do_status("")
    
    def emptyline(self):
        """Non fare nulla con linea vuota"""
        pass
    
    def default(self, line):
        """Gestisci comandi sconosciuti"""
        if line.lower() in ['exit', 'quit', 'q']:
            return self.do_chiudi("")
        
        # Pass to chatbot as fallback
        print(f"\n🤖 {line}")
        self.do_chat(line)


def main():
    """Entry point"""
    print(MoreLinksCLI.intro)
    cli = MoreLinksCLI()
    
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("\n\n👋 Arrivederci!")
        cli.db.close()
        cli.memory.close()


if __name__ == "__main__":
    main()
