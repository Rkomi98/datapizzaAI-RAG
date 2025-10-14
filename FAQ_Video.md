# Datapizza-AI FAQ (Video)

---
id: faq_002
category: framework
tags: [framework, client, integrazioni, standard]
updated: 2025-10-14
status: answered
language: it
---

### Q: Ci sono differenze o somiglianze nel modo in cui l'astrazione dei client provider è gestita in Datapizza-AI rispetto ad altri framework?

**A:**  
A grandi linee, per quanto riguarda la parte client, questo approccio è lo standard nel settore: qualunque framework GenAI propone un layer di astrazione sui client.

---
id: faq_003
category: integrazioni
tags: [llm, open-source, llama, client, compatibilità]
updated: 2025-10-14
status: answered
language: it
---

### Q: Datapizza-AI funziona con modelli Llama?

**A:**  
Sì, il framework supporta anche Llama. All'interno della documentazione (su doc.datapizza.ai) è possibile trovare le istruzioni per eseguire un client Llama o un server Llama in locale.

---
id: faq_004
category: framework
tags: [integrazioni, vectorstore, roadmap, grafana, database]
updated: 2025-10-14
status: answered
language: it
---

### Q: Datapizza-AI supporta anche Grafana (come Vector Store)?

**A:**  
Non supportiamo nativamente Grafana per ora, ma è in pipeline e rientra nella roadmap del progetto.

---
id: faq_005
category: rag
tags: [rag, documenti, parser, open-source, integrazioni, azure, dockling]
updated: 2025-10-14
status: answered
language: it
---

### Q: Perché Datapizza-AI ha scelto di includere Dockling come parser per i documenti, e quali sono i vantaggi rispetto a soluzioni come Azure Document Intelligence?

**A:**  
Il team di Datapizza usa spesso Document Intelligence di Azure internamente, insieme ad altri LLM, e sono le due soluzioni incluse nel framework. È stato scelto Dockling per avere una pipeline fruibile da tutti: non si poteva rilasciare un framework con un unico parser a pagamento e Dockling è risultato fra i migliori framework open source provati, garantendo una soluzione aperta per l'estrazione.

---
id: faq_006
category: rag
tags: [rag, chunking, splitter, moduli, avanzato]
updated: 2025-10-14
status: answered
language: it
---

### Q: Ci sono moduli che integrano tecniche di chunking avanzate?

**A:**  
Il chunking viene svolto principalmente dai parser. Tuttavia, nel framework esistono diversi splitter che consentono di eseguire operazioni differenti sull'output del parser e si incoraggia la creazione di splitter personalizzati.

---
id: faq_007
category: rag
tags: [rag, chunking, splitter, documentazione, supporto]
updated: 2025-10-14
status: answered
language: it
---

### Q: Sarebbe utile un modulo che aiuti a scegliere meglio gli splitter per il chunking?

**A:**  
Il team ha valutato l'idea di creare un modulo dedicato, ma ha deciso di non includerlo. Gli splitter sono pochi e semplici da utilizzare e la documentazione è pensata per guidare la scelta senza bisogno di strumenti aggiuntivi.

---
id: faq_008
category: privacy
tags: [privacy, gpt, gdpr, locale, modelli, llama, azure]
updated: 2025-10-14
status: answered
language: it
---

### Q: Per la gestione dei documenti aziendali (contenuto molto tecnico), posso interrogare i miei documenti in locale senza timore che vengano usati dati sensibili?

**A:**  
Sì, è possibile, a patto di utilizzare un modello locale. Grazie all'integrazione del client Llama, è possibile ospitare un modello (ad esempio Mistral o Llama) in locale ed eseguire tutte le operazioni sulla propria macchina, evitando che i documenti lascino l'ambiente interno. È anche importante notare che il framework include il client Azure Open AI, che permette di utilizzare i modelli OpenAI in esecuzione su server Azure, generalmente GDPR compliant e ospitati in Europa.

---
id: faq_009
category: framework
tags: [framework, stregatto, competizione, chatbot, obiettivi]
updated: 2025-10-14
status: answered
language: it
---

### Q: Qual è la differenza tra Datapizza-AI e il framework Stregatto?

**A:**  
Il framework Stregatto non è considerato un competitor diretto di Datapizza-AI. Stregatto punta a chi deve sviluppare chatbot in modo rapido, mentre Datapizza-AI, pur potendo essere usato per un chatbot (la demo lo mostra con 32 righe di codice), è progettato per coprire un ampio ventaglio di applicazioni e supportare progetti complessi.

---
id: faq_010
category: pipeline
tags: [pipeline, dag, airflow, integrazioni, dipendenze]
updated: 2025-10-14
status: answered
language: it
---

### Q: Avete previsto l'integrazione con Airflow?

**A:**  
Non è stata implementata l'integrazione con Airflow perché il team non ne ha avvertito l'esigenza. L'obiettivo era evitare dipendenze da software esterni con astrazioni proprie, preferendo sviluppare internamente le Pipeline (come la DAG Pipeline). In futuro si valuterà se aggiungere il supporto.

---
id: faq_011
category: pipeline
tags: [pipeline, dag, langgraph, confronto, complessità]
updated: 2025-10-14
status: answered
language: it
---

### Q: Il concetto di DAG Pipeline è simile a quello dei grafi di LangChain (LangGraph)?

**A:**  
Secondo il team le due soluzioni non competono sullo stesso piano. La DAG Pipeline di Datapizza-AI è volutamente essenziale per comprendere le dipendenze tra i moduli, mentre LangGraph può essere considerato un ecosistema più ricco di funzionalità.

---
id: faq_012
category: framework
tags: [casi_d'uso, rag, agenti, multi-agente, delivery]
updated: 2025-10-14
status: answered
language: it
---

### Q: Quali sono gli esempi di utilizzi concreti di questo framework?

**A:**  
Il framework nasce per realizzare use case ad alto impatto, pronti per la produzione.  
Esempi concreti includono:  
1. Sistemi RAG (Retrieval Augmented Generation) in cui un modello generativo risponde basandosi su informazioni tratte da basi di conoscenza aziendali (ad esempio PDF o file Excel).  
2. Sistemi multi-agente, come:  
   - Agenti che collaborano per analizzare dati presenti su file Excel o database, con ruoli specializzati per il recupero dati e per la creazione di visualizzazioni.  
   - Agenti che collaborano per scrivere blog post ottimizzati per la SEO, basandosi su fonti web con ruoli dedicati al recupero dati, alla stesura del draft e all'ottimizzazione SEO.

---
id: faq_013
category: monitoring
tags: [costi, token, monitoring, tracking, configurazione]
updated: 2025-10-14
status: answered
language: it
---

### Q: Avete pensato a un layer di tracking costi per monitorare il consumo di token per tenant o utente in tempo reale?

**A:**  
Il sistema di tracing e monitoring attuale mostra già i token usati in input e in output, oltre alla durata e alla latenza delle chiamate. È stata discussa l'aggiunta di un meccanismo basato su file di configurazione per calcolare automaticamente i costi, così da evitare valori hardcoded che diventerebbero obsoleti quando i provider aggiornano i listini.

---
id: faq_014
category: client
tags: [client, api, openai, parametri_specifici, customizzazione]
updated: 2025-10-14
status: answered
language: it
---

### Q: Come vengono gestiti i parametri specifici di un provider, come ad esempio il `previous_response_id` di OpenAI?

**A:**  
Il framework è stato progettato per permettere l'aggiunta di argomenti che non sono condivisi da tutti i client. Parametri come il `previous_response_id` (tipico di OpenAI) possono essere passati alla chiamata e verranno inoltrati correttamente al provider.

---
id: faq_015
category: evaluation
tags: [evaluation, testing, metriche, sviluppo, retrieval, llm_judges]
updated: 2025-10-14
status: answered
language: it
---

### Q: Il framework ha strumenti pensati per facilitare e velocizzare l'evaluation dei modelli e delle risposte?

**A:**  
L'evaluation è uno dei pilastri del team di Ricerca e Sviluppo dedicato alla GenAI, ma le funzionalità non sono ancora state rilasciate come open source perché considerate immature. Internamente esistono metriche per la fase di retrieval in una RAG e strumenti come gli LLM judges per valutare le risposte finali, che verranno pubblicati quando saranno pronti.

---
id: faq_016
category: client
tags: [client, thinking_budget, google, parametri_specifici, ragionamento]
updated: 2025-10-14
status: answered
language: it
---

### Q: Datapizza-AI supporta anche il thinking budget di Google?

**A:**  
Sì, come per altri parametri opzionali specifici di un provider, è possibile aggiungere parametri come il thinking budget.  
(Nota: il thinking budget è un parametro che indica quanto in profondità il modello deve ragionare prima di rispondere, influenzando tempo e token utilizzati.)

---
id: faq_017
category: agenti
tags: [agenti, strumenti_visuali, nocode, lowcode, controllo, vendor_lockin]
updated: 2025-10-14
status: answered
language: it
---

### Q: Quali sono i vantaggi di usare Datapizza-AI rispetto a tool visuali (no code/low code) per agenti conversazionali, come Flowwise o Agent Builder di OpenAI?

**A:**  
Gli strumenti visuali (no code/low code) sono utili per automazioni semplici, a basso rischio, o per prove rapide, soprattutto per persone con background non tecnico. Tuttavia, tendono a limitarsi quando la complessità aumenta e offrono un controllo ridotto.  
Datapizza-AI, invece, è stato progettato per garantire:  
1. Massima potenza e controllo, fornendo a un ingegnere tutto il necessario per sviluppare soluzioni completamente custom su documenti proprietari o per automatizzare azioni specifiche nei casi d'uso più complessi.  
2. Anti vendor lock-in, adottando un approccio aperto e agnostico rispetto a framework e provider, in contrasto con gli ecosistemi proprietari dei grandi vendor.  
3. Velocità di apprendimento, perché l'interfaccia del framework è pensata per essere più rapida da padroneggiare rispetto alle interfacce grafiche complesse dei vendor.

---
id: faq_018
category: agenti
tags: [contesto, memory, bloat, compressione, state_management]
updated: 2025-10-14
status: answered
language: it
---

### Q: Come gestite il bloat del contesto quando cresce troppo (ad esempio con più agenti che si scambiano informazioni)? C'è un meccanismo di compressione del contesto o di state management ottimizzato?

**A:**  
È un tema cruciale su cui il team sta lavorando. Al momento non esiste in Datapizza-AI un sistema nativo per comprimere o selezionare in modo ottimizzato i turni di conversazione nella memory, ma l'obiettivo è individuare la soluzione più efficace e integrarla presto nel framework.
