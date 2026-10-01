"""
Ticket Triage Agent
Agente multi-step per classificare e rispondere a ticket di supporto tecnico,
con escalation automatica a un umano quando la confidenza è bassa.
Stack 100% gratuito: Ollama (LLM locale) + ChromaDB + sentence-transformers.
"""

import sqlite3
from datetime import datetime
from typing import TypedDict, Optional

from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END


# ============================================================
# CONFIGURAZIONE MODELLO E EMBEDDINGS
# ============================================================
# LLM locale via Ollama — nessun costo, nessuna API key richiesta.
# temperature=0 rende le risposte più deterministiche (utile per classificazione).
llm = ChatOllama(model="llama3.1", temperature=0)

# Modello di embedding gratuito per il retrieval semantico (gira in locale).
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Parole che il sistema non deve mai includere in una risposta automatica.
PAROLE_VIETATE = ["rimborso garantito", "risolto al 100%", "nessun costo"]


# ============================================================
# STATO CONDIVISO TRA GLI AGENTI
# ============================================================
# Questo dizionario tipizzato passa da un nodo all'altro del grafo,
# accumulando informazioni man mano che il ticket viene processato.
class TicketState(TypedDict):
    ticket_text: str
    category: Optional[str]
    kb_results: Optional[list]
    draft_response: Optional[str]
    confidence: Optional[float]
    final_action: Optional[str]


# ============================================================
# SETUP KNOWLEDGE BASE (da eseguire una volta sola per popolare il DB)
# ============================================================
def build_knowledge_base():
    documenti = [
        # ===== BUG NOTI CON SOLUZIONE (6 voci) =====
        "L'export IFC può bloccarsi se il modello supera 500MB. Soluzione: dividere il progetto in sotto-progetti o aumentare il timeout nelle impostazioni avanzate (Progetto > Export > Timeout).",
        
        "Errore 'Sync failed' dopo un aggiornamento dell'app: causato spesso da cache locale corrotta. Soluzione: svuotare la cache da Impostazioni > Manutenzione > Pulisci cache, poi riavviare l'app.",
        
        "Il rendering 3D rallenta o si blocca con modelli oltre 10.000 elementi: attivare la modalità 'Performance' in Preferenze > Visualizzazione > Modalità rendering.",
        
        "Errore 'File corrotto' all'apertura di un progetto salvato: nella maggior parte dei casi il backup automatico più recente si trova in File > Cronologia versioni, ripristinabile con un click.",
        
        "Le quote automatiche non si aggiornano dopo una modifica al modello: è un problema noto quando l'opzione 'Aggiornamento automatico quote' è disattivata. Riattivarla da Disegno > Quote > Impostazioni.",
        
        "Il plugin di collisioni (clash detection) restituisce falsi positivi su elementi sovrapposti intenzionalmente: usare la funzione 'Ignora coppia' per escludere manualmente quelle collisioni dai report futuri.",
        
        # ===== DOMANDE D'USO / HOW-TO (6 voci) =====
        "Per importare un file Revit, usare il plugin BIM Connector versione 3.2 o superiore, scaricabile dal marketplace integrato in Impostazioni > Plugin.",
        
        "Per condividere un progetto con un collaboratore esterno all'organizzazione, usare la funzione 'Invita' nella barra laterale (icona persona), non l'export diretto che non mantiene i permessi di editing.",
        
        "I livelli di dettaglio (LOD) del modello si configurano da Progetto > Impostazioni > Precisione modello, con 5 livelli disponibili da LOD 100 a LOD 500.",
        
        "Per generare automaticamente elenchi materiali (BOM) da un modello, usare lo strumento 'Estrazione quantità' in Analisi > Report, selezionando le categorie di elementi da includere.",
        
        "Per lavorare offline e sincronizzare in seguito, attivare 'Modalità offline' da Impostazioni > Sincronizzazione: le modifiche vengono messe in coda e caricate alla riconnessione.",
        
        "Per confrontare due versioni dello stesso progetto, usare 'Confronto versioni' in Cronologia > Confronta, che evidenzia in rosso gli elementi rimossi e in verde quelli aggiunti.",
        
        # ===== CONFIGURAZIONI / LIMITI TECNICI (4 voci) =====
        "Il piano Free supporta fino a 3 progetti attivi contemporaneamente e 2GB di storage cloud totale.",
        
        "I formati di export supportati sono: IFC, DWG, PDF, PNG. Non è supportato l'export diretto in formato nativo Revit (RVT) per limitazioni della licenza Autodesk.",
        
        "Il numero massimo di collaboratori simultanei su un singolo progetto è 15 nel piano Team, illimitato nel piano Enterprise.",
        
        "I file allegati (immagini, PDF di riferimento) hanno un limite di 50MB per singolo file nel piano Team.",
        
        # ===== CASI LIMITE — per testare i guardrail (2 voci) =====
        "Per problemi di licenza enterprise o fatturazione, contattare il team commerciale dedicato all'indirizzo sales@esempio.com. Il supporto tecnico non gestisce direttamente le questioni di licenza.",
        
        "Errori legati a plugin di terze parti non ufficiali non sono coperti dal supporto standard: si consiglia di disabilitare temporaneamente i plugin non certificati per isolare il problema prima di contattare l'assistenza.",
    ]
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.create_documents(documenti)
    Chroma.from_documents(chunks, embeddings, persist_directory="./kb_db")
    print(f"Knowledge base creata con {len(documenti)} documenti")


# ============================================================
# NODO 1 — ROUTER: classifica il ticket in una categoria
# ============================================================
def router_node(state: TicketState) -> TicketState:
    prompt = f"""Classifica questo ticket in una categoria: bug, domanda, feature_request.
    Rispondi SOLO con una parola tra queste tre, nient'altro.
    Ticket: {state['ticket_text']}"""

    result = llm.invoke(prompt)
    categoria_grezza = result.content.strip().lower()

    # Parsing difensivo: i modelli locali a volte aggiungono testo extra
    # oltre alla parola richiesta, quindi cerchiamo la categoria all'interno
    # della risposta invece di fare un confronto esatto.
    for cat in ["bug", "domanda", "feature_request"]:
        if cat in categoria_grezza:
            state["category"] = cat
            return state

    state["category"] = "domanda"  # fallback sicuro se il parsing fallisce
    return state


# ============================================================
# NODO 2 — RICERCA NELLA KNOWLEDGE BASE
# ============================================================
def kb_search_node(state: TicketState) -> TicketState:
    db = Chroma(persist_directory="./kb_db", embedding_function=embeddings)
    results = db.similarity_search(state["ticket_text"], k=3)
    state["kb_results"] = [r.page_content for r in results]
    
    # DEBUG temporaneo — rimuovi dopo
    print("\n--- Documenti recuperati ---")
    for r in state["kb_results"]:
        print(r)
    print("---\n")
    
    return state


# ============================================================
# NODO 3 — SCRITTURA RISPOSTA + CALCOLO CONFIDENZA
# ============================================================
def write_response_node(state: TicketState) -> TicketState:
    context = "\n".join(state["kb_results"])
    prompt = f"""Basandoti SOLO su questo contesto, scrivi una risposta breve al ticket.
    Se il contesto non è sufficiente, rispondi esattamente "INSUFFICIENTE".
    Non inventare informazioni non presenti nel contesto.

    Contesto: {context}
    Ticket: {state['ticket_text']}"""

    result = llm.invoke(prompt)
    risposta = result.content
    state["draft_response"] = risposta

    # Confidenza semplificata: se il modello dichiara di non avere
    # abbastanza contesto, la confidenza è bassa e scatta l'escalation.
    state["confidence"] = 0.3 if "INSUFFICIENTE" in risposta else 0.8
    return state


# ============================================================
# GUARDRAIL — controllo finale prima dell'invio
# ============================================================
def check_guardrail(risposta: str) -> bool:
    """Ritorna False se la risposta contiene una frase vietata."""
    return not any(parola in risposta.lower() for parola in PAROLE_VIETATE)


# ============================================================
# LOGGING SU SQLITE
# ============================================================
def log_run(state: TicketState):
    conn = sqlite3.connect("logs.db")
    conn.execute("""CREATE TABLE IF NOT EXISTS logs 
        (ticket TEXT, categoria TEXT, confidenza REAL, azione TEXT, timestamp TEXT)""")
    conn.execute("INSERT INTO logs VALUES (?, ?, ?, ?, ?)", (
        state["ticket_text"], state["category"], state["confidence"],
        state.get("final_action", ""), datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


# ============================================================
# COSTRUZIONE DEL GRAFO — collega i nodi in sequenza con branch condizionale
# ============================================================
graph = StateGraph(TicketState)
graph.add_node("router", router_node)
graph.add_node("kb_search", kb_search_node)
graph.add_node("write_response", write_response_node)

graph.set_entry_point("router")
graph.add_edge("router", "kb_search")
graph.add_edge("kb_search", "write_response")


def route_after_write(state: TicketState) -> str:
    """Decide se inviare automaticamente o escalare a un umano,
    in base alla confidenza calcolata nel nodo precedente."""
    return "send" if state["confidence"] > 0.7 else "escalate"


graph.add_conditional_edges("write_response", route_after_write, {
    "send": END,
    "escalate": END,
})

app = graph.compile()


# ============================================================
# ESECUZIONE PRINCIPALE
# ============================================================
if __name__ == "__main__":
    # Esegui build_knowledge_base() una sola volta per creare il DB vettoriale.
    # Decommenta la riga sotto al primo avvio, poi puoi ricommentarla.
    # build_knowledge_base()

    ticket_di_test = input("Inserisci il testo del ticket: ")
    result = app.invoke({"ticket_text": ticket_di_test})

    # Applica il guardrail finale prima di decidere l'azione da loggare.
    risposta_ok = check_guardrail(result["draft_response"])
    result["final_action"] = "send" if (result["confidence"] > 0.7 and risposta_ok) else "escalate"

    print("Categoria:", result["category"])
    print("Risposta:", result["draft_response"])
    print("Confidenza:", result["confidence"])

    log_run(result)