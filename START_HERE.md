# 🚀 START HERE - Chatbot RAG FAQ Datapizza-AI

## ✨ Novità: Frontend Web Disponibile!

Ora il chatbot ha un'**interfaccia web moderna e minimal** oltre alla versione terminale!

## 🎯 Avvio Rapido (3 minuti)

### 1️⃣ Verifica che tutto sia pronto

```bash
source rag/bin/activate
python test_setup.py
```

Se vedi "6/6 controlli superati", sei pronto! ✅

### 2️⃣ Avvia il Frontend Web

```bash
./run_web.sh
```

**oppure**

```bash
streamlit run app.py
```

L'app si aprirà automaticamente nel browser su `http://localhost:8501` 🌐

## 🎨 Cosa Offre il Frontend Web

### Design Minimal e Moderno
- 💬 **Chat Interface** - Conversazioni fluide stile messaging app
- 🎨 **Purple Gradient** - Design elegante e professionale
- 📱 **Responsive** - Funziona su desktop, tablet e mobile
- ⚡ **Real-time** - Risposte istantanee

### Funzionalità Avanzate
- 💡 **Suggerimenti** - Esempi di domande nella sidebar
- ⚙️ **Impostazioni** - Regola numero di chunks da recuperare
- 📊 **Statistiche** - Vedi metriche in tempo reale
- 🗑️ **Pulisci Chat** - Reset conversazione con un click
- 📚 **Link Risorse** - Accesso rapido a documentazione

### User Experience
- 👋 **Messaggio di benvenuto** al primo utilizzo
- 🤔 **Indicatore caricamento** durante elaborazione
- ✅ **Validazione setup** all'avvio
- 🎯 **Error handling** chiaro e utile

## 💻 Alternativa: Interfaccia Terminale

Se preferisci il terminale:

```bash
python chatbot_faq.py
```

## 📚 Documentazione

- **INTERFACE_PREVIEW.md** - Anteprima visiva dell'interfaccia
- **WEB_FEATURES.md** - Caratteristiche dettagliate del frontend
- **QUICK_START.md** - Guida rapida per iniziare
- **README.md** - Documentazione completa del progetto

## 🆘 Problemi?

### Il browser non si apre?

Apri manualmente: http://localhost:8501

### Errore "chatbot not initialized"?

1. Verifica che `.env` contenga la tua API key OpenAI
2. Assicurati che Qdrant sia attivo: `docker run -p 6333:6333 qdrant/qdrant`
3. Esegui l'ingestion: `python ingest_faq.py`

### Porta già in uso?

```bash
streamlit run app.py --server.port 8502
```

## 🎓 Prossimi Passi

1. **Prova il chatbot** - Fai domande su Datapizza-AI
2. **Esplora le impostazioni** - Modifica parametri nella sidebar
3. **Leggi la documentazione** - Scopri tutte le funzionalità
4. **Personalizza** - Modifica colori e stile in `app.py`

## 💡 Esempi di Domande

Prova a chiedere:

- "Cosa differenzia Datapizza-AI da Langchain?"
- "Supporta modelli Llama?"
- "Come funziona la memory?"
- "Posso usare documenti aziendali in locale?"
- "Quali sono i casi d'uso concreti?"
- "Come gestite il bloat del contesto?"

## 🎉 Divertiti!

Hai ora un chatbot RAG completo e funzionante con:
- ✅ Interfaccia web moderna
- ✅ Retrieval semantico avanzato
- ✅ Risposte contestualizzate
- ✅ Design minimal e user-friendly

---

**Costruito con ❤️ usando [Datapizza-AI](https://docs.datapizza.ai/) e [Streamlit](https://streamlit.io/)**

