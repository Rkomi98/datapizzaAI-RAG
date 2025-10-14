"""
Frontend web per il Chatbot RAG FAQ Datapizza-AI.
Interfaccia chat semplice e moderna con Streamlit.
"""

import streamlit as st
from chatbot_faq import FAQChatbot
import time

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
    }
    
    /* Messaggi */
    .user-message {
        background-color: #667eea;
        color: white;
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        margin-left: 20%;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
    }
    
    .bot-message {
        background-color: #f7f7f8;
        color: #1a1a1a;
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        margin-right: 20%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Input box */
    .stTextInput > div > div > input {
        border-radius: 2rem;
        border: 2px solid #e0e0e0;
        padding: 0.75rem 1.5rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
    }
    
    /* Pulsanti */
    .stButton > button {
        border-radius: 2rem;
        padding: 0.5rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar */
    .sidebar-content {
        padding: 1rem;
    }
    
    /* Info boxes */
    .info-box {
        background-color: #f0f2f6;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
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

if "chatbot" not in st.session_state:
    with st.spinner("🔧 Inizializzazione chatbot..."):
        try:
            st.session_state.chatbot = FAQChatbot()
            st.session_state.chatbot_ready = True
        except Exception as e:
            st.session_state.chatbot_ready = False
            st.session_state.error_message = str(e)

# Header
st.markdown('<h1 class="main-header">🍕 Chatbot FAQ Datapizza-AI</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Chiedimi qualsiasi cosa su Datapizza-AI!</p>', unsafe_allow_html=True)

# Verifica se il chatbot è pronto
if not st.session_state.chatbot_ready:
    st.error(f"""
    ⚠️ **Errore nell'inizializzazione del chatbot**
    
    {st.session_state.error_message}
    
    **Assicurati di:**
    1. Aver eseguito l'ingestion: `python ingest_faq.py`
    2. Aver configurato il file `.env` con OPENAI_API_KEY
    3. Aver avviato Qdrant: `docker run -p 6333:6333 qdrant/qdrant`
    """)
    st.stop()

# Sidebar con informazioni e suggerimenti
with st.sidebar:
    st.markdown("### 💡 Suggerimenti")
    st.markdown("""
    Prova a chiedere:
    - Cosa differenzia Datapizza-AI da altri framework?
    - Supporta modelli Llama?
    - Come funziona la memory?
    - Quali sono i casi d'uso concreti?
    - Posso usare documenti aziendali in locale?
    """)
    
    st.markdown("---")
    
    st.markdown("### ⚙️ Impostazioni")
    
    # Numero di chunks da recuperare
    k = st.slider("Chunks da recuperare", min_value=1, max_value=10, value=5, 
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
            
            # Aggiungi risposta bot
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Mostra risposta bot
            st.markdown(f'<div class="bot-message">🤖 {response}</div>', unsafe_allow_html=True)
            
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

