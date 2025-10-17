#!/bin/bash

# Script per avviare il frontend web del chatbot RAG FAQ Datapizza-AI

set -e

echo "=================================================="
echo "🌐 Avvio Frontend Web Chatbot FAQ Datapizza-AI"
echo "=================================================="
echo ""

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

# Carica le variabili d'ambiente (senza esportare accidentalmente stack trace)
set -a
source .env
set +a

# Verifica che le API key siano configurate
if grep -q "your_openai_api_key_here" .env; then
    echo "❌ Errore: OPENAI_API_KEY non configurata!"
    echo "Modifica il file .env e inserisci la tua OpenAI API key"
    exit 1
fi
if grep -q "your_google_api_key_here" .env; then
    echo "❌ Errore: GOOGLE_API_KEY non configurata!"
    echo "Modifica il file .env e inserisci la tua Google API key"
    exit 1
fi

if [ -z "${OPENAI_API_KEY:-}" ]; then
    echo "❌ Errore: variabile OPENAI_API_KEY vuota o non presente."
    exit 1
fi

if [ -z "${GOOGLE_API_KEY:-}" ]; then
    echo "❌ Errore: variabile GOOGLE_API_KEY vuota o non presente."
    exit 1
fi

echo "✅ Configurazione verificata"
echo ""

# Verifica configurazione Qdrant
echo "🔍 Verifica configurazione Qdrant..."
if [ -n "${QDRANT_LOCATION:-}" ]; then
    echo "ℹ️ Qdrant embedded configurato: '${QDRANT_LOCATION}'"
elif [ -n "${QDRANT_URL:-}" ]; then
    echo "✅ Qdrant remoto configurato: ${QDRANT_URL}"
else
    Q_HOST=${QDRANT_HOST:-localhost}
    Q_PORT=${QDRANT_PORT:-6333}
    SCHEME="http"
    case "${QDRANT_HTTPS:-}" in
        1|true|TRUE|yes|YES|on|ON) SCHEME="https" ;;
    esac
    Q_URL="${SCHEME}://${Q_HOST}:${Q_PORT}"
    if curl -s "${Q_URL}/" > /dev/null 2>&1; then
        echo "✅ Qdrant locale raggiungibile su ${Q_URL}"
    else
        echo "❌ Qdrant locale non raggiungibile (${Q_URL})!"
        echo ""
        echo "Avvia Qdrant con:"
        echo "  docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant"
        echo ""
        exit 1
    fi
fi

echo ""
echo "=================================================="
echo "✅ Tutto pronto!"
echo "=================================================="
echo ""
echo "🌐 Avvio interfaccia web..."
echo "L'applicazione si aprirà nel browser tra pochi secondi"
echo ""
echo "Per fermare il server: premi Ctrl+C"
echo ""
echo "=================================================="
echo ""

# Avvia streamlit
streamlit run app.py
