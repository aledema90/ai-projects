# Ticket Triage Agent

Agente multi-step che classifica e risponde automaticamente ai ticket di supporto tecnico per un software BIM, con escalation automatica a un operatore umano quando la confidenza è bassa.

## Il problema

I team di supporto tecnico B2B perdono tempo prezioso a smistare manualmente ticket tra bug, domande d'uso e richieste feature. Questo agente automatizza la classificazione e propone risposte basate sulla knowledge base esistente, mantenendo un umano nel loop per i casi incerti.

## Come funziona

Ticket in ingresso
↓
Router (classifica: bug / domanda / feature request)
↓
Ricerca nella knowledge base (retrieval semantico)
↓
Generazione risposta
↓
Check di confidenza → invio automatico OPPURE escalation umana

## Esempio

**Input**: "L'export IFC si blocca al 90%"

**Output**:

- Categoria: `bug`
- Risposta: "L'export IFC può bloccarsi se il modello supera 500MB. Soluzione: dividere in sotto-progetti."
- Confidenza: 0.8 → inviata automaticamente

## Stack tecnologico

| Componente            | Tecnologia            | Perché                                                        |
| --------------------- | --------------------- | ------------------------------------------------------------- |
| Orchestrazione agenti | LangGraph             | Controllo esplicito su stato e branch condizionali            |
| LLM                   | Ollama (Llama 3.1)    | 100% locale e gratuito, nessuna dipendenza da API a pagamento |
| Embeddings            | sentence-transformers | Retrieval semantico gratuito, gira in locale                  |
| Vector DB             | ChromaDB              | Leggero, zero configurazione                                  |
| Log                   | SQLite                | Persistenza semplice senza infrastruttura cloud               |

Il sistema è progettato **model-agnostic**: l'interfaccia LangChain permette di sostituire Ollama con Claude API cambiando una sola riga di codice, per scenari dove serve maggiore qualità di ragionamento a fronte di un costo per chiamata.

## Guardrail implementati

- Filtro su parole vietate prima dell'invio (es. promesse non autorizzate)
- Soglia di confidenza sotto la quale il sistema escalation invece di rispondere
- Parsing difensivo dell'output del modello per gestire risposte fuori formato

## Come farlo girare

```bash
# 1. Installa Ollama da ollama.com, poi:
ollama pull llama3.1

# 2. Setup ambiente
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Esegui
python main.py
```

## Eval

Testato su un set di 30-50 ticket etichettati manualmente, con accuratezza di classificazione misurata e valutazione qualitativa delle risposte tramite LLM-as-judge.

## Cosa ho imparato / prossimi passi

- [Da completare: insight reali dopo aver testato il sistema]
- [Da completare: eventuali limiti riscontrati con modelli locali vs cloud]
- Possibili estensioni: multi-lingua, integrazione con sistema ticketing reale (Zendesk/Freshdesk)

---

_Progetto costruito come parte di un percorso di apprendimento AI Product Management._
