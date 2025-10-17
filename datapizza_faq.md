# Datapizza-AI FAQ

---
id: faq_001
category: framework
tags: [framework, differenze, langchain, debug, modularità]
updated: 2025-10-14
status: answered
language: it
---

### Q: Cosa differenzia Datapizza-ai da altri framework già in circolazione?

**A:**  
La differenza principale con gli altri framework è il diverso livello di astrazione dei moduli. Langchain (ad esempio) ti permette di fare un sacco di cose, però usa astrazioni (a nostro avviso) un po' troppo elevate, che non ti permettono di uscire dai binari che il framework ti impone (o ti permette di farlo ma con estrema difficoltà).  
Un altro problema che abbiamo riscontrato con altri framework è la difficoltà del debug quando qualcosa si rompe: i diversi livelli di astrazione delle classi rendono il debug estremamente complesso.  

Siccome stiamo costruendo diversi prodotti GenAI con clienti diversi, abbiamo spesso bisogno di soluzioni "non standard". Da qui nasce la necessità di un framework che permetta di creare POC con pochissime righe di codice, ma che consenta anche di personalizzare rapidamente i moduli.  

---
id: faq_hf_models
category: integrazioni
tags: [huggingface, open-source, llm, compatibilità, client, prompt]
updated: 2025-10-14
status: answered
language: en
---

### Q: What about using the library even with open-source LLM models from Hugging Face? Does the code architecture remain the same, or should you always adapt prompt and other things based on the model selected?

**A:**  
At the moment, Hugging Face models are not supported natively.  
That said, the library is flexible enough that you can extend the Client to work with open-source LLMs too!

---
id: faq_memory_json
category: memory
tags: [memory, json, persistence, llm, chat, stato, reintegro]
updated: 2025-10-14
status: answered
language: it
related: []
---

### Q: Ho notato che la classe Memory offre i metodi `json_dumps()` e `json_loads(json_str)`.  
Vorrei capire se importare una memoria JSON salvata su DB e reiniettarla nel flusso LLM è un uso previsto e supportato.  
Ci sono vincoli sul formato JSON, sul versioning o sulla compatibilità futura?  
E qual è il modo consigliato per reintegrare una memoria preesistente nel modello (ad esempio, inizializzando lo stato memory prima di una nuova query)?  
Immaginate un’app ChatGPT-like in cui un utente ha più chat salvate: come prevedete la gestione e il ripristino di una memoria già esistente da cui ripartire?

**A:**  
Quella che hai descritto è esattamente il modo corretto di importare una memoria all'interno dell'applicativo.  
Puoi tranquillamente fare il dump della memoria su un DB e utilizzare `json_loads()` nel momento del bisogno per reintegrarla nel flusso dell’agente.  

**Alternative approach:**  
Ciao Salvo! Anche noi, dopo vari test, abbiamo optato per un approccio basato su un *manifest* inserito direttamente nel *system prompt* dell'agente.  
Per ora è la soluzione che ci ha portato a una maggiore stabilità nei casi d’uso complessi.


---
id: faq_audio_support
category: integrazioni
tags: [audio, google, client, file, inline]
updated: 2025-10-15
status: answered
language: it
related: []
---

### Q: Ciao a tutti, sto iniziando ad usare datapizza-ai ed vorrei sapere se il supporto ai file audio è solo del client Google

**A:**  
Yess, google è l'unico a supportare file audio inline all'intreno della conversazione, tutti gli altri ti obbligano a caricare un file e poi analizzare quello

---
id: faq_tool_stampa_pensieri
category: tools
tags: [stampa-pensieri, tool, testing, ragionamento, json]
updated: 2025-10-15
status: answered
language: it
related: []
---

### Q: per evitare che il modello fosse in qualche modo condizionato dall'uso del tool "Stampa pensieri" era necessario eseguirlo a posteriori non mi è chiaro come forzare la chiamata al tool ma dopo che abbia già fatto la chiamata il client.

**A:**  
Se vuoi usarlo per fare testing, invece di usare un tool è più comodo far rispondere al modello con un json con questa struttura:

{
    "risposta": # risposta alla domanda utente,
    "ragionamento": # il ragionamento che ti ha portato alla risposta
}

Quando fai il rilascio invece lo fai rispondere normalmente

---
id: faq_integrazione_progetti
category: use-cases
tags: [integrazione, progetti, agenti, rag, pipeline, chatbot]
updated: 2025-10-15
status: answered
language: it
related: []
---

### Q: Domanda ma se la volessi integrare in un mio progetto? Per cosa è “più portata” diciamo? Insomma a cosa serve? Devo pagare una fee?

**A:**  
Diciamo che questo framework serve ad aiutare gli sviluppatori nei loro progetti di Generative AI.  
Questi possono essere o semplici chatbot, o magari sistemi agentici. Per esempio hai un agente che riesce a riconoscere la richiesta dell'utente e in base alla sua richiesta chiama una serie di tool con un ordine specifico in base alla necessità.  
Grazie al framework risulta facile costruire un proprio sistema RAG o pipeline.
Infine, essendo opensource, il framework è free e sei libero di usarlo come vuoi :)!

---
id: faq_structured_responses
category: integrazioni
tags: [structured-responses, openai-like, base_url, autenticazione, errori, server]
updated: 2025-10-15
status: answered
language: it
related: []
---

### Q: Ciao, ho provato ad utilizzare le structured responses con il client openai like. Nello specifico, posso utilizzare n modelli passando il base_url di un servizio che ho sviluppato e nella key le informazioni che autenticano al servizio.  
Ottengo un Internal Server Error se uso le structured responses. Volevo chiedervi se fosse normale in quanto supportate solo dai client nativi.

**A:**  
Il server che hai sviluppato deve supportare questo tipo di risposte.  
Bisognerebbe scendere nel dettaglio di ciò che hai costruito e dell'errore che ricevi per dare una risposta certa.  
Sì, comunque ti direi di verificare il server che restituisce la risposta: probabilmente non supporta questo tipo di risposte.

---
id: faq_stregatto
category: framework
tags: [stregatto, cheshirecat, differenze, framework, applicativi]
updated: 2025-10-15
status: answered
language: it
related: []
---

### Q: Vale la pena sto framework e quanto ha di diverso dallo Stregatto?

**A:**  
Diciamo che coprono due esigenze diverse.  
Il tuo fork (come CheshireCat) fornisce già applicativi funzionanti e pronti all'uso (principalmente chatbot).  
Il tuo fork è interessante, però ha come punto di forza la creazione di applicativi già pronti, funzionanti e scalabili di CheshireCat.  

Il nostro framework invece ti permette di costruire soluzioni AI scendendo più in profondità, customizzando moduli per scrivere la migliore soluzione AI per risolvere un determinato problema.  
In sintesi, coprono due esigenze diverse.

---
id: faq_placeholder_example
category: integrazioni
tags: [placeholder, draft]
updated: 2025-10-14
status: draft
language: en
---

### Q: <Write the question here>

**A:**  
No answer yet.
