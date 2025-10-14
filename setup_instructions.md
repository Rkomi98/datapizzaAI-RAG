# Setup e Utilizzo del Chatbot RAG Datapizza-AI

## 📋 Prerequisiti

1. **Python 3.13+** (già configurato nel virtual environment)
2. **Qdrant Vector Database**
3. **OpenAI API Key**

## 🚀 Setup Completo

### 1. Attivare l'environment virtuale

```bash
source rag/bin/activate
```

### 2. Installare le dipendenze (se necessario)

```bash
pip install -r requirements.txt
```

### 3. Configurare le variabili d'ambiente

Crea un file `.env` nella root del progetto:

```bash
cp .env.example .env
```

Modifica il file `.env` e inserisci la tua OpenAI API Key:

```
OPENAI_API_KEY=sk-proj-...
```

### 4. Avviare Qdrant

Puoi avviare Qdrant usando Docker:

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

Oppure scarica e avvia Qdrant localmente da: https://qdrant.tech/documentation/quick-start/

### 5. Eseguire l'Ingestion delle FAQ

Prima di usare il chatbot, devi processare e ingerire i documenti FAQ:

```bash
python ingest_faq.py
```

Questo script:
- Legge i file `datapizza_faq.md` e `FAQ_Video.md`
- Li processa e divide in chunks
- Genera embeddings con OpenAI
- Li salva nel vector store Qdrant

Output atteso:
```
============================================================
🚀 Inizio ingestion delle FAQ Datapizza-AI
============================================================

📦 Setup vector store...
✓ Collection 'datapizza_faq' creata con successo

🔧 Creazione pipeline di ingestion...

📚 Ingestion documenti...
📄 Processando datapizza_faq.md...
✓ datapizza_faq.md processato con successo
📄 Processando FAQ_Video.md...
✓ FAQ_Video.md processato con successo

✅ Ingestion completata!
============================================================
```

### 6. Avviare il Chatbot

```bash
python chatbot_faq.py
```

## 💬 Utilizzo del Chatbot

Una volta avviato, il chatbot entrerà in modalità interattiva:

```
======================================================================
🤖 Chatbot FAQ Datapizza-AI
======================================================================
Fai le tue domande su Datapizza-AI!
Digita 'exit', 'quit' o 'esci' per terminare.
======================================================================

👤 Tu: Come si differenzia Datapizza-AI da Langchain?

🤖 Bot: La differenza principale è il diverso livello di astrazione...
```

### Esempi di Domande

- "Cosa differenzia Datapizza-AI da Langchain?"
- "Supporta modelli Llama?"
- "Come funziona la gestione della memory?"
- "Posso usare documenti aziendali in locale?"
- "Quali sono i casi d'uso concreti?"

## 🔧 Troubleshooting

### Errore: "OPENAI_API_KEY non trovata"
Assicurati di aver creato il file `.env` e inserito la tua API key.

### Errore: "Connection refused" (Qdrant)
Verifica che Qdrant sia in esecuzione su `localhost:6333`

### Errore: "Collection not found"
Esegui prima lo script di ingestion: `python ingest_faq.py`

### Il chatbot risponde sempre "Non sono ancora state fatte domande a riguardo"
Possibili cause:
1. L'ingestion non è stata eseguita correttamente
2. La soglia di similarity è troppo alta
3. La domanda è troppo generica o fuori topic

## 📚 Struttura del Progetto

```
.
├── datapizza_faq.md           # FAQ generali
├── FAQ_Video.md               # FAQ da video
├── ingest_faq.py              # Script per ingestion
├── chatbot_faq.py             # Chatbot interattivo
├── requirements.txt           # Dipendenze Python
├── .env                       # Configurazione (da creare)
├── .env.example              # Template configurazione
└── setup_instructions.md      # Questo file
```

## 🎯 Come Funziona

### Pipeline di Ingestion
1. **TextParser**: Legge i file markdown
2. **NodeSplitter**: Divide il testo in chunks di max 1000 caratteri
3. **ChunkEmbedder**: Genera embeddings con OpenAI (text-embedding-3-small)
4. **QdrantVectorstore**: Salva chunks ed embeddings nel database

### Pipeline di Retrieval (DagPipeline)
1. **ToolRewriter**: Riscrive la query per migliorare il retrieval
2. **OpenAIEmbedder**: Genera embedding della query
3. **QdrantVectorstore**: Recupera i chunks più simili
4. **ChatPromptTemplate**: Formatta prompt con contesto recuperato
5. **OpenAIClient**: Genera la risposta finale (gpt-4o-mini)

## 🔒 Note sulla Privacy

- Le query e i documenti vengono inviati a OpenAI per generare embeddings e risposte
- Se necessiti di privacy completa, considera l'uso di modelli locali (Llama/Mistral)
- Qdrant può essere configurato con persistenza su disco per non perdere i dati

## 📖 Risorse

- [Documentazione Datapizza-AI](https://docs.datapizza.ai/)
- [Guida RAG](https://docs.datapizza.ai/0.0.2/Guides/RAG/rag/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)

