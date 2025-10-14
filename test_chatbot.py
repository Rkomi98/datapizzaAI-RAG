"""
Script per testare il chatbot con domande predefinite.
Utile per verificare il funzionamento senza interazione manuale.
"""

import os
from dotenv import load_dotenv
from chatbot_faq import FAQChatbot

# Carica variabili d'ambiente
load_dotenv()

def test_chatbot():
    """Testa il chatbot con una serie di domande predefinite."""
    print("=" * 70)
    print("🧪 Test Chatbot FAQ Datapizza-AI")
    print("=" * 70)
    print()
    
    # Inizializza il chatbot
    try:
        print("📦 Inizializzazione chatbot...")
        chatbot = FAQChatbot()
        print("✅ Chatbot inizializzato con successo\n")
    except Exception as e:
        print(f"❌ Errore nell'inizializzazione: {e}")
        return
    
    # Domande di test
    test_questions = [
        # Domande che dovrebbero trovare risposte
        ("Cosa differenzia Datapizza-AI da Langchain?", True),
        ("Supporta modelli Llama?", True),
        ("Come funziona la memory?", True),
        ("Posso usare documenti aziendali in locale senza problemi di privacy?", True),
        ("Quali sono i casi d'uso concreti?", True),
        ("Come gestite il bloat del contesto?", True),
        
        # Domande fuori topic (dovrebbero restituire il messaggio di fallback)
        ("Che cos'è la fotosintesi clorofilliana?", False),
        ("Qual è la capitale della Francia?", False),
        ("Come si fa la pizza margherita?", False),
    ]
    
    print("🔍 Esecuzione test...\n")
    print("=" * 70)
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": len(test_questions)
    }
    
    for i, (question, should_find_answer) in enumerate(test_questions, 1):
        print(f"\n[Test {i}/{len(test_questions)}]")
        print(f"👤 Domanda: {question}")
        print(f"🎯 Atteso: {'Risposta trovata' if should_find_answer else 'Nessuna risposta'}")
        print()
        
        try:
            response = chatbot.ask(question)
            
            is_fallback = "Non sono ancora state fatte domande a riguardo" in response
            found_answer = not is_fallback
            
            # Verifica se il risultato corrisponde all'atteso
            test_passed = found_answer == should_find_answer
            
            if test_passed:
                print("✅ Test PASSATO")
                results["passed"] += 1
            else:
                print("❌ Test FALLITO")
                results["failed"] += 1
            
            print(f"🤖 Risposta: {response[:200]}{'...' if len(response) > 200 else ''}")
            
        except Exception as e:
            print(f"❌ Errore: {e}")
            results["failed"] += 1
        
        print("-" * 70)
    
    # Riepilogo
    print("\n" + "=" * 70)
    print("📊 RIEPILOGO TEST")
    print("=" * 70)
    print(f"✅ Test passati: {results['passed']}/{results['total']}")
    print(f"❌ Test falliti: {results['failed']}/{results['total']}")
    print(f"📈 Percentuale successo: {(results['passed']/results['total']*100):.1f}%")
    print("=" * 70)
    
    if results["failed"] == 0:
        print("\n🎉 Tutti i test sono passati! Il chatbot funziona correttamente.")
    else:
        print(f"\n⚠️  {results['failed']} test non hanno passato. Controlla la configurazione.")
    
    print()

if __name__ == "__main__":
    test_chatbot()

