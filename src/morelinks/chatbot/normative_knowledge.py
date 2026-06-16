"""
MoreLinks - Normative Knowledge Base
Complete Italian business regulations knowledge
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


class RegulationExpert:
    """Expert system for Italian business regulations"""
    
    def __init__(self):
        # Complete regulation database
        self.regulations = self._load_regulations()
    
    def _load_regulations(self) -> Dict[str, Dict]:
        """Load complete regulation database"""
        return {
            # ==================== CONTABILITÀ E BILANCIO ====================
            "CC-2423": {
                "title": "Redazione del Bilancio (Art. 2423 CC)",
                "code": "CC-ART2423",
                "category": "Contabilità",
                "description": "Gli amministratori devono redigere il bilancio di esercizio che comprende lo stato patrimoniale, il conto economico e la nota integrativa.",
                "articles": [
                    "Art. 2423 - Bilancio di esercizio",
                    "Art. 2423-bis - Criteri di valutazione",
                    "Art. 2424 - Stato patrimoniale", 
                    "Art. 2425 - Conto economico",
                    "Art. 2425-bis - Conto economico riclassificato",
                    "Art. 2426 - Nota integrativa",
                    "Art. 2427 - Contenuto nota integrativa",
                    "Art. 2428 - Relazione sulla gestione",
                    "Art. 2429 - Relazione dei sindaci"
                ],
                "obligations": [
                    "Redazione in forma chiara e corretta",
                    "Rappresentazione veritiera e corretta della situazione patrimoniale",
                    "Osservanza criteri di valutazione ex Art. 2426",
                    "Obbligo di deposito presso Registro delle Imprese",
                    "Approvazione entro 120 giorni dalla chiusura esercizio",
                    "Relazione sulla gestione obbligatoria"
                ],
                "penalties": "Sanzioni amministrative da € 2.065 a € 12.911 per violazioni formali; reato di false comunicazioni sociali (Art. 2621-2622 CC) punibile con reclusione da 1 a 5 anni",
                "deadlines": [
                    {"name": "Approvazione bilancio", "when": "Entro 120 gg dalla chiusura esercizio"},
                    {"name": "Deposito atto approvazione", "when": "Entro 30 gg dall'approvazione"}
                ],
                "source": "Codice Civile Italiano",
                "last_updated": "2024-01-01"
            },
            
            "OIC-PRINCIPI": {
                "title": "Principi Contabili OIC",
                "code": "OIC-PRINCIPI",
                "category": "Contabilità",
                "description": "I Principi Contabili OIC emanati dall'Organismo Italiano di Contabilità disciplinano la redazione del bilancio secondo le regole italiane, in conformità con le norme europee e la tassonomia XBRL.",
                "articles": [
                    "OIC 1 - Presentazione del bilancio",
                    "OIC 2 - Immobilizzazioni materiali",
                    "OIC 3 - Immobilizzazioni immateriali",
                    "OIC 4 - Partecipazioni",
                    "OIC 5 - Titoli",
                    "OIC 6 - Strumenti finanziari derivati",
                    "OIC 7 - Variazioni delle risorse",
                    "OIC 9 - Crediti",
                    "OIC 10 - Rimanenze",
                    "OIC 11 - Disponibilità liquide",
                    "OIC 12 - Patrimonio netto",
                    "OIC 13 - Debiti",
                    "OIC 14 - Fondi rischi e oneri",
                    "OIC 15 - Ricavi",
                    "OIC 19 - Debiti verso fornitori",
                    "OIC 20 - Titoli",
                    "OIC 21 - Consolidato",
                    "OIC 23 - Verifiche ex Art. 2409",
                    "OIC 24 - Immobilizzazioni immateriali",
                    "OIC 25 - Imposte sul reddito"
                ],
                "obligations": [
                    "Applicazione obbligatoria per i soggetti OIC",
                    "Adeguamento automatico agli aggiornamenti OIC",
                    "Nota integrativa completa con info ex Art. 2427",
                    "Informazioni comparative esercizio precedente",
                    "Riclassificazione voci per continuità"
                ],
                "penalties": "Sanzioni per bilancio non conforme ai principi contabili; possibile responsabilità degli amministratori",
                "source": "Organismo Italiano di Contabilità (OIC)",
                "last_updated": "2024-12-31"
            },
            
            "CC-2086": {
                "title": "Gestione Aziendale (Art. 2086 CC)",
                "code": "CC-2086",
                "category": "Amministrazione",
                "description": "L'imprenditore è tenuto a istituire un assetto organizzativo, amministrativo e contabile adeguato alla natura e alle dimensioni dell'impresa, anche in funzione della rilevazione tempestiva della crisi d'impresa.",
                "articles": [
                    "Art. 2086 - Obblighi gestionali",
                    "Art. 2087 - Tutela condizioni di lavoro",
                    "Art. 2088 - Obblighi contabili",
                    "Art. 2214 - Scritture contabili",
                    "Art. 2216 - Contabilità industriale"
                ],
                "obligations": [
                    "Istituire assetto organizzativo adeguato",
                    "Adeguata struttura amministrativa e contabile",
                    "Rilevazione tempestiva della crisi",
                    "Adozione misure per superamento crisi",
                    "Conservazione documentazione 10 anni"
                ],
                "penalties": "Responsabilità per omessa/adeguata organizzazione; possibile fallimento",
                "source": "Codice Civile + L. 155/2017 (Codice della Crisi)",
                "last_updated": "2024-01-01"
            },
            
            # ==================== SCADENZE E ADEMPIMENTI ====================
            "DPR-917-82": {
                "title": "Scadenze Fiscali (DPR 917/86 - TUIR)",
                "code": "DPR-917-ART82",
                "category": "Scadenze",
                "description": "Definizione delle scadenze per dichiarazioni fiscali, versamenti e adempimenti IVA per i soggetti con esercizio coincidente con anno solare.",
                "articles": [
                    "DPR 917/1986 - TUIR",
                    "Art. 82 - Redditi di impresa",
                    "Art. 83 - Ricavi",
                    "Art. 95 - Costi deducibili",
                    "Art. 108 - Ammortamenti",
                    "Art. 109 - Spese generiche"
                ],
                "obligations": [
                    "Dichiarazione IVA entro 30 aprile",
                    "Dichiarazione redditi entro 30 novembre",
                    "Versamento imposte entro scadenze trimestrali",
                    "Comunicazioni periodiche IVA (entro 1° trimestre)",
                    "Esterometro per operazioni extra-UE (entro mese successivo)",
                    "CU ex Art. 4 c.6-ter DPR 322/98"
                ],
                "penalties": "Interessi di mora 3,75% annuo + sanzioni 30% per omessi versamenti; ravvedimento operoso con riduzione sanzioni (30% se regolarizzazione entro 30 gg, 10% entro 90 gg, 1/10 entro anno)",
                "deadlines": [
                    {"name": "Versamento IVA 1° trimestre", "when": "16 maggio"},
                    {"name": "Versamento IVA 2° trimestre", "when": "16 settembre"},
                    {"name": "Versamento IVA 3° trimestre", "when": "16 dicembre"},
                    {"name": "Dichiarazione IVA annuale", "when": "30 aprile"},
                    {"name": "Dichiarazione redditi", "when": "30 novembre"},
                    {"name": "Esterometro", "when": "Ultimo giorno mese successivo"}
                ],
                "source": "DPR 917/1986 + Provvedimenti Agenzia Entrate",
                "last_updated": "2024-01-01"
            },
            
            "DLGS231-ART7": {
                "title": "Registro delle Imprese (DLgs 30/2006)",
                "code": "DLGS231-ART7",
                "category": "Scadenze",
                "description": "Obblighi di comunicazione e deposito atti presso la Camera di Commercio, inclusa l'iscrizione di atti costitutivi, modifiche e bilanci.",
                "articles": [
                    "DLgs 30/2006 - Registro Imprese",
                    "Art. 7 - Iscrizione atti",
                    "Art. 8 - Comunicazioni obbligatorie",
                    "Art. 16 - Deposito bilanci",
                    "Art. 21 - Reclamo e ricorso",
                    "Art. 23 - Cancellazione"
                ],
                "obligations": [
                    "Iscrizione atto costitutivo entro 20 gg da atto",
                    "Deposito bilanci entro 30 giorni dall'approvazione",
                    "Comunicazione variazioni sede, oggetto, amministratori",
                    "Nomina revisori se obbligatoria (SPA, SAPA > limiti Art. 2435-bis)",
                    "Depositare comunicazione liquidazioni",
                    "Iscrizione patti sociali"
                ],
                "penalties": "€ 30-€ 500 per omessa/ritardata comunicazione; responsabilità amministrativa; difficoltà probatorie",
                "deadlines": [
                    {"name": "Iscrizione atto costitutivo", "when": "Entro 20 gg"},
                    {"name": "Deposito bilancio", "when": "Entro 30 gg dall'approvazione"},
                    {"name": "Variazioni organi", "when": "Entro 30 gg"}
                ],
                "source": "DLgs 30/2006 + Regolamento Camerale",
                "last_updated": "2024-01-01"
            },
            
            # ==================== GDPR E PRIVACY ====================
            "GDPR-32": {
                "title": "Sicurezza dei Dati (GDPR Art. 32)",
                "code": "GDPR-ART32",
                "category": "Privacy",
                "description": "Il titolare e il responsabile del trattamento devono implementare misure tecniche e organizzative adeguate per garantire un livello di sicurezza appropriato al rischio, includendo pseudonimizzazione, cifratura, resilienza, capacità di ripristino.",
                "articles": [
                    "Reg. UE 679/2016 (GDPR)",
                    "Art. 5 - Principi trattamento",
                    "Art. 6 - Base giuridica",
                    "Art. 13-14 - Informativa interessato",
                    "Art. 15-22 - Diritti interessato",
                    "Art. 24 - Responsabilità titolare",
                    "Art. 25 - Privacy by design",
                    "Art. 28 - Responsabile trattamento",
                    "Art. 30 - Registro trattamenti",
                    "Art. 32 - Sicurezza trattamento",
                    "Art. 33 - Notifica Garante",
                    "Art. 34 - Comunicazione interessato"
                ],
                "obligations": [
                    "Misure tecniche: crittografia, pseudonimizzazione, backup",
                    "Misure organizzative: policy, formazione, procedure",
                    "Registro trattamenti (Art. 30) per titolari >250 dipendenti",
                    "Valutazione impatto (DPIA) se rischio elevato (Art. 35)",
                    "Nomina DPO se richiesto (Art. 37)",
                    "Accordi Art. 28 con responsabili trattamento",
                    "Notifica Garante entro 72 ore per violazioni gravi (Art. 33)",
                    "Comunicazione agli interessati se violazione prob. (Art. 34)",
                    "Verifica periodica efficacia misure"
                ],
                "penalties": "Sanzioni fino a € 20.000.000 o 4% fatturato globale per violazioni gravi (Art. 83.5); fino a € 10.000.000 o 2% per violazioni procedurali (Art. 83.4)",
                "deadlines": [
                    {"name": "Notifica violazione Garante", "when": "Entro 72 ore"},
                    {"name": "Risposta richiesta interessato", "when": "1 mese (estendibile 2 mesi)"},
                    {"name": "Aggiornamento registro", "when": "Continuo"},
                    {"name": "Verifica DPO", "when": "Annuale"}
                ],
                "source": "Regolamento UE 2016/679 (GDPR)",
                "last_updated": "2024-01-01"
            },
            
            "PRIVACY-196": {
                "title": "Codice Privacy (DLgs 196/2003)",
                "code": "PRIVACY-DLGS196",
                "category": "Privacy",
                "description": "Codice in materia di protezione dei dati personali che integra il GDPR con disposizioni specifiche per il contesto italiano, inclusi trattamenti per finalità di lavoro, sanità, pubblica sicurezza.",
                "articles": [
                    "DLgs 196/2003 come modificato da DLgs 101/2018",
                    "Art. 2 - Ambito applicativo",
                    "Art. 2-quinquies - Consenso minori (14 anni)",
                    "Art. 2-sexies - Trattamento dati lavoratori",
                    "Art. 2-septies - Dati genetici/biometrici",
                    "Art. 2-undecies - Salvaguardie interessi vitali",
                    "Art. 3 - Garante per protezione dati personali",
                    "Art. 13 - Informativa standardizzata",
                    "Art. 15 - Accesso difensivo"
                ],
                "obligations": [
                    "Adeguamento procedure aziendali a GDPR + DLgs 196/2003",
                    "Informativa completa a interessati",
                    "Gestione richieste esercizio diritti",
                    "Sicurezza trattamento ex Art. 32 GDPR",
                    "Consenso esplicito per finalità marketing",
                    "Verifica idoneità per trattamento dati lavoratori"
                ],
                "penalties": "Sanzioni GDPR + sanzioni disciplinari interne; nullità informative insufficienti",
                "source": "DLgs 196/2003 come modificato",
                "last_updated": "2024-01-01"
            },
            
            # ==================== RESPONSABILITÀ AMMINISTRATIVA ====================
            "DLSLGS231": {
                "title": "Responsabilità Amministrativa Enti (DLgs 231/2001)",
                "code": "DLSLGS231",
                "category": "Responsabilità",
                "description": "La responsabilità degli enti per reati commessi nel loro interesse o a loro vantaggio da persone che rivestono funzioni di rappresentanza, amministrazione o direzione. Introduce la possibilità di sanzioni per l'azienda stessa.",
                "articles": [
                    "DLgs 231/2001",
                    "Art. 5 - Responsabilità dell'ente",
                    "Art. 6 - Esclusione - Modelli organizzativi",
                    "Art. 7 - Reati omicidio colposo/lesioni colpose",
                    "Art. 8 - Omicidio colposo/art. 589 cp",
                    "Art. 9 - Lesioni personali colpose/art. 590 cp",
                    "Art. 24 - Reati societari",
                    "Art. 24-bis - Delitti informatici",
                    "Art. 24-ter - Delitti di criminalità organizzata",
                    "Art. 25 - Corruzione",
                    "Art. 25-bis - Falsificazione monete",
                    "Art. 25-ter - Reati contro PA",
                    "Art. 25-quater - Terrorismo",
                    "Art. 25-quinquies - Delitti contro personalità Stato",
                    "Art. 25-sexies - Market abuse",
                    "Art. 25-septies - Omicidio colposo/lesioni",
                    "Art. 25-octies - Ricettazione/riciclaggio",
                    "Art. 25-decies - Induzione a rendere false dichiarazioni",
                    "Art. 25-undecies - Reati ambientali",
                    "Art. 25-duodecies - Impiego cittadini terzi irregolari"
                ],
                "obligations": [
                    "Adozione Modello Organizzativo 231 (MOG)",
                    "Nomina Organismo di Vigilanza (OdV) monocratico/collegiale",
                    "Codice Etico aziendale",
                    "Procedure specifiche per reati presupposto",
                    "Formazione continua dipendenti",
                    "Sistema disciplinare interno",
                    "Whistleblowing (DLgs 24/2023)",
                    "Aggiornamento periodico MOG",
                    "Verifiche periodiche efficacia",
                    "Flussi informativi verso OdV"
                ],
                "penalties": "Sanzioni pecuniarie da € 100 a € 1.500.000 (in base a quotazione/fatturato); sanzioni interdittive (sospensione attività, revoca licenze, divieto contrarre PA); confisca; pubblicazione sentenza; commissariamento giudiziario",
                "deadlines": [
                    {"name": "Aggiornamento MOG", "when": "Ogni 3 anni o al mutamento attività/rischi"},
                    {"name": "Verifica OdV", "when": "Almeno annuale"},
                    {"name": "Formazione", "when": "Annuale"}
                ],
                "source": "DLgs 231/2001 e successive modifiche",
                "last_updated": "2024-01-01"
            },
            
            # ==================== ANTIRICICLAGGIO ====================
            "DLGS231-AML": {
                "title": "Antiriciclaggio (DLgs 231/2007)",
                "code": "DLGS231-AML",
                "category": "Antiriciclaggio",
                "description": "Prevenzione dell'utilizzo del sistema finanziario per fini di riciclaggio dei proventi di attività criminose e di finanziamento del terrorismo, in attuazione delle direttive europee.",
                "articles": [
                    "DLgs 231/2007 come modificato da DLgs 90/2017",
                    "Art. 10 - Adozione misure adeguate",
                    "Art. 14 - Adeguata verifica",
                    "Art. 15 - Semplificata",
                    "Art. 16 - Rafforzata",
                    "Art. 18 - Conservazione documenti",
                    "Art. 19 - Segnalazione operazioni sospette",
                    "Art. 21 - Casi di non segnalazione",
                    "Art. 35 - Registrazione operazioni",
                    "Art. 36 - Anomalie",
                    "Art. 41 - Conservazione documenti (10 anni)",
                    "Art. 42 - Accesso informazioni"
                ],
                "obligations": [
                    "Adeguata verifica cliente (KYC) - identificazione e verifica",
                    "Identificazione titolari effettivi (persone fisiche >25%)",
                    "Registrazione operazioni in contanti >€ 15.000",
                    "Segnalazione operazioni sospette (SOS) a UIF",
                    "Conservazione documenti 10 anni",
                    "Formazione continua personale",
                    "Procedura interna antiriciclaggio",
                    "Responsabile antiriciclaggio (per soggetti obbligati)",
                    "Valutazione rischio (misure basate sul rischio)",
                    "Segregazione funzioni"
                ],
                "penalties": "Sanzioni amministrative da € 5.000 a € 5.000.000; responsabilità penale per omessa segnalazione; sospensione/chiusura attività; confisca valori",
                "deadlines": [
                    {"name": "Conservazione documenti", "when": "10 anni da operazione"},
                    {"name": "Segnalazione SOS", "when": "Immediatamente (non oltre 30 gg)"},
                    {"name": "Formazione personale", "when": "Annuale"}
                ],
                "source": "DLgs 231/2007 + DLgs 90/2017 + VI Direttiva AML",
                "last_updated": "2024-01-01"
            },
            
            # ==================== LAVORO E PREVIDENZA ====================
            "STATUTO-LAVORATORI": {
                "title": "Statuto dei Lavoratori (L. 300/1970)",
                "code": "STATUTO-LAVORATORI",
                "category": "Lavoro",
                "description": "Norme sulla tutela della libertà e dignità dei lavoratori, sulla libertà sindacale e sull'attività sindacale nei luoghi di lavoro, incluse tutele contro licenziamenti illegittimi.",
                "articles": [
                    "L. 300/1970 - Statuto lavoratori",
                    "Art. 1 - Libertà di pensiero",
                    "Art. 2 - Divieto indagini opinioni",
                    "Art. 3 - Limitazioni uso impianti audiovisivi",
                    "Art. 4 - Controlli a distanza (ora Art. 4 DLgs 151/2015)",
                    "Art. 5 - Investigazioni private",
                    "Art. 8 - Mansioni e progressioni",
                    "Art. 13 - Trasferimenti",
                    "Art. 15 - Limiti alle sanzioni disciplinari",
                    "Art. 18 - Tutela contro licenziamenti",
                    "Art. 20 - Nullità licenziamento discriminatorio"
                ],
                "obligations": [
                    "Rispetto libertà sindacali e di pensiero",
                    "Procedura per controlli a distanza (accordo sindacale o autorizzazione)",
                    "Criteri per valutazioni e licenziamenti (Art. 5 L. 604/1966)",
                    "Igiene e sicurezza sul lavoro",
                    "Procedura preventiva per modifiche organizzative",
                    "Contrattazione di secondo livello"
                ],
                "penalties": "Nullità clausole contrattuali illegittime; risarcimento danni; reintegro nel posto di lavoro; nullità licenziamento discriminatorio",
                "source": "L. 300/1970 + L. 604/1966 + Jobs Act",
                "last_updated": "2024-01-01"
            },
            
            "DLGS81-2008": {
                "title": "Testo Unico Sicurezza Lavoro (DLgs 81/2008)",
                "code": "DLGS81-2008",
                "category": "Lavoro",
                "description": "Testo unico in materia di salute e sicurezza nei luoghi di lavoro, con obblighi per datori di lavoro, dirigenti, preposti e lavoratori, inclusa la valutazione dei rischi e le misure di prevenzione.",
                "articles": [
                    "DLgs 81/2008 - TUSL",
                    "Art. 2 - Definizioni",
                    "Art. 17 - Obblighi datore di lavoro non delegabili",
                    "Art. 18 - Obblighi generali datore di lavoro",
                    "Art. 19 - Obblighi dirigenti",
                    "Art. 20 - Obblighi lavoratori",
                    "Art. 28 - Oggetto della valutazione rischi",
                    "Art. 29 - Documento di valutazione rischi (DVR)",
                    "Art. 30 - Misure prevenzione protezione",
                    "Art. 32 - Formazione",
                    "Art. 37 - Formazione e addestramento",
                    "Art. 18-bis - Rappresentante lavoratori sicurezza (RLS)",
                    "Art. 47 - Consultazione RLS",
                    "Art. 50 - Attribuzioni RLS",
                    "D.Lgs. 106/2009 - Modifiche"
                ],
                "obligations": [
                    "Valutazione tutti i rischi (obbligo non delegabile Art. 17)",
                    "DVR documento obbligatorio con data certa",
                    "Nomina RSPP interno o esterno",
                    "Nomina/addestramento addetti primo soccorso",
                    "Nomina/addestramento addetti antincendio",
                    "Sorveglianza sanitaria (visite mediche periodiche)",
                    "Formazione/addestramento lavoratori",
                    "Dispositivi protezione individuale (DPI)",
                    "Piano emergenza ed evacuazione",
                    "Protocollo COVID-19 se applicabile",
                    "Consultazione RLS",
                    "Segnaletica di sicurezza",
                    "Fornire informativa rischi specifici"
                ],
                "penalties": "Arresto 3-6 mesi o ammenda € 2.500-€ 10.000 per mancata valutazione rischi; responsabilità penale per infortuni; omicidio colposo (art. 589 cp) fino a 5 anni reclusione; lesioni colpose aggravate (art. 590 cp) fino a 3 anni",
                "deadlines": [
                    {"name": "Aggiornamento DVR", "when": "Annuale o al mutamento rischi"},
                    {"name": "Formazione generale lavoratori", "when": "All'avvio rapporto"},
                    {"name": "Formazione specifica", "when": "Secondo rischi mansione"},
                    {"name": "Visita medica", "when": "Pre-assuntiva + periodica"}
                ],
                "source": "DLgs 81/2008 + DLgs 106/2009",
                "last_updated": "2024-01-01"
            },
            
            # ==================== FATTURAZIONE ELETTRONICA ====================
            "FE-DLGS127": {
                "title": "Fatturazione Elettronica (DLgs 127/2015)",
                "code": "FE-DLGS127",
                "category": "Fatturazione",
                "description": "Obbligo di fatturazione elettronica per le operazioni B2B e B2C tramite Sistema di Interscambio (SDI) dell'Agenzia delle Entrate, con emissione in formato XML conforme alle specifiche FatturaPA.",
                "articles": [
                    "DLgs 127/2015 - Estensione obbligo FE",
                    "Art. 1 - Ambito applicativo",
                    "DM 17 giugno 2014 - Specifiche tecniche FatturaPA",
                    "Provvedimento Agenzia Entrate - Formato FatturaPA",
                    "Art. 21 DPR 633/1972 - Fattura",
                    "Art. 21-bis - Fattura semplificata",
                    "Art. 21-ter - Autofattura",
                    "Art. 39 - Emissione fattura",
                    "Art. 48 - Sistema di Interscambio"
                ],
                "obligations": [
                    "Emissione fatture in formato XML via SDI",
                    "Conservazione elettronica fatture 10 anni",
                    "Dati obbligatori: P.IVA, C.F., dati cliente completo",
                    "Numerazione progressiva annuale",
                    "Lotto fatture se richieste",
                    "Fatture accompagnatorie se trasporto merci",
                    "TD01 (fattura), TD04 (nota credito), TD06 (parcella)",
                    "Regime Martini se forfettario"
                ],
                "penalties": "Sanzioni da € 250 a € 2.000 per fattura omessa/irregolare; € 100-€ 500 per incompletezza dati obbligatori; perdita deducibilità costi; indeducibilità IVA",
                "deadlines": [
                    {"name": "Invio fattura SDI", "when": "Entro 12 giorni da data operazione"},
                    {"name": "Conservazione", "when": "10 anni"},
                    {"name": "Esterometro (operazioni extra-UE)", "when": "Entro mese successivo"}
                ],
                "source": "DLgs 127/2015 + provvedimenti AE",
                "last_updated": "2024-01-01"
            },
            
            # ==================== VIDEOSORVEGLIANZA ====================
            "GARANTE-VS": {
                "title": "Videosorveglianza (Provvedimento Garante 2010)",
                "code": "GARANTE-VS",
                "category": "Privacy",
                "description": "Linee guida del Garante per la videosorveglianza nel rispetto della privacy dei lavoratori e dei terzi, con requisiti per informativa, durata conservazione e limiti all'utilizzo.",
                "articles": [
                    "Provvedimento Garante 8 aprile 2010",
                    "Linee guida videosorveglianza",
                    "Art. 4 L. 300/1970 - Controlli a distanza",
                    "Art. 113 - Uso impianti audiovisivi",
                    "Regolamento Europeo Privacy (GDPR)",
                    "Art. 2-quater DLgs 196/2003 - Autorizzazione generica"
                ],
                "obligations": [
                    "Informativa completa a lavoratori e visitatori (art. 13 GDPR)",
                    "Cartelli ben visibili (formato, dimensione, posizione)",
                    "Limitazione registrazione a zone critiche/non protette",
                    "Durata conservazione massima 24-72 ore (eccezioni motivate)",
                    "Misure sicurezza adeguate per impianti",
                    "Autorizzazione sindacale o accordo per luoghi di lavoro (Art. 4 L. 300/70)",
                    "Regolamento interno se impianto con accesso a luoghi pubblici",
                    "Divieto riprese WC, spogliatoi, aree riposo"
                ],
                "penalties": "Sanzioni privacy del Garante; nullità registrazioni se senza informativa; licenziamento illegittimo se usato impropriamente per controllo; Art. 171 Codice Privacy - sanzioni penali",
                "deadlines": [
                    {"name": "Informativa", "when": "Prima dell'installazione"},
                    {"name": "Durata conservazione", "when": "Max 72 ore (ecc. motivate)"},
                    {"name": "Verifica periodica", "when": "Annuale"}
                ],
                "source": "Provvedimento Garante 8/4/2010 + GDPR",
                "last_updated": "2024-01-01"
            },
            
            # ==================== WHISTLEBLOWING ====================
            "WHISTLE-DLGS24": {
                "title": "Whistleblowing (DLgs 24/2023)",
                "code": "WHISTLE-DLGS24",
                "category": "Compliance",
                "description": "Tutela delle persone che segnalano, denunciano o divulgano informazioni su violazioni di normative nazionali e comunitarie ottenute nel contesto lavorativo, in attuazione della Direttiva UE 2019/1937.",
                "articles": [
                    "DLgs 24/2023 - Whistleblowing",
                    "Art. 1 - Ambito applicativo",
                    "Art. 2 - Definizioni",
                    "Art. 3 - Segnalazioni interne",
                    "Art. 4 - Canali interni",
                    "Art. 5 - Gestione segnalazioni",
                    "Art. 6 -Comunicazioni al Garante",
                    "Art. 7 - Denuncia all'autorità giudiziaria",
                    "Art. 8 - Divulgazione pubblica",
                    "Art. 12 - Condizioni per tutela",
                    "Art. 16 - Divieto ritorsioni",
                    "Art. 17 - Misure di protezione",
                    "Art. 20 - Sanzioni"
                ],
                "obligations": [
                    "Attivazione canale interno segnalazioni (obbligatorio per >50 dip. dal 15/07/2023)",
                    "Procedura gestione segnalazioni entro 3 mesi",
                    "Tutela riservatezza segnalante",
                    "Divieto atti ritorsivi verso segnalante",
                    "Registro interno delle segnalazioni",
                    "Formazione personale (dipendenti, manager)",
                    "Responsabile interno (RP per PMI, consulente esterno per micro)",
                    "Policy aziendale whistleblowing",
                    "Comunica. a Gestore canale esterno se >249 dip."
                ],
                "penalties": "Sanzioni per atti ritorsivi (€ 10.000-€ 50.000); risarcimento whistleblower; nullità clausole contrattuali; possibile revoca contratto",
                "deadlines": [
                    {"name": "Attivazione canale interno", "when": "Immediato (obbligatorio)"},
                    {"name": "Gestione segnalazione", "when": "Entro 3 mesi"},
                    {"name": "Formazione", "when": "Annuale"},
                    {"name": "Report annuale", "when": "31 marzo"}
                ],
                "source": "DLgs 24/2023 + Direttiva UE 2019/1937",
                "last_updated": "2024-01-01"
            },
            
            # ==================== NUOVA SAB (SOGGETTI ABILITATI) ====================
            "SOGGETTI-ABILITATI": {
                "title": "Soggetti Abilitati - Compliance Fiscale",
                "code": "SOGGETTI-ABILITATI",
                "category": "Fiscale",
                "description": "Obblighi per commercialisti, consulenti del lavoro,CAF e altri intermediari abilitati alla trasmissione telematica delle dichiarazioni fiscali.",
                "articles": [
                    "DPR 322/1998 - Regolamento dichiarazioni",
                    "Art. 3 - Soggetti abilitati",
                    "D.M. 15/2012 - Requisiti",
                    "Circolare AE 38/2012 - Istruzioni",
                    "D.Lgs. 241/1997 - Norma. catasto società"
                ],
                "obligations": [
                    "Registrazione all'Agenzia Entrate",
                    "Utilizzo prodotti software certificati",
                    "Invio telematico diretto o tramite intermediari",
                    "Conservazione copie dichiarazioni 10 anni",
                    "Rilascio ricevuta a contribuente",
                    "Responsabilità per errori trasmissione"
                ],
                "penalties": "Radiazione dall'albo per gravi violazioni; responsabilità civilistica",
                "source": "DPR 322/1998 + D.Lgs. 241/1997",
                "last_updated": "2024-01-01"
            },
            
            # ==================== TRASPARENZA ====================
            "TRASPARENZA-DLGS33": {
                "title": "Trasparenza Amministrativa (DLgs 33/2013)",
                "code": "TRASPARENZA-DLGS33",
                "category": "Trasparenza",
                "description": "Obblighi di pubblicazione per le pubbliche amministrazioni e soggetti privati con partecipazione pubblica, relativi a organizzazione, attività e servizi.",
                "articles": [
                    "DLgs 33/2013 - Trasparenza",
                    "Art. 1 - Oggetto e definizioni",
                    "Art. 8 - Pubblicazione dati",
                    "Art. 10 - Programma trasparenza",
                    "Art. 12 - Pubblicazione documenti",
                    "Art. 14 - Incarichi amministratori",
                    "Art. 15 - Consulenze e collaborazioni",
                    "Art. 16 - Tassi assenza/presenza"
                ],
                "obligations": [
                    "Pubblicazione organigramma e funzogramma",
                    "Pubblicazione compensi dirigenti/amministratori",
                    "Pubblicazione bandi e contratti",
                    "Pubblicazione bilanci e dati finanziari",
                    "Pubblicazione procedure concorsuali",
                    "Aggiornamento periodico dati"
                ],
                "penalties": "Responsabilità dirigenziale; mancata designazione RPC; sanzioni pecuniarie",
                "source": "DLgs 33/2013 come modificato",
                "last_updated": "2024-01-01"
            },
            
            # ==================== COMUNICAZIONI UNICHE ====================
            "COMUNICAZIONE-UNICA": {
                "title": "Comunicazione Unica per nascita impresa",
                "code": "COMUNICAZIONE-UNICA",
                "category": "Scadenze",
                "description": "Procedura telematica unificata per l'iscrizione al Registro Imprese, Adm, Inps, Inail e ASL in un'unica comunicazione per le nuove attività.",
                "articles": [
                    "D.L. 7/2007 convertito L. 40/2007",
                    "D.M. 18 gennaio 2007",
                    "Circ. Min. Sviluppo Economico",
                    "Circolare Unioncamere"
                ],
                "obligations": [
                    "Comunicazione Unica telematica per nuova impresa",
                    "Reperimento codice SCIA/autorizzazione",
                    "Iscrizione INPS/INAIL",
                    "Regolarità contributiva",
                    "Denuncia inizio attività ASL"
                ],
                "penalties": "Sanzioni per inizio attività senza comunicazione; blocco accesso finanziamenti",
                "source": "L. 40/2007 + normative settoriali",
                "last_updated": "2024-01-01"
            }
        }
    
    def get_all(self) -> List[Dict]:
        """Get all regulations"""
        return list(self.regulations.values())
    
    def get_by_category(self, category: str) -> List[Dict]:
        """Get regulations by category"""
        return [r for r in self.regulations.values() if r["category"] == category]
    
    def get_by_code(self, code: str) -> Optional[Dict]:
        """Get regulation by code"""
        return self.regulations.get(code)
    
    def search(self, query: str) -> List[Dict]:
        """Search regulations by keyword"""
        query_lower = query.lower()
        results = []
        
        for reg in self.regulations.values():
            # Search in title, description, articles, obligations
            search_text = " ".join([
                reg.get("title", ""),
                reg.get("description", ""),
                " ".join(reg.get("articles", [])),
                " ".join(reg.get("obligations", []))
            ]).lower()
            
            if query_lower in search_text:
                results.append(reg)
            elif any(word in search_text for word in query_lower.split()):
                results.append(reg)
        
        return results
    
    def get_categories(self) -> List[str]:
        """Get all categories"""
        categories = set()
        for reg in self.regulations.values():
            categories.add(reg["category"])
        return sorted(list(categories))
    
    def get_upcoming_deadlines(self, days: int = 30) -> List[Dict]:
        """Get upcoming deadlines in next N days"""
        # Simplified - would need actual date logic
        deadlines = []
        for reg in self.regulations.values():
            if "deadlines" in reg:
                for dl in reg["deadlines"]:
                    deadlines.append({
                        "regulation": reg["title"],
                        "code": reg["code"],
                        "name": dl["name"],
                        "when": dl["when"]
                    })
        return deadlines


class NormativeKnowledge:
    """Interface for normative queries with database integration"""
    
    def __init__(self, database=None):
        self.db = database
        self.expert = RegulationExpert()
    
    def search(self, query: str) -> List[Dict]:
        """Search regulations"""
        return self.expert.search(query)
    
    def get_all(self) -> List[Dict]:
        """Get all regulations"""
        return self.expert.get_all()
    
    def get_by_category(self, category: str) -> List[Dict]:
        """Get by category"""
        return self.expert.get_by_category(category)
    
    def get_by_code(self, code: str) -> Optional[Dict]:
        """Get by code"""
        return self.expert.get_by_code(code)
    
    def get_categories(self) -> List[str]:
        """Get categories"""
        return self.expert.get_categories()
    
    def get_upcoming_deadlines(self, days: int = 30) -> List[Dict]:
        """Get deadlines"""
        return self.expert.get_upcoming_deadlines(days)
    
    def explain_obligation(self, regulation_code: str) -> str:
        """Explain obligations for a regulation"""
        reg = self.expert.get_by_code(regulation_code)
        if not reg:
            return "Regolamento non trovato"
        
        result = f"📋 **{reg['title']}**\n\n"
        result += f"📖 {reg['description']}\n\n"
        result += "⚠️ **Obblighi:**\n"
        for i, obl in enumerate(reg.get("obligations", []), 1):
            result += f"{i}. {obl}\n"
        
        return result
    
    def explain_penalties(self, regulation_code: str) -> str:
        """Explain penalties for a regulation"""
        reg = self.expert.get_by_code(regulation_code)
        if not reg:
            return "Regolamento non trovato"
        
        result = f"⚖️ **{reg['title']}**\n\n"
        result += f"**Sanzioni:**\n{reg.get('penalties', 'Consulta il testo ufficiale')}\n\n"
        result += f"📌 Ultimo aggiornamento: {reg.get('last_updated', 'N/A')}"
        
        return result
