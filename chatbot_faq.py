"""
Chatbot RAG per rispondere alle domande sulle FAQ di Datapizza-AI.
Utilizza DagPipeline per retrieval e generazione risposte.
"""

import os
from dotenv import load_dotenv
from datapizza.clients.openai import OpenAIClient
from datapizza.embedders.openai import OpenAIEmbedder
from datapizza.modules.prompt import ChatPromptTemplate
from datapizza.modules.rewriters import ToolRewriter
from datapizza.pipeline import DagPipeline
from datapizza.vectorstores.qdrant import QdrantVectorstore
from datapizza.core.vectorstore import VectorConfig

# Carica variabili d'ambiente
load_dotenv()

class FAQChatbot:
    """Chatbot RAG per le FAQ di Datapizza-AI."""
    
    def __init__(self):
        """Inizializza il chatbot con tutti i componenti necessari."""
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY non trovata nel file .env")
        
        # Inizializza componenti
        self._setup_clients()
        self._setup_pipeline()
    
    def _setup_clients(self):
        """Configura i client OpenAI."""
        self.openai_client = OpenAIClient(
            model="gpt-4o-mini",
            api_key=self.openai_api_key
        )
        
        self.embedder = OpenAIEmbedder(
            api_key=self.openai_api_key,
            model_name="text-embedding-3-small"
        )
        
        self.query_rewriter = ToolRewriter(
            client=self.openai_client,
            system_prompt="""Riscrivi la domanda dell'utente per migliorare il retrieval.
            Espandi abbreviazioni, aggiungi contesto e mantieni i termini tecnici importanti.
            Restituisci solo la query riscritta, senza spiegazioni aggiuntive."""
        )
    
    def _setup_vectorstore(self):
        """Configura il vector store Qdrant."""
        retriever = QdrantVectorstore(
            host="localhost",
            port=6333
        )
        return retriever
    
    def _setup_pipeline(self):
        """Configura la DagPipeline per il retrieval e la generazione."""
        self.retriever = self._setup_vectorstore()
        
        # System prompt da aggiungere alla configurazione del client
        self.system_prompt = """Sei un assistente esperto di Datapizza-AI, un framework Python per applicazioni GenAI.

Il tuo compito è rispondere alle domande degli utenti basandoti ESCLUSIVAMENTE sulle FAQ fornite.

REGOLE IMPORTANTI:
1. Se trovi informazioni rilevanti nelle FAQ, rispondi in modo chiaro e completo
2. Se NON trovi informazioni rilevanti, rispondi ESATTAMENTE: "Non sono ancora state fatte domande a riguardo."
3. Non inventare informazioni che non sono nelle FAQ
4. Puoi citare le FAQ specifiche se utile
5. Mantieni un tono professionale e amichevole
6. Rispondi in italiano"""
        
        # Template per il prompt (senza system_prompt nel costruttore)
        self.prompt_template = ChatPromptTemplate(
            user_prompt_template="Domanda dell'utente: {{user_prompt}}",
            retrieval_prompt_template="""
Informazioni dalle FAQ:
{% for chunk in chunks %}
---
{{ chunk.text }}
---
{% endfor %}
"""
        )
        
        # Crea la DagPipeline
        self.dag_pipeline = DagPipeline()
        
        # Aggiungi moduli
        self.dag_pipeline.add_module("rewriter", self.query_rewriter)
        self.dag_pipeline.add_module("embedder", self.embedder)
        self.dag_pipeline.add_module("retriever", self.retriever)
        self.dag_pipeline.add_module("prompt", self.prompt_template)
        self.dag_pipeline.add_module("generator", self.openai_client)
        
        # Connetti i moduli
        self.dag_pipeline.connect("rewriter", "embedder", target_key="text")
        self.dag_pipeline.connect("embedder", "retriever", target_key="query_vector")
        self.dag_pipeline.connect("retriever", "prompt", target_key="chunks")
        self.dag_pipeline.connect("prompt", "generator", target_key="memory")
    
    def ask(self, question: str, k: int = 5, score_threshold: float = 0.5) -> str:
        """
        Invia una domanda al chatbot e ottiene una risposta.
        
        Args:
            question: La domanda dell'utente
            k: Numero di chunks da recuperare (default: 5)
            score_threshold: Soglia minima di similarity score (default: 0.5)
        
        Returns:
            La risposta del chatbot
        """
        try:
            # Esegui la pipeline
            result = self.dag_pipeline.run({
                "rewriter": {"user_prompt": question},
                "prompt": {"user_prompt": question},
                "retriever": {
                    "collection_name": "datapizza_faq",
                    "k": k
                },
                "generator": {
                    "input": question,
                    "system_prompt": self.system_prompt
                }
            })
            
            # Estrai la risposta dal generator
            generator_result = result.get("generator")
            
            # Il generator restituisce un ClientResponse object che contiene blocks
            response_text = ""
            if hasattr(generator_result, 'content'):
                # ClientResponse ha un attributo content che è una lista di blocks
                content = generator_result.content
                if isinstance(content, list):
                    # Estrai il testo da ogni TextBlock
                    for block in content:
                        if hasattr(block, 'content'):
                            response_text += block.content
                        elif isinstance(block, str):
                            response_text += block
                else:
                    response_text = str(content)
            elif isinstance(generator_result, str):
                response_text = generator_result
            else:
                response_text = str(generator_result)
            
            return response_text.strip()
            
        except Exception as e:
            print(f"⚠ Errore durante l'elaborazione: {e}")
            return "Si è verificato un errore nell'elaborazione della domanda."
    
    def interactive_mode(self):
        """Modalità interattiva per chattare con il bot."""
        print("=" * 70)
        print("🤖 Chatbot FAQ Datapizza-AI")
        print("=" * 70)
        print("Fai le tue domande su Datapizza-AI!")
        print("Digita 'exit', 'quit' o 'esci' per terminare.")
        print("=" * 70)
        print()
        
        while True:
            try:
                # Ottieni la domanda dall'utente
                question = input("\n👤 Tu: ").strip()
                
                # Check per uscire
                if question.lower() in ['exit', 'quit', 'esci', 'q']:
                    print("\n👋 Arrivederci!")
                    break
                
                if not question:
                    continue
                
                # Ottieni e mostra la risposta
                print("\n🤖 Bot: ", end="", flush=True)
                response = self.ask(question)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Arrivederci!")
                break
            except Exception as e:
                print(f"\n⚠ Errore: {e}")

def main():
    """Funzione principale per avviare il chatbot."""
    try:
        chatbot = FAQChatbot()
        chatbot.interactive_mode()
    except Exception as e:
        print(f"✗ Errore nell'inizializzazione del chatbot: {e}")
        print("\nAssicurati di:")
        print("1. Aver eseguito l'ingestion (python ingest_faq.py)")
        print("2. Aver configurato il file .env con OPENAI_API_KEY")
        print("3. Aver avviato Qdrant (docker run -p 6333:6333 qdrant/qdrant)")

if __name__ == "__main__":
    main()

