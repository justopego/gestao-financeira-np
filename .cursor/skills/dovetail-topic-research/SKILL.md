---
name: dovetail-topic-research
description: >-
  Pesquisa exaustiva no Dovetail sobre um tema usando o MCP Dovetail — search_workspace com paginação,
  variações de query e get_* para conteúdo completo. Usar quando o utilizador quiser "tudo" sobre um tópico no Dovetail.
---

# Pesquisa exaustiva de tema no Dovetail

## Fluxo

1. Confirmar tema + sinónimos + PT/EN.
2. `search_workspace`: `limit` 100, `offset` 0, 100, 200… até esgotar; sem `types` salvo pedido contrário.
3. Repetir com queries alternativas; consolidar e deduplicar.
4. `get_data_content` / `get_insight_content` / outros `get_*` quando precisar de corpo completo.
5. Opcional: `get_dovetail_projects` → `list_project_data` / `list_project_insights` com cursores.

## Formato de output sugerido

- **Queries usadas**
- **Por tipo** (HIGHLIGHT, INSIGHT, …): lista com título, 1 linha, ID/ref
- **Síntese** transversal
- **Próximos passos** (tags/projetos a abrir no Dovetail)
