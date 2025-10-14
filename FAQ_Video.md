
--------------------------------------------------------------------------------
id: faq_002category: frameworktags: [framework, client, integrazioni, standard]updated: 2025-10-14status: answeredlanguage: it
Q: Ci sono differenze o somiglianze nel modo in cui l'astrazione dei client provider è gestita in Datapizza-AI rispetto ad altri framework?
A:
A grandi linee, per quanto riguarda la parte client, questo approccio è lo standard nel settore, nel senso che qualunque framework GenAI dà la possibilità di fare l'astrazione sui client
.

--------------------------------------------------------------------------------
id: faq_003category: integrazionitags: [llm, open-source, llama, client, compatibilità]updated: 2025-10-14status: answeredlanguage: it
Q: Datapizza-AI funziona con modelli Llama?
A:
Sì, il framework supporta anche Llama
. All'interno della documentazione (su doc.datapizza.ai), è possibile trovare come eseguire un client Llama o un server Llama in locale
.

--------------------------------------------------------------------------------
id: faq_004category: frameworktags: [integrazioni, vectorstore, roadmo, grafana, database]updated: 2025-10-14status: answeredlanguage: it
Q: Datapizza-AI supporta anche Grafana (come Vector Store)?
A:
Non supportiamo nativamente Grafana per ora, ma è in pipeline, quindi è nella roadmap del progetto
.

--------------------------------------------------------------------------------
id: faq_005category: ragtags: [rag, documenti, parser, open-source, integrazioni, azure, dockling]updated: 2025-10-14status: answeredlanguage: it
Q: Perché Datapizza-AI ha scelto di includere Dockling come parser per i documenti, e quali sono i vantaggi rispetto a soluzioni come Azure Document Intelligence?
A:
Il team di Datapizza usa spesso Document Intelligence di Azure internamente, assieme ad altri LLM, e sono le due soluzioni incluse nel framework
. Hanno scelto di includere Dockling perché volevano avere una pipeline che fosse fruibile da tutti. Non potevano rilasciare un framework con un unico parser a pagamento, e Dockling è risultato essere uno dei migliori tra i framework open source provati, garantendo una soluzione open per l'estrazione
.

--------------------------------------------------------------------------------
id: faq_006category: ragtags: [rag, chunking, splitter, moduli, avanzato]updated: 2025-10-14status: answeredlanguage: it
Q: Ci sono moduli che integrano tecniche di chunking avanzate?
A:
Il chunking viene fatto principalmente dai parser
. Tuttavia, nel framework esistono diversi splitter che permettono di fare cose diverse dopo l'output del parser. Il framework è molto semplice e aperto, tanto che si incoraggia a sviluppare il proprio splitter custom
.

--------------------------------------------------------------------------------
id: faq_007category: ragtags: [rag, chunking, splitter, documentazione, supporto]updated: 2025-10-14status: answeredlanguage: it
Q: Sarebbe utile un modulo che aiuti a scegliere meglio gli splitter per il chunking?
A:
Il team ha pensato a un tale modulo, ma ha deciso di non includerlo
. L'idea è che gli splitter sono veramente pochi e semplici da utilizzare, e si presuppone che la documentazione sia scritta abbastanza bene da non necessitare di uno strumento di supporto per la scelta
.

--------------------------------------------------------------------------------
id: faq_008category: privacytags: [privacy, gpt, gdpr, locale, modelli, lama, azure]updated: 2025-10-14status: answeredlanguage: it
Q: Per la gestione dei documenti aziendali (contenuto molto tecnico), posso interrogare i miei documenti in locale senza paure che possano essere usati i dati sensibili?
A:
Sì, questo è possibile, a patto che si utilizzi un modello locale
. Grazie al fatto che il framework integra il client Lama, è possibile ospitare il proprio modello (come Mistral o Llama) in locale ed eseguire tutte le operazioni lì. Se si rimane in locale, il documento non lascia la macchina
.
È anche importante notare che il framework include il client Azure Open AI, che permette di utilizzare i modelli di Open AI che girano su un server Azure, i quali sono di solito GDPR compliant e ospitati in Europa
.

--------------------------------------------------------------------------------
id: faq_009category: frameworktags: [framework, stregatto, competizione, chatbot, obiettivi]updated: 2025-10-14status: answeredlanguage: it
Q: Qual è la differenza tra Datapizza-AI e il framework Stregatto?
A:
Il framework Stregatto non è visto in competizione con Datapizza-AI
. Stregatto si rivolge principalmente a persone che hanno bisogno di sviluppare dei chatbot in modo molto rapido e veloce. Datapizza-AI, pur potendo essere usato per un chatbot (la demo ne ha mostrato uno con 32 righe di codice), ha potenzialità infinite e permette di sviluppare qualunque tipo di applicativo, non solo chatbot. Si ritiene che servano due nicchie diverse
.

--------------------------------------------------------------------------------
id: faq_010category: pipelinetags: [pipeline, dag, airflow, integrazioni, dipendenze]updated: 2025-10-14status: answeredlanguage: it
Q: Avete previsto l'integrazione con Airflow?
A:
Non è stata implementata l'integrazione con Airflow perché il team non ha avuto la necessità di farlo
. L'idea era di evitare di legarsi a un provider o un software esterno (non proprio) di cui si devono imparare le astrazioni, come è successo con i framework GenAI preesistenti. La scelta è stata di sviluppare internamente le Pipeline (come la DAG Pipeline). È possibile che in futuro venga implementato il supporto
.

--------------------------------------------------------------------------------
id: faq_011category: pipelinetags: [pipeline, dag, langgraph, confronto, complessità]updated: 2025-10-14status: answeredlanguage: it
Q: Il concetto di DAG Pipeline è simile a quello dei grafi di LangChain (LangGraph)?
A:
Secondo il team, le due soluzioni non competono sullo stesso livello
. La DAG Pipeline di Datapizza AI è stata pensata per essere molto grezza e permette di andare "molto nel piccolo" per capire le dipendenze di ogni modulo. Non ha moltissime feature. LangGraph, invece, potrebbe essere considerato un ecosistema più evoluto e grande
.

--------------------------------------------------------------------------------
id: faq_012category: frameworktags: [casi d'uso, rag, agenti, multi-agente, delivery]updated: 2025-10-14status: answeredlanguage: it
Q: Quali sono gli esempi di utilizzi concreti di questo framework?
A:
Il framework è stato creato per sviluppare use case che abbiano un impatto vero e siano rilasciabili in produzione
.
Esempi di utilizzi concreti includono
:
1. Sistemi RAG (Retrieval Augmented Generation): Un modello generativo che risponde basandosi su informazioni pescate da una base di conoscenza aziendale (come PDF o file Excel)
.
2. Sistemi Multi-Agente:
    ◦ Agenti che collaborano per analizzare dati presenti su file Excel o database, con agenti specializzati nel recupero dati, e un agente specializzato nel creare visualizzazioni grafiche per spiegare l'analisi
.
    ◦ Agenti che collaborano per scrivere blog post ottimizzati per la SEO, basati su fonti web (agenti specializzati nel recupero dati, nella creazione del draft e nell'ottimizzazione SEO)
.

--------------------------------------------------------------------------------
id: faq_013category: monitoringtags: [costi, token, monitoring, tracking, file di configurazione]updated: 2025-10-14status: answeredlanguage: it
Q: Avete pensato a un layer di tracking costi per monitorare i token usage per tenant o utente in tempo reale?
A:
Il sistema di tracing e monitoring attuale mostra già i token usati in input e in output, oltre alla durata e alla latenza delle chiamate
.
È stata discussa la possibilità di aggiungere un meccanismo che, tramite un file di configurazione, permetta di calcolare automaticamente i costi
. Questo approccio è preferito perché i costi dei provider cambiano nel tempo, e hardcodare i costi nel framework non avrebbe senso
.

--------------------------------------------------------------------------------
id: faq_014category: clienttags: [client, api, openai, parametri specifici, customizzazione]updated: 2025-10-14status: answeredlanguage: it
Q: Come vengono gestiti i parametri specifici di un provider, come ad esempio il  di Open AI?
A:
Il framework è stato costruito per lasciare la libertà di aggiungere argomenti che non sono necessariamente in comune con tutti i client
. Parametri come il previous_response_ID (che è puramente di Open AI) possono essere aggiunti durante la chiamata e verranno inseriti nella richiesta al provider
.

--------------------------------------------------------------------------------
id: faq_015category: evaluationtags: [evaluation, testing, metriche, sviluppo, retrieval, llm_judges]updated: 2025-10-14status: answeredlanguage: it
Q: Il framework ha strumenti pensati per facilitare e velocizzare l'evaluation dei modelli/risposte?
A:
Sì, l'evaluation è uno dei pilastri su cui si basa il team di Ricerca e Sviluppo (R&D) per la GenAI
. Tuttavia, le funzionalità di evaluation non sono state ancora rilasciate come open source perché non sono state reputate abbastanza mature
.
Queste funzionalità, che sono presenti nel repository interno, includono metriche per la fase di retrieval in una RAG e strumenti come gli LLM judges per valutare le risposte finali dei modelli
.

--------------------------------------------------------------------------------
id: faq_016category: clienttags: [client, thinking_budget, google, parametri specifici, ragionamento]updated: 2025-10-14status: answeredlanguage: it
Q: Datapizza-AI supporta anche il thinking budget di Google?
A:
Sì, come per altri parametri opzionali specifici di un provider, viene lasciata la possibilità di aggiungere parametri come il thinking budget
.
(Nota: il  è un parametro che specifica il livello di profondità a cui il modello deve "pensare" o ragionare prima di dare una risposta, influenzando tempo e token spesi in )
.

--------------------------------------------------------------------------------
id: faq_017category: agentitags: [agenti, strumenti_visuali, nocode, lowcode, controllo, vendor_lockin]updated: 2025-10-14status: answeredlanguage: it
Q: Quali sono i vantaggi di usare Datapizza-AI rispetto all'utilizzo di tool visuali (no code/low code) per agenti conversazionali, come Flowwise o Agent Builder di Open AI?
A:
Gli strumenti visuali (no code/low code) sono utili per automazioni semplici, a basso rischio, o per fare un esperimento rapido, specialmente per persone con un background non tecnico (come un marketer per scrivere blog post)
.
Tuttavia, questi strumenti storicamente si limitano e si fermano oltre un certo genere di attività, offrendo un controllo limitato
.
Datapizza-AI, invece, è stato progettato per
:
1. Massima Potenza e Controllo: Dare il massimo controllo a un ingegnere per sviluppare soluzioni completamente custom sui propri documenti o per eseguire azioni specifiche, specialmente per problemi complessi o progetti critici
.
2. Anti-Vendor Lock-in: Gli strumenti dei grandi vendor (Google, Open AI, Microsoft) hanno sempre un incentivo a creare lock-in all'interno del proprio ecosistema
. Il principio fondamentale di Datapizza AI è l'opposto: essere aperto e completamente agnostico rispetto ai framework e ai provider
.
3. Velocità di Apprendimento: È pensato per essere talmente intuitivo e semplice da imparare che si ritiene possa essere più veloce imparare a usare il framework che le interfacce grafiche complesse dei vendor
.

--------------------------------------------------------------------------------
id: faq_018category: agentitags: [contesto, memory, bloat, compressione, state_management]updated: 2025-10-14status: answeredlanguage: it
Q: Come gestite il bloat del contesto quando cresce troppo (ad esempio, con più agenti che si passano informazioni)? C'è un meccanismo di compressione del contesto o di state management ottimizzato?
A:
Questa è una tematica cruciale su cui il team di sviluppo sta attualmente lavorando
. Al momento, non è presente nativamente su Datapizza AI un modo per comprimere o fare una selezione ottimizzata dei turni di conversazione nella memory. Tuttavia, l'obiettivo è studiare la soluzione più efficace e implementarla presto nel framework.
