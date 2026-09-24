## Problem Statement

[chi ha il problema, quanto costa non risolverlo]

## User & Context

[chi usa il sistema, in che momento, con che livello di fiducia]

## Success Metrics

- Metrica primaria: es. % di ticket risolti senza escalation
- Metrica di qualità: es. accuratezza classificazione > 85%
- Metrica di costo: es. costo per chiamata < $0.05

## Guardrails (sezione critica — spesso assente nei PRD normali)

- Cosa il sistema NON deve fare mai (es. non deve promettere rimborsi)
- Soglie di confidenza sotto le quali si ferma e chiede aiuto umano
- Dati sensibili che non deve mai processare/loggare

## Failure Modes

[cosa succede se un agente si blocca, se l'API è down, se l'output è malformato]

## Launch Plan

[rollout graduale: 10% traffico → review manuale → 100%]
