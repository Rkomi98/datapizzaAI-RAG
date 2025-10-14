"""
Script per l'ingestion delle FAQ nel vector store.
Processa i file markdown delle FAQ e li inserisce in Qdrant.
"""

import os
from dotenv import load_dotenv
from datapizza.core.vectorstore import VectorConfig
from datapizza.embedders import ChunkEmbedder
from datapizza.embedders.openai import OpenAIEmbedder
from datapizza.modules.parsers import TextParser
from datapizza.modules.splitters import NodeSplitter
from datapizza.pipeline import IngestionPipeline
from datapizza.vectorstores.qdrant import QdrantVectorstore

# Carica variabili d'ambiente
load_dotenv()

def setup_vectorstore():
    """Configura e crea la collection nel vector store."""
    vectorstore = QdrantVectorstore(
        host="localhost",
        port=6333
    )
    
    # Crea la collection se non esiste
    try:
        vectorstore.create_collection(
            "datapizza_faq",
            vector_config=[VectorConfig(name="embedding", dimensions=1536)]
        )
        print("✓ Collection 'datapizza_faq' creata con successo")
    except Exception as e:
        print(f"⚠ Collection già esistente o errore: {e}")
    
    return vectorstore

def create_ingestion_pipeline(vectorstore):
    """Crea la pipeline di ingestion."""
    
    # Inizializza l'embedder
    embedder_client = OpenAIEmbedder(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name="text-embedding-3-small",
    )
    
    # Crea la pipeline
    ingestion_pipeline = IngestionPipeline(
        modules=[
            TextParser(),  # Parser per file markdown
            NodeSplitter(max_char=1000),  # Split in chunks di max 1000 caratteri
            ChunkEmbedder(client=embedder_client),  # Genera embeddings
        ],
        vector_store=vectorstore,
        collection_name="datapizza_faq"
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
            pipeline.run(
                faq_file, 
                metadata={
                    "source": faq_file,
                    "type": "faq",
                    "language": "it"
                }
            )
            print(f"✓ {faq_file} processato con successo")
        except Exception as e:
            print(f"✗ Errore nel processare {faq_file}: {e}")

def main():
    """Funzione principale per l'ingestion."""
    print("=" * 60)
    print("🚀 Inizio ingestion delle FAQ Datapizza-AI")
    print("=" * 60)
    
    # Verifica API key
    if not os.getenv("OPENAI_API_KEY"):
        print("✗ ERRORE: OPENAI_API_KEY non trovata nel file .env")
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

