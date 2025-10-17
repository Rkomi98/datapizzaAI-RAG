"""
Frontend web per il Chatbot RAG Datapizza-AI.
Integra FAQ locali e documentazione ufficiale (MCP) in un'unica interfaccia Streamlit.
"""

import streamlit as st
from chatbot_enhanced import EnhancedFAQChatbot
from datapizza.memory import Memory

# Configurazione della pagina
st.set_page_config(
    page_title="Chatbot FAQ Datapizza-AI",
    page_icon="🍕",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# CSS personalizzato per un look minimal e moderno
st.markdown("""
<style>
    /* Stile generale */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Messaggi */
    .user-message {
        background-color: #667eea;
        color: #ffffff;
        padding: 1.2rem;
        border-radius: 1rem;
        margin: 0.8rem 0;
        margin-left: 20%;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        font-weight: 500;
    }

    .bot-message {
        background-color: #ffffff;
        color: #2d2d2d;
        padding: 1.2rem;
        border-radius: 1rem;
        margin: 0.8rem 0;
        margin-right: 20%;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #e8e8e8;
        font-weight: 400;
        line-height: 1.5;
    }
    
    /* Input box */
    .stTextInput > div > div > input {
        border-radius: 2rem;
        border: 2px solid #d0d0d0;
        padding: 0.9rem 1.5rem;
        font-size: 1rem;
        background-color: #ffffff;
        color: #2d2d2d;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
        background-color: #fafafa;
    }

    .stTextInput > div > div > input::placeholder {
        color: #888;
        font-weight: 400;
    }

    /* Pulsanti */
    .stButton > button {
        border-radius: 2rem;
        padding: 0.6rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: #ffffff;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    
    /* Sidebar */
    .sidebar-content {
        padding: 1rem;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #ffffff;
        border-left: 4px solid #667eea;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1.5rem 0;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
        border: 1px solid #e8e8e8;
    }

    .info-box h4 {
        color: #667eea;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }

    .info-box p {
        color: #555;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #888;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

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
    with st.spinner("🔧 Inizializzazione chatbot con Google Gemini 2.5 Flash..."):
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
elif st.session_state.get("chatbot_ready", False):
    # Mantieni sincronizzato il flag di debug
    st.session_state.chatbot.set_debug_mode(st.session_state.debug)

# Header
st.markdown('<h1 class="main-header">🍕 Chatbot Datapizza-AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">FAQ + documentazione ufficiale in un unico assistente.</p>', unsafe_allow_html=True)

# Verifica se il chatbot è pronto
if not st.session_state.chatbot_ready:
    st.error(f"""
    ⚠️ **Errore nell'inizializzazione del chatbot**
    
    {st.session_state.error_message}
    
    **Assicurati di:**
    1. Aver eseguito l'ingestion: `python ingest_faq.py`
    2. Aver configurato il file `.env` con GOOGLE_API_KEY e OPENAI_API_KEY
    3. Aver indicizzato la documentazione ufficiale con `python -m datapizza_mcp.indexer`
    4. Aver configurato Qdrant (host remoto o embedded) tramite le variabili `QDRANT_*`
    """)
    st.stop()

# Sidebar con informazioni e suggerimenti
with st.sidebar:
    st.markdown("### 🧠 Modello AI")
    st.info("**Google Gemini 2.5 Flash** con Memory attiva\n\nIntegra FAQ + documentazione ufficiale (MCP).")
    
    st.markdown("### 💡 Suggerimenti")
    st.markdown("""
    Prova a chiedere:
    - Cosa differenzia Datapizza-AI da altri framework?
    - Supporta modelli Llama?
    - Come funziona la memory?
    - Quali sono i casi d'uso concreti?
    - Posso usare documenti aziendali in locale?
    
    **Novità**: Il chatbot ora ricorda la conversazione! 🧠
    """)
    
    st.markdown("---")

    st.markdown("### 🧪 Debug")
    debug_toggle = st.checkbox(
        "Mostra dettagli retrieval",
        value=st.session_state.debug,
        help="Abilita il logging della query riscritta, dei chunk trovati e di eventuali fallback.",
    )
    if debug_toggle != st.session_state.debug:
        st.session_state.debug = debug_toggle
        if st.session_state.get("chatbot_ready", False):
            st.session_state.chatbot.set_debug_mode(debug_toggle)
        st.session_state.debug_logs = []

    if st.session_state.debug:
        if st.session_state.debug_logs:
            last_debug = st.session_state.debug_logs[-1]
            st.markdown("**Query riscritta**")
            st.code(last_debug.get("rewritten_query") or "—", language="text")

            if last_debug.get("fallback_overridden"):
                st.warning("Il modello aveva restituito il fallback: mostrato il testo più rilevante dalle FAQ.")
            elif last_debug.get("fallback_triggered"):
                st.info("Il modello ha restituito il fallback (nessuna informazione rilevante trovata).")

            st.markdown("**Top chunk (max 3)**")
            for chunk in last_debug.get("chunks", [])[:3]:
                source = chunk.get("metadata", {}).get("source", "sorgente sconosciuta")
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
                    bullet += f" · score: {score_label}"
                st.markdown(f"{bullet}\n\n    {preview}")
            docs_excerpt = last_debug.get("official_docs_excerpt")
            if last_debug.get("official_docs_used") and docs_excerpt:
                st.markdown("**Documentazione ufficiale (estratto)**")
                st.code(docs_excerpt, language="markdown")
        else:
            st.info("Invia una domanda per visualizzare i dettagli di debug.")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Impostazioni")

    docs_toggle = st.checkbox(
        "Includi documentazione ufficiale",
        value=st.session_state.use_official_docs,
        help="Abilita il recupero tramite MCP della collection 'datapizza_official_docs'.",
        disabled=not getattr(st.session_state.chatbot, "supports_official_docs", False),
    )
    if docs_toggle != st.session_state.use_official_docs:
        st.session_state.use_official_docs = docs_toggle
        if st.session_state.get("chatbot_ready", False):
            st.session_state.chatbot.use_official_docs = docs_toggle
        st.session_state.debug_logs = []
        st.rerun()
    
    # Numero di chunks da recuperare
    k = st.slider("Chunks da recuperare", min_value=1, max_value=20, value=10, 
                  help="Numero di chunks rilevanti da recuperare dal vector store")
    
    # Score threshold
    # score_threshold = st.slider("Soglia di similarity", min_value=0.0, max_value=1.0, value=0.5, step=0.05,
    #                             help="Soglia minima per considerare un chunk rilevante")
    
    st.markdown("---")
    
    # Statistiche
    st.markdown("### 📊 Statistiche")
    st.metric("Messaggi totali", len(st.session_state.messages))
    
    # Pulsante per pulire la chat
    if st.button("🗑️ Pulisci chat", use_container_width=True):
        st.session_state.messages = []
        # Resetta anche la memory per cancellare il contesto
        st.session_state.memory = Memory()
        st.session_state.chatbot.memory = st.session_state.memory
        st.session_state.debug_logs = []
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 📚 Risorse")
    st.markdown("""
    - [Documentazione](https://docs.datapizza.ai/)
    - [GitHub](https://github.com/datapizza-labs/datapizza-ai)
    - [Guida RAG](https://docs.datapizza.ai/0.0.2/Guides/RAG/rag/)
    """)

# Area messaggi
chat_container = st.container()

with chat_container:
    # Mostra messaggi esistenti
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">👤 {message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)

# Input utente (sempre visibile in fondo)
st.markdown("---")

# Form per l'input
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.text_input(
            "Messaggio",
            placeholder="Scrivi la tua domanda qui...",
            label_visibility="collapsed"
        )
    
    with col2:
        submit_button = st.form_submit_button("Invia", use_container_width=True)

# Gestione invio messaggio
if submit_button and user_input:
    # Aggiungi messaggio utente
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Mostra messaggio utente
    st.markdown(f'<div class="user-message">👤 {user_input}</div>', unsafe_allow_html=True)
    
    # Mostra indicatore di caricamento
    with st.spinner("🤔 Sto pensando..."):
        try:
            # Ottieni risposta dal chatbot
            response = st.session_state.chatbot.ask(user_input, k=k)
            debug_info = st.session_state.chatbot.last_debug_info

            # Salva log di debug
            if debug_info:
                st.session_state.debug_logs.append(debug_info)
                if len(st.session_state.debug_logs) > 50:
                    st.session_state.debug_logs = st.session_state.debug_logs[-50:]
            
            # Aggiungi risposta bot
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Mostra risposta bot
            st.markdown(f'<div class="bot-message">🤖 {response}</div>', unsafe_allow_html=True)

            # Se il debug è attivo, mostra i dettagli anche nell'interfaccia principale
            if st.session_state.debug and debug_info:
                with st.expander("🔍 Dettagli retrieval", expanded=False):
                    st.markdown("**Query riscritta**")
                    st.code(debug_info.get("rewritten_query") or "—", language="text")

                    if debug_info.get("fallback_overridden"):
                        st.warning("Il modello aveva restituito il fallback: mostrato il testo dei chunk più rilevanti.")
                    elif debug_info.get("fallback_triggered"):
                        st.info("Il modello ha restituito il fallback (nessuna informazione rilevante trovata).")

                    chunks = debug_info.get("chunks", [])
                    if chunks:
                        st.markdown("**Chunk recuperati**")
                        for chunk in chunks[:3]:
                            source = chunk.get("metadata", {}).get("source", "sorgente sconosciuta")
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
                                bullet += f" · score: {score_label}"
                            st.markdown(f"{bullet}\n\n    {preview}")
                    else:
                        st.info("Nessun chunk recuperato dal vector store.")
                    docs_excerpt = debug_info.get("official_docs_excerpt")
                    if debug_info.get("official_docs_used") and docs_excerpt:
                        st.markdown("**Documentazione ufficiale (estratto)**")
                        st.code(docs_excerpt, language="markdown")
            
        except Exception as e:
            error_message = f"Si è verificato un errore: {str(e)}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
    
    # Ricarica la pagina per mostrare i nuovi messaggi
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    Costruito con ❤️ usando <a href="https://docs.datapizza.ai/" target="_blank">Datapizza-AI</a> 
    e <a href="https://streamlit.io/" target="_blank">Streamlit</a>
</div>
""", unsafe_allow_html=True)

# Messaggio di benvenuto (solo se non ci sono messaggi)
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="info-box">
        <h4>👋 Benvenuto!</h4>
        <p>Sono il tuo assistente virtuale per le FAQ di Datapizza-AI. 
        Puoi farmi qualsiasi domanda sul framework e cercherò di risponderti basandomi 
        sulle informazioni disponibili.</p>
        <p><strong>Inizia facendo una domanda qui sotto! ⬇️</strong></p>
    </div>
    """, unsafe_allow_html=True)
