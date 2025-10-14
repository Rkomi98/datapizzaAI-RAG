# 🌐 Anteprima Interfaccia Web

## Layout Generale

```
┌─────────────────────────────────────────────────────────────────┐
│                 🍕 Chatbot FAQ Datapizza-AI                     │
│           Chiedimi qualsiasi cosa su Datapizza-AI!              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 👋 Benvenuto!                                           │   │
│  │                                                         │   │
│  │ Sono il tuo assistente virtuale per le FAQ di          │   │
│  │ Datapizza-AI. Puoi farmi qualsiasi domanda sul        │   │
│  │ framework e cercherò di risponderti basandomi sulle    │   │
│  │ informazioni disponibili.                              │   │
│  │                                                         │   │
│  │ Inizia facendo una domanda qui sotto! ⬇️               │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  [Scrivi la tua domanda qui...]                    [  Invia  ] │
└─────────────────────────────────────────────────────────────────┘
```

## Con Conversazione Attiva

```
┌───────────────────────────────────────────────────────┬─────────┐
│  🍕 Chatbot FAQ Datapizza-AI                          │ 💡      │
│                                                       │ Sugge-  │
├───────────────────────────────────────────────────────┤ rimenti │
│                                                       │         │
│              ┌──────────────────────────────────┐    │ Prova a │
│              │ 👤 Supporta modelli Llama?       │    │ chiedere│
│              └──────────────────────────────────┘    │         │
│                                                       │ • Cosa  │
│  ┌────────────────────────────────────────────┐      │   diffe-│
│  │ 🤖 Sì, il framework supporta anche Llama.  │      │   renzia│
│  │    È possibile utilizzare modelli locali,  │      │         │
│  │    grazie all'integrazione del client      │      │ • Sup-  │
│  │    Llama. Inoltre, è disponibile la        │      │   porta │
│  │    documentazione su docs.datapizza.ai...  │      │   Llama?│
│  └────────────────────────────────────────────┘      │         │
│                                                       │ ---     │
│              ┌──────────────────────────────────┐    │         │
│              │ 👤 Come funziona la memory?      │    │ ⚙️       │
│              └──────────────────────────────────┘    │ Imposta │
│                                                       │ zioni   │
│  ┌────────────────────────────────────────────┐      │         │
│  │ 🤖 La memoria nel framework Datapizza-AI   │      │ Chunks: │
│  │    funziona attraverso i metodi            │      │ ●───○   │
│  │    json_dumps() e json_loads()...          │      │ 1    10 │
│  └────────────────────────────────────────────┘      │         │
│                                                       │ ---     │
├───────────────────────────────────────────────────────┤         │
│  [Scrivi la tua domanda qui...]       [  Invia  ]    │ 📊      │
└───────────────────────────────────────────────────────┴─────────┘
```

## Elementi dell'Interfaccia

### 🎨 Stile

#### Header
- **Colore**: Gradient purple/blue (#667eea → #764ba2)
- **Font**: Large, bold, centrato
- **Emoji**: 🍕 per brand identity

#### Messaggi Utente (👤)
- **Background**: Purple (#667eea)
- **Colore testo**: Bianco
- **Posizione**: Allineati a destra
- **Ombra**: Soft shadow per profondità
- **Border radius**: Arrotondati (1rem)

#### Messaggi Bot (🤖)
- **Background**: Grigio chiaro (#f7f7f8)
- **Colore testo**: Scuro (#1a1a1a)
- **Posizione**: Allineati a sinistra
- **Ombra**: Subtle shadow
- **Border radius**: Arrotondati (1rem)

#### Input Box
- **Border**: 2px solid #e0e0e0
- **Border radius**: Completamente arrotondato (2rem)
- **Padding**: Generoso per comfort
- **Focus**: Highlight blu con glow

#### Pulsante Invio
- **Background**: Gradient purple (#667eea → #764ba2)
- **Colore**: Bianco
- **Hover**: Lift animation (translateY -2px)
- **Border radius**: Completamente arrotondato

### 📱 Sidebar

```
┌──────────────────────┐
│  💡 Suggerimenti     │
├──────────────────────┤
│  Prova a chiedere:   │
│                      │
│  • Cosa differenzia  │
│    Datapizza-AI?     │
│  • Supporta modelli  │
│    Llama?            │
│  • Come funziona     │
│    la memory?        │
│                      │
├──────────────────────┤
│  ⚙️ Impostazioni      │
├──────────────────────┤
│  Chunks da           │
│  recuperare          │
│  ●────────○          │
│  1    5   10         │
│                      │
├──────────────────────┤
│  📊 Statistiche      │
├──────────────────────┤
│  Messaggi totali     │
│        12            │
│                      │
│  [🗑️ Pulisci chat]   │
│                      │
├──────────────────────┤
│  📚 Risorse          │
├──────────────────────┤
│  • Documentazione    │
│  • GitHub            │
│  • Guida RAG         │
└──────────────────────┘
```

## 🎭 Stati dell'Interfaccia

### Stato Iniziale
- Messaggio di benvenuto visibile
- Input box vuoto
- Sidebar con suggerimenti
- Footer con credits

### Stato "Pensando"
```
┌──────────────────────────────┐
│  🤔 Sto pensando...          │
│  ⏳ Elaborazione in corso... │
└──────────────────────────────┘
```

### Stato Errore
```
┌──────────────────────────────────────────┐
│  ⚠️ Errore nell'inizializzazione         │
│                                          │
│  Assicurati di:                          │
│  1. Aver eseguito l'ingestion           │
│  2. Aver configurato .env               │
│  3. Aver avviato Qdrant                 │
└──────────────────────────────────────────┘
```

## 🎬 Flusso di Interazione

1. **Utente apre l'app**
   - Vede messaggio di benvenuto
   - Sidebar mostra suggerimenti

2. **Utente digita domanda**
   - Input box evidenziato
   - Testo formattato

3. **Utente invia (Enter o click)**
   - Messaggio appare nella chat
   - Indicatore "Sto pensando..." appare

4. **Bot elabora**
   - Query rewriting
   - Embedding generation
   - Vector search
   - Response generation

5. **Bot risponde**
   - Risposta appare nella chat
   - Scroll automatico
   - Statistiche aggiornate

6. **Utente continua**
   - Può fare altre domande
   - Cronologia mantenuta
   - Context preserved

## 🌈 Palette Colori

```
Primary Purple:   #667eea
Accent Violet:    #764ba2
Light Gray:       #f7f7f8
Dark Text:        #1a1a1a
Border Gray:      #e0e0e0
Background:       #FFFFFF
```

## 📐 Dimensioni e Spaziature

- **Container max-width**: 1200px
- **Padding messaggi**: 1rem
- **Margin messaggi**: 0.5rem verticale
- **Border radius**: 1rem (messaggi), 2rem (input/button)
- **Box shadow**: 
  - Messaggi: `0 2px 8px rgba(0,0,0,0.1)`
  - Button hover: `0 4px 12px rgba(102,126,234,0.4)`

## 💻 Responsive Breakpoints

- **Desktop** (>1200px): Full layout con sidebar espansa
- **Tablet** (768px-1200px): Layout compatto
- **Mobile** (<768px): Stack verticale, sidebar collassata

## 🎯 User Experience

### Feedback Visivo
- ✅ Hover states su tutti i clickable
- ✅ Focus states su input
- ✅ Loading indicators
- ✅ Smooth transitions

### Accessibilità
- ✅ Contrasto colori WCAG AA
- ✅ Keyboard navigation
- ✅ Screen reader friendly
- ✅ Clear visual hierarchy

### Performance
- ✅ Lazy loading dei messaggi
- ✅ Caching del chatbot
- ✅ Fast initial load
- ✅ Smooth scrolling

## 🚀 Come Appare in Azione

### Esempio Completo di Conversazione

```
═══════════════════════════════════════════════════════════════
                🍕 Chatbot FAQ Datapizza-AI                    
             Chiedimi qualsiasi cosa su Datapizza-AI!          
═══════════════════════════════════════════════════════════════

                     ╔══════════════════════════════════╗
                     ║ 👤 Supporta modelli Llama?       ║
                     ╚══════════════════════════════════╝

╔════════════════════════════════════════════════════════════╗
║ 🤖 Sì, il framework supporta anche Llama. All'interno     ║
║    della documentazione (su docs.datapizza.ai) è          ║
║    possibile trovare le istruzioni per eseguire un        ║
║    client Llama o un server Llama in locale.              ║
╚════════════════════════════════════════════════════════════╝

                     ╔══════════════════════════════════╗
                     ║ 👤 E per documenti aziendali?    ║
                     ╚══════════════════════════════════╝

╔════════════════════════════════════════════════════════════╗
║ 🤖 Sì, è possibile utilizzare documenti aziendali in      ║
║    locale senza problemi di privacy, a patto di           ║
║    utilizzare un modello locale come Mistral o Llama...   ║
╚════════════════════════════════════════════════════════════╝

───────────────────────────────────────────────────────────────
 [Scrivi la tua domanda qui...]                    [  Invia  ]
───────────────────────────────────────────────────────────────
          Costruito con ❤️ usando Datapizza-AI                
═══════════════════════════════════════════════════════════════
```

## ✨ Easter Eggs

- 🍕 Emoji pizza nel titolo (brand identity)
- 💜 Purple gradient (AI/tech aesthetic)
- 🎨 Hover animations
- ⚡ Smooth transitions
- 🌊 Fluid scrolling

