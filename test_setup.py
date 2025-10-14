"""
Script di test per verificare che tutti i componenti siano configurati correttamente.
"""

import os
import sys

def check_environment():
    """Verifica che l'environment virtuale sia attivo."""
    print("🔍 Verifica environment virtuale...")
    venv_path = os.environ.get('VIRTUAL_ENV', '')
    
    if 'rag' in venv_path:
        print(f"✅ Environment virtuale attivo: {venv_path}")
        return True
    else:
        print("⚠️  Environment virtuale non attivo o non corretto")
        print("   Esegui: source rag/bin/activate")
        return False

def check_dependencies():
    """Verifica che le dipendenze siano installate."""
    print("\n🔍 Verifica dipendenze...")
    
    required_packages = [
        'datapizza',
        'dotenv',
        'qdrant_client',
        'openai'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} non trovato")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Pacchetti mancanti: {', '.join(missing)}")
        print("   Esegui: pip install -r requirements.txt")
        return False
    
    return True

def check_env_file():
    """Verifica che il file .env esista e sia configurato."""
    print("\n🔍 Verifica file .env...")
    
    if not os.path.exists('.env'):
        print("❌ File .env non trovato")
        print("   Crea il file .env copiando .env.example")
        return False
    
    print("✅ File .env trovato")
    
    # Verifica che l'API key sia configurata
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY', '')
    
    if not api_key or api_key == 'your_openai_api_key_here':
        print("❌ OPENAI_API_KEY non configurata")
        print("   Modifica il file .env e inserisci la tua API key")
        return False
    
    print("✅ OPENAI_API_KEY configurata")
    return True

def check_qdrant():
    """Verifica che Qdrant sia raggiungibile."""
    print("\n🔍 Verifica connessione a Qdrant...")
    
    try:
        import httpx
        response = httpx.get('http://localhost:6333/health', timeout=5.0)
        
        if response.status_code == 200:
            print("✅ Qdrant è in esecuzione e raggiungibile")
            return True
        else:
            print(f"⚠️  Qdrant risponde ma con status code: {response.status_code}")
            return False
            
    except Exception as e:
        print("❌ Impossibile connettersi a Qdrant")
        print(f"   Errore: {e}")
        print("   Avvia Qdrant con: docker run -p 6333:6333 qdrant/qdrant")
        return False

def check_faq_files():
    """Verifica che i file FAQ esistano."""
    print("\n🔍 Verifica file FAQ...")
    
    faq_files = ['datapizza_faq.md', 'FAQ_Video.md']
    all_found = True
    
    for faq_file in faq_files:
        if os.path.exists(faq_file):
            print(f"✅ {faq_file}")
        else:
            print(f"❌ {faq_file} non trovato")
            all_found = False
    
    return all_found

def check_scripts():
    """Verifica che gli script principali esistano."""
    print("\n🔍 Verifica script principali...")
    
    scripts = ['ingest_faq.py', 'chatbot_faq.py']
    all_found = True
    
    for script in scripts:
        if os.path.exists(script):
            print(f"✅ {script}")
        else:
            print(f"❌ {script} non trovato")
            all_found = False
    
    return all_found

def main():
    """Esegue tutti i controlli."""
    print("=" * 70)
    print("🔧 Test Setup Chatbot RAG Datapizza-AI")
    print("=" * 70)
    
    checks = [
        ("Environment virtuale", check_environment),
        ("Dipendenze Python", check_dependencies),
        ("File .env", check_env_file),
        ("Connessione Qdrant", check_qdrant),
        ("File FAQ", check_faq_files),
        ("Script principali", check_scripts),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Errore durante il test '{name}': {e}")
            results.append((name, False))
    
    # Riepilogo
    print("\n" + "=" * 70)
    print("📊 RIEPILOGO")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} controlli superati")
    
    if passed == total:
        print("\n🎉 Setup completato con successo!")
        print("\nProssimi passi:")
        print("1. Esegui l'ingestion: python ingest_faq.py")
        print("2. Avvia il chatbot: python chatbot_faq.py")
        print("   oppure usa: ./run_chatbot.sh")
    else:
        print("\n⚠️  Alcuni controlli non sono stati superati.")
        print("Segui le istruzioni sopra per risolvere i problemi.")
        sys.exit(1)
    
    print("=" * 70)

if __name__ == "__main__":
    main()

