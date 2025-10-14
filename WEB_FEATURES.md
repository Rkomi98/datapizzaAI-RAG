# Interfaccia Web - Caratteristiche

## 🌐 Frontend Web con Streamlit

Il chatbot include un'interfaccia web moderna e intuitiva costruita con Streamlit.

## ✨ Caratteristiche

### 🎨 Design Moderno
- **Gradiente purple/blue** per l'header
- **Messaggi stilizzati** con colori differenti per utente e bot
- **Animazioni smooth** sui pulsanti
- **Layout responsive** che si adatta a diverse dimensioni schermo
- **Emoji** per rendere l'interfaccia più amichevole

### 💬 Interfaccia Chat
- **Cronologia messaggi** sempre visibile
- **Scrolling automatico** ai nuovi messaggi
- **Indicatore di caricamento** durante l'elaborazione
- **Input box** sempre accessibile in fondo alla pagina
- **Form submit** con tasto Invio

### ⚙️ Sidebar con Controlli

#### Suggerimenti
- Esempi di domande predefinite
- Aiuto per iniziare a usare il chatbot

#### Impostazioni
- **Slider per chunks** - Controlla quanti chunk recuperare (1-10)
- Personalizzazione parametri di retrieval

#### Statistiche
- Conteggio messaggi totali
- Metriche in tempo reale

#### Pulsanti Azione
- **Pulisci chat** - Reset della conversazione
- Gestione rapida della sessione

#### Link Utili
- Documentazione Datapizza-AI
- GitHub repository
- Guida RAG

### 🚀 Funzionalità Avanzate

#### Gestione Sessione
- **Stato persistente** durante l'uso
- **Cronologia messaggi** mantenuta
- **Inizializzazione automatica** del chatbot

#### Error Handling
- **Messaggi di errore chiari** se manca configurazione
- **Guida troubleshooting** inline
- **Verifica prerequisiti** all'avvio

#### User Experience
- **Messaggio di benvenuto** al primo utilizzo
- **Footer informativo** con credits
- **Responsive design** per mobile e desktop

## 🎯 Come Usare

### Avvio

```bash
# Modo 1: Script helper
./run_web.sh

# Modo 2: Comando diretto
streamlit run app.py

# Modo 3: Con parametri personalizzati
streamlit run app.py --server.port 8501 --server.address localhost
```

### Interazione

1. **Scrivi la domanda** nell'input box in fondo
2. **Premi Invio** o clicca "Invia"
3. **Attendi la risposta** (indicatore di caricamento)
4. **Leggi la risposta** che appare nella chat

### Personalizzazione

#### Modifica Colori
Modifica il blocco CSS in `app.py`:
```python
st.markdown("""
<style>
    .user-message {
        background-color: #667eea;  # Cambia questo
    }
    ...
</style>
""", unsafe_allow_html=True)
```

#### Cambia Numero di Chunks
Usa lo slider nella sidebar o modifica il default:
```python
k = st.slider("Chunks da recuperare", min_value=1, max_value=10, value=5)
```

#### Aggiungi Nuove Funzionalità
Il codice è modulare e facile da estendere:
- Aggiungi nuove metriche nella sidebar
- Implementa export della conversazione
- Aggiungi filtri o ricerche avanzate

## 🔧 Configurazione

### Porte e Networking

Default: `http://localhost:8501`

Personalizza con:
```bash
streamlit run app.py --server.port 8080
```

### Temi

Streamlit supporta temi light/dark. Configura in `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#1a1a1a"
font = "sans serif"
```

### Performance

Per dataset grandi, abilita caching:
```python
@st.cache_resource
def init_chatbot():
    return FAQChatbot()
```

## 📱 Mobile Support

L'interfaccia è responsive e funziona su:
- 📱 Smartphone
- 💻 Tablet
- 🖥️ Desktop

Il layout si adatta automaticamente alla dimensione dello schermo.

## 🎨 Componenti UI

### Messaggi
- **User**: Sfondo purple, allineati a destra
- **Bot**: Sfondo grigio chiaro, allineati a sinistra
- **Emoji**: 👤 per utente, 🤖 per bot

### Input
- **Placeholder**: "Scrivi la tua domanda qui..."
- **Border radius**: Arrotondato per look moderno
- **Focus state**: Highlight blu alla selezione

### Buttons
- **Gradient background**: Purple-to-violet
- **Hover effect**: Lift animation
- **Border radius**: Completamente arrotondati

## 🚨 Troubleshooting

### Il browser non si apre automaticamente
```bash
# Apri manualmente
firefox http://localhost:8501
# o
chrome http://localhost:8501
```

### Porta già in uso
```bash
streamlit run app.py --server.port 8502
```

### Errore "chatbot not initialized"
1. Verifica che `.env` sia configurato
2. Controlla che Qdrant sia attivo
3. Esegui l'ingestion se necessario

## 💡 Tips & Tricks

### Ricarica Hot
Streamlit ricarica automaticamente quando modifichi `app.py`

### Debug Mode
Abilita logging più verbose:
```bash
streamlit run app.py --logger.level=debug
```

### Nascondi Menu
```python
st.set_page_config(
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)
```

## 🔮 Funzionalità Future

Possibili estensioni:
- 💾 Export conversazioni in PDF/JSON
- 🔊 Text-to-speech per le risposte
- 🎤 Voice input
- 🌍 Multilingua
- 📊 Analytics dashboard
- 👥 Multi-user support
- 🔐 Autenticazione
- 📁 Upload documenti dinamico

## 🎓 Risorse per Personalizzazione

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Streamlit Gallery](https://streamlit.io/gallery)
- [CSS Reference](https://www.w3schools.com/css/)
- [Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet)

