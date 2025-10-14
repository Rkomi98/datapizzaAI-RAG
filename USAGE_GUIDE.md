# Guida all'Utilizzo del Chatbot RAG FAQ Datapizza-AI

## 📋 Introduzione

Questo documento fornisce una guida passo-passo per utilizzare il chatbot RAG che risponde alle domande sulle FAQ di Datapizza-AI.

## 🎯 Cosa fa questo sistema?

Il chatbot:
1. Analizza le domande che gli vengono poste
2. Cerca informazioni rilevanti nelle FAQ esistenti usando la ricerca semantica
3. Genera una risposta basata esclusivamente sulle informazioni trovate
4. Se non trova nulla di rilevante, risponde: **"Non sono ancora state fatte domande a riguardo."**

## 🚦 Setup Iniziale (Da fare una sola volta)

### Passo 1: Verifica l'Environment

```bash
# Assicurati di essere nella directory del progetto
cd /home/mcalcaterra/Documenti/GitHub/datapizzaAI-RAG

# Attiva l'environment virtuale
source rag/bin/activate
```

Dovresti vedere `(rag)` all'inizio del prompt del terminale.

### Passo 2: Configura l'API Key

1. Apri il file `.env` (o crealo se non esiste)
2. Inserisci la tua OpenAI API Key:

```
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXXXXXX
```

**Importante:** Non condividere mai la tua API key!

### Passo 3: Avvia Qdrant

Apri un **nuovo terminale** ed esegui:

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

Lascia questo terminale aperto. Qdrant deve rimanere in esecuzione.

Se non hai Docker, scarica Qdrant da: https://qdrant.tech/documentation/quick-start/

### Passo 4: Verifica il Setup

Torna al terminale con l'environment attivo ed esegui:

```bash
python test_setup.py
```

Se tutto è OK, vedrai:
```
🎉 Setup completato con successo!
```

### Passo 5: Ingestion delle FAQ (Solo la prima volta)

```bash
python ingest_faq.py
```

Questo processo:
- Legge i file `datapizza_faq.md` e `FAQ_Video.md`
- Li divide in chunks
- Genera embeddings
- Li salva in Qdrant

Output atteso:
```
🚀 Inizio ingestion delle FAQ Datapizza-AI
✓ Collection 'datapizza_faq' creata con successo
📄 Processando datapizza_faq.md...
✓ datapizza_faq.md processato con successo
📄 Processando FAQ_Video.md...
✓ FAQ_Video.md processato con successo
✅ Ingestion completata!
```

**Nota:** L'ingestion va eseguita solo una volta, o quando aggiorni le FAQ.

## 💬 Utilizzo del Chatbot

### Avvio

```bash
python chatbot_faq.py
```

Oppure usa lo script helper:

```bash
./run_chatbot.sh
```

### Interazione

Una volta avviato, vedrai:

```
======================================================================
🤖 Chatbot FAQ Datapizza-AI
======================================================================
Fai le tue domande su Datapizza-AI!
Digita 'exit', 'quit' o 'esci' per terminare.
======================================================================

👤 Tu: 
```

Digita la tua domanda e premi Invio.

### Esempi di Domande

**Domande che trovano risposta:**

```
👤 Tu: Cosa differenzia Datapizza-AI da Langchain?

🤖 Bot: La differenza principale con altri framework è il diverso livello 
di astrazione dei moduli. Langchain ti permette di fare molte cose, però 
usa astrazioni un po' troppo elevate...
```

```
👤 Tu: Posso usare modelli Llama?

🤖 Bot: Sì, il framework supporta anche Llama. All'interno della 
documentazione (su docs.datapizza.ai) è possibile trovare le istruzioni...
```

```
👤 Tu: Come funziona la memory?

🤖 Bot: La classe Memory offre i metodi json_dumps() e json_loads(json_str).
Puoi fare il dump della memoria su un DB e utilizzare json_loads() per 
reintegrarla nel flusso dell'agente...
```

**Domande fuori topic:**

```
👤 Tu: Che cos'è la fotosintesi clorofilliana?

🤖 Bot: Non sono ancora state fatte domande a riguardo.
```

```
👤 Tu: Qual è la capitale della Francia?

🤖 Bot: Non sono ancora state fatte domande a riguardo.
```

### Uscire dal Chatbot

Digita uno di questi comandi:
- `exit`
- `quit`
- `esci`
- `q`

Oppure premi `Ctrl+C`

## 🔄 Workflow Tipico

### Uso Giornaliero

1. **Apri terminale 1**: Avvia Qdrant (se non è già attivo)
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

2. **Apri terminale 2**: Avvia il chatbot
   ```bash
   cd /home/mcalcaterra/Documenti/GitHub/datapizzaAI-RAG
   source rag/bin/activate
   python chatbot_faq.py
   ```

3. **Fai le tue domande!**

### Aggiornamento FAQ

Se aggiorni i file FAQ:

1. Modifica `datapizza_faq.md` o `FAQ_Video.md`
2. Ri-esegui l'ingestion:
   ```bash
   python ingest_faq.py
   ```
3. Riavvia il chatbot (se era già in esecuzione)

## 🐛 Risoluzione Problemi Comuni

### Problema: "OPENAI_API_KEY non trovata"

**Soluzione:**
1. Verifica che il file `.env` esista
2. Verifica che contenga la riga: `OPENAI_API_KEY=sk-...`
3. Assicurati che non ci siano spazi prima o dopo l'uguale

### Problema: "Connection refused" (Qdrant)

**Soluzione:**
1. Verifica che Qdrant sia in esecuzione:
   ```bash
   curl http://localhost:6333/health
   ```
2. Se non risponde, avvia Qdrant:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

### Problema: "Collection not found"

**Soluzione:**
Esegui l'ingestion:
```bash
python ingest_faq.py
```

### Problema: Risposte sempre "Non sono ancora state fatte domande..."

**Possibili cause e soluzioni:**

1. **L'ingestion non è stata eseguita**
   ```bash
   python ingest_faq.py
   ```

2. **La domanda è troppo diversa dalle FAQ**
   - Prova a riformulare la domanda
   - Usa termini tecnici presenti nelle FAQ

3. **La soglia di similarity è troppo alta**
   - Apri `chatbot_faq.py`
   - Cerca `score_threshold = 0.5`
   - Prova a ridurlo a `0.3`

### Problema: "Environment virtuale non attivo"

**Soluzione:**
```bash
source rag/bin/activate
```

Dovresti vedere `(rag)` nel prompt.

## 💡 Tips e Best Practices

### Formulazione delle Domande

**✅ Buone domande:**
- "Come si differenzia Datapizza-AI da altri framework?"
- "Supporta modelli open source?"
- "Posso usare documenti aziendali in locale?"
- "Quali sono i casi d'uso?"

**❌ Domande troppo generiche:**
- "Cos'è l'AI?"
- "Come funziona Python?"
- "Che ore sono?"

### Ottimizzazione

- **Per risposte più accurate**: Usa `gpt-4o` invece di `gpt-4o-mini`
- **Per risposte più veloci**: Riduci `k` (numero di chunks recuperati)
- **Per più contesto**: Aumenta `k` e `max_char` nei chunks

### Monitoraggio Costi

Ogni domanda consuma:
- ~100-200 tokens per gli embeddings
- ~500-2000 tokens per la generazione (dipende dalla risposta)

Con i prezzi attuali di OpenAI:
- ~$0.0001 per domanda (embeddings)
- ~$0.001-0.005 per domanda (generazione con gpt-4o-mini)

## 📊 Metriche e Performance

### Tempi di risposta tipici:
- Query rewriting: ~0.5-1s
- Embedding: ~0.2-0.5s
- Retrieval: ~0.1-0.3s
- Generazione: ~1-3s
- **Totale: ~2-5 secondi per domanda**

### Capacità:
- FAQ supportate: Illimitate
- Chunks per FAQ: Dipende dalla lunghezza
- Queries simultanee: 1 (modalità interattiva)

## 🔐 Sicurezza

- ✅ La API key è in `.env` (escluso da Git)
- ✅ I dati rimangono su OpenAI per max 30 giorni (policy OpenAI)
- ✅ Qdrant gira localmente (i dati non escono dalla tua macchina)
- ⚠️  Per privacy completa, usa modelli locali (Llama/Mistral)

## 📚 Prossimi Passi

Dopo aver preso confidenza con il chatbot:

1. **Personalizza i prompt** in `chatbot_faq.py`
2. **Aggiungi nuove FAQ** ai file markdown
3. **Sperimenta con altri modelli** (GPT-4, Claude, Llama)
4. **Estendi le funzionalità** (web interface, multi-utente, ecc.)
5. **Integra con applicazioni** esistenti

## 🆘 Supporto

Per problemi o domande:
- Consulta la [documentazione Datapizza-AI](https://docs.datapizza.ai/)
- Controlla i log del chatbot per errori specifici
- Verifica che tutti i servizi siano attivi (Qdrant, API OpenAI)

## 📝 Note Finali

Questo chatbot è un esempio di come costruire un sistema RAG completo e funzionante. 
È progettato per essere:
- **Facile da usare** per utenti non tecnici
- **Facile da estendere** per sviluppatori
- **Pronto per la produzione** con piccole modifiche

Buon utilizzo! 🚀

