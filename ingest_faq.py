"""
Script per l'ingestion delle FAQ nel vector store.
Processa i file markdown delle FAQ e li inserisce in Qdrant.
Utilizza Google Embedder per generare gli embeddings.
"""

import os

from dotenv import load_dotenv
from qdrant_client import models as qdrant_models

from datapizza.core.vectorstore import VectorConfig
from datapizza.embedders import ChunkEmbedder
from datapizza.embedders.google import GoogleEmbedder
from datapizza.modules.parsers import TextParser
from datapizza.modules.splitters import NodeSplitter
from datapizza.pipeline import IngestionPipeline

from qdrant_config import COLLECTION_NAME, build_qdrant_vectorstore, describe_qdrant_target

# Carica variabili d'ambiente
load_dotenv()

EMBEDDING_MODEL = os.getenv("FAQ_EMBEDDING_MODEL", "gemini-embedding-001")
EMBEDDING_DIM_OVERRIDE = os.getenv("FAQ_EMBEDDING_DIM")
SCRIPTS_DIR = "Scripts"


def _detect_embedding_dimension(embedder_client: GoogleEmbedder) -> int:
    """Calcola dinamicamente la dimensione degli embedding generati dal client Google."""
    probe_text = "Datapizza-AI FAQ dimension probe."
    vector = embedder_client.embed(probe_text)

    if isinstance(vector, list) and vector:
        if isinstance(vector[0], float):
            return len(vector)
        if isinstance(vector[0], list) and vector[0]:
            return len(vector[0])

    raise ValueError(
        "Impossibile determinare la dimensione degli embedding restituiti da Google Embedder."
    )


def _gather_faq_files() -> list[str]:
    """Restituisce la lista dei file FAQ da processare, includendo eventuali script."""
    faq_files = [
        "datapizza_faq.md",
        "FAQ_Video.md",
    ]

    if os.path.isdir(SCRIPTS_DIR):
        for filename in sorted(os.listdir(SCRIPTS_DIR)):
            path = os.path.join(SCRIPTS_DIR, filename)
            if os.path.isfile(path) and filename.lower().endswith(".md"):
                faq_files.append(path)

    return faq_files


def _detect_language_from_path(path: str) -> str:
    """Deduce la lingua dal percorso del file (Scripts considerato inglese)."""
    normalized = os.path.normpath(path)
    first_segment = normalized.split(os.sep)[0].lower()
    if first_segment == SCRIPTS_DIR.lower():
        return "en"
    return "it"

def _extract_vector_dimensions(collection_info: qdrant_models.CollectionInfo) -> dict[str, int]:
    """Return the dense vector dimensions configured on the collection."""
    dims: dict[str, int] = {}
    vectors_cfg = collection_info.config.params.vectors

    if isinstance(vectors_cfg, qdrant_models.VectorParams):
        dims["default"] = vectors_cfg.size
    elif isinstance(vectors_cfg, dict):
        for name, params in vectors_cfg.items():
            if isinstance(params, qdrant_models.VectorParams):
                dims[name] = params.size
    return dims


def setup_vectorstore(embedding_dim: int):
    """Configura e crea la collection nel vector store con la dimensione richiesta dagli embedding."""
    vectorstore = build_qdrant_vectorstore()

    client = vectorstore.get_client()

    print(f"🔗 Target Qdrant: {describe_qdrant_target()}")

    try:
        if client.collection_exists(COLLECTION_NAME):
            info = client.get_collection(COLLECTION_NAME)
            configured_dims = _extract_vector_dimensions(info)
            current_dim = configured_dims.get("embedding") or configured_dims.get("default")

            if current_dim == embedding_dim:
                print(f"✓ Collection '{COLLECTION_NAME}' già esistente con {embedding_dim} dimensioni")
            else:
                print(
                    f"⚠ Collection '{COLLECTION_NAME}' trovata con {current_dim} dimensioni: ricreo con {embedding_dim}"
                )
                vectorstore.delete_collection(COLLECTION_NAME)
                vectorstore.create_collection(
                    COLLECTION_NAME,
                    vector_config=[VectorConfig(name="embedding", dimensions=embedding_dim)]
                )
                print(f"✓ Collection '{COLLECTION_NAME}' ricreata con successo ({embedding_dim} dimensioni)")
        else:
            vectorstore.create_collection(
                COLLECTION_NAME,
                vector_config=[VectorConfig(name="embedding", dimensions=embedding_dim)]
            )
            print(f"✓ Collection '{COLLECTION_NAME}' creata con successo ({embedding_dim} dimensioni)")
    except Exception as e:
        print(f"✗ Errore nella configurazione della collection: {e}")
        raise
    
    return vectorstore

def create_ingestion_pipeline(vectorstore, embedder_client: GoogleEmbedder):
    """Crea la pipeline di ingestion con Google Embedder."""
    
    # Crea la pipeline
    ingestion_pipeline = IngestionPipeline(
        modules=[
            TextParser(),  # Parser per file markdown
            NodeSplitter(max_char=2000),  # Split in chunks più grandi per non spezzare Q&A
            ChunkEmbedder(client=embedder_client),  # Genera embeddings
        ],
        vector_store=vectorstore,
        collection_name=COLLECTION_NAME
    )
    
    return ingestion_pipeline

def ingest_documents(pipeline, faq_files):
    """Processa e ingerisce i documenti FAQ."""
    for faq_file in faq_files:
        if not os.path.exists(faq_file):
            print(f"⚠ File non trovato: {faq_file}")
            continue
        
        try:
            print(f"📄 Processando {faq_file}...")
            
            # Leggi il contenuto del file
            with open(faq_file, 'r', encoding='utf-8') as f:
                content = f.read()

            language = _detect_language_from_path(faq_file)
            category = "scripts" if language == "en" else "faq"
            
            # Il TextParser si aspetta una stringa, non un filepath
            pipeline.run(
                content, 
                metadata={
                    "source": faq_file,
                    "type": category,
                    "language": language
                }
            )
            print(f"✓ {faq_file} processato con successo ({language.upper()})")
        except Exception as e:
            print(f"✗ Errore nel processare {faq_file}: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Funzione principale per l'ingestion."""
    print("=" * 60)
    print("🚀 Inizio ingestion delle FAQ Datapizza-AI")
    print(f"   (Google Embedder - {EMBEDDING_MODEL})")
    print("=" * 60)
    
    # Verifica API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("✗ ERRORE: GOOGLE_API_KEY non trovata nel file .env")
        return

    # Inizializza il Google Embedder
    embedder_client = GoogleEmbedder(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model_name=EMBEDDING_MODEL,
    )

    # Determina la dimensione degli embedding
    if EMBEDDING_DIM_OVERRIDE:
        embedding_dim = int(EMBEDDING_DIM_OVERRIDE)
        print(f"📏 Dimensione embedding forzata da variabile d'ambiente: {embedding_dim}")
    else:
        try:
            embedding_dim = _detect_embedding_dimension(embedder_client)
            print(f"📏 Dimensione embedding rilevata: {embedding_dim}")
        except Exception as e:
            print(f"✗ Impossibile determinare la dimensione degli embedding: {e}")
            return
    
    # Setup vector store
    print("\n📦 Setup vector store...")
    vectorstore = setup_vectorstore(embedding_dim)
    
    # Crea pipeline
    print("\n🔧 Creazione pipeline di ingestion...")
    pipeline = create_ingestion_pipeline(vectorstore, embedder_client)
    
    # File FAQ da processare
    faq_files = _gather_faq_files()
    print(f"\n🗂️ Documenti rilevati ({len(faq_files)}):")
    for path in faq_files:
        lang = _detect_language_from_path(path)
        print(f"   • {path} [{lang.upper()}]")
    
    # Ingest documenti
    print("\n📚 Ingestion documenti...")
    ingest_documents(pipeline, faq_files)
    
    # Verifica risultati
    print("\n✅ Ingestion completata!")
    print("=" * 60)

if __name__ == "__main__":
    main()
