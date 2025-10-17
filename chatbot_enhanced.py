"""
Chatbot RAG Enhanced - Integra FAQ locali e documentazione ufficiale via MCP.
Gestisce automaticamente l'assenza del modulo MCP in ambienti deployati.
"""

import os
import sys
import asyncio
from typing import Any, Dict, List
from pathlib import Path

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

# Aggiungi il percorso del MCP server al path (se presente) e gestisci import opzionale
MCP_AVAILABLE = False
MCP_IMPORT_ERROR: Exception | None = None
query_documentation = None

_mcp_server_path = Path(__file__).parent / "mcp-server-datapizza" / "datapizza-mcp-server" / "src"
if _mcp_server_path.exists():
    sys.path.insert(0, str(_mcp_server_path))

try:
    from datapizza_mcp.retriever import query_documentation as _query_documentation

    query_documentation = _query_documentation
    MCP_AVAILABLE = True
except ModuleNotFoundError as exc:
    MCP_IMPORT_ERROR = exc
except Exception as exc:  # pragma: no cover - best-effort informative fallback
    MCP_IMPORT_ERROR = exc

# Carica variabili d'ambiente
load_dotenv()

EMBEDDING_MODEL = os.getenv("FAQ_EMBEDDING_MODEL", "gemini-embedding-001")


class EnhancedFAQChatbot:
    """Chatbot RAG che interroga sia FAQ locali che documentazione ufficiale."""
    
    def __init__(self, memory: Memory = None, debug_mode: bool = False, use_official_docs: bool = True):
        """Inizializza il chatbot.
        
        Args:
            memory: Istanza di Memory per gestire la cronologia
            debug_mode: Abilita il logging di debug
            use_official_docs: Se True, integra anche la documentazione ufficiale via MCP
        """
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY non trovata nel file .env")
        
        self.memory = memory if memory is not None else Memory()
        self.debug_mode = debug_mode
        self.supports_official_docs = MCP_AVAILABLE and query_documentation is not None

        if use_official_docs and not self.supports_official_docs:
            details = (
                f" Dettagli import: {MCP_IMPORT_ERROR}"
                if MCP_IMPORT_ERROR
                else ""
            )
            raise ImportError(
                "Impossibile caricare la documentazione ufficiale (modulo 'datapizza_mcp' non disponibile). "
                "Installa il server MCP, ad esempio aggiungendo "
                "'git+https://github.com/mat1312/mcp-server-datapizza@main#subdirectory=datapizza-mcp-server' "
                "a requirements.txt."
                f"{details}"
            )

        self.use_official_docs = use_official_docs and self.supports_official_docs
        self.last_debug_info: Dict[str, Any] | None = None
        
        # Inizializza componenti
        self._setup_clients()
        self._setup_pipeline()
    
    def _setup_clients(self):
        """Configura i client Google (Gemini 2.5 Flash)."""
        self.google_client = GoogleClient(
            model="gemini-2.5-flash",
            api_key=self.google_api_key,
            system_prompt="Sei un assistente esperto che risponde alle domande su Datapizza-AI.",
            temperature=0.7
        )
        
        self.embedder = GoogleEmbedder(
            api_key=self.google_api_key,
            model_name=EMBEDDING_MODEL
        )
        
        self.query_rewriter = ToolRewriter(
            client=self.google_client,
            system_prompt="""Riscrivi la domanda dell'utente per migliorare il retrieval.
            - Mantieni il contesto specifico: "questo framework" si riferisce a "Datapizza-AI"
            - Espandi abbreviazioni ma resta specifico
            - Aggiungi termini chiave rilevanti per Datapizza-AI
            - Restituisci solo la query riscritta, senza spiegazioni aggiuntive."""
        )
    
    def _setup_vectorstore(self):
        """Configura il vector store Qdrant per le FAQ."""
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
        """Configura la DagPipeline per il retrieval dalle FAQ."""
        self.retriever = self._setup_vectorstore()
        
        self.system_prompt = """Sei un assistente esperto di Datapizza-AI, un framework Python per applicazioni GenAI.

Il tuo compito è rispondere alle domande degli utenti basandoti sulle informazioni fornite.

FONTI DISPONIBILI:
1. FAQ Locali: Domande e risposte comuni degli utenti
2. Documentazione Ufficiale: Docs dal repository GitHub di datapizza-ai

REGOLE IMPORTANTI:
1. Usa le informazioni dalle FAQ e dalla documentazione ufficiale per rispondere
2. Se trovi informazioni rilevanti, usale per costruire una risposta completa
3. SOLO se non trovi NESSUNA informazione utile, rispondi: "Non ho trovato informazioni su questo argomento."
4. Non inventare informazioni che non sono nelle fonti
5. Sintetizza e organizza le informazioni in modo chiaro
6. Mantieni un tono professionale e amichevole
7. Se hai sia FAQ che docs ufficiali, combina le informazioni nel modo più utile
8. Rispondi in italiano"""
        
        # Template per il prompt
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
        
        # Crea la DagPipeline per FAQ
        self.dag_pipeline = DagPipeline()
        
        self.dag_pipeline.add_module("rewriter", self.query_rewriter)
        self.dag_pipeline.add_module("embedder", self.embedder)
        self.dag_pipeline.add_module("retriever", self.retriever)
        self.dag_pipeline.add_module("prompt", self.prompt_template)
        self.dag_pipeline.add_module("generator", self.google_client)
        
        self.dag_pipeline.connect("rewriter", "embedder", target_key="text")
        self.dag_pipeline.connect("embedder", "retriever", target_key="query_vector")
        self.dag_pipeline.connect("retriever", "prompt", target_key="chunks")
        self.dag_pipeline.connect("prompt", "generator", target_key="memory")

    def set_debug_mode(self, enabled: bool):
        """Abilita o disabilita il debug runtime."""
        self.debug_mode = enabled
    
    async def ask_async(self, question: str, k: int = 10, score_threshold: float = 0.5) -> str:
        """
        Versione asincrona di ask() che interroga sia FAQ che docs ufficiali.
        
        Args:
            question: La domanda dell'utente
            k: Numero di chunks da recuperare dalle FAQ (default: 10)
            score_threshold: Soglia minima di similarity score (default: 0.5)
        
        Returns:
            La risposta del chatbot
        """
        env_debug = os.getenv("FAQ_DEBUG", "").lower() in {"1", "true", "yes", "on"}
        debug_mode = self.debug_mode or env_debug
        self.last_debug_info = None

        try:
            # 1. Interroga le FAQ locali (sincrono)
            if debug_mode:
                print("🔍 Step 1: Interrogo le FAQ locali...")
            
            faq_result = self.dag_pipeline.run({
                "rewriter": {"user_prompt": question},
                "prompt": {"user_prompt": question},
                "retriever": {
                    "collection_name": COLLECTION_NAME,
                    "k": k
                },
                "generator": {
                    "input": question,
                    "system_prompt": self.system_prompt,
                    "memory": self.memory
                }
            })
            
            rewritten_query = faq_result.get("rewriter")
            faq_chunks = faq_result.get("retriever") or []
            faq_chunk_previews: List[Dict[str, Any]] = []
            
            if debug_mode:
                print(f"   • Query riscritta: {rewritten_query}")
                print(f"   • Chunk FAQ recuperati: {len(faq_chunks)}")

            for chunk in faq_chunks:
                metadata = getattr(chunk, "metadata", {}) or {}
                faq_chunk_previews.append(
                    {
                        "id": getattr(chunk, "id", None),
                        "score": getattr(chunk, "score", None),
                        "metadata": metadata,
                        "text": chunk.text,
                    }
                )
            
            # 2. Interroga la documentazione ufficiale (asincrono)
            official_docs_text = ""
            if self.use_official_docs and query_documentation:
                if debug_mode:
                    print("🔍 Step 2: Interrogo la documentazione ufficiale...")
                
                try:
                    official_docs_text = await query_documentation(question, max_results=3)
                    if debug_mode:
                        print(f"   • Documentazione ufficiale recuperata: {len(official_docs_text)} caratteri")
                except Exception as e:
                    if debug_mode:
                        print(f"   ⚠ Errore nel recuperare docs ufficiali: {e}")
                    official_docs_text = ""
            
            # 3. Combina le informazioni e genera la risposta finale
            if debug_mode:
                print("🔍 Step 3: Genero la risposta finale...")
            
            # Costruisci il contesto combinato
            combined_context = ""
            
            # Aggiungi FAQ
            if faq_chunks:
                combined_context += "=== INFORMAZIONI DALLE FAQ ===\n\n"
                for i, chunk in enumerate(faq_chunks[:5], 1):
                    combined_context += f"FAQ #{i}:\n{chunk.text}\n\n"
            
            # Aggiungi docs ufficiali
            if official_docs_text and len(official_docs_text) > 100:
                combined_context += "\n=== DOCUMENTAZIONE UFFICIALE ===\n\n"
                combined_context += official_docs_text + "\n\n"
            
            # Genera risposta finale usando il client direttamente
            final_prompt = f"""{self.system_prompt}

{combined_context}

Domanda dell'utente: {question}

Rispondi alla domanda basandoti sulle informazioni sopra riportate."""
            
            # Usa il client Google per generare la risposta
            final_response = self.google_client.invoke(
                input=final_prompt,
                memory=self.memory
            )
            
            # Estrai il testo dalla risposta
            response_text = ""
            if hasattr(final_response, 'content'):
                content = final_response.content
                if isinstance(content, list):
                    for block in content:
                        if hasattr(block, 'content'):
                            response_text += block.content
                        elif isinstance(block, str):
                            response_text += block
                else:
                    response_text = str(content)
            else:
                response_text = str(final_response)
            
            final_response_text = response_text.strip()
            
            # Salva nella memory
            self.memory.add_turn(TextBlock(content=question), role=ROLE.USER)
            self.memory.add_turn(TextBlock(content=final_response_text), role=ROLE.ASSISTANT)
            
            if debug_mode:
                print(f"✅ Risposta generata: {len(final_response_text)} caratteri")

            official_excerpt = ""
            if official_docs_text:
                official_excerpt = official_docs_text.strip()
                if len(official_excerpt) > 800:
                    official_excerpt = official_excerpt[:800] + "…"

            self.last_debug_info = {
                "question": question,
                "rewritten_query": rewritten_query,
                "chunks": faq_chunk_previews,
                "fallback_triggered": False,
                "fallback_overridden": False,
                "response": final_response_text,
                "official_docs_used": bool(official_docs_text),
                "official_docs_excerpt": official_excerpt,
                "official_docs_supported": self.supports_official_docs,
            }
            
            return final_response_text
            
        except Exception as e:
            print(f"⚠ Errore durante l'elaborazione: {e}")
            import traceback
            traceback.print_exc()
            return "Si è verificato un errore nell'elaborazione della domanda."
    
    def ask(self, question: str, k: int = 10, score_threshold: float = 0.5) -> str:
        """
        Versione sincrona di ask() (wrapper per ask_async).
        """
        return asyncio.run(self.ask_async(question, k, score_threshold))
    
    def interactive_mode(self):
        """Modalità interattiva per chattare con il bot."""
        print("=" * 70)
        print("🤖 Chatbot Enhanced - FAQ + Documentazione Ufficiale")
        print("=" * 70)
        print("Fai le tue domande su Datapizza-AI!")
        print("Digita 'exit', 'quit' o 'esci' per terminare.")
        print("=" * 70)
        print()
        
        while True:
            try:
                question = input("\n👤 Tu: ").strip()
                
                if question.lower() in ['exit', 'quit', 'esci', 'q']:
                    print("\n👋 Arrivederci!")
                    break
                
                if not question:
                    continue
                
                print("\n🤖 Bot: ", end="", flush=True)
                response = self.ask(question)
                print(response)
                
            except KeyboardInterrupt:
                print("\n\n👋 Arrivederci!")
                break
            except Exception as e:
                print(f"\n⚠ Errore: {e}")


def main():
    """Funzione principale per avviare il chatbot enhanced."""
    try:
        chatbot = EnhancedFAQChatbot(use_official_docs=True, debug_mode=False)
        chatbot.interactive_mode()
    except Exception as e:
        print(f"✗ Errore nell'inizializzazione del chatbot: {e}")
        print("\nAssicurati di:")
        print("1. Aver eseguito l'ingestion delle FAQ (python ingest_faq.py)")
        print("2. Aver indicizzato la docs ufficiale (python -m datapizza_mcp.indexer)")
        print("3. Aver configurato il file .env con GOOGLE_API_KEY e OPENAI_API_KEY")
        print("4. Aver avviato Qdrant o configurato Qdrant Cloud")


if __name__ == "__main__":
    main()
