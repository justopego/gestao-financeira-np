(function () {
  "use strict";

  var LOCALES = [
    { key: "produto", sheetName: "Nuvem Pago (produto)" },
    { key: "exp-orders", sheetName: "Exportável Orders" },
    { key: "exp-np", sheetName: "Exportável Nuvem Pago" },
    { key: "api", sheetName: "API" }
  ];

  function pillInformamos(pill) {
    if (pill.classList.contains("pill--success")) return "Sim";
    if (pill.classList.contains("pill--neutral")) return "Não";
    return "";
  }

  /**
   * Conciliação financeira: Sim/Não por origem (aba), alinhado às regras das pills
   * dinâmicas na página — não depende do separador selecionado no momento.
   */
  function pillInformamosConciliacaoFinanceiraPerLocale(pill, localeKey) {
    var id = pill.id || "";
    if (id === "pill-nome-cliente") {
      return localeKey === "exp-orders" ? "Sim" : "Não";
    }
    if (id === "pill-juros" || id === "pill-mdr") {
      return localeKey === "produto" || localeKey === "exp-orders" ? "Sim" : "Não";
    }
    if (id === "pill-valor-liquido" || id === "pill-data-mudanca-status") {
      return localeKey === "api" ? "Não" : "Sim";
    }
    return pillInformamos(pill);
  }

  /**
   * Conciliação bancária: Sim/Não por origem, alinhado a syncPillsNeutralOnApi e às pills
   * da página (independente da aba selecionada no momento do download).
   */
  function pillInformamosConciliacaoBancariaPerLocale(pill, localeKey) {
    var id = pill.id || "";
    if (id === "pill-nome-cliente") {
      return localeKey === "exp-orders" ? "Sim" : "Não";
    }
    if (id === "pill-valor-liquido" || id === "pill-data-mudanca-status") {
      return localeKey === "api" ? "Não" : "Sim";
    }
    if (id === "pill-juros" || id === "pill-mdr") {
      return localeKey === "api" || localeKey === "exp-np" ? "Não" : "Sim";
    }
    return pillInformamos(pill);
  }

  /**
   * DRE: Sim/Não conforme as classes das pills no HTML (sem alternância por aba na UI).
   * Mantém a mesma estrutura de export que as outras telas; útil se no futuro houver regras por local.
   */
  function pillInformamosDrePerLocale(pill) {
    return pillInformamos(pill);
  }

  /**
   * DFC: Sim/Não conforme as classes das pills no HTML (igual à DRE).
   */
  function pillInformamosDfcPerLocale(pill) {
    return pillInformamos(pill);
  }

  function tabsForPill(pill) {
    var raw = (pill.getAttribute("data-tabs") || "").trim();
    return raw.split(/\s+/).filter(Boolean);
  }

  function buildRowsForLocale(pills, localeKey, section) {
    var perLocale = section.getAttribute("data-export-per-locale-sim") === "true";
    var title = (section.getAttribute("data-export-title") || "").trim();
    var rows = [];
    if (title) {
      rows.push([title, ""]);
      rows.push([]);
    }
    rows.push(["Dado", "Já informamos?"]);
    var seen = Object.create(null);
    for (var i = 0; i < pills.length; i++) {
      var pill = pills[i];
      var tabs = tabsForPill(pill);
      if (tabs.indexOf(localeKey) === -1) continue;
      var name = pill.textContent.replace(/\s+/g, " ").trim();
      if (!name || seen[name]) continue;
      seen[name] = true;
      var informamos;
      if (perLocale) {
        var variant = (section.getAttribute("data-export-variant") || "financeira")
          .trim()
          .toLowerCase();
        if (variant === "bancaria") {
          informamos = pillInformamosConciliacaoBancariaPerLocale(pill, localeKey);
        } else if (variant === "dre") {
          informamos = pillInformamosDrePerLocale(pill, localeKey);
        } else if (variant === "dfc") {
          informamos = pillInformamosDfcPerLocale(pill, localeKey);
        } else {
          informamos = pillInformamosConciliacaoFinanceiraPerLocale(pill, localeKey);
        }
      } else {
        informamos = pillInformamos(pill);
      }
      rows.push([name, informamos]);
    }
    return rows;
  }

  function sanitizeSheetName(name) {
    var s = name.replace(/[:\\/*?\[\]]/g, "").substring(0, 31);
    return s || "Sheet";
  }

  function exportDadosNecessarios(section) {
    if (typeof XLSX === "undefined") return;
    var rawBase = (section.getAttribute("data-export-basename") || "dados-necessarios").trim();
    var basename = rawBase.replace(/[^\w-]+/g, "-").replace(/^-|-$/g, "") || "dados-necessarios";
    var pills = section.querySelectorAll(".js-dados-pill");
    var wb = XLSX.utils.book_new();
    for (var j = 0; j < LOCALES.length; j++) {
      var loc = LOCALES[j];
      var aoa = buildRowsForLocale(pills, loc.key, section);
      var ws = XLSX.utils.aoa_to_sheet(aoa);
      XLSX.utils.book_append_sheet(wb, ws, sanitizeSheetName(loc.sheetName));
    }
    if (section.getAttribute("data-export-extra-sheet-externos") === "true") {
      var aoaExt = buildRowsForLocale(pills, "externos", section);
      var wsExt = XLSX.utils.aoa_to_sheet(aoaExt);
      XLSX.utils.book_append_sheet(wb, wsExt, sanitizeSheetName("Dados externos"));
    }
    if (section.getAttribute("data-export-extra-sheet-conta-externa") === "true") {
      var aoaCe = buildRowsForLocale(pills, "conta-externa", section);
      var wsCe = XLSX.utils.aoa_to_sheet(aoaCe);
      XLSX.utils.book_append_sheet(wb, wsCe, sanitizeSheetName("Conta bancária externa"));
    }
    XLSX.writeFile(wb, basename + "-dados-necessarios.xlsx");
  }

  function init() {
    document.querySelectorAll(".dados-necessarios-download").forEach(function (btn) {
      btn.addEventListener("click", function (e) {
        e.preventDefault();
        var section = btn.closest("#dados-necessarios-section");
        if (!section) return;
        if (typeof XLSX === "undefined") return;
        exportDadosNecessarios(section);
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
