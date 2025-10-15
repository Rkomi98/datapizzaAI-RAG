"""
Chatbot RAG per rispondere alle domande sulle FAQ di Datapizza-AI.
Utilizza DagPipeline per retrieval e generazione risposte.
Integra Google Client (Gemini 2.5 Flash) con Memory per conversazioni contestuali.
"""

import os
from typing import Any, Dict, List

from dotenv import load_dotenv

from datapizza.clients.google import GoogleClient
from datapizza.embedders.google import GoogleEmbedder
from datapizza.modules.prompt import ChatPromptTemplate
from datapizza.modules.rewriters import ToolRewriter
from datapizza.pipeline import DagPipeline
from datapizza.memory import Memory
from datapizza.type import ROLE, TextBlock

from qdrant_config import (
    COLLECTION_NAME,
    build_qdrant_vectorstore,
    describe_qdrant_target,
)

# Carica variabili d'ambiente
load_dotenv()

EMBEDDING_MODEL = os.getenv("FAQ_EMBEDDING_MODEL", "gemini-embedding-001")

class FAQChatbot:
    """Chatbot RAG per le FAQ di Datapizza-AI con Google Gemini e Memory."""
    
    def __init__(self, memory: Memory = None, debug_mode: bool = False):
        """Inizializza il chatbot con tutti i componenti necessari.
        
        Args:
            memory: Istanza di Memory per gestire la cronologia della conversazione
            debug_mode: Abilita il logging di debug dei passi di retrieval
        """
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY non trovata nel file .env")
        
        # Inizializza o usa la memory fornita
        self.memory = memory if memory is not None else Memory()
        self.debug_mode = debug_mode
        self.last_debug_info: Dict[str, Any] | None = None
        
        # Inizializza componenti
        self._setup_clients()
        self._setup_pipeline()
    
    def _setup_clients(self):
        """Configura i client Google (Gemini 2.5 Flash)."""
        self.google_client = GoogleClient(
            model="gemini-2.5-flash",  # Gemini 2.5 Flash
            api_key=self.google_api_key,
            system_prompt="Sei un assistente esperto che risponde alle domande sulle FAQ di Datapizza-AI.",
            temperature=0.7
        )
        
        self.embedder = GoogleEmbedder(
            api_key=self.google_api_key,
            model_name=EMBEDDING_MODEL
        )
        
        self.query_rewriter = ToolRewriter(
            client=self.google_client,
            system_prompt="""Riscrivi la domanda dell'utente per migliorare il retrieval dalle FAQ di Datapizza-AI.
            - Mantieni il contesto specifico: "questo framework" si riferisce a "Datapizza-AI"
            - Espandi abbreviazioni ma resta specifico
            - Aggiungi termini chiave rilevanti per Datapizza-AI
            - Restituisci solo la query riscritta, senza spiegazioni aggiuntive."""
        )
    
    def _setup_vectorstore(self):
        """Configura il vector store Qdrant."""
        vectorstore = build_qdrant_vectorstore()

        try:
            client = vectorstore.get_client()
            if not client.collection_exists(COLLECTION_NAME):
                raise RuntimeError(
                    f"La collection '{COLLECTION_NAME}' non esiste su {describe_qdrant_target()}. "
                    "Esegui prima lo script di ingestion o verifica la configurazione Qdrant."
                )
        except Exception as exc:
            raise RuntimeError(
                f"Impossibile connettersi a Qdrant ({describe_qdrant_target()}): {exc}"
            ) from exc

        return vectorstore
    
    def _setup_pipeline(self):
        """Configura la DagPipeline per il retrieval e la generazione."""
        self.retriever = self._setup_vectorstore()
        
        # System prompt da aggiungere alla configurazione del client
        self.system_prompt = """Sei un assistente esperto di Datapizza-AI, un framework Python per applicazioni GenAI.

Il tuo compito è rispondere alle domande degli utenti basandoti sulle FAQ fornite.

REGOLE IMPORTANTI:
1. Se trovi anche solo parzialmente informazioni rilevanti nelle FAQ, usale per rispondere
2. SOLO se le FAQ non contengono NESSUNA informazione utile, rispondi: "Non sono ancora state fatte domande a riguardo."
3. Non inventare informazioni che non sono nelle FAQ
4. Sintetizza e organizza le informazioni delle FAQ in modo chiaro
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
        
        # Aggiungi moduli (con query rewriter riattivato)
        self.dag_pipeline.add_module("rewriter", self.query_rewriter)
        self.dag_pipeline.add_module("embedder", self.embedder)
        self.dag_pipeline.add_module("retriever", self.retriever)
        self.dag_pipeline.add_module("prompt", self.prompt_template)
        self.dag_pipeline.add_module("generator", self.google_client)
        
        # Connetti i moduli (con rewriter)
        self.dag_pipeline.connect("rewriter", "embedder", target_key="text")
        self.dag_pipeline.connect("embedder", "retriever", target_key="query_vector")
        self.dag_pipeline.connect("retriever", "prompt", target_key="chunks")
        self.dag_pipeline.connect("prompt", "generator", target_key="memory")

    def set_debug_mode(self, enabled: bool):
        """Abilita o disabilita il debug runtime (override della variabile d'ambiente)."""
        self.debug_mode = enabled
    
    def ask(self, question: str, k: int = 10, score_threshold: float = 0.5) -> str:
        """
        Invia una domanda al chatbot e ottiene una risposta.
        La conversazione viene salvata nella Memory per mantenere il contesto.
        
        Args:
            question: La domanda dell'utente
            k: Numero di chunks da recuperare (default: 5)
            score_threshold: Soglia minima di similarity score (default: 0.5)
        
        Returns:
            La risposta del chatbot
        """
        env_debug = os.getenv("FAQ_DEBUG", "").lower() in {"1", "true", "yes", "on"}
        debug_mode = self.debug_mode or env_debug
        self.last_debug_info = None

        fallback_message = "Non sono ancora state fatte domande a riguardo."
        fallback_triggered = False
        fallback_overridden = False

        chunk_previews: List[Dict[str, Any]] = []

        try:
            # Esegui la pipeline con memory e query rewriter
            result = self.dag_pipeline.run({
                "rewriter": {"user_prompt": question},  # Ri-scrivi la query
                "prompt": {"user_prompt": question},
                "retriever": {
                    "collection_name": COLLECTION_NAME,
                    "k": k
                },
                "generator": {
                    "input": question,
                    "system_prompt": self.system_prompt,
                    "memory": self.memory  # Passa la memory al generator
                }
            })
            
            rewritten_query = result.get("rewriter")
            retrieved_chunks = result.get("retriever") or []

            chunk_previews = []
            language_counts: Dict[str, int] = {}

            for chunk in retrieved_chunks:
                metadata = getattr(chunk, "metadata", {}) or {}
                lang = metadata.get("language") or metadata.get("Language") or "unknown"
                language_counts[lang] = language_counts.get(lang, 0) + 1

                chunk_previews.append(
                    {
                        "id": getattr(chunk, "id", None),
                        "score": getattr(chunk, "score", None),
                        "metadata": metadata,
                        "text": chunk.text,
                    }
                )

            if debug_mode:
                print("🔍 FAQ_DEBUG attivo")
                print(f"   • Query originale : {question}")
                print(f"   • Query riscritta : {rewritten_query}")
                print(f"   • Chunk recuperati: {len(retrieved_chunks)}")
                if language_counts:
                    print("   • Lingue chunk     :", language_counts)
                for idx, chunk in enumerate(retrieved_chunks[:3], 1):
                    meta = getattr(chunk, "metadata", {}) or {}
                    src = meta.get("source")
                    lang = meta.get("language")
                    preview = chunk.text.replace("\n", " ")[:240]
                    print(f"     #{idx}: {preview}{'…' if len(chunk.text) > 240 else ''}")

            # Estrai la risposta dal generator
            generator_result = result.get("generator")
            
            # Il generator restituisce un ClientResponse object che contiene blocks
            response_text = ""
            response_content = None
            
            if hasattr(generator_result, 'content'):
                # ClientResponse ha un attributo content che è una lista di blocks
                content = generator_result.content
                response_content = content
                
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
                response_content = [TextBlock(content=generator_result)]
            else:
                response_text = str(generator_result)
                response_content = [TextBlock(content=response_text)]

            if response_text.strip() == fallback_message:
                fallback_triggered = True
            
            final_response = response_text.strip()

            # Salva il turno di conversazione nella memory
            self.memory.add_turn(TextBlock(content=question), role=ROLE.USER)
            if response_content:
                if isinstance(response_content, list):
                    for block in response_content:
                        self.memory.add_turn(block, role=ROLE.ASSISTANT)
                else:
                    self.memory.add_turn(response_content, role=ROLE.ASSISTANT)
            else:
                self.memory.add_turn(TextBlock(content=response_text), role=ROLE.ASSISTANT)

            self.last_debug_info = {
                "question": question,
                "rewritten_query": rewritten_query,
                "debug_enabled": debug_mode,
                "chunks": chunk_previews,
                "fallback_triggered": fallback_triggered,
                "fallback_overridden": fallback_overridden,
                "response": final_response,
            }
            
            return final_response
            
        except Exception as e:
            print(f"⚠ Errore durante l'elaborazione: {e}")
            import traceback
            traceback.print_exc()
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
        print("2. Aver configurato il file .env con GOOGLE_API_KEY")
        print("3. Aver avviato Qdrant (docker run -p 6333:6333 qdrant/qdrant)")

if __name__ == "__main__":
    main()
