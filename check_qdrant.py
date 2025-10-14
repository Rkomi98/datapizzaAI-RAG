"""
Script per verificare il contenuto di Qdrant dopo l'ingestion.
"""

from qdrant_client import QdrantClient

def check_collection():
    """Verifica il contenuto della collection datapizza_faq."""
    print("=" * 70)
    print("🔍 Verifica contenuto Qdrant")
    print("=" * 70)
    print()
    
    # Connessione a Qdrant
    client = QdrantClient(host="localhost", port=6333)
    
    collection_name = "datapizza_faq"
    
    # Verifica che la collection esista
    try:
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        print(f"📚 Collections trovate: {collection_names}")
        
        if collection_name not in collection_names:
            print(f"\n❌ Collection '{collection_name}' non trovata!")
            print("   Esegui prima: python ingest_faq.py")
            return
        
        print(f"✅ Collection '{collection_name}' trovata")
        print()
        
        # Ottieni informazioni sulla collection
        collection_info = client.get_collection(collection_name)
        print(f"📊 Informazioni collection:")
        print(f"  - Points count: {collection_info.points_count}")
        print(f"  - Vectors count: {collection_info.vectors_count}")
        print()
        
        if collection_info.points_count == 0:
            print("⚠️  La collection è vuota! Esegui: python ingest_faq.py")
            return
        
        # Recupera alcuni punti di esempio
        print(f"📄 Esempi di chunks salvati (primi 5):")
        print()
        
        points = client.scroll(
            collection_name=collection_name,
            limit=5,
            with_payload=True,
            with_vectors=False
        )[0]
        
        for i, point in enumerate(points, 1):
            print(f"--- Chunk {i} (ID: {point.id}) ---")
            payload = point.payload
            
            if 'text' in payload:
                text = payload['text']
                print(f"Testo: {text[:200]}{'...' if len(text) > 200 else ''}")
            
            if 'metadata' in payload:
                print(f"Metadata: {payload['metadata']}")
            
            print()
        
        # Test di ricerca
        print("=" * 70)
        print("🔍 Test ricerca semantica")
        print("=" * 70)
        print()
        
        test_query = "Cosa differenzia Datapizza da Langchain?"
        print(f"Query: {test_query}")
        print()
        
        # Per testare la ricerca, dovrei generare l'embedding della query
        # Ma per ora vediamo solo se ci sono dati
        print(f"✅ Collection contiene {collection_info.points_count} chunks")
        print("   Per testare la ricerca completa, usa il chatbot")
        
    except Exception as e:
        print(f"❌ Errore: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_collection()

