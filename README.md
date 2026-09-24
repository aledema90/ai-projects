# ai-projects

Contenitore multiprogetto per esperimenti e prototipi basati su AI.

Ogni cartella è un progetto indipendente: ha il proprio README, dipendenze e (eventualmente) repo dedicato. Qui troverai agent, pipeline RAG, tool e prove rapide — senza pretesa di prodotto finito.

## Progetti

| Cartella | Descrizione |
| --- | --- |
| [`ticket-agent/`](./ticket-agent) | Agente multi-step che classifica e risponde a ticket di supporto BIM, con escalation umana a bassa confidenza |

## Come è organizzato

```
ai-projects/
├── README.md          ← questo file
├── LICENSE
├── .gitignore         ← regole comuni a tutti i progetti
└── <nome-progetto>/   ← un esperimento = una cartella
    ├── README.md
    └── ...
```

- **Root**: overview, licenza, ignore condivisi.
- **Subfolder**: codice e docs del singolo esperimento. Apri il README della cartella per setup e dettagli.

## Aggiungere un progetto

1. Crea una cartella in root (`mkdir mio-esperimento`).
2. Aggiungi un `README.md` con problema, approccio e come avviarlo.
3. Se serve, un `.gitignore` locale (quello root copre già venv, `.env`, DB locali, ecc.).

## Note

Stack e modelli variano per progetto (locale con Ollama, API cloud, ecc.). Controlla sempre il README della cartella prima di installare o eseguire qualcosa.
