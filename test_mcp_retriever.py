"""
Test script per il MCP retriever - interroga la documentazione ufficiale di datapizza-ai
"""

import asyncio
import sys
from pathlib import Path

# Aggiungi il percorso del MCP server al path
mcp_server_path = Path(__file__).parent / "mcp-server-datapizza" / "datapizza-mcp-server" / "src"
sys.path.insert(0, str(mcp_server_path))

from datapizza_mcp.retriever import query_documentation


async def test_queries():
    """Test delle query sulla documentazione ufficiale."""
    
    queries = [
        "How can I install datapizza-ai?",
        "How can I set up a RAG?", 
        "How can I monitor my pipeline?",
        "Quali sono i principali moduli di datapizza-ai?",
        "Come funziona il DagPipeline?"
    ]
    
    print("=" * 80)
    print("🔍 TEST MCP RETRIEVER - Documentazione Ufficiale Datapizza-AI")
    print("=" * 80)
    print()
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*80}")
        print(f"📝 QUERY {i}/{len(queries)}: {query}")
        print(f"{'='*80}\n")
        
        try:
            result = await query_documentation(query, max_results=5)
            print(result)
            print()
        except Exception as e:
            print(f"❌ Errore durante la query: {e}")
            import traceback
            traceback.print_exc()
        
        # Pausa tra le query per non sovraccaricare
        if i < len(queries):
            await asyncio.sleep(1)
    
    print("\n" + "=" * 80)
    print("✅ Test completato!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(test_queries())

