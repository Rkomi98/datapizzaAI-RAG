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
