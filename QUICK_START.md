# Quick Start - Chatbot RAG FAQ Datapizza-AI

## ⚡ Avvio Rapido (3 passi)

### 1. Configura l'API Key

Apri il file `.env` e inserisci la tua OpenAI API key:

```bash
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXX
```

### 2. Avvia Qdrant (in un terminale separato)

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 3. Avvia il Chatbot

**Opzione A - Interfaccia Web (Consigliata)** 🌐
```bash
source rag/bin/activate
./run_web.sh
```

**Opzione B - Terminale** 💻
```bash
source rag/bin/activate
python chatbot_faq.py
```

## ✅ Fatto!

### Interfaccia Web
L'applicazione si aprirà automaticamente nel browser con:
- 💬 Chat interattiva
- ⚙️ Impostazioni personalizzabili
- 📊 Statistiche in tempo reale
- 🎨 Design moderno e minimal

Ora puoi fare domande come:
- "Cosa differenzia Datapizza-AI da altri framework?"
- "Supporta modelli Llama?"
- "Come funziona la memory?"

Per uscire: digita `exit` o premi `Ctrl+C`

---

## 🔧 Troubleshooting

### Se è la prima volta che usi il chatbot:

```bash
# 1. Verifica setup
python test_setup.py

# 2. Esegui ingestion (solo la prima volta)
python ingest_faq.py

# 3. Avvia chatbot
python chatbot_faq.py
```

### Se qualcosa non funziona:

- **Qdrant non raggiungibile**: Verifica che sia in esecuzione su porta 6333
- **API Key mancante**: Controlla il file `.env`
- **Collection vuota**: Esegui `python ingest_faq.py`

---

## 📚 Documentazione Completa

- **README.md** - Documentazione dettagliata del progetto
- **USAGE_GUIDE.md** - Guida completa all'utilizzo
- **setup_instructions.md** - Istruzioni di setup dettagliate

