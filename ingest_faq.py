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

from qdrant_config import (
    COLLECTION_NAME,
    EMBEDDING_DIM,
    build_qdrant_vectorstore,
    describe_qdrant_target,
)

# Carica variabili d'ambiente
load_dotenv()


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


def setup_vectorstore():
    """Configura e crea la collection nel vector store.
    
    Nota: Google text-embedding-004 usa 768 dimensioni.
    """
    vectorstore = build_qdrant_vectorstore()

    client = vectorstore.get_client()

    print(f"🔗 Target Qdrant: {describe_qdrant_target()}")

    try:
        if client.collection_exists(COLLECTION_NAME):
            info = client.get_collection(COLLECTION_NAME)
            configured_dims = _extract_vector_dimensions(info)
            current_dim = configured_dims.get("embedding") or configured_dims.get("default")

            if current_dim == EMBEDDING_DIM:
                print(f"✓ Collection '{COLLECTION_NAME}' già esistente con {EMBEDDING_DIM} dimensioni")
            else:
                print(
                    f"⚠ Collection '{COLLECTION_NAME}' trovata con {current_dim} dimensioni: ricreo con {EMBEDDING_DIM}"
                )
                vectorstore.delete_collection(COLLECTION_NAME)
                vectorstore.create_collection(
                    COLLECTION_NAME,
                    vector_config=[VectorConfig(name="embedding", dimensions=EMBEDDING_DIM)]
                )
                print(f"✓ Collection '{COLLECTION_NAME}' ricreata con successo ({EMBEDDING_DIM} dimensioni)")
        else:
            vectorstore.create_collection(
                COLLECTION_NAME,
                vector_config=[VectorConfig(name="embedding", dimensions=EMBEDDING_DIM)]
            )
            print(f"✓ Collection '{COLLECTION_NAME}' creata con successo ({EMBEDDING_DIM} dimensioni)")
    except Exception as e:
        print(f"✗ Errore nella configurazione della collection: {e}")
        raise
    
    return vectorstore

def create_ingestion_pipeline(vectorstore):
    """Crea la pipeline di ingestion con Google Embedder."""
    
    # Inizializza il Google Embedder
    embedder_client = GoogleEmbedder(
        api_key=os.getenv("GOOGLE_API_KEY"),
        model_name="text-embedding-004",
    )
    
    # Crea la pipeline
    ingestion_pipeline = IngestionPipeline(
        modules=[
            TextParser(),  # Parser per file markdown
            NodeSplitter(max_char=1000),  # Split in chunks di max 1000 caratteri
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
            
            # Il TextParser si aspetta una stringa, non un filepath
            pipeline.run(
                content, 
                metadata={
                    "source": faq_file,
                    "type": "faq",
                    "language": "it"
                }
            )
            print(f"✓ {faq_file} processato con successo")
        except Exception as e:
            print(f"✗ Errore nel processare {faq_file}: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Funzione principale per l'ingestion."""
    print("=" * 60)
    print("🚀 Inizio ingestion delle FAQ Datapizza-AI")
    print("   (Google Embedder - text-embedding-004)")
    print("=" * 60)
    
    # Verifica API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("✗ ERRORE: GOOGLE_API_KEY non trovata nel file .env")
        return
    
    # Setup vector store
    print("\n📦 Setup vector store...")
    vectorstore = setup_vectorstore()
    
    # Crea pipeline
    print("\n🔧 Creazione pipeline di ingestion...")
    pipeline = create_ingestion_pipeline(vectorstore)
    
    # File FAQ da processare
    faq_files = [
        "datapizza_faq.md",
        "FAQ_Video.md"
    ]
    
    # Ingest documenti
    print("\n📚 Ingestion documenti...")
    ingest_documents(pipeline, faq_files)
    
    # Verifica risultati
    print("\n✅ Ingestion completata!")
    print("=" * 60)

if __name__ == "__main__":
    main()
