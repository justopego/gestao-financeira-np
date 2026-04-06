#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera HTML para cada insight em dovetail-export/insights/*.md (exceto README).
Secções 1–6: extração heurística + aviso quando não há detalhe por tarefa no texto.
"""
from __future__ import annotations

import html as html_module
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "dovetail-export" / "Dovetail-Gestao-Financeira-INSIGHTS-INDEX.md"
INSIGHTS = ROOT / "dovetail-export" / "insights"
OUT = Path(__file__).resolve().parent

# IDs com ficheiro HTML já escrito à mão (este script não sobrescreve)
SKIP_IDS = frozenset(
    {
        "6pb4TbEfeOnthaPr8S4Ohn",
        "o0oV8hJoq0HkVx81Mdkjn",
        "475KIzTqhhJF7TtgKXvY7b",
    }
)

KW = re.compile(
    r"financeir|gestão financeira|gestao financeira|pagamento|crédito|credito|empréstimo|emprestimo|"
    r"estorno|saque|recebimento|concilia|relatório|relatorio|parcela|boleto|\bpix\b|Nuvem Pago|Nuvemshop|"
    r"\bERP\b|faturamento|fluxo de caixa|capital|contas a pagar|tarifa|taxa|saldo|transferência|"
    r"transferencia|checkout|meio de pagamento|bloqueio|fraude|emissão de nota|nota fiscal",
    re.I,
)


def parse_index() -> dict[str, tuple[str, str]]:
    """id -> (titulo, projeto)"""
    out: dict[str, tuple[str, str]] = {}
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 5:
            continue
        try:
            num = int(parts[1])
        except ValueError:
            continue
        m_id = re.search(r"`([^`]+)`", parts[2])
        if not m_id:
            continue
        rid = m_id.group(1)
        title = parts[3]
        project = parts[4]
        out[rid] = (title, project)
    return out


def clean_line(s: str) -> str:
    s = re.sub(r"^>\s*", "", s.strip())
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"[`*_#]+", "", s)
    return s.strip()


def extract_bullets(md: str, limit: int = 18) -> list[str]:
    seen: set[str] = set()
    bullets: list[str] = []
    for line in md.splitlines():
        line_stripped = line.strip()
        if not line_stripped or line_stripped.startswith("| ---"):
            continue
        if not KW.search(line_stripped):
            continue
        c = clean_line(line_stripped)
        if len(c) < 25 or len(c) > 700:
            continue
        if c in seen:
            continue
        seen.add(c)
        bullets.append(c)
        if len(bullets) >= limit:
            break
    return bullets


def page_shell(
    title: str,
    insight_id: str,
    projeto: str,
    body_inner: str,
) -> str:
    esc_title = html_module.escape(title)
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{esc_title}</title>
  <style>
    :root {{ font-family: "Georgia", "Times New Roman", serif; line-height: 1.55; color: #1a1a1a; }}
    body {{ max-width: 52rem; margin: 0 auto; padding: 1.5rem 1.25rem 3rem; background: #faf9f7; }}
    header {{ border-bottom: 1px solid #ccc; padding-bottom: 1rem; margin-bottom: 1.5rem; }}
    h1 {{ font-size: 1.35rem; font-weight: 600; margin: 0 0 0.35rem; }}
    .meta {{ font-size: 0.9rem; color: #555; }}
    h2 {{ font-size: 1.05rem; margin-top: 1.75rem; border-top: 1px solid #e0ddd6; padding-top: 1rem; }}
    .warn {{ background: #fff8e6; border: 1px solid #e6d08c; padding: 0.85rem 1rem; border-radius: 6px; margin: 1rem 0; font-size: 0.95rem; }}
    ul {{ padding-left: 1.2rem; }}
    li {{ margin: 0.35rem 0; }}
    a {{ color: #0b57d0; }}
    footer {{ margin-top: 2.5rem; font-size: 0.85rem; color: #666; }}
  </style>
</head>
<body>
  <header>
    <h1>{esc_title}</h1>
    <p class="meta">ID Dovetail: <code>{html_module.escape(insight_id)}</code> · Projeto: {html_module.escape(projeto)}</p>
    <p class="meta"><a href="index.html">← Índice</a> · Fonte: <code>dovetail-export/insights/{html_module.escape(insight_id)}.md</code></p>
  </header>
  <main>
{body_inner}
  </main>
  <footer>
    Página gerada a partir do export local. Não substitui validação no Dovetail.
  </footer>
</body>
</html>
"""


def generic_body(bullets: list[str]) -> str:
    bhtml = ""
    if bullets:
        bhtml = "<ul>\n" + "\n".join(f"    <li>{html_module.escape(b)}</li>" for b in bullets) + "\n  </ul>"
    else:
        bhtml = "<p><em>Nenhuma linha com palavras-chave financeiras óbvias foi destacada automaticamente; veja o relatório completo no ficheiro Markdown.</em></p>"

    return f"""
  <div class="warn">
    <strong>Atenção:</strong> este ficheiro é um <strong>relatório de insight</strong> (síntese), não uma transcrição integral de uma única entrevista.
    As respostas abaixo são <strong>parciais</strong>: onde o texto não detalha passo a passo, frequência ou ferramentas por tarefa, isso está indicado explicitamente.
  </div>

  <h2>1. Tarefas relacionadas à gestão financeira (trechos relevantes no documento)</h2>
  {bhtml}

  <h2>2. Passo a passo (fluxo) por tarefa</h2>
  <p><strong>Não consta</strong> no export, de forma sistemática, um fluxo numerado por tarefa de gestão financeira. O documento mistura descobertos e citações de vários participantes.</p>

  <h2>3. Dificuldades por tarefa</h2>
  <p>As dificuldades aparecem ligadas a temas (ex.: crédito, cobrança), mas <strong>não estão mapeadas tarefa a tarefa</strong> com o nível de detalhe pedido. Consulte as citações no Markdown fonte.</p>

  <h2>4. Dados utilizados por tarefa</h2>
  <p><strong>Não especificado</strong> de forma consistente por tarefa neste relatório agregado.</p>

  <h2>5. Frequência de cada tarefa</h2>
  <p><strong>Não especificado</strong> na maioria dos casos neste export.</p>

  <h2>6. Ferramentas</h2>
  <p>Mencione-se ferramentas ou canais apenas nas citações do relatório (ex.: WhatsApp, e-mail, produto Nuvemshop). <strong>Não há inventário completo</strong> por entrevistado neste ficheiro.</p>
"""


def main() -> None:
    meta = parse_index()
    OUT.mkdir(parents=True, exist_ok=True)
    for path in sorted(INSIGHTS.glob("*.md")):
        if path.name == "README.md":
            continue
        insight_id = path.stem
        if insight_id in SKIP_IDS:
            continue
        title, projeto = meta.get(insight_id, (insight_id, "—"))
        md = path.read_text(encoding="utf-8")
        bullets = extract_bullets(md)
        out_path = OUT / f"{insight_id}.html"
        out_path.write_text(
            page_shell(title, insight_id, projeto, generic_body(bullets)),
            encoding="utf-8",
        )
        print("wrote", out_path.name)


if __name__ == "__main__":
    main()
