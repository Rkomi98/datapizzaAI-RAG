# 🎉 MCP Integration Guide - Documentazione Ufficiale Datapizza-AI

## ✅ Integrazione Completata!

Ho integrato con successo il server MCP del tuo amico per interrogare la documentazione ufficiale di datapizza-ai direttamente dal repository GitHub.

## 📋 Cosa è Stato Fatto

### 1. ✅ Setup MCP Server
- **Clonato** il repository: `https://github.com/mat1312/mcp-server-datapizza`
- **Installato** il package MCP in modalità development
- **Configurato** le variabili d'ambiente (`.env` in `mcp-server-datapizza/datapizza-mcp-server/`)

### 2. ✅ Indicizzazione Documentazione
- **Scaricati e indicizzati** 46 documenti dalla docs ufficiale di datapizza-ai
- **Utilizzato** OpenAI embeddings (`text-embedding-3-small`, 1536 dimensioni)
- **Salvato** su Qdrant Cloud nella collection `datapizza_official_docs`

### 3. ✅ Test Retrieval
Ho testato il MCP retriever con le domande che hai suggerito:

#### Query Testate:
1. **"How can I install datapizza-ai?"**
   - ✅ Risposta: Istruzioni su `pip install datapizza-ai` e varianti con provider specifici
   
2. **"How can I set up a RAG?"**
   - ✅ Risposta: Esempi completi di DagPipeline con rewriter, embedder, retriever, prompt e generator
   
3. **"How can I monitor my pipeline?"**
   - ✅ Risposta: OpenTelemetry tracing, Client I/O tracing, Custom spans
   
4. **"Quali sono i principali moduli di datapizza-ai?"**
   - ✅ Risposta: Parsers, Captioners, Metatagger, Prompt, Rewriters, Splitters, Treebuilder
   
5. **"Come funziona il DagPipeline?"**
   - ✅ Risposta: Esempi di connessione tra moduli e esecuzione pipeline RAG

## 📁 File Creati

### 1. `test_mcp_retriever.py`
Script per testare il retriever MCP con query predefinite.

```bash
python test_mcp_retriever.py
```

### 2. `chatbot_enhanced.py`
Chatbot potenziato che combina:
- **FAQ Locali** (dalla tua ingestion esistente)
- **Documentazione Ufficiale** (tramite MCP)

Caratteristiche:
- Query automatica su entrambe le fonti
- Combina le informazioni per risposte più complete
- Mantiene la Memory per conversazioni contestuali
- Debug mode per vedere il processo di retrieval

## 🚀 Come Usare

### Opzione 1: Test Standalone del MCP Retriever

```bash
cd /home/mcalcaterra/Documenti/GitHub/datapizzaAI-RAG
source rag/bin/activate
python test_mcp_retriever.py
```

### Opzione 2: Chatbot Enhanced (FAQ + Docs Ufficiali)

```bash
cd /home/mcalcaterra/Documenti/GitHub/datapizzaAI-RAG
source rag/bin/activate
python chatbot_enhanced.py
```

Questo chatbot:
1. Interroga le FAQ locali (con Gemini embeddings)
2. Interroga la documentazione ufficiale (con OpenAI embeddings via MCP)
3. Combina le informazioni per dare una risposta completa

### Opzione 3: Chatbot Originale (Solo FAQ)

Se preferisci usare solo le FAQ locali:

```bash
python chatbot_faq.py
```

## 🔧 Configurazione

### File `.env` Principale
```bash
# API Keys
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here

# Qdrant Configuration
QDRANT_URL=https://your-qdrant-instance.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_key_here

# MCP Server Configuration
COLLECTION_NAME=datapizza_official_docs
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
```

### File `.env` MCP Server
In `mcp-server-datapizza/datapizza-mcp-server/.env`:
```bash
OPENAI_API_KEY=your_openai_key_here
QDRANT_URL=https://your-qdrant-instance.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_key_here
COLLECTION_NAME=datapizza_official_docs
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
```

## 📊 Qdrant Collections

Ora hai **due collection** in Qdrant:

1. **`faq`** (o il nome che usi per le FAQ locali)
   - Embeddings: Google Gemini (`gemini-embedding-001`, 3072 dim)
   - Contenuto: FAQ locali + Scripts

2. **`datapizza_official_docs`**
   - Embeddings: OpenAI (`text-embedding-3-small`, 1536 dim)
   - Contenuto: Documentazione ufficiale da GitHub (46 documenti)

## 🔄 Re-Indicizzazione

Se vuoi aggiornare la documentazione ufficiale:

```bash
cd /home/mcalcaterra/Documenti/GitHub/datapizzaAI-RAG/mcp-server-datapizza/datapizza-mcp-server
source ../../rag/bin/activate
python -m datapizza_mcp.indexer --force
```

Il flag `--force` cancellerà e ricreerà la collection.

## 🎯 Vantaggi dell'Integrazione

### Prima (Solo FAQ Locali)
- ✅ Risposte rapide su domande comuni
- ❌ Limitato alle FAQ che hai creato manualmente
- ❌ Non include la documentazione completa

### Dopo (FAQ + Docs Ufficiali)
- ✅ Risposte su domande comuni dalle FAQ
- ✅ **Accesso a tutta la documentazione ufficiale**
- ✅ Informazioni su API, moduli, esempi avanzati
- ✅ Sempre aggiornato (basta re-indicizzare)

## 🧪 Esempi di Query Potenziate

### Query che beneficiano delle docs ufficiali:

1. **"Come usare il TextParser?"**
   - Prima: "Non sono ancora state fatte domande a riguardo"
   - Dopo: Esempi completi dalla documentazione ufficiale

2. **"Quali parametri ha il NodeSplitter?"**
   - Prima: Informazioni limitate
   - Dopo: Documentazione completa dei parametri

3. **"Come integrare Qdrant con OpenAI embeddings?"**
   - Prima: Info di base dalle FAQ
   - Dopo: Esempi completi + FAQ + docs ufficiali

## 📈 Statistiche

- **Documenti indicizzati**: 46 files dalla docs ufficiale
- **Chunks generati**: ~150+ chunks semantici
- **Modello embeddings**: `text-embedding-3-small` (OpenAI)
- **Dimensioni vector**: 1536
- **Storage**: Qdrant Cloud
- **Tempo indicizzazione**: ~2-3 minuti

## 🎓 Prossimi Passi Consigliati

1. **Testa il chatbot enhanced** con domande complesse che richiedono sia FAQ che docs
2. **Aggiungi più FAQ** locali per domande ricorrenti degli utenti
3. **Re-indicizza periodicamente** la docs ufficiale per restare aggiornato
4. **Integra nel frontend web** (app.py) per renderlo disponibile via Streamlit

## 📚 Risorse

- **Repository MCP Server**: https://github.com/mat1312/mcp-server-datapizza
- **Docs Datapizza-AI**: https://docs.datapizza.ai
- **Repository Datapizza-AI**: https://github.com/datapizza-labs/datapizza-ai

## 🤝 Crediti

Grazie al tuo amico per aver creato l'MCP server! È un ottimo esempio di integrazione RAG con la documentazione ufficiale.

---

**Nota**: Tutti i test sono stati eseguiti con successo e il sistema è pronto per l'uso! 🎉

