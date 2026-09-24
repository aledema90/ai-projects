# ai-projects

Multi-project container for AI experiments and prototypes.

Each folder is an independent project: its own README, dependencies, and (optionally) its own repo. You'll find agents, RAG pipelines, tools, and quick spikes — not production products.

## Projects

| Folder | Description |
| --- | --- |
| [`ticket-agent/`](./ticket-agent) | Multi-step agent that classifies and answers BIM support tickets, with human escalation on low confidence |

## Layout

```
ai-projects/
├── README.md          ← this file
├── LICENSE
├── .gitignore         ← shared ignore rules for all projects
└── <project-name>/    ← one experiment = one folder
    ├── README.md
    └── ...
```

- **Root**: overview, license, shared ignores.
- **Subfolder**: that experiment's code and docs. Open the folder README for setup and details.

## Adding a project

1. Create a folder at the root (`mkdir my-experiment`).
2. Add a `README.md` with the problem, approach, and how to run it.
3. Add a local `.gitignore` if needed (the root one already covers venvs, `.env`, local DBs, etc.).

## Notes

Stack and models vary by project (local Ollama, cloud APIs, etc.). Always check the folder README before installing or running anything.
