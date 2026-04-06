# Estrutura das telas internas (detalhe de tarefa)

Documento de referência para replicar o padrão das páginas **detalhe da tarefa** em HTML estático (mesmo layout visual e blocos semânticos).

**Ficheiros de referência no projeto**

| Ficheiro | Notas |
|----------|--------|
| `conciliacao-financeira-detalhe.html` | Tabs em «Dados necessários», pills com `data-tabs` + JS de filtro; toggle opcional em «Principais dores» ↔ pills |
| `conciliacao-bancaria-detalhe.html` | Variante de «Dados necessários» (matriz tipo produto ou blocos OFX/ERP); acordeão de dores |
| `fechamento-de-caixa-detalhe.html` | Estrutura semelhante à financeira |
| `dre-detalhe.html` | Secção «Passo a passo» em tabela; «Dados necessários» em dois grupos de pills |

Ligação a partir do resumo: `gestao-financeira-nuvempago-2026.html` → lista `.detail-item` com `href` para cada `*-detalhe.html`.

---

## 1. Esqueleto da página (`<body>`)

Ordem fixa recomendada:

```
header.app-header
  a.header-pill [Voltar → gestao-financeira-nuvempago-2026.html]
  p.header-context  "Detalhe da tarefa"
  div.header-actions
    a.header-pill  âncoras internas (#principais-dores, #conclusao) e/ou outras páginas

div.page
  main.main
    [1] Hero
        p.eyebrow              (nível: operacional / estratégico / registo)
        h1.title-hero          (nome da tarefa)

    [2] section.section-block  "O que é?"
        div
          h2.section-title
          p.section-body (um ou mais)
        div (overflow-x auto)
          table.data-table       (Atividade | O que responde? | Foco principal)

    [3] section.section-block#dados-necessarios-section  (opcional / variável)
        h2.section-title
        p.section-body
        [opcional] div.segmented[role=tablist] + botões role=tab data-tab="..."
        div.dados-necessarios-wrap
          subsecções + h3.subsection-title + div.pill-row + span.pill...

    [4] section.section-block  "Jornada macro" ou "Passo a passo"
        h2.section-title
        p.section-body (opcional)
        div.journey
          article.journey-card × N
          svg.journey-arrow (entre cartões)

    [5] section.section-block#principais-dores
        h2.section-title
        p.section-body (opcional)
        div.pain-stack
          section × N
            button.pain-header (acordeão)
            div.pain-panel[role=region]
              div.pain-grid
                div.pain-card
                  p / p.small
        [opcional] div.section-block#conclusao (pode ficar dentro deste section)

script(s) no final do body
```

---

## 2. Cabeçalho (`header.app-header`)

- **Voltar:** `a.header-pill` com `href="gestao-financeira-nuvempago-2026.html"` e `aria-label="Voltar ao resumo"`.
- **Contexto:** `p.header-context` — texto curto centrado (ex.: «Detalhe da tarefa»).
- **Ações:** `div.header-actions` com `a.header-pill` para saltos `#principais-dores`, `#conclusao` ou links cruzados entre tarefas (opcional).

---

## 3. Hero

| Elemento | Classe | Conteúdo típico |
|----------|--------|------------------|
| Linha de contexto | `eyebrow` | Nível na hierarquia (ex.: Nível operacional) |
| Título | `title-hero` | Nome da tarefa (gradiente no texto) |

---

## 4. Bloco «O que é?»

- `h2.section-title` — pode usar `<span class="light">` na primeira palavra (ex.: «O **que** é?»).
- `p.section-body` — tipografia clara; usar `<strong>` para ênfase.
- `table.data-table` — 3 colunas habituais: **Atividade** | **O que responde?** | **Foco principal** (ou **Foco / cadência**).

---

## 5. «Dados necessários» (`#dados-necessarios-section`)

Padrões usados:

1. **Só texto + pills** — sem tabs (`dre-detalhe`, variantes simples).
2. **Tabs** — `div.segmented[role="tablist"]` com `button[role="tab"][data-tab="todos|produto|..."]`; classe `active` + `aria-selected` no tab ativo.
3. **Pills** — `span.pill.pill--success` ou `pill--neutral`; para filtro por tab, classe extra `js-dados-pill` e atributo `data-tabs="palavra1 palavra2"` (lista de `data-tab` onde o pill aparece).
4. **Regra CSS** — `.pill[hidden] { display: none !important; }` (o atributo `hidden` nos pills incompatíveis com o tab).

Blocos consolidados opcionais: `#dados-consolidados-block` com `hidden` quando o modo é «Exportável Orders» (exemplo em `conciliacao-financeira-detalhe.html`).

---

## 6. Jornada

- `div.journey` — flex, wrap.
- `article.journey-card` — `journey-card__step`, `journey-card__title`, `journey-card__desc`.
- `svg.journey-arrow` entre cartões (escondido em mobile com media query).

Alternativa: **tabela** `data-table` com passos em linhas (como em `dre-detalhe.html`).

---

## 7. Principais dores (`#principais-dores`)

- Cada acordeão: `button.pain-header` com `aria-expanded`, `aria-controls` → `id` do painel.
- Painel: `div.pain-panel[role="region"][aria-labelledby]`; usar `hidden` quando fechado.
- Conteúdo: `div.pain-grid` → `div.pain-card` → `p` / `p.small`.
- Ícones: círculo + exclamação no cabeçalho; chevron que roda com `[aria-expanded="false"]`.

**Conclusão:** bloco `div.section-block#conclusao` (muitas vezes **dentro** de `#principais-dores`, após `pain-stack`) para o `a.header-pill[href="#conclusao"]` funcionar.

---

## 8. JavaScript habitual

1. **Acordeão das dores** — `querySelectorAll('#principais-dores button.pain-header')`, alternar `hidden` no painel e `aria-expanded`.
2. **Tabs em Dados necessários** — ler `data-tab` do botão; mostrar/ocultar `.js-dados-pill` conforme `data-tabs`; opcionalmente `syncTogglePillAria` se existir toggle que esconde pills específicos (`pill-valor-liquido`, etc.).

---

## 9. Tokens CSS (`:root`)

Reutilizar o mesmo conjunto de variáveis nas telas para consistência:

- Fundo: `--bg-radial-inner`, `--bg-radial-mid`, `--bg-radial-outer`
- Interação: `--primary-interactive`, `--accent-blue`, `--primary-surface`
- Texto: `--text-muted`, `--text-card-muted`, `--white`
- Tabelas/cartões: `--border-subtle`, `--header-bg`, `--card-bg-diagram`
- Pills: `--success-*`, `--neutral-pill-*`
- Dores: `--pain-header-*`, `--pain-title`, `--pain-card-*`
- Tabs: `--segment-bg`, `--segment-active-bg`

Fontes: **Inter** + **Plus Jakarta Sans** (título hero), via Google Fonts no `<head>`.

---

## 10. Checklist — nova tela `nome-tarefa-detalhe.html`

- [ ] `<title>` e `h1.title-hero` coerentes
- [ ] Link «Voltar» para `gestao-financeira-nuvempago-2026.html`
- [ ] Âncoras `#principais-dores` e `#conclusao` existem no DOM
- [ ] Tabela resumo com uma linha mínima por tarefa
- [ ] `id="dados-necessarios-section"` se houver bloco homónimo
- [ ] Acordeão: `aria-*` consistentes; primeiro painel aberto ou fechado conforme desenho
- [ ] Atualizar `gestao-financeira-nuvempago-2026.html` (ou índice) com `href` para o novo ficheiro
- [ ] Testar tabs/pills se existirem (modo «Todos» e cada tab)

---

## 11. Nome dos ficheiros

Padrão: **`<tema>-detalhe.html`**, em minúsculas, hífen, sem espaços.

---

*Gerado para o projeto «Gestão financeira - dados necessários». Podes guardar ou exportar este `.md` para PDF/Word a partir do editor.*
