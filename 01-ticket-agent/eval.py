"""
Eval suite per il ticket triage agent.
Esegui separatamente da main.py con: python eval.py
"""

from main import app  # importa il grafo già compilato da main.py

eval_set = [
    {"ticket": "L'export si blocca sempre quasi alla fine, cosa faccio?", "expected_category": "bug"},
    {"ticket": "Dopo l'ultimo aggiornamento non riesco più a sincronizzare", "expected_category": "bug"},
    {"ticket": "Il programma diventa lentissimo con progetti grandi", "expected_category": "bug"},
    {"ticket": "Il file non si apre, dice che è corrotto", "expected_category": "bug"},
    {"ticket": "Le misure sul disegno non si aggiornano da sole", "expected_category": "bug"},
    {"ticket": "Il clash detection segnala collisioni che non esistono davvero", "expected_category": "bug"},
    {"ticket": "Non riesco a importare il mio file Revit", "expected_category": "domanda"},
    {"ticket": "Come faccio a far lavorare un collega esterno sul mio progetto?", "expected_category": "domanda"},
    {"ticket": "Dove imposto il livello di dettaglio del modello?", "expected_category": "domanda"},
    {"ticket": "Come genero la lista dei materiali automaticamente?", "expected_category": "domanda"},
    {"ticket": "Posso lavorare senza connessione internet?", "expected_category": "domanda"},
    {"ticket": "Come vedo cosa è cambiato tra due versioni del progetto?", "expected_category": "domanda"},
    {"ticket": "Ho un problema strano con la fatturazione del mio abbonamento", "expected_category": "domanda"},
    {"ticket": "Un plugin che ho scaricato da un sito esterno crasha l'app", "expected_category": "bug"},
    {"ticket": "Sarebbe utile poter esportare direttamente in formato RVT", "expected_category": "feature_request"},
    {"ticket": "Vorrei poter avere più di 3 progetti nel piano free", "expected_category": "feature_request"},
]


def run_eval():
    correct = 0
    dettagli = []

    for item in eval_set:
        result = app.invoke({"ticket_text": item["ticket"]})
        is_correct = result["category"] == item["expected_category"]
        correct += is_correct

        dettagli.append({
            "ticket": item["ticket"],
            "atteso": item["expected_category"],
            "ottenuto": result["category"],
            "corretto": is_correct,
            "confidenza": result["confidence"],
        })

    accuratezza = correct / len(eval_set) * 100
    print(f"\nAccuratezza classificazione: {accuratezza:.1f}% ({correct}/{len(eval_set)})\n")

    # Mostra solo gli errori per un debug rapido
    print("--- Casi sbagliati ---")
    for d in dettagli:
        if not d["corretto"]:
            print(f"Ticket: {d['ticket']}")
            print(f"  Atteso: {d['atteso']} | Ottenuto: {d['ottenuto']}\n")

    return dettagli


if __name__ == "__main__":
    run_eval()