"""
Frontend web per FAQaccia.
Integra FAQ locali e documentazione ufficiale (MCP) in un'unica interfaccia Streamlit.
"""

import streamlit as st
from chatbot_enhanced import EnhancedFAQChatbot
from datapizza.memory import Memory

LANGUAGE_OPTIONS = {
    "it": {
        "label": "Italiano",
        "flag": "🇮🇹",
        "ui": {
            "language_label": "Lingua",
            "init_spinner": "🔧 Inizializzazione chatbot con Google Gemini 2.5 Flash...",
            "init_error": """⚠️ **Errore nell'inizializzazione del chatbot**

{error}

**Assicurati di:**
1. Aver eseguito l'ingestion: `python ingest_faq.py`
2. Aver configurato il file `.env` con GOOGLE_API_KEY e OPENAI_API_KEY
3. Aver indicizzato la documentazione ufficiale con `python -m datapizza_mcp.indexer`
4. Aver configurato Qdrant (host remoto o embedded) tramite le variabili `QDRANT_*`
""",
            "hero_subtitle": "Il chatbot per rispondere ai dubbi sul framework Datapizza-AI.",
            "sidebar_model_title": "### 🧠 Modello AI",
            "sidebar_model_info": "**Google Gemini 2.5 Flash** con Memory attiva\n\nIntegra FAQ + documentazione ufficiale (MCP).",
            "sidebar_tips_title": "### 💡 Suggerimenti",
            "sidebar_tips_body": """Prova a chiedere:
- Cosa differenzia Datapizza-AI da altri framework?
- Supporta modelli Llama?
- Come funziona la memory?
- Quali sono i casi d'uso concreti?
- Posso usare documenti aziendali in locale?

**Novità**: Il chatbot ora ricorda la conversazione! 🧠
""",
            "sidebar_debug_title": "### 🧪 Debug",
            "debug_checkbox_label": "Mostra dettagli retrieval",
            "debug_checkbox_help": "Abilita il logging della query riscritta, dei chunk trovati e di eventuali fallback.",
            "debug_no_logs": "Invia una domanda per visualizzare i dettagli di debug.",
            "debug_query_rewritten": "**Query riscritta**",
            "debug_fallback_overridden": "Il modello aveva restituito il fallback: mostrato il testo più rilevante dalle FAQ.",
            "debug_fallback_triggered": "Il modello ha restituito il fallback (nessuna informazione rilevante trovata).",
            "debug_top_chunks_sidebar": "**Top chunk (max 3)**",
            "debug_chunk_source_unknown": "sorgente sconosciuta",
            "score_label": " · punteggio: ",
            "debug_docs_excerpt": "**Documentazione ufficiale (estratto)**",
            "debug_docs_chunks_sidebar": "**Chunk documentazione (max 2)**",
            "debug_docs_chunk_source_fallback": "documentazione",
            "debug_details_title": "🔍 Dettagli retrieval",
            "debug_chunks_label": "**Chunk recuperati**",
            "debug_no_chunks": "Nessun chunk recuperato dal vector store.",
            "debug_top_chunks_expander": "**Top chunk (max 3)**",
            "debug_docs_chunks_expander": "**Chunk documentazione (max 3)**",
            "docs_not_supported_info": "Configura OPENAI_API_KEY per abilitare la documentazione ufficiale (Qdrant deve contenere 'datapizza_official_docs').",
            "docs_toggle_label": "Includi documentazione ufficiale",
            "docs_toggle_help": "Abilita il recupero tramite MCP della collection 'datapizza_official_docs'.",
            "settings_title": "### ⚙️ Impostazioni",
            "slider_label": "Chunks da recuperare",
            "slider_help": "Numero di chunks rilevanti da recuperare dal vector store",
            "stats_title": "### 📊 Statistiche",
            "metric_messages": "Messaggi totali",
            "clear_chat_button": "🗑️ Pulisci chat",
            "resources_title": "### 📚 Risorse",
            "resources_links": """- [Documentazione](https://docs.datapizza.ai/)
- [GitHub](https://github.com/datapizza-labs/datapizza-ai)
- [Guida RAG](https://docs.datapizza.ai/0.0.2/Guides/RAG/rag/)
""",
            "empty_chat_title": "Benvenuto in FAQaccia!",
            "empty_chat_intro": "Chiedimi qualcosa per iniziare oppure prova uno dei suggerimenti.",
            "empty_chat_suggestions": [
                "Come posso integrare Datapizza-AI in un progetto esistente?",
                "Quali differenze ci sono rispetto a un classico framework RAG?",
                "Serve una chiave API per usare la documentazione ufficiale?",
            ],
            "input_label": "Messaggio",
            "input_placeholder": "Scrivi la tua domanda qui...",
            "submit_button": "Invia",
            "thinking_spinner": "🤔 Sto pensando...",
            "generic_error": "Si è verificato un errore: {error}",
            "footer_text": """<div class="footer">
        Costruito con ❤️ usando <a href="https://docs.datapizza.ai/" target="_blank">Datapizza-AI</a>
        e <a href="https://streamlit.io/" target="_blank">Streamlit</a>
    </div>
    </div>""",
            "user_avatar": "TU",
            "assistant_avatar": "AI",
        },
    },
    "en": {
        "label": "English",
        "flag": "🇬🇧",
        "ui": {
            "language_label": "Language",
            "init_spinner": "🔧 Initializing chatbot with Google Gemini 2.5 Flash...",
            "init_error": """⚠️ **Chatbot initialization error**

{error}

**Make sure to:**
1. Run the ingestion: `python ingest_faq.py`
2. Configure the `.env` file with GOOGLE_API_KEY and OPENAI_API_KEY
3. Index the official documentation with `python -m datapizza_mcp.indexer`
4. Configure Qdrant (remote host or embedded) via the `QDRANT_*` variables
""",
            "hero_subtitle": "The chatbot that answers questions about the Datapizza-AI framework.",
            "sidebar_model_title": "### 🧠 AI Model",
            "sidebar_model_info": "**Google Gemini 2.5 Flash** with active Memory\n\nCombines FAQ + official documentation (MCP).",
            "sidebar_tips_title": "### 💡 Tips",
            "sidebar_tips_body": """Try asking:
- What sets Datapizza-AI apart from other frameworks?
- Does it support Llama models?
- How does the memory work?
- What are concrete use cases?
- Can I use on-premise company documents?

**What's new**: The chatbot now remembers the conversation! 🧠
""",
            "sidebar_debug_title": "### 🧪 Debug",
            "debug_checkbox_label": "Show retrieval details",
            "debug_checkbox_help": "Enable logging for the rewritten query, retrieved chunks, and fallback status.",
            "debug_no_logs": "Send a question to view the debug details.",
            "debug_query_rewritten": "**Rewritten query**",
            "debug_fallback_overridden": "The model returned the fallback; showing the most relevant FAQ snippet instead.",
            "debug_fallback_triggered": "The model returned the fallback (no relevant information found).",
            "debug_top_chunks_sidebar": "**Top chunks (max 3)**",
            "debug_chunk_source_unknown": "unknown source",
            "score_label": " · score: ",
            "debug_docs_excerpt": "**Official documentation (excerpt)**",
            "debug_docs_chunks_sidebar": "**Documentation chunks (max 2)**",
            "debug_docs_chunk_source_fallback": "documentation",
            "debug_details_title": "🔍 Retrieval details",
            "debug_chunks_label": "**Retrieved chunks**",
            "debug_no_chunks": "No chunks retrieved from the vector store.",
            "debug_top_chunks_expander": "**Top chunks (max 3)**",
            "debug_docs_chunks_expander": "**Documentation chunks (max 3)**",
            "docs_not_supported_info": "Configure OPENAI_API_KEY to enable the official documentation (Qdrant must contain 'datapizza_official_docs').",
            "docs_toggle_label": "Include official documentation",
            "docs_toggle_help": "Enable MCP retrieval from the 'datapizza_official_docs' collection.",
            "settings_title": "### ⚙️ Settings",
            "slider_label": "Chunks to retrieve",
            "slider_help": "Number of relevant chunks to fetch from the vector store",
            "stats_title": "### 📊 Statistics",
            "metric_messages": "Total messages",
            "clear_chat_button": "🗑️ Clear chat",
            "resources_title": "### 📚 Resources",
            "resources_links": """- [Documentation](https://docs.datapizza.ai/)
- [GitHub](https://github.com/datapizza-labs/datapizza-ai)
- [RAG guide](https://docs.datapizza.ai/0.0.2/Guides/RAG/rag/)
""",
            "empty_chat_title": "Welcome to FAQaccia!",
            "empty_chat_intro": "Ask me something to get started or try one of the suggestions.",
            "empty_chat_suggestions": [
                "How can I integrate Datapizza-AI into an existing project?",
                "What makes it different from a classic RAG framework?",
                "Do I need an API key to use the official documentation?",
            ],
            "input_label": "Message",
            "input_placeholder": "Type your question here...",
            "submit_button": "Send",
            "thinking_spinner": "🤔 Thinking...",
            "generic_error": "An error occurred: {error}",
            "footer_text": """<div class="footer">
        Built with ❤️ using <a href="https://docs.datapizza.ai/" target="_blank">Datapizza-AI</a>
        and <a href="https://streamlit.io/" target="_blank">Streamlit</a>
    </div>
    </div>""",
            "user_avatar": "YOU",
            "assistant_avatar": "AI",
        },
    },
    "de": {
        "label": "Deutsch",
        "flag": "🇩🇪",
        "ui": {
            "language_label": "Sprache",
            "init_spinner": "🔧 Chatbot wird mit Google Gemini 2.5 Flash initialisiert...",
            "init_error": """⚠️ **Fehler bei der Initialisierung des Chatbots**

{error}

**Stelle sicher, dass du:**
1. Die Ingestion ausgeführt hast: `python ingest_faq.py`
2. Die Datei `.env` mit GOOGLE_API_KEY und OPENAI_API_KEY konfiguriert hast
3. Die offizielle Dokumentation mit `python -m datapizza_mcp.indexer` indiziert hast
4. Qdrant (Remote-Host oder Embedded) über die Variablen `QDRANT_*` konfiguriert hast
""",
            "hero_subtitle": "Der Chatbot, der Fragen zum Datapizza-AI-Framework beantwortet.",
            "sidebar_model_title": "### 🧠 KI-Modell",
            "sidebar_model_info": "**Google Gemini 2.5 Flash** mit aktivem Gedächtnis\n\nKombiniert FAQ + offizielle Dokumentation (MCP).",
            "sidebar_tips_title": "### 💡 Tipps",
            "sidebar_tips_body": """Frag zum Beispiel:
- Was unterscheidet Datapizza-AI von anderen Frameworks?
- Unterstützt es Llama-Modelle?
- Wie funktioniert das Memory?
- Welche konkreten Use Cases gibt es?
- Kann ich lokale Unternehmensdokumente nutzen?

**Neu**: Der Chatbot merkt sich jetzt das Gespräch! 🧠
""",
            "sidebar_debug_title": "### 🧪 Debug",
            "debug_checkbox_label": "Retrieval-Details anzeigen",
            "debug_checkbox_help": "Aktiviere das Logging für die umformulierte Anfrage, gefundene Chunks und etwaige Fallbacks.",
            "debug_no_logs": "Stelle eine Frage, um die Debug-Details zu sehen.",
            "debug_query_rewritten": "**Umformulierte Anfrage**",
            "debug_fallback_overridden": "Das Modell hat den Fallback geliefert; stattdessen wird der relevanteste FAQ-Ausschnitt angezeigt.",
            "debug_fallback_triggered": "Das Modell hat den Fallback ausgegeben (keine relevanten Informationen gefunden).",
            "debug_top_chunks_sidebar": "**Top-Chunks (max. 3)**",
            "debug_chunk_source_unknown": "unbekannte Quelle",
            "score_label": " · Score: ",
            "debug_docs_excerpt": "**Offizielle Dokumentation (Auszug)**",
            "debug_docs_chunks_sidebar": "**Dokumentations-Chunks (max. 2)**",
            "debug_docs_chunk_source_fallback": "Dokumentation",
            "debug_details_title": "🔍 Retrieval-Details",
            "debug_chunks_label": "**Abgerufene Chunks**",
            "debug_no_chunks": "Keine Chunks aus dem Vektor-Store gefunden.",
            "debug_top_chunks_expander": "**Top-Chunks (max. 3)**",
            "debug_docs_chunks_expander": "**Dokumentations-Chunks (max. 3)**",
            "docs_not_supported_info": "Konfiguriere OPENAI_API_KEY, um die offizielle Dokumentation zu aktivieren (Qdrant muss 'datapizza_official_docs' enthalten).",
            "docs_toggle_label": "Offizielle Dokumentation einbeziehen",
            "docs_toggle_help": "Aktiviert den MCP-Retrieval der Collection 'datapizza_official_docs'.",
            "settings_title": "### ⚙️ Einstellungen",
            "slider_label": "Chunks abrufen",
            "slider_help": "Anzahl relevanter Chunks, die aus dem Vektor-Store geholt werden",
            "stats_title": "### 📊 Statistiken",
            "metric_messages": "Nachrichten insgesamt",
            "clear_chat_button": "🗑️ Chat löschen",
            "resources_title": "### 📚 Ressourcen",
            "resources_links": """- [Dokumentation](https://docs.datapizza.ai/)
- [GitHub](https://github.com/datapizza-labs/datapizza-ai)
- [RAG-Anleitung](https://docs.datapizza.ai/0.0.2/Guides/RAG/rag/)
""",
            "empty_chat_title": "Willkommen bei FAQaccia!",
            "empty_chat_intro": "Frag mich etwas, um zu starten, oder nutze eine der Vorschläge.",
            "empty_chat_suggestions": [
                "Wie integriere ich Datapizza-AI in ein bestehendes Projekt?",
                "Worin unterscheidet es sich von einem klassischen RAG-Framework?",
                "Brauche ich einen API-Schlüssel, um die offizielle Dokumentation zu nutzen?",
            ],
            "input_label": "Nachricht",
            "input_placeholder": "Schreibe deine Frage hier...",
            "submit_button": "Senden",
            "thinking_spinner": "🤔 Ich überlege...",
            "generic_error": "Es ist ein Fehler aufgetreten: {error}",
            "footer_text": """<div class="footer">
        Erstellt mit ❤️ dank <a href="https://docs.datapizza.ai/" target="_blank">Datapizza-AI</a>
        und <a href="https://streamlit.io/" target="_blank">Streamlit</a>
    </div>
    </div>""",
            "user_avatar": "DU",
            "assistant_avatar": "AI",
        },
    },
}

DEFAULT_LANGUAGE = "it"


def get_ui_value(language: str, key: str):
    default_ui = LANGUAGE_OPTIONS[DEFAULT_LANGUAGE]["ui"]
    lang_ui = LANGUAGE_OPTIONS.get(language, {}).get("ui", {})
    if key in lang_ui:
        return lang_ui[key]
    return default_ui.get(key)

# Configurazione della pagina
st.set_page_config(
    page_title="FAQaccia",
    page_icon="🍕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizzato per un look immersivo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

    :root {
        color-scheme: light dark;
    }

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    body {
        background:
            radial-gradient(circle at 20% 20%, rgba(56, 189, 248, 0.14) 0%, transparent 45%),
            radial-gradient(circle at 80% 0%, rgba(246, 114, 128, 0.16) 0%, transparent 40%),
            #0b1220;
        color: #e2e8f0;
    }

    .stApp {
        background: linear-gradient(160deg, rgba(15, 23, 42, 0.75) 0%, rgba(15, 23, 42, 0.45) 100%);
    }

    .main {
        padding: 0 !important;
    }

    .app-wrapper {
        max-width: 1100px;
        margin: 0 auto;
        position: relative;
    }

    .hero {
        text-align: center;
    }

    .language-bar {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 0.8rem;
    }

    .language-bar [data-baseweb="radio"] {
        margin: 0;
    }

    .language-bar div[role="radiogroup"] {
        display: flex;
        gap: 0.4rem;
    }

    .language-bar div[role="radio"] > div:first-child {
        display: none;
    }

    .language-bar div[role="radio"] > div:nth-child(2) {
        background: rgba(15, 23, 42, 0.6);
        padding: 0.35rem 0.55rem;
        border-radius: 12px;
        font-size: 1.15rem;
        transition: background 0.2s ease, transform 0.2s ease;
        border: 1px solid rgba(148, 163, 184, 0.35);
    }

    .language-bar div[role="radio"][aria-checked="true"] > div:nth-child(2) {
        background: linear-gradient(135deg, #38bdf8, #6366f1);
        color: #0f172a;
        transform: translateY(-1px);
        border-color: transparent;
    }

    .faqaccia-title {
        font-family: 'Poppins', sans-serif;
        font-size: 2.8rem;
        line-height: 1.15;
        margin: 1.2rem 0 0.8rem;
        color: #f8fafc;
    }

    .hero-subtitle {
        color: #cbd5f5;
        max-width: 640px;
        margin: 0 auto;
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .chat-shell {
        margin-top: 1.1rem;
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 24px;
        padding: 1.4rem 1.6rem 1.2rem;
        backdrop-filter: blur(22px);
        box-shadow: 0 22px 50px rgba(15, 23, 42, 0.55);
    }

    .chat-message {
        display: flex;
        align-items: flex-start;
        gap: 14px;
        margin: 1rem 0;
    }

    .chat-message .avatar {
        width: 44px;
        height: 44px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        font-size: 1.05rem;
        color: #0f172a;
        background: linear-gradient(135deg, #fef3c7, #fbbf24);
        box-shadow: 0 12px 24px rgba(251, 191, 36, 0.25);
    }

    .chat-message.assistant .avatar {
        background: linear-gradient(135deg, #38bdf8, #6366f1);
        color: #f8fafc;
        box-shadow: 0 12px 28px rgba(99, 102, 241, 0.28);
    }

    .chat-message .bubble {
        max-width: 76%;
        background: rgba(15, 23, 42, 0.48);
        border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 1rem 1.2rem;
        border-radius: 18px;
        font-size: 0.98rem;
        line-height: 1.6;
        color: #e2e8f0;
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.35);
    }

    .chat-message .bubble p {
        margin: 0 0 0.6rem;
    }

    .chat-message .bubble p:last-child {
        margin-bottom: 0;
    }

    .chat-message .bubble ul {
        margin: 0 0 0.6rem 1.2rem;
    }

    .chat-message.user {
        flex-direction: row-reverse;
        text-align: right;
    }

    .chat-message.user .bubble {
        background: linear-gradient(135deg, #fb7185, #f97316);
        color: #0f172a;
        border: none;
        box-shadow: 0 18px 28px rgba(249, 115, 22, 0.28);
    }

    .chat-message .bubble code {
        background: rgba(148, 163, 184, 0.18);
        color: #f8fafc;
        padding: 0.2rem 0.35rem;
        border-radius: 6px;
        font-size: 0.85rem;
    }

    .chat-message .bubble pre {
        background: rgba(15, 23, 42, 0.88);
        padding: 0.75rem;
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.25);
        color: #f8fafc;
        overflow-x: auto;
    }

    .chat-message.user .bubble code {
        background: rgba(255, 255, 255, 0.25);
        color: #111827;
    }

    .empty-chat {
        text-align: center;
        padding: 2.8rem 1.2rem;
        border: 1px dashed rgba(148, 163, 184, 0.32);
        border-radius: 20px;
        background: rgba(15, 23, 42, 0.45);
        color: #cbd5f5;
        margin: 1rem 0;
    }

    .empty-chat h4 {
        margin-bottom: 0.6rem;
        color: #f8fafc;
        font-family: 'Poppins', sans-serif;
    }

    .empty-chat ul {
        margin: 1.1rem auto 0;
        padding: 0;
        list-style: none;
        display: inline-block;
        text-align: left;
    }

    .empty-chat ul li {
        position: relative;
        padding-left: 1.3rem;
        margin: 0.35rem 0;
    }

    .empty-chat ul li::before {
        content: "•";
        position: absolute;
        left: 0;
        color: #38bdf8;
        font-weight: 700;
    }

    .input-card {
        margin-top: 1.4rem;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 26px;
        padding: 1.2rem 1.4rem 1.1rem;
        backdrop-filter: blur(18px);
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.45);
    }

    .stTextInput > div > div > input {
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.25);
        padding: 0.95rem 1.2rem;
        color: #f1f5f9;
    }

    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.35);
        background: rgba(15, 23, 42, 0.78);
    }

    .stTextInput > div > div > input::placeholder {
        color: rgba(226, 232, 240, 0.45);
    }

    .stButton > button {
        border-radius: 14px;
        padding: 0.6rem 0;
        font-weight: 600;
        font-size: 0.95rem;
        background: linear-gradient(135deg, #38bdf8, #6366f1);
        border: none;
        color: #f8fafc;
        box-shadow: 0 12px 24px rgba(99, 102, 241, 0.3);
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 18px 30px rgba(56, 189, 248, 0.35);
    }

    .footer {
        text-align: center;
        padding: 3rem 0 1rem;
        color: rgba(226, 232, 240, 0.68);
        font-size: 0.85rem;
    }

    .footer a {
        color: #c4d1ff;
        text-decoration: none;
    }

    .footer a:hover {
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

# Gestione lingua
if "language" not in st.session_state:
    st.session_state.language = DEFAULT_LANGUAGE

language_codes = list(LANGUAGE_OPTIONS.keys())
current_language_code = st.session_state.language


def ui_text(key: str):
    return get_ui_value(st.session_state.language, key)


# Inizializzazione dello stato della sessione
if "messages" not in st.session_state:
    st.session_state.messages = []

# Stato debug e log
if "debug" not in st.session_state:
    st.session_state.debug = False
if "debug_logs" not in st.session_state:
    st.session_state.debug_logs = []
if "use_official_docs" not in st.session_state:
    st.session_state.use_official_docs = True

# Inizializza la Memory per mantenere il contesto della conversazione
if "memory" not in st.session_state:
    st.session_state.memory = Memory()

should_init_chatbot = (
    "chatbot" not in st.session_state
    or not isinstance(st.session_state.get("chatbot"), EnhancedFAQChatbot)
)

if should_init_chatbot:
    with st.spinner(ui_text("init_spinner")):
        try:
            # Passa la memory condivisa al chatbot
            st.session_state.chatbot = EnhancedFAQChatbot(
                memory=st.session_state.memory,
                debug_mode=st.session_state.debug,
                use_official_docs=st.session_state.use_official_docs,
            )
            st.session_state.chatbot_ready = True
        except Exception as e:
            st.session_state.chatbot_ready = False
            st.session_state.error_message = str(e)
    if st.session_state.get("chatbot_ready", False):
        st.session_state.use_official_docs = st.session_state.chatbot.use_official_docs
elif st.session_state.get("chatbot_ready", False):
    # Mantieni sincronizzato il flag di debug
    st.session_state.chatbot.set_debug_mode(st.session_state.debug)
    st.session_state.use_official_docs = st.session_state.chatbot.use_official_docs

# Verifica se il chatbot è pronto
if not st.session_state.chatbot_ready:
    st.error(ui_text("init_error").format(error=st.session_state.error_message))
    st.stop()

# Wrapper principale
st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="language-bar">', unsafe_allow_html=True)
    selected_language = st.radio(
        ui_text("language_label"),
        options=language_codes,
        format_func=lambda code: LANGUAGE_OPTIONS[code]["flag"],
        horizontal=True,
        index=language_codes.index(st.session_state.language),
        label_visibility="collapsed",
        key="language_selector",
    )
    st.markdown("</div>", unsafe_allow_html=True)
if selected_language != st.session_state.language:
    st.session_state.language = selected_language
    st.rerun()

current_language_code = st.session_state.language

# Hero section
hero_html = f"""
    <section class="hero">
        <h1 class="faqaccia-title">FAQaccia</h1>
        <p class="hero-subtitle">{ui_text('hero_subtitle')}</p>
    </section>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# Sidebar con informazioni e suggerimenti
with st.sidebar:
    st.markdown(ui_text("sidebar_model_title"))
    st.info(ui_text("sidebar_model_info"))

    st.markdown(ui_text("sidebar_tips_title"))
    st.markdown(ui_text("sidebar_tips_body"))

    st.markdown("---")

    st.markdown(ui_text("sidebar_debug_title"))
    debug_toggle = st.checkbox(
        ui_text("debug_checkbox_label"),
        value=st.session_state.debug,
        help=ui_text("debug_checkbox_help"),
    )
    if debug_toggle != st.session_state.debug:
        st.session_state.debug = debug_toggle
        if st.session_state.get("chatbot_ready", False):
            st.session_state.chatbot.set_debug_mode(debug_toggle)
        st.session_state.debug_logs = []

    if st.session_state.debug:
        if st.session_state.debug_logs:
            last_debug = st.session_state.debug_logs[-1]
            st.markdown(ui_text("debug_query_rewritten"))
            st.code(last_debug.get("rewritten_query") or "—", language="text")

            if last_debug.get("fallback_overridden"):
                st.warning(ui_text("debug_fallback_overridden"))
            elif last_debug.get("fallback_triggered"):
                st.info(ui_text("debug_fallback_triggered"))

            st.markdown(ui_text("debug_top_chunks_sidebar"))
            for chunk in last_debug.get("chunks", [])[:3]:
                metadata = chunk.get("metadata", {}) or {}
                source = metadata.get("source") or ui_text("debug_chunk_source_unknown")
                score = chunk.get("score")
                score_label = None
                if score is not None:
                    try:
                        score_label = round(float(score), 3)
                    except (TypeError, ValueError):
                        score_label = score
                preview = chunk.get("text", "").strip().replace("\n", " ")
                preview = preview[:220] + ("…" if len(preview) > 220 else "")
                bullet = f"- `{source}`"
                if score_label is not None:
                    bullet += f"{ui_text('score_label')}{score_label}"
                st.markdown(f"{bullet}\n\n    {preview}")
            docs_excerpt = last_debug.get("official_docs_excerpt")
            if last_debug.get("official_docs_used") and docs_excerpt:
                st.markdown(ui_text("debug_docs_excerpt"))
                st.code(docs_excerpt, language="markdown")
                doc_chunks = last_debug.get("official_docs_chunks") or []
                if doc_chunks:
                    st.markdown(ui_text("debug_docs_chunks_sidebar"))
                    for chunk in doc_chunks[:2]:
                        meta = chunk.get("metadata", {}) or {}
                        source = meta.get("file_path") or meta.get("source") or ui_text(
                            "debug_docs_chunk_source_fallback"
                        )
                        score = chunk.get("score")
                        score_label = None
                        if score is not None:
                            try:
                                score_label = round(float(score), 3)
                            except (TypeError, ValueError):
                                score_label = score
                        preview = (chunk.get("text") or "").strip().replace("\n", " ")
                        preview = preview[:220] + ("…" if len(preview) > 220 else "")
                        bullet = f"- `{source}`"
                        if score_label is not None:
                            bullet += f"{ui_text('score_label')}{score_label}"
                        st.markdown(f"{bullet}\n\n    {preview}")
        else:
            st.info(ui_text("debug_no_logs"))

    st.markdown("---")

    st.markdown(ui_text("settings_title"))

    docs_supported = getattr(st.session_state.chatbot, "supports_official_docs", False)
    if not docs_supported:
        st.info(ui_text("docs_not_supported_info"))

    docs_toggle = st.checkbox(
        ui_text("docs_toggle_label"),
        value=st.session_state.use_official_docs,
        help=ui_text("docs_toggle_help"),
        disabled=not docs_supported,
    )
    if docs_toggle != st.session_state.use_official_docs:
        st.session_state.use_official_docs = docs_toggle
        if st.session_state.get("chatbot_ready", False):
            st.session_state.chatbot.use_official_docs = docs_toggle
        st.session_state.debug_logs = []
        st.rerun()

    # Numero di chunks da recuperare
    k = st.slider(
        ui_text("slider_label"),
        min_value=1,
        max_value=20,
        value=10,
        help=ui_text("slider_help"),
    )

    st.markdown("---")

    # Statistiche
    st.markdown(ui_text("stats_title"))
    st.metric(ui_text("metric_messages"), len(st.session_state.messages))

    # Pulsante per pulire la chat
    if st.button(ui_text("clear_chat_button"), use_container_width=True):
        st.session_state.messages = []
        # Resetta anche la memory per cancellare il contesto
        st.session_state.memory = Memory()
        st.session_state.chatbot.memory = st.session_state.memory
        st.session_state.debug_logs = []
        st.rerun()

    st.markdown("---")

    st.markdown(ui_text("resources_title"))
    st.markdown(ui_text("resources_links"))

# Area messaggi
chat_container = st.container()

with chat_container:
    if st.session_state.messages:
        st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            role = message["role"]
            avatar = ui_text("user_avatar") if role == "user" else ui_text("assistant_avatar")
            classes = "chat-message user" if role == "user" else "chat-message assistant"
            st.markdown(
                f'<div class="{classes}"><div class="avatar">{avatar}</div><div class="bubble">',
                unsafe_allow_html=True,
            )
            st.markdown(message["content"])
            st.markdown("</div></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        suggestions = ui_text("empty_chat_suggestions")
        suggestion_items = "".join(f"<li>{item}</li>" for item in suggestions)
        empty_chat_html = f"""
            <div class="empty-chat">
                <h4>{ui_text('empty_chat_title')}</h4>
                <p>{ui_text('empty_chat_intro')}</p>
                <ul>
                    {suggestion_items}
                </ul>
            </div>
        """
        st.markdown(empty_chat_html, unsafe_allow_html=True)

# Form per l'input
st.markdown('<div class="input-card">', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([7, 1.2])

    with col1:
        user_input = st.text_input(
            ui_text("input_label"),
            placeholder=ui_text("input_placeholder"),
            label_visibility="collapsed",
        )

    with col2:
        submit_button = st.form_submit_button(ui_text("submit_button"), use_container_width=True)

# Gestione invio messaggio
if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner(ui_text("thinking_spinner")):
        try:
            response = st.session_state.chatbot.ask(
                user_input,
                language=current_language_code,
                k=k,
            )
            debug_info = st.session_state.chatbot.last_debug_info

            if debug_info:
                st.session_state.debug_logs.append(debug_info)
                if len(st.session_state.debug_logs) > 50:
                    st.session_state.debug_logs = st.session_state.debug_logs[-50:]

            st.session_state.messages.append({"role": "assistant", "content": response})

            if st.session_state.debug and debug_info:
                with st.expander(ui_text("debug_details_title"), expanded=False):
                    st.markdown(ui_text("debug_query_rewritten"))
                    st.code(debug_info.get("rewritten_query") or "—", language="text")

                    if debug_info.get("fallback_overridden"):
                        st.warning(ui_text("debug_fallback_overridden"))
                    elif debug_info.get("fallback_triggered"):
                        st.info(ui_text("debug_fallback_triggered"))

                    chunks = debug_info.get("chunks", [])
                    if chunks:
                        st.markdown(ui_text("debug_chunks_label"))
                        for chunk in chunks[:3]:
                            metadata = chunk.get("metadata", {}) or {}
                            source = metadata.get("source") or ui_text("debug_chunk_source_unknown")
                            score = chunk.get("score")
                            score_label = None
                            if score is not None:
                                try:
                                    score_label = round(float(score), 3)
                                except (TypeError, ValueError):
                                    score_label = score
                            preview = chunk.get("text", "").strip().replace("\n", " ")
                            preview = preview[:320] + ("…" if len(preview) > 320 else "")
                            bullet = f"- `{source}`"
                            if score_label is not None:
                                bullet += f"{ui_text('score_label')}{score_label}"
                            st.markdown(f"{bullet}\n\n    {preview}")
                    else:
                        st.info(ui_text("debug_no_chunks"))
                    docs_excerpt = debug_info.get("official_docs_excerpt")
                    if debug_info.get("official_docs_used") and docs_excerpt:
                        st.markdown(ui_text("debug_docs_excerpt"))
                        st.code(docs_excerpt, language="markdown")
                        doc_chunks = debug_info.get("official_docs_chunks") or []
                        if doc_chunks:
                            st.markdown(ui_text("debug_docs_chunks_expander"))
                            for chunk in doc_chunks[:3]:
                                meta = chunk.get("metadata", {}) or {}
                                source = meta.get("file_path") or meta.get("source") or ui_text(
                                    "debug_docs_chunk_source_fallback"
                                )
                                score = chunk.get("score")
                                score_label = None
                                if score is not None:
                                    try:
                                        score_label = round(float(score), 3)
                                    except (TypeError, ValueError):
                                        score_label = score
                                preview = (chunk.get("text") or "").strip().replace("\n", " ")
                                preview = preview[:320] + ("…" if len(preview) > 320 else "")
                                bullet = f"- `{source}`"
                                if score_label is not None:
                                    bullet += f"{ui_text('score_label')}{score_label}"
                                st.markdown(f"{bullet}\n\n    {preview}")

        except Exception as e:
            error_message = ui_text("generic_error").format(error=str(e))
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(ui_text("footer_text"), unsafe_allow_html=True)
