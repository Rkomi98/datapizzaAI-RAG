#!/bin/bash

# Script per avviare il chatbot RAG FAQ Datapizza-AI
# Verifica che tutti i prerequisiti siano soddisfatti

set -e

echo "=================================================="
echo "🚀 Avvio Chatbot RAG Datapizza-AI FAQ"
echo "=================================================="
echo ""

# Verifica che siamo nella directory corretta
if [ ! -f "chatbot_faq.py" ]; then
    echo "❌ Errore: File chatbot_faq.py non trovato!"
    echo "Assicurati di essere nella directory corretta"
    exit 1
fi

# Verifica environment virtuale
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Environment virtuale non attivo!"
    echo "Attivazione in corso..."
    source rag/bin/activate
    echo "✅ Environment virtuale attivato"
else
    echo "✅ Environment virtuale già attivo: $VIRTUAL_ENV"
fi

# Verifica file .env
if [ ! -f ".env" ]; then
    echo "❌ Errore: File .env non trovato!"
    echo "Copia .env.example in .env e configura la tua API key"
    exit 1
fi

# Verifica che l'API key sia configurata
if grep -q "your_openai_api_key_here" .env; then
    echo "❌ Errore: OPENAI_API_KEY non configurata!"
    echo "Modifica il file .env e inserisci la tua OpenAI API key"
    exit 1
fi

echo "✅ Configurazione verificata"
echo ""

# Verifica se Qdrant è in esecuzione
echo "🔍 Verifica connessione a Qdrant..."
if curl -s http://localhost:6333/health > /dev/null 2>&1; then
    echo "✅ Qdrant è in esecuzione"
else
    echo "❌ Qdrant non è in esecuzione!"
    echo ""
    echo "Avvia Qdrant con:"
    echo "  docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant"
    echo ""
    exit 1
fi

echo ""
echo "=================================================="
echo "✅ Tutti i prerequisiti soddisfatti!"
echo "=================================================="
echo ""

# Avvia il chatbot
python chatbot_faq.py

