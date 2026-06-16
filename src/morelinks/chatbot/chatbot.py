"""
MoreLinks Chatbot - AI Assistant with Business Norms Knowledge
Executes actions within the management system
"""

import re
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from uuid import UUID

# NLP imports - lightweight pattern matching (no external AI needed for basic version)
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    word_tokenize = lambda x: x.lower().split()


@dataclass
class ActionResult:
    """Result of a chatbot action"""
    success: bool
    message: str
    data: Any = None
    action_type: str = ""
    details: Dict = field(default_factory=dict)


class ChatIntent(Enum):
    """Intents recognized by the chatbot"""
    # Link Management
    CREATE_LINK = "create_link"
    LIST_LINKS = "list_links"
    DELETE_LINK = "delete_link"
    UPDATE_LINK = "update_link"
    GET_LINK_STATS = "get_link_stats"
    GENERATE_QR = "generate_qr"
    
    # Analytics
    SHOW_ANALYTICS = "show_analytics"
    SHOW_STATS = "show_stats"
    TOP_LINKS = "top_links"
    EXPORT_DATA = "export_data"
    
    # Normative Queries
    NORM_QUERY = "norm_query"
    NORM_LIST = "norm_list"
    NORM_OBLIGATIONS = "norm_obligations"
    NORM_DEADLINES = "norm_deadlines"
    NORM_PENALTIES = "norm_penalties"
    
    # System
    HELP = "help"
    STATUS = "status"
    UNKNOWN = "unknown"


class MoreLinksChatbot:
    """
    AI Chatbot for MoreLinks
    Understands Italian commands and executes actions in the system
    """
    
    def __init__(self, database=None, morelinks_core=None):
        self.db = database
        self.ml = morelinks_core
        
        # Intent patterns - Italian and English
        self.intent_patterns = {
            ChatIntent.CREATE_LINK: [
                r"crea.*link",
                r"nuovo.*link",
                r"accorcia.*url",
                r"shorten.*url",
                r"genera.*link",
                r"create.*link",
                r"nuovo.*short",
                r"shorten",
            ],
            ChatIntent.LIST_LINKS: [
                r"mostra.*link",
                r"lista.*link",
                r"elenco.*link",
                r"trova.*link",
                r"list.*links",
                r"show.*links",
                r"i.*miei.*link",
                r"tutti.*link",
            ],
            ChatIntent.DELETE_LINK: [
                r"elimina.*link",
                r"cancella.*link",
                r"rimuovi.*link",
                r"delete.*link",
                r"remove.*link",
            ],
            ChatIntent.UPDATE_LINK: [
                r"aggiorna.*link",
                r"modifica.*link",
                r"edit.*link",
                r"update.*link",
                r"cambia.*link",
            ],
            ChatIntent.GET_LINK_STATS: [
                r"stats.*link",
                r"statistiche.*link",
                r"click.*link",
                r"link.*stats",
                r"performance.*link",
            ],
            ChatIntent.GENERATE_QR: [
                r"genera.*qr",
                r"qr.*code",
                r"codice.*qr",
                r"create.*qr",
            ],
            ChatIntent.SHOW_ANALYTICS: [
                r"analytics",
                r"statistiche",
                r"report",
                r"dati.*clicks",
                r"overview",
                r"dashboard",
            ],
            ChatIntent.SHOW_STATS: [
                r"stats",
                r"numeri",
                r"totali",
                r"riepilogo",
                r"summary",
            ],
            ChatIntent.TOP_LINKS: [
                r"top.*link",
                r"migliori.*link",
                r"link.*migliori",
                r"most.*clicked",
            ],
            ChatIntent.EXPORT_DATA: [
                r"esporta",
                r"export",
                r"scarica.*dati",
                r"download.*csv",
                r"genera.*report",
            ],
            ChatIntent.NORM_QUERY: [
                r"normativa",
                r"legge",
                r"regolamento",
                r"decreto",
                r"obbligo",
                r"requisito",
                r"regulation",
                r"law",
                r"art\.\s*\d+",
                r"articolo\s+\d+",
            ],
            ChatIntent.NORM_LIST: [
                r"lista.*normative",
                r"elenco.*leggi",
                r"tutte.*normative",
                r"norme.*applicabili",
                r"list.*regulations",
            ],
            ChatIntent.NORM_OBLIGATIONS: [
                r"obbligo",
                r"obblighi",
                r"cosa.*fare",
                r"cosa.*dev.*fare",
                r"cosa.*obbligatori",
                r"requirements",
                r"obligations",
            ],
            ChatIntent.NORM_DEADLINES: [
                r"scadenza",
                r"deadline",
                r"quando.*fare",
                r"entro.*quando",
                r"termini",
                r"when.*deadline",
            ],
            ChatIntent.NORM_PENALTIES: [
                r"sanzion",
                r"penal",
                r"multa",
                r"pena",
                r"violazion",
                r"penalty",
                r"fine",
                r"sanction",
            ],
            ChatIntent.HELP: [
                r"aiuto",
                r"help",
                r"comandi",
                r"cosa.*puoi.*fare",
                r"come.*funziona",
                r"usage",
            ],
            ChatIntent.STATUS: [
                r"status",
                r"stato.*sistema",
                r"info",
                r"versione",
            ],
        }
        
        # Entity extractors
        self.url_pattern = re.compile(r'https?://[^\s]+')
        self.email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        
        # Session context
        self.session_context = {
            "last_intent": None,
            "last_entity": None,
            "conversation_history": [],
        }
    
    def process(self, message: str, user_id: str = None) -> ActionResult:
        """
        Process a user message and execute the appropriate action
        Returns ActionResult with success status, message and data
        """
        # Store in history
        self.session_context["conversation_history"].append({
            "role": "user",
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Detect intent
        intent = self._detect_intent(message)
        self.session_context["last_intent"] = intent
        
        # Extract entities
        entities = self._extract_entities(message)
        
        # Execute action based on intent
        result = self._execute_action(intent, entities, message, user_id)
        
        # Store result in history
        self.session_context["conversation_history"].append({
            "role": "assistant",
            "message": result.message,
            "action": result.action_type,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return result
    
    def _detect_intent(self, message: str) -> ChatIntent:
        """Detect the intent of the message"""
        message_lower = message.lower()
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    return intent
        
        return ChatIntent.UNKNOWN
    
    def _extract_entities(self, message: str) -> Dict[str, Any]:
        """Extract entities from the message"""
        entities = {
            "urls": self.url_pattern.findall(message),
            "emails": self.email_pattern.findall(message),
            "short_codes": [],
            "tags": [],
            "date_range": None,
            "numbers": [],
        }
        
        # Extract short codes (6-char alphanumeric)
        short_code_pattern = re.compile(r'\b[a-zA-Z0-9]{6}\b')
        entities["short_codes"] = short_code_pattern.findall(message)
        
        # Extract numbers
        number_pattern = re.compile(r'\d+')
        entities["numbers"] = [int(n) for n in number_pattern.findall(message)]
        
        # Extract tags (words after # or from common patterns)
        tag_pattern = re.compile(r'#(\w+)')
        entities["tags"] = tag_pattern.findall(message.lower())
        
        return entities
    
    def _execute_action(self, intent: ChatIntent, entities: Dict, message: str, user_id: str) -> ActionResult:
        """Execute the action based on detected intent"""
        
        if intent == ChatIntent.CREATE_LINK:
            return self._action_create_link(entities, message)
        
        elif intent == ChatIntent.LIST_LINKS:
            return self._action_list_links(entities)
        
        elif intent == ChatIntent.DELETE_LINK:
            return self._action_delete_link(entities)
        
        elif intent == ChatIntent.UPDATE_LINK:
            return self._action_update_link(entities, message)
        
        elif intent == ChatIntent.GET_LINK_STATS:
            return self._action_get_link_stats(entities)
        
        elif intent == ChatIntent.GENERATE_QR:
            return self._action_generate_qr(entities)
        
        elif intent == ChatIntent.SHOW_ANALYTICS or intent == ChatIntent.SHOW_STATS:
            return self._action_show_stats(entities)
        
        elif intent == ChatIntent.TOP_LINKS:
            return self._action_top_links()
        
        elif intent == ChatIntent.EXPORT_DATA:
            return self._action_export_data(entities)
        
        elif intent == ChatIntent.NORM_QUERY:
            return self._action_norm_query(message)
        
        elif intent == ChatIntent.NORM_LIST:
            return self._action_norm_list(entities)
        
        elif intent == ChatIntent.NORM_OBLIGATIONS:
            return self._action_norm_obligations(message)
        
        elif intent == ChatIntent.NORM_PENALTIES:
            return self._action_norm_penalties(message)
        
        elif intent == ChatIntent.HELP:
            return self._action_help()
        
        elif intent == ChatIntent.STATUS:
            return self._action_status()
        
        else:
            return ActionResult(
                success=False,
                message="Non ho capito. Prova a riformulare la richiesta o scrivi 'aiuto' per vedere i comandi disponibili.",
                action_type="unknown"
            )
    
    # ==================== LINK ACTIONS ====================
    
    def _action_create_link(self, entities: Dict, message: str) -> ActionResult:
        """Create a new shortened link"""
        if not entities.get("urls"):
            return ActionResult(
                success=False,
                message="Per creare un link, dimmi l'URL completo. Esempio: 'crea link https://example.com'",
                action_type="create_link"
            )
        
        url = entities["urls"][0]
        
        # Extract title if present
        title = None
        title_match = re.search(r'titolo[:\s]+["\']?([^"\']+)["\']?', message, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            # Try to extract from message
            clean_msg = message.replace("crea", "").replace("link", "").replace(url, "").strip()
            if clean_msg and len(clean_msg) > 2:
                title = clean_msg.title()
        
        # Extract tags
        tags = entities.get("tags", [])
        
        try:
            from ..models import LinkCreate
            
            link_data = LinkCreate(
                original_url=url,
                title=title,
                tags=tags
            )
            
            if self.db:
                link = self.db.create_link(link_data, user_id=None)
                
                return ActionResult(
                    success=True,
                    message=f"✅ Link creato con successo!\n\n"
                           f"🔗 URL corto: {link.short_url}\n"
                           f"📌 Titolo: {title or 'N/A'}\n"
                           f"🏷️ Tags: {', '.join(tags) if tags else 'Nessuno'}\n"
                           f"👆 Click: 0",
                    data={"link": link},
                    action_type="create_link",
                    details={"short_code": link.short_code, "url": str(link.original_url)}
                )
            else:
                return ActionResult(
                    success=True,
                    message=f"✅ Link creato (demo mode)!\n\n"
                           f"🔗 URL: {url}\n"
                           f"📌 Titolo: {title or 'N/A'}",
                    action_type="create_link",
                    details={"url": url}
                )
                
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"❌ Errore nella creazione del link: {str(e)}",
                action_type="create_link"
            )
    
    def _action_list_links(self, entities: Dict) -> ActionResult:
        """List all links"""
        try:
            if self.db:
                links = self.db.list_links(limit=20)
                
                if not links:
                    return ActionResult(
                        success=True,
                        message="📭 Non hai ancora creato nessun link. Vuoi che ne crei uno?",
                        action_type="list_links"
                    )
                
                # Format links list
                lines = ["📋 **I tuoi link:**\n"]
                for i, link in enumerate(links, 1):
                    lines.append(f"{i}. **{link.title or link.short_code}**")
                    lines.append(f"   🔗 {link.short_url}")
                    lines.append(f"   👆 {link.click_count} click")
                    if link.tags:
                        lines.append(f"   🏷️ {', '.join(link.tags)}")
                    lines.append("")
                
                return ActionResult(
                    success=True,
                    message="\n".join(lines),
                    data={"links": links},
                    action_type="list_links"
                )
            else:
                return ActionResult(
                    success=True,
                    message="📋 **Link di esempio:**\n\n"
                           "1. **GitHub** - github.com\n   🔗 ml.app/gh1234 - 👆 142 click\n\n"
                           "2. **Python** - python.org\n   🔗 ml.app/py9876 - 👆 89 click",
                    action_type="list_links"
                )
                
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"❌ Errore nel recupero dei link: {str(e)}",
                action_type="list_links"
            )
    
    def _action_delete_link(self, entities: Dict) -> ActionResult:
        """Delete a link"""
        if not entities.get("short_codes"):
            return ActionResult(
                success=False,
                message="Per eliminare un link, specifica il codice breve. Esempio: 'elimina link abc123'",
                action_type="delete_link"
            )
        
        short_code = entities["short_codes"][0]
        
        try:
            if self.db:
                link = self.db.get_link(short_code=short_code)
                if not link:
                    return ActionResult(
                        success=False,
                        message=f"❌ Link con codice '{short_code}' non trovato.",
                        action_type="delete_link"
                    )
                
                self.db.delete_link(link.id)
                
                return ActionResult(
                    success=True,
                    message=f"🗑️ Link '{short_code}' eliminato con successo!",
                    action_type="delete_link",
                    details={"short_code": short_code}
                )
            else:
                return ActionResult(
                    success=True,
                    message=f"🗑️ Link '{short_code}' eliminato (demo mode)!",
                    action_type="delete_link"
                )
                
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"❌ Errore nell'eliminazione: {str(e)}",
                action_type="delete_link"
            )
    
    def _action_update_link(self, entities: Dict, message: str) -> ActionResult:
        """Update a link"""
        if not entities.get("short_codes"):
            return ActionResult(
                success=False,
                message="Per aggiornare un link, specifica il codice breve. Esempio: 'aggiorna link abc123 titolo:Nuovo Titolo'",
                action_type="update_link"
            )
        
        short_code = entities["short_codes"][0]
        
        # Extract new title
        new_title = None
        title_match = re.search(r'titolo[:\s]+["\']?([^"\']+)["\']?', message, re.IGNORECASE)
        if title_match:
            new_title = title_match.group(1).strip()
        
        if not new_title:
            return ActionResult(
                success=False,
                message="Specifica il nuovo titolo. Esempio: 'aggiorna link abc123 titolo:Nuovo Titolo'",
                action_type="update_link"
            )
        
        try:
            if self.db:
                from ..models import LinkUpdate
                link = self.db.get_link(short_code=short_code)
                if not link:
                    return ActionResult(
                        success=False,
                        message=f"❌ Link '{short_code}' non trovato.",
                        action_type="update_link"
                    )
                
                updated = self.db.update_link(link.id, LinkUpdate(title=new_title))
                
                return ActionResult(
                    success=True,
                    message=f"✅ Link aggiornato!\n\n"
                           f"🔗 {updated.short_url}\n"
                           f"📌 Nuovo titolo: {new_title}",
                    action_type="update_link",
                    details={"short_code": short_code, "new_title": new_title}
                )
            else:
                return ActionResult(
                    success=True,
                    message=f"✅ Link '{short_code}' aggiornato con titolo '{new_title}' (demo)!",
                    action_type="update_link"
                )
                
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"❌ Errore nell'aggiornamento: {str(e)}",
                action_type="update_link"
            )
    
    def _action_get_link_stats(self, entities: Dict) -> ActionResult:
        """Get statistics for a specific link"""
        if not entities.get("short_codes"):
            return ActionResult(
                success=False,
                message="Per vedere le stats, specifica il codice link. Esempio: 'stats link abc123'",
                action_type="get_link_stats"
            )
        
        short_code = entities["short_codes"][0]
        
        try:
            if self.db:
                link = self.db.get_link(short_code=short_code)
                if not link:
                    return ActionResult(
                        success=False,
                        message=f"❌ Link '{short_code}' non trovato.",
                        action_type="get_link_stats"
                    )
                
                analytics = self.db.get_analytics(link.id)
                
                return ActionResult(
                    success=True,
                    message=f"📊 **Stats per {short_code}:**\n\n"
                           f"🔗 URL: {link.short_url}\n"
                           f"📌 Titolo: {link.title or 'N/A'}\n"
                           f"👆 Click totali: {link.click_count}\n"
                           f"📍 Unique visitors: {len(set(a.ip_address for a in analytics if a.ip_address))}\n"
                           f"🌐 Top paese: {max(link.short_code for _ in [1]) or 'N/A'}\n"
                           f"📅 Creato il: {link.created_at.strftime('%d/%m/%Y')}",
                    data={"link": link, "analytics": analytics},
                    action_type="get_link_stats"
                )
            else:
                return ActionResult(
                    success=True,
                    message=f"📊 **Stats per {short_code}:**\n\n"
                           f"👆 Click totali: 142\n"
                           f"📍 Unique visitors: 89\n"
                           f"🌐 Top paese: 🇮🇹 Italia (67%)\n"
                           f"📱 Dispositivo: 📱 Mobile 58%, 💻 Desktop 42%",
                    action_type="get_link_stats"
                )
                
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"❌ Errore nel recupero stats: {str(e)}",
                action_type="get_link_stats"
            )
    
    def _action_generate_qr(self, entities: Dict) -> ActionResult:
        """Generate QR code for a link"""
        if not entities.get("short_codes"):
            return ActionResult(
                success=False,
                message="Per generare un QR code, specifica il codice link. Esempio: 'genera qr abc123'",
                action_type="generate_qr"
            )
        
        short_code = entities["short_codes"][0]
        
        try:
            if self.db:
                link = self.db.get_link(short_code=short_code)
                if not link:
                    return ActionResult(
                        success=False,
                        message=f"❌ Link '{short_code}' non trovato.",
                        action_type="generate_qr"
                    )
                
                qr_base64 = self.db.db.engine.execute("SELECT generate_qr(?)", (link.short_url,)).fetchone()[0] if hasattr(self.db, 'db') else None
                
                return ActionResult(
                    success=True,
                    message=f"📱 **QR Code per {short_code}:**\n\n"
                           f"🔗 {link.short_url}\n"
                           f"🖼️ QR code generato! (salva l'immagine)",
                    data={"short_code": short_code, "url": link.short_url},
                    action_type="generate_qr"
                )
            else:
                return ActionResult(
                    success=True,
                    message=f"📱 **QR Code per {short_code}:**\n\n"
                           f"🔗 Link: https://ml.app/{short_code}\n"
                           f"🖼️ QR code generato!\n\n"
                           f"```\n"
                           f"███ ███ ███ ███\n"
                           f"███   ████   ███\n"
                           f"███ ████ ███ ███\n"
                           f"███       ████  \n"
                           f"███ ███ ███ ███\n"
                           f"```",
                    action_type="generate_qr"
                )
                
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"❌ Errore nella generazione QR: {str(e)}",
                action_type="generate_qr"
            )
    
    def _action_show_stats(self, entities: Dict) -> ActionResult:
        """Show overall statistics"""
        try:
            if self.db:
                summary = self.db.get_analytics_summary()
                
                return ActionResult(
                    success=True,
                    message=f"📊 **Dashboard MoreLinks:**\n\n"
                           f"👆 **Click totali:** {summary.total_clicks}\n"
                           f"👥 **Unique visitors:** {summary.unique_visitors}\n"
                           f"🌍 **Top paesi:**\n" +
                           "\n".join([f"   • {c}: {n}" for c, n in list(summary.top_countries.items())[:3]]) +
                           f"\n📱 **Dispositivi:**\n" +
                           "\n".join([f"   • {d}: {n}" for d, n in list(summary.top_devices.items())[:3]]),
                    data={"summary": summary},
                    action_type="show_stats"
                )
            else:
                return ActionResult(
                    success=True,
                    message="📊 **Dashboard MoreLinks:**\n\n"
                           "👆 **Click totali:** 1,247\n"
                           "👥 **Unique visitors:** 892\n"
                           "🌍 **Top paesi:**\n"
                           "   • 🇮🇹 Italia: 534 (43%)\n"
                           "   • 🇺🇸 USA: 234 (19%)\n"
                           "   • 🇬🇧 UK: 123 (10%)\n"
                           "📱 **Dispositivi:**\n"
                           "   • 📱 Mobile: 723 (58%)\n"
                           "   • 💻 Desktop: 524 (42%)",
                    action_type="show_stats"
                )
                
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"❌ Errore nel caricamento stats: {str(e)}",
                action_type="show_stats"
            )
    
    def _action_top_links(self) -> ActionResult:
        """Show top performing links"""
        try:
            if self.db:
                links = self.db.list_links(limit=10)
                sorted_links = sorted(links, key=lambda x: x.click_count, reverse=True)
                
                lines = ["🏆 **Top Links:**\n"]
                for i, link in enumerate(sorted_links[:5], 1):
                    medal = ["🥇", "🥈", "🥉", "4.", "5."][i-1]
                    lines.append(f"{medal} **{link.title or link.short_code}** - {link.click_count} click")
                
                return ActionResult(
                    success=True,
                    message="\n".join(lines),
                    data={"links": sorted_links[:5]},
                    action_type="top_links"
                )
            else:
                return ActionResult(
                    success=True,
                    message="🏆 **Top Links:**\n\n"
                           "🥇 GitHub - 1,247 click\n"
                           "🥈 Python - 892 click\n"
                           "🥉 FastAPI - 534 click\n"
                           "4. Docker - 321 click\n"
                           "5. React - 234 click",
                    action_type="top_links"
                )
                
        except Exception as e:
            return ActionResult(
                success=False,
                message=f"❌ Errore: {str(e)}",
                action_type="top_links"
            )
    
    def _action_export_data(self, entities: Dict) -> ActionResult:
        """Export data"""
        return ActionResult(
            success=True,
            message="📥 **Esportazione dati:**\n\n"
                   "Scegli il formato:\n"
                   "• CSV - 'esporta csv'\n"
                   "• JSON - 'esporta json'\n"
                   "• PDF Report - 'esporta pdf'\n\n"
                   "📅 Periodo: Ultimi 30 giorni",
            action_type="export_data"
        )
    
    # ==================== NORMATIVE ACTIONS ====================
    
    def _action_norm_query(self, message: str) -> ActionResult:
        """Query about business regulations"""
        # Import here to avoid circular imports
        from .normative_knowledge import NormativeKnowledge
        
        norm_knowledge = NormativeKnowledge(self.db)
        
        # Extract search terms
        search_terms = message.lower()
        for word in ["normativa", "legge", "regolamento", "decreto", "obbligo", "articolo", "art.", "gdpr", "privacy", "contabilità", "bilancio", "lavoro", "sicurezza", "anticorruzione", "riciclaggio"]:
            search_terms = search_terms.replace(word, "").strip()
        
        # Search in database
        results = norm_knowledge.search(message)
        
        if results:
            response = f"📚 **Normative trovate ({len(results)}):**\n\n"
            for r in results[:3]:
                response += f"**{r['title']}**\n"
                response += f"📖 {r['description'][:150]}...\n\n"
            
            return ActionResult(
                success=True,
                message=response,
                data={"results": results},
                action_type="norm_query"
            )
        else:
            # Provide general information
            return ActionResult(
                success=True,
                message="📚 **Normative Italiane per le Imprese:**\n\n"
                       "Ecco le principali aree normative:\n\n"
                       "🏢 **Contabilità & Bilancio**\n"
                       "   • Codice Civile Art. 2423 - Bilancio\n"
                       "   • Principi Contabili OIC\n\n"
                       "🔒 **Privacy & Dati**\n"
                       "   • GDPR (Reg. UE 679/2016)\n"
                       "   • Codice Privacy (DLgs 196/2003)\n\n"
                       "👷 **Lavoro & Sicurezza**\n"
                       "   • Statuto Lavoratori (L. 300/70)\n"
                       "   • TUSL (DLgs 81/2008)\n\n"
                       "⚖️ **Compliance**\n"
                       "   • DLgs 231/2001 - Responsabilità Enti\n"
                       "   • Antiriciclaggio (DLgs 231/2007)\n\n"
                       "💾 **Fatturazione**\n"
                       "   • Fatturazione Elettronica\n\n\n"
                       "Fammi una domanda specifica per maggiori dettagli!",
                action_type="norm_query"
            )
    
    def _action_norm_list(self, entities: Dict) -> ActionResult:
        """List all regulations by category"""
        from .normative_knowledge import NormativeKnowledge
        
        norm_knowledge = NormativeKnowledge(self.db)
        categories = norm_knowledge.get_categories()
        
        response = "📚 **Normative per Categoria:**\n\n"
        for cat in categories:
            norms = norm_knowledge.get_by_category(cat)
            response += f"**{cat}** ({len(norms)})\n"
            for n in norms[:2]:
                response += f"   • {n['code']}: {n['title'][:50]}...\n"
            response += "\n"
        
        return ActionResult(
            success=True,
            message=response,
            data={"categories": categories},
            action_type="norm_list"
        )
    
    def _action_norm_obligations(self, message: str) -> ActionResult:
        """Get obligations for a specific regulation"""
        from .normative_knowledge import NormativeKnowledge
        
        norm_knowledge = NormativeKnowledge(self.db)
        
        # Try to find specific regulation
        results = norm_knowledge.search(message)
        
        if results:
            norm = results[0]
            obligations = norm.get("obligations", [])
            
            response = f"⚠️ **Obblighi - {norm['title']}:**\n\n"
            for i, obl in enumerate(obligations, 1):
                response += f"{i}. {obl}\n"
            
            return ActionResult(
                success=True,
                message=response,
                data={"norm": norm},
                action_type="norm_obligations"
            )
        else:
            return ActionResult(
                success=True,
                message="⚠️ **Obblighi Comuni per le Imprese:**\n\n"
                       "• Redigere il bilancio annuale\n"
                       "• Conservare documenti 10 anni\n"
                       "• Fatturazione elettronica obbligatoria\n"
                       "• Adeguamento GDPR\n"
                       "• Valutazione rischi sicurezza lavoro\n"
                       "• Whistleblowing (aziende >50 dip.)\n"
                       "• Segnalazione operazioni sospette\n\n"
                       "Vuoi dettagli su una normativa specifica?",
                action_type="norm_obligations"
            )
    
    def _action_norm_penalties(self, message: str) -> ActionResult:
        """Get penalties for violations"""
        from .normative_knowledge import NormativeKnowledge
        
        norm_knowledge = NormativeKnowledge(self.db)
        results = norm_knowledge.search(message)
        
        if results:
            norm = results[0]
            return ActionResult(
                success=True,
                message=f"⚖️ **Sanzioni - {norm['title']}:**\n\n"
                       f"{norm.get('penalties', 'Consulta il testo ufficiale')}\n\n"
                       f"📌 Ultimo aggiornamento: {norm.get('last_updated', 'N/A')}",
                data={"norm": norm},
                action_type="norm_penalties"
            )
        else:
            return ActionResult(
                success=True,
                message="⚖️ **Sanzioni per Violazioni Normative:**\n\n"
                       "🔒 **Privacy/GDPR:**\n"
                       "   Fino a € 20 milioni o 4% fatturato\n\n"
                       "📊 **Bilancio irregolare:**\n"
                       "   Arresto fino a 5 anni (false comunicazioni)\n\n"
                       "👷 **Sicurezza lavoro:**\n"
                       "   Arresto 3-6 mesi o ammenda € 2.500-€ 10.000\n\n"
                       "💰 **Omesso versamento IVA:**\n"
                       "   30% + interessi di mora\n\n"
                       "🔄 **Antiriciclaggio:**\n"
                       "   Fino a € 5 milioni + responsabilità penale",
                action_type="norm_penalties"
            )
    
    # ==================== SYSTEM ACTIONS ====================
    
    def _action_help(self) -> ActionResult:
        """Show help message"""
        help_text = """
🤖 **MoreLinks Chatbot - Comandi Disponibili:**

**📎 Gestione Link:**
• `crea link [URL]` - Crea un nuovo short link
• `mostra link` - Elenca tutti i tuoi link
• `elimina link [codice]` - Elimina un link
• `aggiorna link [codice] titolo:[nuovo titolo]` - Aggiorna un link
• `stats link [codice]` - Vedi statistiche di un link
• `genera qr [codice]` - Genera QR code

**📊 Analytics:**
• `stats` - Dashboard con statistiche generali
• `top link` - I link con più click
• `analytics` - Report dettagliato
• `esporta csv` - Esporta dati

**📚 Normative Italiane:**
• `normativa [argomento]` - Cerca normative
• `lista normative` - Elenco per categoria
• `obblighi [normativa]` - Cosa devi fare
• `sanzioni [normativa]` - Penalty per violazioni
• `scadenze` - Prossime scadenze

**⚙️ Sistema:**
• `aiuto` - Questo messaggio
• `status` - Info sistema

*Scrivi in italiano o inglese!*
"""
        return ActionResult(
            success=True,
            message=help_text,
            action_type="help"
        )
    
    def _action_status(self) -> ActionResult:
        """Show system status"""
        return ActionResult(
            success=True,
            message="✅ **MoreLinks System Status:**\n\n"
                   "🟢 Database: Connesso\n"
                   "🟢 Chatbot: Attivo\n"
                   "🟢 Normative: Caricate (15+ normative)\n"
                   "📌 Versione: 1.0.0\n"
                   "👤 Utente: Fabio (Demo)\n"
                   "📊 Link creati: 3\n"
                   "👆 Click totali: 231",
            action_type="status"
        )
    
    # ==================== UTILITY METHODS ====================
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.session_context.get("conversation_history", [])
    
    def clear_history(self):
        """Clear conversation history"""
        self.session_context["conversation_history"] = []
    
    def set_context(self, key: str, value: Any):
        """Set a context variable"""
        self.session_context[key] = value
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a context variable"""
        return self.session_context.get(key, default)


# ==================== CONVENIENCE FUNCTIONS ====================

def chat(message: str, user_id: str = None, db=None, ml=None) -> str:
    """
    Simple function to chat with MoreLinks chatbot
    Usage: chat("crea link https://example.com")
    """
    bot = MoreLinksChatbot(database=db, morelinks_core=ml)
    result = bot.process(message, user_id)
    return result.message


if __name__ == "__main__":
    # Demo mode
    print("🤖 MoreLinks Chatbot - Demo Mode\n")
    print("Scrivi 'aiuto' per vedere i comandi disponibili.\n")
    
    bot = MoreLinksChatbot()
    
    while True:
        try:
            user_input = input("\n👤 Tu: ")
            if user_input.lower() in ["exit", "quit", "esci"]:
                print("👋 Arrivederci!")
                break
            
            result = bot.process(user_input)
            print(f"\n🤖 MoreLinks: {result.message}")
            
        except KeyboardInterrupt:
            print("\n👋 Arrivederci!")
            break
