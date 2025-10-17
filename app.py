"""
Frontend web per FAQaccia.
Integra FAQ locali e documentazione ufficiale (MCP) in un'unica interfaccia Streamlit.
"""

import streamlit as st
from chatbot_enhanced import EnhancedFAQChatbot
from datapizza.memory import Memory

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
        padding: 1.5rem 1.5rem 4rem;
        position: relative;
    }

    .hero {
        text-align: center;
        padding: 3.5rem 0 2rem;
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
        margin-top: 1.4rem;
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
        margin-top: 1.8rem;
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
    if st.session_state.get("chatbot_ready", False):
        st.session_state.use_official_docs = st.session_state.chatbot.use_official_docs
elif st.session_state.get("chatbot_ready", False):
    # Mantieni sincronizzato il flag di debug
    st.session_state.chatbot.set_debug_mode(st.session_state.debug)
    st.session_state.use_official_docs = st.session_state.chatbot.use_official_docs

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

# Wrapper principale
st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)

# Hero section
st.markdown(
    """
    <section class="hero">
        <h1 class="faqaccia-title">FAQaccia</h1>
        <p class="hero-subtitle">Il chatbot per rispondere ai dubbi sul framework Datapizza-AI.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

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
                doc_chunks = last_debug.get("official_docs_chunks") or []
                if doc_chunks:
                    st.markdown("**Chunk documentazione (max 2)**")
                    for chunk in doc_chunks[:2]:
                        meta = chunk.get("metadata", {})
                        source = meta.get("file_path") or meta.get("source") or "documentazione"
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
                            bullet += f" · score: {score_label}"
                        st.markdown(f"{bullet}\n\n    {preview}")
        else:
            st.info("Invia una domanda per visualizzare i dettagli di debug.")
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Impostazioni")

    docs_supported = getattr(st.session_state.chatbot, "supports_official_docs", False)
    if not docs_supported:
        st.info("Configura OPENAI_API_KEY per abilitare la documentazione ufficiale (Qdrant deve contenere 'datapizza_official_docs').")

    docs_toggle = st.checkbox(
        "Includi documentazione ufficiale",
        value=st.session_state.use_official_docs,
        help="Abilita il recupero tramite MCP della collection 'datapizza_official_docs'.",
        disabled=not docs_supported,
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
    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    if st.session_state.messages:
        for message in st.session_state.messages:
            role = message["role"]
            avatar = "TU" if role == "user" else "AI"
            classes = "chat-message user" if role == "user" else "chat-message assistant"
            st.markdown(
                f'<div class="{classes}"><div class="avatar">{avatar}</div><div class="bubble">',
                unsafe_allow_html=True,
            )
            st.markdown(message["content"])
            st.markdown("</div></div>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div class="empty-chat">
                <h4>Benvenuto in FAQaccia!</h4>
                <p>Chiedimi qualcosa per iniziare oppure prova uno dei suggerimenti.</p>
                <ul>
                    <li>Come posso integrare Datapizza-AI in un progetto esistente?</li>
                    <li>Quali differenze ci sono rispetto a un classico framework RAG?</li>
                    <li>Serve una chiave API per usare la documentazione ufficiale?</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# Form per l'input
st.markdown('<div class="input-card">', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([7, 1.2])

    with col1:
        user_input = st.text_input(
            "Messaggio",
            placeholder="Scrivi la tua domanda qui...",
            label_visibility="collapsed",
        )

    with col2:
        submit_button = st.form_submit_button("Invia", use_container_width=True)

# Gestione invio messaggio
if submit_button and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("🤔 Sto pensando..."):
        try:
            response = st.session_state.chatbot.ask(user_input, k=k)
            debug_info = st.session_state.chatbot.last_debug_info

            if debug_info:
                st.session_state.debug_logs.append(debug_info)
                if len(st.session_state.debug_logs) > 50:
                    st.session_state.debug_logs = st.session_state.debug_logs[-50:]

            st.session_state.messages.append({"role": "assistant", "content": response})

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
                        doc_chunks = debug_info.get("official_docs_chunks") or []
                        if doc_chunks:
                            st.markdown("**Chunk documentazione (max 3)**")
                            for chunk in doc_chunks[:3]:
                                meta = chunk.get("metadata", {})
                                source = meta.get("file_path") or meta.get("source") or "documentazione"
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
                                    bullet += f" · score: {score_label}"
                                st.markdown(f"{bullet}\n\n    {preview}")

        except Exception as e:
            error_message = f"Si è verificato un errore: {str(e)}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})

    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div class="footer">
        Costruito con ❤️ usando <a href="https://docs.datapizza.ai/" target="_blank">Datapizza-AI</a>
        e <a href="https://streamlit.io/" target="_blank">Streamlit</a>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)
