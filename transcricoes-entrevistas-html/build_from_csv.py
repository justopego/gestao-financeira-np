#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera HTML por entrevista com secções 1–6 a partir de resumos curados.
A transcrição integral fica no Dovetail (vídeo + texto); cada entrevista
referencia o cartão de dados correspondente.
"""
from __future__ import annotations

import html
import re
import unicodedata
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
# CSVs (existência usada só para validar que a entrevista tem ficheiro local alinhado)
CSV_ROOT = Path("/Users/anapego/Documents/IA/Gestão financeira")
# Cartões no Dovetail (projeto Gestão financeira) — vídeo e transcrição.
DOVETAIL_DATA_BASE = "https://helpful-wolverine-3h5n.dovetail.com/data"
# Pasta partilhada com gravações em vídeo das entrevistas.
INTERVIEW_VIDEOS_DRIVE_FOLDER = (
    "https://drive.google.com/drive/folders/18aNTuXVOq37rAxQnoOeDpE5LBXDA-6wY?usp=drive_link"
)
INTERVIEWS: list[dict] = [
    {
        "slug": "bpo-ana",
        "interviewee": "Ana",
        "store": "BPO — financeira de clientes Nuvem Pago",
        "title": "Ana — BPO — financeira de clientes Nuvem Pago",
        "csv": CSV_ROOT / "BPO- Ana.csv",
        "dovetail_data_id": "1q6irf90zrivOAATfVu7tx",
        "tasks": [
            "Conciliação financeira dos recebimentos do cliente (para DFC — fluxo de caixa).",
            "Elaboração da DRE / “ADRE” (demonstração de resultados) mês a mês em regime de competência.",
            "Conciliação entre o que está na Nuvem (pedidos) e o que foi importado no ERP do cliente.",
            "Cadastro no sistema das taxas acordadas com o meio de pagamento e conferência com extratos de recebimento.",
            "Conciliação bancária: entrar no banco do cliente (dados de ontem), classificar movimentos (incl. PIX) e lançar para conciliar.",
            "Identificar tarifas/taxas cobradas incorretamente ou divergentes do acordado.",
        ],
        "fluxo": [
            "Mensalmente: montar a DRE de competência.",
            "Na DFC: conciliar todos os recebimentos — a conciliação financeira mostra se valores batem com vendas e se há cobrança indevida.",
            "Conciliar pedidos Nuvem com importação no ERP; dar baixa em pedidos quando necessário para a conciliação fechar.",
            "Cadastrar taxas combinadas no sistema; comparar extrato de recebimento da Nuvem Pago com o cadastrado — se diferir, investigar se a taxa foi errada ou o sistema não aplicou a configuração.",
            "Diariamente (rotina citada): acessar o banco do cliente com data de ontem, tratar PIX e demais movimentos, classificar e lançar no sistema para conciliação.",
            "Exemplo comparativo citado: PayPal oferecia relatório diário com líquido e taxas; usar como referência de boa prática.",
        ],
        "dificuldades": [
            "Dificuldade em obter informações suficientes diretamente na Nuvem Pago; dependência de relatórios enviados pelo gerente (Paulo).",
            "Cliente sem conciliação adequada não percebe aumento de taxas ou cobrança incorreta.",
            "ERP que não conciliava recebimentos automaticamente gerou descontrole e clientes pedindo estorno.",
            "Parcelas/baixas exigem entrar no ERP (ex.: Tiny) e trabalho manual; necessidade de planilha Excel/OFX em alguns fluxos.",
            "Quando taxas estão erradas no cadastro, conciliação “automática” do ERP pode mascarar o problema até gerar estorno manual.",
        ],
        "dados": [
            "Relatórios de recebimento / extratos Nuvem Pago.",
            "Pedidos na Nuvem e registros importados no ERP.",
            "Taxas acordadas cadastradas vs taxas efetivamente descontadas.",
            "Extrato bancário do cliente (movimentação diária, inclusive PIX).",
            "Relatórios de parcelas com baixas.",
        ],
        "frequencia": [
            "DRE: mês a mês.",
            "Conciliação bancária no banco do cliente: todos os dias (citado explicitamente).",
            "Demais conciliações: conforme ciclo do cliente e fechamento; menção a clientes com conciliação bancária diária.",
        ],
        "ferramentas": [
            "Nuvem Pago / relatórios fornecidos pelo gerente da conta.",
            "ERP dos clientes (ex.: Tiny mencionado).",
            "Sistemas de contabilidade/gestão onde cadastra taxas e lança movimentos.",
            "Excel / planilhas; OFX citado como formato.",
            "Banco do cliente (acesso para conciliação).",
            "PayPal citado como referência de relatório diário (não necessariamente ferramenta atual).",
        ],
    },
    {
        "slug": "denis",
        "interviewee": "Denis",
        "store": "Wishin",
        "title": "Denis — Wishin",
        "csv": CSV_ROOT / "Denis.csv",
        "dovetail_data_id": "anIGioNw4MjsrFzJAGngN",
        "tasks": [
            "Transferir valores do Nuvem Pago para o banco de operação da empresa.",
            "Apurar recebimentos de cartão — resumo de quais operações geraram o crédito.",
            "Após receber: pagamentos conforme fluxo de caixa; eventual aplicação financeira (Denis) quando há menos contas a pagar.",
            "Construir previsão de recebíveis: entender escalonamento de contas a receber futuro a partir das vendas.",
            "Relatório diário de conciliação: comparar o disponível na plataforma com o que entrou, taxas, estornos e saldo final do dia.",
            "Solicitar relatório de vendas e relatório de fluxo de pagamento (período) ao suporte; confrontar com controle “a olho nu” em Excel.",
            "Conferir transferências e saídas (estornos, etc.).",
        ],
        "fluxo": [
            "Venda aprovada gera contas a receber futuro; precisam da composição/escalonamento para previsão a receber — pedem relatório de contas a receber futuro.",
            "PIX: quando aprovado já fica liberado; demais meios aguardam liberação.",
            "Diariamente (relatório citado): tudo que entrou no dia; retiradas de taxas e estornos; saldo final.",
            "Solicitam relatório de vendas; montam controle próprio e pedem à Nuvem demonstrativo de entradas para conciliar resultados.",
            "Depara entre saldo inicial e futuro; batem saldo disponível na plataforma com planilha de entradas/saídas.",
            "Transferências: conferência das transferências realizadas.",
        ],
        "dificuldades": [
            "Envio de informações por Excel/planilha dificulta processo ideal diário.",
            "Ideal seria diário por causa de movimentação e compensação; na prática parte do depara é semanal.",
            "Prazo: às vezes precisam do relatório até o último dia do mês.",
            "Necessidade de relatório robusto de contas a receber futuro na plataforma.",
        ],
        "dados": [
            "Saldo disponível e movimentação na plataforma Nuvem.",
            "Entradas, taxas, estornos, saldo final do dia.",
            "Relatórios de vendas e fluxo de pagamento enviados pelo suporte.",
            "Comparativo com planilha Excel própria.",
        ],
        "frequencia": [
            "Relatório de fechamento diário (comparativo disponível vs taxas/estornos/saldo): feito todos os dias (participante 3).",
            "Depara diário mencionado pelo entrevistador: na prática feito semanalmente pela mesma pessoa.",
            "Relatórios do suporte: semanal ou mensal (contexto da conversa).",
            "Ideal citado pelo time: processo diário.",
        ],
        "ferramentas": [
            "Plataforma Nuvem (Nuvem Pago).",
            "Excel / planilhas.",
            "Relatórios enviados pelo time de suporte.",
            "Banco de operação (transferências).",
        ],
    },
    {
        "slug": "fabricio-nayara",
        "interviewee": "Fabrício / Nayara",
        "store": "Mulher Elástica",
        "title": "Fabrício / Nayara — Mulher Elástica",
        "csv": CSV_ROOT / "Fabricio.csv",
        "dovetail_data_id": "5kwSgJxj5PjYFmS7jjp2Bb",
        "tasks": [
            "Trabalhar o relatório recebido via Drive (atualizado pela equipe de suporte — Juliana).",
            "No Excel: separar PIX, cartão de débito e cartão de crédito; consolidar em planilha única de fluxo de caixa.",
            "Programar fluxo de caixa com base nos recebimentos futuros.",
            "Conferir se as taxas contratadas batem com o cobrado (identificar cobranças indebidas mensalmente).",
            "Manipular relatório linha a linha (ex.: somar vendas do dia) quando o arquivo lista muitas vendas empilhadas.",
        ],
        "fluxo": [
            "Recebem arquivo no Drive (atualização semanal).",
            "Nayara extrai para Excel, aplica filtros e, na prática, cria várias planilhas intermediárias para alimentar uma planilha única de fluxo.",
            "Fluxo de caixa do e-commerce não está no ERP — fica na planilha Excel.",
            "Verificação de taxas com fórmulas no Excel comparando ao contratado.",
        ],
        "dificuldades": [
            "Processo muito manual e “engessado”.",
            "Drive só mostra recebíveis até determinado mês (ex.: mês 7) enquanto há parcelamentos em até 6 vezes — não conseguem programar o fluxo além desse horizonte no relatório atual.",
            "Gostariam de separar meios de pagamento já dentro da plataforma em vez de filtrar tudo no Excel.",
            "Três ERPs diferentes (fábrica vs e-commerce); gestão financeira/estoque fragmentada.",
            "Relatório com dezenas de vendas em linhas exige seleção manual para totalizar por dia.",
        ],
        "dados": [
            "Dados do Drive semanal.",
            "Vendas por meio (PIX, débito, crédito).",
            "Taxas contratadas vs efetivas.",
            "Saldo disponível e saldo futuro (discutidos na entrevista).",
        ],
        "frequencia": [
            "Atualização do Drive: semanal (equipe disponibiliza).",
            "Conferência de taxas: todo mês (cobranças indebidas citadas como recorrentes).",
        ],
        "ferramentas": [
            "Google Drive (planilha/arquivo atualizado pela Juliana/suporte).",
            "Microsoft Excel.",
            "Três ERPs (contexto operacional da empresa).",
            "Painel Nuvem Pago (desejado para mais visibilidade + download de relatórios).",
        ],
    },
    {
        "slug": "flor-de-cacto",
        "interviewee": "Regina",
        "store": "Flor de Cacto",
        "title": "Regina — Flor de Cacto",
        "csv": CSV_ROOT / "Flor de cacto.csv",
        "dovetail_data_id": "6rXQo1KwXYz0iuYwzKi8hw",
        "tasks": [
            "Fazer conferência financeira no Nuvem Pago (formato diferente do banco tradicional — sem extrato simples).",
            "Usar painel de vendas: filtrar tudo que vendeu no dia; conferir numeração sequencial dos pedidos.",
            "Aplicar regras de recebimento: vendas ‘do dia’ vs vendas após cut-off (ex.: após ~21h caem no dia seguinte); PIX fim de semana recebe na segunda.",
            "Cartão com antecipação em dois dias: projetar recebimento (ex.: venda quarta → sexta) e conferir saldo disponível de manhã.",
            "Transferir saldo zerando disponível e validar que novos PIX e liquidações D+2 compõem o saldo exibido.",
        ],
        "fluxo": [
            "Primeiro: painel de vendas do dia — confere intervalo de números de pedido (sequencial, sem ‘pular’).",
            "Regra: tudo vendido no ‘dia fixo’ deveria receber no dia; exceção: vendas tardias (ex. 20h59) relatadas como recebimento no dia seguinte (validado com time Nuvem).",
            "Cartão: antecipação D+2; liberação do montante costuma ocorrer de madrugada (~4h citado como referência interna).",
            "Manhã: conferência do que recebeu em data X; compõe saldo disponível com PIX do dia anterior + liquidações de cartão de D-2.",
            "Regina sendo treinada para assumir os controles.",
        ],
        "dificuldades": [
            "Nuvem Pago não é domicílio bancário — conferência menos trivial que extrato tradicional.",
            "Informações no painel/relatórios mudam ou parecem inconsistentes (horários, parâmetros).",
            "Alto volume de vendas com valores similares dificultava bater saldo quando o painel não detalhava quais vendas compunham o recebimento.",
            "Dependência de solicitação de relatórios à Nuvem para chegar a consenso na conferência.",
        ],
        "dados": [
            "Pedidos do dia (números sequenciais, horários, valores).",
            "Relatórios de recebimento e saldo disponível.",
            "Regras de antecipação cartão e comportamento PIX.",
        ],
        "frequencia": [
            "Conferência matinal do saldo/recebimentos (rotina descrita em detalhe).",
            "Transferências quando necessário (ex.: zerar saldo às 10h40 e acompanhar recomposição).",
        ],
        "ferramentas": [
            "Painel de vendas Nuvemshop.",
            "Nuvem Pago (saldo disponível, relatórios).",
            "Comparação mental/processo com prática de banco tradicional (extrato).",
        ],
    },
    {
        "slug": "gabriel",
        "interviewee": "Gabriel",
        "store": "Cidus",
        "title": "Gabriel — Cidus",
        "csv": CSV_ROOT / "Gabriel.csv",
        "dovetail_data_id": "7jUMRf6M2U4mq6vek04VAl",
        "tasks": [
            "Após saldo livre no Nuvem Pago: Iuri transfere para a conta bancária da empresa (padrão fixo).",
            "Administrar lançamentos contábeis/financeiros — hoje processo manual.",
            "Conciliar vendas com taxas de meio de pagamento: Nuvemshop envia venda para o Bling (ERP) mas não envia as taxas do meio de pagamento.",
        ],
        "fluxo": [
            "Venda → período de recebimento → saldo disponível no Nuvem Pago → transferência automática para conta bancária.",
            "Lançamentos: feitos manualmente porque integração não traz taxas (testado com Nuvem Pago e outro meio de pagamento citado).",
        ],
        "dificuldades": [
            "Integração Nuvemshop → Bling manda venda mas não taxas do meio de pagamento.",
            "Configuração de aliases etc. não resolve envio das taxas ao ERP.",
        ],
        "dados": [
            "Vendas na Nuvemshop.",
            "Taxas do meio de pagamento (têm de ser obtidas fora do fluxo automático para o ERP).",
        ],
        "frequencia": [
            "Transferência: sempre que há saldo a movimentar (padrão descrito como rotina fixa da equipe).",
            "Frequência exata dos lançamentos manuais: não quantificada na abertura da transcrição lida.",
        ],
        "ferramentas": [
            "Nuvem Pago.",
            "Nuvemshop.",
            "Bling (ERP).",
            "Conta bancária da empresa.",
        ],
    },
    {
        "slug": "maria-laura",
        "interviewee": "Maria Laura",
        "store": "Mais Mu",
        "title": "Maria Laura — Mais Mu",
        "csv": CSV_ROOT / "MAria laura.csv",
        "dovetail_data_id": "3Gav10MPA948accI2Kwioy",
        "tasks": [
            "Acompanhar eventualmente chargebacks (e-mail quando ocorrem).",
            "Antes na plataforma anterior: gestão de chargebacks com visão de status e resultado da disputa.",
            "Com Nuvem Pago: enviar contestação via formulário; acompanhar resultados indiretamente via planilha compartilhada pela equipe.",
            "Pedir visão de parcelamento por meio de pagamento (% PIX, cartão, parcelas) ao Rodrigo.",
        ],
        "fluxo": [
            "Chargeback: recebe e-mail → preenche forms de contestação → esperava confirmação por e-mail (nunca recebeu) → resultado da disputa não chega por canal oficial.",
            "Time compartilha planilha com chargebacks, valores e resultados.",
        ],
        "dificuldades": [
            "Perda de visibilidade vs gestão integrada na plataforma anterior (Mercado Pago citado como ter ganho algumas disputas).",
            "Formulário sem confirmação de recebimento nem retorno formal do desfecho.",
            "Impressão de perder mais disputas hoje (com ressalva de evento pontual de ‘ataque’ com muitos chargebacks no ano passado).",
        ],
        "dados": [
            "E-mails de chargeback.",
            "Planilha interna compartilhada pelo time.",
            "Breakdown de meios de pagamento (via Rodrigo).",
        ],
        "frequencia": [
            "Rotina de ‘olhar pagamentos’: não fixa — aproximadamente a cada 15 dias ou uma vez por mês.",
            "Conciliações e download de relatórios: feitas pelo time de financeiro (Maria foca mais no negócio).",
            "Chargebacks: eventuais.",
        ],
        "ferramentas": [
            "E-mail.",
            "Formulário Nuvem Pago (contestação).",
            "Planilha (time interno).",
            "Mercado Pago (referência ao período anterior).",
        ],
    },
    {
        "slug": "thales",
        "interviewee": "Thales",
        "store": "Loja Reforma",
        "title": "Thales — Loja Reforma",
        "csv": CSV_ROOT / "Thales.csv",
        "dovetail_data_id": "1iq4PmBvTXQvvJzA7uqxHB",
        "tasks": [
            "Acompanhar métricas simples: faturamento do dia, devoluções do dia (de preferência separadas).",
            "Conciliação de taxas e fechamento mensal (alinhar vendas com notas e valores).",
            "Verificar se saldo disponível confere com o esperado após taxas, devoluções, chargebacks retidos, saques e créditos de defesa.",
        ],
        "fluxo": [
            "Referência PayPal: período de fechamento mostrava dia, data, valor faturado, taxa, devolução, reembolso de taxa, saques, saldo retido por chargeback, outras entradas (ex.: crédito após defesa).",
            "Na Nuvem: crédito de confiança / valores retidos que depois aparecem como entrada — clicar para ver transação de origem.",
            "Usar essa visão para fechar mês e validar saldo.",
        ],
        "dificuldades": [
            "Quer acesso rápido às informações; sente falta de transparência/simplicidade comparada ao PayPal citado.",
        ],
        "dados": [
            "Faturamento e devoluções diárias.",
            "Taxas, saldo disponível, retidos, estornos, saques.",
        ],
        "frequencia": [
            "Conciliação de taxa: às vezes uma vez por mês (próximo ao fechamento mensal); equipe crescendo para revisar diariamente.",
        ],
        "ferramentas": [
            "Nuvem Pago.",
            "PayPal citado como benchmark de extrato detalhado.",
        ],
    },
]

def slugify_pt(text: str) -> str:
    """Identificador URL estável (minúsculas, hífens), sem acentos."""
    s = unicodedata.normalize("NFD", text.strip())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def task_card_glossary_fragment(label: str, is_acronym: bool) -> str:
    frag = label.strip().lower() if is_acronym else slugify_pt(label)
    return html.escape(frag, quote=True)


def gloss_top_bar_link_html(*, on_glossary_page: bool = False) -> str:
    """Link para o glossário na top-bar (dentro de .wrap), à direita."""
    current = ' aria-current="page"' if on_glossary_page else ""
    return f"<a href=\"glossario.html\"{current}>Glossário</a>"


def theme_head_fragment() -> str:
    """Mesmo sistema visual que apresentacao-gestao-financeira-q2-2026.html (tema Nimbus / cosmic glass)."""
    return r"""
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    :root {
      --bg: #000B19;
      --bg-glass: rgba(255, 255, 255, 0.04);
      --border-glass: rgba(255, 255, 255, 0.08);
      --blue-300: #60A5FA;
      --blue-400: #3B82F6;
      --blue-500: #0050C3;
      --gradient: linear-gradient(135deg, #60A5FA, #3B82F6, #0050C3);
      --text-1: #FFFFFF;
      --text-2: #8FA8C8;
      --text-3: #6B83A8;
      --font: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      --ease: cubic-bezier(0.16, 1, 0.3, 1);
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: var(--font);
      background-color: var(--bg);
      color: var(--text-1);
      min-height: 100%;
      overflow-x: hidden;
      -webkit-font-smoothing: antialiased;
    }
    body::before {
      content: "";
      position: fixed;
      inset: 0;
      background-image:
        radial-gradient(ellipse 80% 60% at 50% 40%, rgba(0, 80, 195, 0.18), transparent 60%),
        radial-gradient(ellipse 70% 50% at 80% 20%, rgba(0, 41, 143, 0.14), transparent 55%),
        radial-gradient(ellipse 60% 50% at 20% 80%, rgba(4, 23, 115, 0.12), transparent 50%);
      pointer-events: none;
      z-index: 0;
    }
    .top-bar {
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding: 0.75rem 0 1rem;
      margin-bottom: 0.5rem;
      background: linear-gradient(to bottom, rgba(0, 11, 25, 0.95) 60%, transparent);
      flex-wrap: wrap;
    }
    .nav-group {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem;
    }
    .top-bar a {
      font-size: 0.75rem;
      color: var(--blue-300);
      text-decoration: none;
      border: 1px solid var(--border-glass);
      padding: 0.35rem 0.85rem;
      border-radius: 999px;
      background: var(--bg-glass);
      transition: background 0.2s, border-color 0.2s;
    }
    .top-bar a:hover, .top-bar a:focus {
      background: rgba(255,255,255,0.08);
      border-color: rgba(96, 165, 250, 0.35);
      outline: none;
    }
    .top-bar a[aria-current="page"] {
      border-color: rgba(96, 165, 250, 0.5);
      background: rgba(0, 80, 195, 0.22);
    }
    .wrap {
      position: relative;
      z-index: 1;
      max-width: 52rem;
      margin: 0 auto;
      padding: 0 1.25rem 4rem;
    }
    .kicker {
      font-size: 0.6875rem;
      font-weight: 600;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: var(--text-3);
      margin-bottom: 0.75rem;
    }
    h1 {
      font-size: clamp(1.5rem, 4vw, 2.35rem);
      font-weight: 700;
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 0.75rem;
    }
    h1 .gradient {
      background: var(--gradient);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
      font-size: 32px;
    }
    .lead {
      font-size: 0.95rem;
      color: var(--text-2);
      line-height: 1.55;
      max-width: 42rem;
      margin-bottom: 0.5rem;
    }
    .src {
      font-size: 0.8125rem;
      color: var(--text-3);
      margin: 0.35rem 0;
      line-height: 1.45;
    }
    .src code {
      font-size: 0.78em;
      word-break: break-all;
    }
    main section.block {
      margin-top: 1.75rem;
      padding-top: 1.5rem;
      border-top: 1px solid var(--border-glass);
    }
    main > section.block:first-of-type {
      border-top: none;
      padding-top: 0.35rem;
      margin-top: 1rem;
    }
    body.page-glossary header h1 {
      margin-bottom: 1.5rem;
    }
    body.page-glossary main > section.block:first-of-type {
      border-top: none;
      padding-top: 0;
      margin-top: 3rem;
    }
    .correlation-block > h2 {
      margin-bottom: 4.25rem;
    }
    .correlation-block h3 {
      font-size: 20px;
      font-weight: 600;
      color: var(--text-1);
      margin: 1.35rem 0 0.65rem;
      letter-spacing: -0.02em;
    }
    .correlation-block h3:first-of-type { margin-top: 0; }
    .correlation-block h4 {
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--blue-300);
      margin: 1rem 0 0.4rem;
    }
    .correlation-block p.corr-body {
      color: var(--text-2);
      font-size: 14px;
      line-height: 1.6;
      margin: 0 0 0.75rem;
      max-width: 48rem;
    }
    .correlation-block ul.corr-list {
      margin: 0 0 1rem;
      padding-left: 1.2rem;
      color: var(--text-2);
      font-size: 0.95rem;
      line-height: 1.55;
      max-width: 48rem;
    }
    .correlation-block ul.corr-list li { margin: 0.4rem 0; }
    .correlation-block .corr-cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(15rem, 1fr));
      gap: 0.85rem;
      margin: 0 0 1rem;
      padding: 0;
      list-style: none;
      max-width: none;
    }
    .correlation-block a.corr-card {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      min-height: 7rem;
      padding: 1rem 1.15rem;
      background: var(--bg-glass);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--border-glass);
      border-radius: 14px;
      border-left: 3px solid var(--blue-500);
      text-decoration: none;
      color: inherit;
      transition: background 0.2s, border-color 0.2s var(--ease);
    }
    .correlation-block a.corr-card:hover,
    .correlation-block a.corr-card:focus {
      background: rgba(255, 255, 255, 0.07);
      border-color: rgba(96, 165, 250, 0.38);
      outline: none;
    }
    .correlation-block a.corr-card--full {
      grid-column: 1 / -1;
    }
    .correlation-block a.corr-card[id] {
      scroll-margin-top: 5.5rem;
    }
    .correlation-block .corr-card-title {
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--blue-300);
      letter-spacing: -0.02em;
      line-height: 1.3;
    }
    .correlation-block .corr-card-text {
      font-family: "SF Compact Display", sans-serif;
      font-size: 0.88rem;
      line-height: 1.55;
      color: var(--text-2);
      margin: 0;
    }
    .correlation-block .corr-card ul.corr-card-bullets {
      margin: 0.5rem 0 0;
      padding-left: 1.1rem;
      color: var(--text-2);
      font-size: 0.88rem;
      line-height: 1.55;
      list-style: disc;
    }
    .correlation-block .corr-card ul.corr-card-bullets li { margin: 0.35rem 0; }
    .correlation-block ol.corr-ol {
      margin: 0 0 1rem;
      padding-left: 1.2rem;
      color: var(--text-2);
      font-size: 0.95rem;
      line-height: 1.55;
      max-width: 48rem;
    }
    .correlation-block ol.corr-ol li { margin: 0.45rem 0; }
    .correlation-block .corr-hierarchy {
      margin: 1rem 0 1.35rem;
      max-width: 42rem;
    }
    .correlation-block .corr-hierarchy__caption {
      font-size: 0.75rem;
      color: var(--text-3);
      margin: 0 0 0.85rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      font-weight: 600;
    }
    .correlation-block .corr-h-stack {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 0;
    }
    .correlation-block .corr-h-tier {
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      align-items: stretch;
      gap: 0.65rem;
      width: 100%;
    }
    .correlation-block .corr-h-tier--top { max-width: 22rem; }
    .correlation-block .corr-h-tier--mid { max-width: 20rem; }
    .correlation-block .corr-h-tier--base { max-width: 100%; }
    .correlation-block .corr-h-vline {
      width: 2px;
      height: 1.1rem;
      background: linear-gradient(180deg, var(--blue-500), rgba(0, 80, 195, 0.25));
      border-radius: 1px;
      flex-shrink: 0;
      box-shadow: 0 0 12px rgba(0, 80, 195, 0.35);
    }
    .correlation-block .corr-h-node {
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
      padding: 0.75rem 1rem;
      background: var(--bg-glass);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid var(--border-glass);
      border-radius: 12px;
      text-decoration: none;
      color: inherit;
      transition: background 0.2s var(--ease), border-color 0.2s var(--ease), transform 0.2s var(--ease);
      flex: 1 1 auto;
      min-width: min(100%, 9.5rem);
      text-align: center;
    }
    .correlation-block a.corr-h-node:hover,
    .correlation-block a.corr-h-node:focus {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(96, 165, 250, 0.4);
      outline: none;
      transform: translateY(-1px);
    }
    .correlation-block .corr-h-node--top {
      box-shadow: inset 0 3px 0 0 var(--blue-400);
      padding-top: 0.85rem;
    }
    .correlation-block .corr-h-node--mid { border-left: 3px solid var(--blue-400); }
    .correlation-block .corr-h-node--base {
      border-bottom: 3px solid rgba(0, 80, 195, 0.45);
    }
    .correlation-block .corr-h-label {
      font-size: 0.625rem;
      font-weight: 700;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: var(--blue-300);
    }
    .correlation-block .corr-h-title {
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-1);
      line-height: 1.25;
    }
    .correlation-block .corr-h-note {
      font-size: 0.72rem;
      line-height: 1.4;
      color: var(--text-3);
    }
    .correlation-block .corr-h-pair {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      justify-content: center;
      width: 100%;
    }
    .correlation-block .corr-h-pair .corr-h-node {
      min-width: min(100%, 8.5rem);
      flex: 1 1 calc(50% - 0.5rem);
      max-width: 11rem;
    }
    @media (min-width: 36rem) {
      .correlation-block .corr-h-tier--base .corr-h-node {
        flex: 1 1 0;
        min-width: 7.5rem;
        max-width: 12rem;
      }
    }
    .correlation-block .corr-divider {
      height: 1px;
      background: var(--border-glass);
      margin: 3.75rem 0;
      max-width: 48rem;
    }
    .correlation-block table.corr-table {
      width: 100%;
      max-width: 48rem;
      border-collapse: collapse;
      font-size: 0.88rem;
      margin-top: 0.75rem;
    }
    .correlation-block table.corr-table th,
    .correlation-block table.corr-table td {
      border: 1px solid var(--border-glass);
      padding: 0.55rem 0.65rem;
      text-align: left;
      vertical-align: top;
    }
    .correlation-block table.corr-table th {
      background: rgba(255,255,255,0.05);
      color: var(--text-1);
      font-weight: 600;
    }
    .correlation-block table.corr-table td { color: var(--text-2); }
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    main h2 {
      font-size: clamp(1.1rem, 2.5vw, 1.45rem);
      font-weight: 600;
      margin-bottom: 0.85rem;
      color: var(--text-1);
    }
    main h2 .num {
      color: var(--blue-400);
      font-weight: 700;
      margin-right: 0.35rem;
    }
    ul {
      margin: 0;
      padding-left: 1.15rem;
      color: var(--text-2);
      max-width: 48rem;
    }
    li { margin: 0.45rem 0; line-height: 1.55; font-family: "SF Compact Display", sans-serif; }
    .task-cards {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(10.75rem, 1fr));
      gap: 0.85rem;
      margin: 0.35rem 0 0;
      padding: 0;
      max-width: none;
    }
    a.task-card {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 4.25rem;
      padding: 0.85rem 1rem;
      background: var(--bg-glass);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--border-glass);
      border-radius: 14px;
      border-left: 3px solid var(--blue-500);
      text-decoration: none;
      color: var(--text-1);
      font-weight: 600;
      font-size: 0.88rem;
      line-height: 1.35;
      text-align: center;
      transition: background 0.2s, border-color 0.2s var(--ease);
    }
    a.task-card:hover, a.task-card:focus {
      background: rgba(255, 255, 255, 0.07);
      border-color: rgba(96, 165, 250, 0.38);
      outline: none;
    }
    a.task-card .task-card-label {
      letter-spacing: -0.02em;
    }
    a.task-card .task-card-label.acronym {
      background: var(--gradient);
      -webkit-background-clip: text;
      background-clip: text;
      color: transparent;
    }
    .card {
      margin-top: 1rem;
      padding: 1rem 1.25rem;
      background: var(--bg-glass);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid var(--border-glass);
      border-radius: 16px;
      border-left: 3px solid var(--blue-500);
    }
    .card p { color: var(--text-2); font-size: 0.9rem; line-height: 1.55; }
    .source-dovetail .src a {
      color: var(--blue-300);
      font-weight: 500;
      text-decoration: underline;
      text-underline-offset: 0.2em;
    }
    .source-dovetail .src a:hover, .source-dovetail .src a:focus {
      color: var(--blue-400);
      outline: none;
    }
    .source-dovetail .src + .src { margin-top: 0.5rem; }
    code {
      font-family: ui-monospace, monospace;
      font-size: 0.82em;
      background: rgba(255,255,255,0.06);
      padding: 0.12em 0.4em;
      border-radius: 6px;
      color: var(--blue-300);
    }
    .progress-foot {
      position: fixed;
      bottom: 0;
      left: 0;
      height: 3px;
      width: 100%;
      background: linear-gradient(90deg, var(--blue-500), var(--blue-300));
      opacity: 0.85;
      z-index: 100;
      pointer-events: none;
      box-shadow: 0 0 12px rgba(0, 80, 195, 0.45);
    }
    .index-list {
      list-style: none;
      padding: 0;
      margin: 1.25rem 0 0;
      max-width: none;
    }
    .index-list li {
      margin: 0;
      border-bottom: 1px solid var(--border-glass);
    }
    .index-list a {
      display: block;
      padding: 0.85rem 0;
      color: var(--text-1);
      text-decoration: none;
      font-weight: 500;
      font-size: 0.95rem;
      transition: color 0.2s, padding-left 0.2s var(--ease);
    }
    .index-list a:hover {
      color: var(--blue-300);
      padding-left: 0.35rem;
    }
    .index-list li span.sub {
      display: block;
      font-size: 0.78rem;
      font-weight: 400;
      color: var(--text-3);
      margin-top: 0.2rem;
    }
  </style>
"""


# Secção 1 (entrevistas): cards fixos alinhados ao glossário; substitui a lista antiga de tarefas.
TASK_SECTION_CARD_LABELS: list[tuple[str, bool]] = [
    ("Conciliação financeira", False),
    ("Conciliação bancária", False),
    ("Conciliação contábil", False),
    ("DRE", True),
    ("DFC", True),
]


def render_tasks_section_cards() -> str:
    cards: list[str] = []
    for label, is_acronym in TASK_SECTION_CARD_LABELS:
        esc = html.escape(label)
        frag = task_card_glossary_fragment(label, is_acronym)
        cls = "task-card-label acronym" if is_acronym else "task-card-label"
        cards.append(
            f'        <a class="task-card" role="listitem" href="glossario.html#{frag}">'
            f'<span class="{cls}">{esc}</span></a>'
        )
    cards_html = "\n".join(cards)
    return f"""    <section class="block">
      <h2>1. Tarefas relacionadas à gestão financeira</h2>
      <div class="task-cards" role="list">
{cards_html}
      </div>
    </section>"""


def render_section(title: str, items: list[str]) -> str:
    lis = "\n".join(f"        <li>{html.escape(x)}</li>" for x in items)
    return f"""    <section class="block">
      <h2>{html.escape(title)}</h2>
      <ul>
{lis}
      </ul>
    </section>"""


def render_glossary_correlation_section() -> str:
    # Conteúdo alinhado ao doc: https://docs.google.com/document/d/16u1Rw4nXbsjfC-9b0a3BCLof3-BIE2wJQdm9bSeqEdA/edit
    e = html.escape
    return f"""      <section class="block correlation-block">
        <h2>Correlação entre as tarefas</h2>

        <h3>{e("1. O nível operacional (as subtarefas de verificação)")}</h3>
        <p class="corr-body">{e(
            'Este é o "chão de fábrica". Essas atividades servem para garantir que a informação é real.'
        )}</p>
        <div class="corr-cards" role="list">
          <a id="fechamento-de-caixa" class="corr-card" role="listitem" href="glossario.html#fechamento-de-caixa">
            <span class="corr-card-title">{e("Fechamento de caixa")}</span>
            <span class="corr-card-text">{e(
                "O fechamento de caixa é a conferência diária de que as vendas feitas no site possuem um "
                "pagamento correspondente."
            )}</span>
          </a>
          <a id="conciliacao-financeira" class="corr-card" role="listitem" href="glossario.html#conciliacao-financeira">
            <span class="corr-card-title">{e("Conciliação financeira")}</span>
            <span class="corr-card-text">{e(
                "É a subtarefa vital do e-commerce. Ela cruza o que o site vendeu vs. o que o meio de pagamento/marketplace "
                "diz que vai pagar. Ela identifica se a taxa do cartão foi cobrada a mais ou se um chargeback ocorreu."
            )}</span>
          </a>
          <a id="conciliacao-bancaria" class="corr-card" role="listitem" href="glossario.html#conciliacao-bancaria">
            <span class="corr-card-title">{e("Conciliação bancária")}</span>
            <span class="corr-card-text">{e(
                "Confronta o que está no seu sistema financeiro com o seu extrato do banco. Serve para garantir que "
                "o dinheiro que o meio de pagamento disse que depositou realmente caiu na sua conta corrente."
            )}</span>
          </a>
        </div>
        <div class="corr-divider" aria-hidden="true"></div>

        <h3>{e("2. O nível de registro (fluxo de caixa)")}</h3>
        <p class="corr-body">{e("Aqui é onde o dia a dia é consolidado.")}</p>
        <div class="corr-cards" role="list">
          <a id="fluxo-de-caixa" class="corr-card corr-card--full" role="listitem" href="glossario.html#fluxo-de-caixa">
            <span class="corr-card-title">{e("Fluxo de caixa")}</span>
            <span class="corr-card-text">{e(
                "É o registro cronológico de todas as entradas e saídas. Ele bebe diretamente das conciliações."
            )}</span>
            <ul class="corr-card-bullets">
              <li><strong>{e("Relação:")}</strong> {e(
                  "Sem conciliação bancária, seu saldo de fluxo de caixa nunca bate com o banco."
              )}</li>
            </ul>
          </a>
        </div>
        <div class="corr-divider" aria-hidden="true"></div>

        <h3>{e("3. O nível estratégico (demonstrativos)")}</h3>
        <p class="corr-body">{e(
            "Aqui é onde você analisa se o negócio está saudável ou se vai quebrar nos próximos meses."
        )}</p>
        <div class="corr-cards" role="list">
          <a id="dre" class="corr-card corr-card--full" role="listitem" href="glossario.html#dre">
            <span class="corr-card-title">{e("DRE (Demonstração do Resultado do Exercício)")}</span>
            <ul class="corr-card-bullets">
              <li><strong>{e("Foco:")}</strong> {e("Lucro ou prejuízo (regime de competência).")}</li>
              <li><strong>{e("O que diz:")}</strong> {e(
                  '"Minha operação é economicamente viável?". Ela registra a venda no momento em que ela acontece. '
                  "Se você vendeu R$ 1.000,00 hoje em 10x, a DRE mostra R$ 1.000,00 hoje."
              )}</li>
            </ul>
          </a>
          <a id="dfc" class="corr-card corr-card--full" role="listitem" href="glossario.html#dfc">
            <span class="corr-card-title">{e("DFC (Demonstração dos Fluxos de Caixa)")}</span>
            <ul class="corr-card-bullets">
              <li><strong>{e("Foco:")}</strong> {e("Dinheiro no bolso (regime de caixa).")}</li>
              <li><strong>{e("O que diz:")}</strong> {e(
                  '"Para onde foi o meu dinheiro?". Diferente do fluxo de caixa comum, a DFC organiza as movimentações '
                  "em 3 grupos: operacional (vendas), investimento (compra de computadores/prateleiras) e "
                  "financiamento (empréstimos/aportes)."
              )}</li>
              <li><strong>{e("Relação com DRE:")}</strong> {e(
                  'A DFC "corrige" a DRE. Enquanto a DRE diz que você lucrou R$ 10.000,00, a DFC pode mostrar que seu '
                  "caixa diminuiu porque esse lucro ainda está parcelado no cartão de crédito dos clientes."
              )}</li>
            </ul>
          </a>
          <a id="conciliacao-contabil" class="corr-card corr-card--full" role="listitem" href="glossario.html#conciliacao-contabil">
            <span class="corr-card-title">{e("Conciliação contábil")}</span>
            <ul class="corr-card-bullets">
              <li><strong>{e("Função:")}</strong> {e(
                  'É o "juiz final". Ela cruza os dados do financeiro com as notas fiscais, impostos e estoque. '
                  "Ela garante que a DRE e o balanço patrimonial que o contador assina são juridicamente perfeitos."
              )}</li>
            </ul>
          </a>
        </div>
        <div class="corr-divider" aria-hidden="true"></div>

        <h3>{e("Resumo: hierarquia e dependência")}</h3>

        <figure class="corr-hierarchy">
          <p class="corr-hierarchy__caption">{e("Organograma · dependência entre níveis")}</p>
          <div class="corr-h-stack">
            <div class="corr-h-tier corr-h-tier--top" role="group" aria-label="{e('Nível topo — relatórios')}">
              <div class="corr-h-pair">
                <a class="corr-h-node corr-h-node--top" href="glossario.html#dre">
                  <span class="corr-h-label">{e("Topo")}</span>
                  <span class="corr-h-title">{e("DRE")}</span>
                  <span class="corr-h-note">{e("Resultado (competência)")}</span>
                </a>
                <a class="corr-h-node corr-h-node--top" href="glossario.html#dfc">
                  <span class="corr-h-label">{e("Topo")}</span>
                  <span class="corr-h-title">{e("DFC")}</span>
                  <span class="corr-h-note">{e("Fluxos formais (caixa)")}</span>
                </a>
              </div>
            </div>
            <div class="corr-h-vline" aria-hidden="true"></div>
            <div class="corr-h-tier corr-h-tier--mid" role="group" aria-label="{e('Nível meio — processo')}">
              <a class="corr-h-node corr-h-node--mid" href="glossario.html#fluxo-de-caixa">
                <span class="corr-h-label">{e("Meio")}</span>
                <span class="corr-h-title">{e("Fluxo de caixa")}</span>
                <span class="corr-h-note">{e("Organiza os dados validados na base")}</span>
              </a>
            </div>
            <div class="corr-h-vline" aria-hidden="true"></div>
            <div class="corr-h-tier corr-h-tier--base" role="group" aria-label="{e('Nível base — subtarefas')}">
              <a class="corr-h-node corr-h-node--base" href="glossario.html#fechamento-de-caixa">
                <span class="corr-h-label">{e("Base")}</span>
                <span class="corr-h-title">{e("Fechamento de caixa")}</span>
                <span class="corr-h-note">{e("Venda ↔ pagamento")}</span>
              </a>
              <a class="corr-h-node corr-h-node--base" href="glossario.html#conciliacao-financeira">
                <span class="corr-h-label">{e("Base")}</span>
                <span class="corr-h-title">{e("Conciliação financeira")}</span>
                <span class="corr-h-note">{e("Site vs meio de pagamento")}</span>
              </a>
              <a class="corr-h-node corr-h-node--base" href="glossario.html#conciliacao-bancaria">
                <span class="corr-h-label">{e("Base")}</span>
                <span class="corr-h-title">{e("Conciliação bancária")}</span>
                <span class="corr-h-note">{e("Sistema vs banco")}</span>
              </a>
            </div>
          </div>
          <figcaption class="sr-only">{e(
              "Do topo à base: DRE e DFC dependem do fluxo de caixa; o fluxo de caixa depende do fechamento de caixa, "
              "da conciliação financeira e da conciliação bancária."
          )}</figcaption>
        </figure>

        <ol class="corr-ol">
          <li>{e(
              "Base (subtarefas): fechamento de caixa + conciliação bancária + conciliação financeira. "
              "(Se falhar aqui, o resto desmorona.)"
          )}</li>
          <li>{e(
              "Meio (processo): fluxo de caixa. (Organiza os dados validados pela base.)"
          )}</li>
          <li>{e(
              "Topo (relatórios): DRE e DFC. (Usam os dados do meio para te dizer se você está rico ou se precisa de um empréstimo.)"
          )}</li>
        </ol>

        <h3>{e("Tabela de diferenças rápidas")}</h3>
        <table class="corr-table">
          <thead>
            <tr>
              <th>{e("Atividade")}</th>
              <th>{e("O que responde?")}</th>
              <th>{e("Foco principal")}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{e("Fechamento de caixa")}</td>
              <td>{e("O pedido foi pago?")}</td>
              <td>{e("Pedido individual")}</td>
            </tr>
            <tr>
              <td>{e("Conciliação financeira")}</td>
              <td>{e("O meio de pagamento me pagou certo?")}</td>
              <td>{e("Taxas e antecipações")}</td>
            </tr>
            <tr>
              <td>{e("Conciliação bancária")}</td>
              <td>{e("O saldo do banco bate?")}</td>
              <td>{e("Saldo bancário")}</td>
            </tr>
            <tr>
              <td>{e("DRE")}</td>
              <td>{e("Tive lucro ou prejuízo?")}</td>
              <td>{e("Competência (venda)")}</td>
            </tr>
            <tr>
              <td>{e("DFC")}</td>
              <td>{e("O que fez o saldo inicial se transformar no saldo final?")}</td>
              <td>{e("Caixa (dinheiro real)")}</td>
            </tr>
          </tbody>
        </table>
      </section>"""


def build_glossary_html() -> str:
    head = theme_head_fragment()
    correlation = render_glossary_correlation_section()
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Glossário</title>
{head}
</head>
<body class="page-glossary">
  <div class="progress-foot" aria-hidden="true"></div>
  <div class="wrap">
    <header>
      <div class="top-bar">
        <div class="nav-group">
          <a href="index.html">← Índice</a>
        </div>
        {gloss_top_bar_link_html(on_glossary_page=True)}
      </div>
      <p class="kicker">Gestão financeira</p>
      <h1><span class="gradient">Glossário</span></h1>
    </header>
    <main>
{correlation}
    </main>
  </div>
</body>
</html>
"""


def dovetail_interview_url(data_id: str) -> str:
    return f"{DOVETAIL_DATA_BASE}/{data_id.strip()}"


def build_page(meta: dict) -> str:
    did = meta.get("dovetail_data_id")
    if not did:
        raise KeyError(f"Entrevista {meta.get('slug')!r} sem dovetail_data_id")
    dt_url = dovetail_interview_url(str(did))
    dt_href = html.escape(dt_url, quote=True)
    drive_href = html.escape(INTERVIEW_VIDEOS_DRIVE_FOLDER, quote=True)

    sections = "\n".join(
        [
            render_tasks_section_cards(),
            render_section("2. Passo a passo (fluxo) mencionado na conversa", meta["fluxo"]),
            render_section("3. Dificuldades encontradas", meta["dificuldades"]),
            render_section("4. Dados utilizados", meta["dados"]),
            render_section("5. Frequência", meta["frequencia"]),
            render_section("6. Ferramentas e canais", meta["ferramentas"]),
        ]
    )

    title = meta["title"]
    interviewee = meta["interviewee"]
    store = meta["store"]
    h1_html = (
        f'      <h1><span class="gradient">{html.escape(interviewee)}</span> — '
        f"{html.escape(store)}</h1>"
    )
    head = theme_head_fragment()
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
{head}
</head>
<body>
  <div class="progress-foot" aria-hidden="true"></div>
  <div class="wrap">
    <header>
      <div class="top-bar">
        <div class="nav-group">
          <a href="index.html">← Índice</a>
        </div>
        {gloss_top_bar_link_html(on_glossary_page=False)}
      </div>
      <p class="kicker">Gestão financeira</p>
{h1_html}
    </header>
    <main>
{sections}
      <section class="block source-dovetail">
        <h2>Fonte</h2>
        <p class="src">Fonte: <a href="{dt_href}" target="_blank" rel="noopener noreferrer">Dovetail — vídeo e transcrição da entrevista</a></p>
        <p class="src">Vídeos: <a href="{drive_href}" target="_blank" rel="noopener noreferrer">Google Drive — pasta das entrevistas (gravações)</a></p>
      </section>
    </main>
  </div>
</body>
</html>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index_links = []
    for meta in INTERVIEWS:
        p = meta["csv"]
        if not p.is_file():
            print("SKIP missing:", p)
            continue
        out = OUT_DIR / f"{meta['slug']}.html"
        out.write_text(build_page(meta), encoding="utf-8")
        print("wrote", out.name)
        index_links.append((meta["title"], f"{meta['slug']}.html"))

    head = theme_head_fragment()
    ol_parts = []
    for t, href in index_links:
        ol_parts.append(
            f'        <li><a href="{html.escape(href)}">{html.escape(t)}'
            f'<span class="sub">Secções 1–6 + Dovetail (vídeo e transcrição)</span></a></li>'
        )
    ol_html = "\n".join(ol_parts)
    index_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Entrevistas — gestão financeira</title>
{head}
</head>
<body>
  <div class="progress-foot" aria-hidden="true"></div>
  <div class="wrap">
    <header>
      <div class="top-bar">
        <div class="nav-group"></div>
        {gloss_top_bar_link_html(on_glossary_page=False)}
      </div>
      <p class="kicker">Payments NP · Q2-2026</p>
      <h1><span class="gradient">Transcrições</span> — gestão financeira</h1>
      <p class="lead">Uma página por entrevista (Nuvem Pago). Visual alinhado à apresentação <code>apresentacao-gestao-financeira-q2-2026.html</code>.</p>
    </header>
    <main>
      <section class="block">
        <h2>Entrevistas</h2>
        <ul class="index-list">
{ol_html}
        </ul>
      </section>
    </main>
  </div>
</body>
</html>
"""
    (OUT_DIR / "index.html").write_text(index_html, encoding="utf-8")
    print("wrote index.html")

    (OUT_DIR / "glossario.html").write_text(build_glossary_html(), encoding="utf-8")
    print("wrote glossario.html")


if __name__ == "__main__":
    main()
