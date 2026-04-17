/**
 * Portão de sessão: sem autenticação válida, o conteúdo fica oculto até introduzir a senha.
 * A sessão usa sessionStorage (fecha o browser / janela anónima → volta a pedir senha).
 * Isto não esconde os ficheiros HTML perante quem inspeciona o repositório ou descarrega URLs diretas com ferramentas; para controlo forte use Cloudflare Worker ou similar.
 */
(function () {
  "use strict";

  var STORAGE_KEY = "gestao_fin_site_auth_v1";

  function timingSafeEqual(a, b) {
    var enc = new TextEncoder();
    var ab = enc.encode(String(a));
    var bb = enc.encode(String(b));
    if (ab.length !== bb.length) {
      return false;
    }
    var x = 0;
    for (var i = 0; i < ab.length; i++) {
      x |= ab[i] ^ bb[i];
    }
    return x === 0;
  }

  function isAuthed() {
    return sessionStorage.getItem(STORAGE_KEY) === "1";
  }

  function unlock() {
    sessionStorage.setItem(STORAGE_KEY, "1");
    var st = document.getElementById("gestao-fin-gate-style");
    if (st && st.parentNode) {
      st.parentNode.removeChild(st);
    }
    var ov = document.getElementById("gestao-fin-gate-overlay");
    if (ov && ov.parentNode) {
      ov.parentNode.removeChild(ov);
    }
  }

  function showGate() {
    var pass = window.__GESTAO_FIN_PASSWORD__;
    if (typeof pass !== "string" || pass.length === 0) {
      pass = "";
    }

    var style = document.createElement("style");
    style.id = "gestao-fin-gate-style";
    style.textContent =
      "html.gestao-fin-gating,html.gestao-fin-gating body{min-height:100vh;margin:0;}" +
      "html.gestao-fin-gating body > *:not(#gestao-fin-gate-overlay){visibility:hidden!important;}";
    document.documentElement.classList.add("gestao-fin-gating");
    document.head.appendChild(style);

    function buildOverlay() {
      var overlay = document.createElement("div");
      overlay.id = "gestao-fin-gate-overlay";
      overlay.setAttribute(
        "style",
        [
          "position:fixed",
          "inset:0",
          "z-index:2147483646",
          "display:flex",
          "align-items:center",
          "justify-content:center",
          "padding:1.5rem",
          "background:radial-gradient(ellipse 120% 100% at 50% 50%,#051e41 0%,#070f2d 50%,#090019 100%)",
          "font-family:system-ui,sans-serif",
          "color:#fff",
          "visibility:visible",
        ].join(";")
      );

      var card = document.createElement("div");
      card.setAttribute(
        "style",
        [
          "width:100%",
          "max-width:22rem",
          "padding:1.5rem",
          "border-radius:12px",
          "background:rgba(255,255,255,0.06)",
          "border:1px solid rgba(255,255,255,0.12)",
          "box-shadow:0 12px 40px rgba(0,0,0,0.35)",
        ].join(";")
      );

      var title = document.createElement("h1");
      title.textContent = "Acesso restrito";
      title.setAttribute("style", "margin:0 0 0.35rem;font-size:1.15rem;font-weight:600");

      var sub = document.createElement("p");
      sub.textContent = "Introduza a senha para ver este conteúdo.";
      sub.setAttribute("style", "margin:0 0 1rem;font-size:0.9rem;color:#8fa8c8;line-height:1.45");

      var err = document.createElement("p");
      err.setAttribute("style", "margin:0 0 0.75rem;font-size:0.85rem;color:#f77a7c;min-height:1.2em");
      err.setAttribute("aria-live", "polite");

      var form = document.createElement("form");
      form.setAttribute("style", "margin:0");
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        err.textContent = "";
        var input = form.querySelector('input[name="password"]');
        var val = input ? input.value : "";
        if (timingSafeEqual(val, pass)) {
          unlock();
        } else {
          err.textContent = "Senha incorreta.";
          if (input) {
            input.value = "";
            input.focus();
          }
        }
      });

      var label = document.createElement("label");
      label.textContent = "Senha";
      label.setAttribute("style", "display:block;font-size:0.85rem;color:#c9d6ea;margin-bottom:0.35rem");

      var input = document.createElement("input");
      input.type = "password";
      input.name = "password";
      input.required = true;
      input.autocomplete = "current-password";
      input.setAttribute(
        "style",
        "width:100%;box-sizing:border-box;padding:0.55rem 0.65rem;border-radius:8px;border:1px solid rgba(255,255,255,0.2);background:rgba(0,0,0,0.25);color:#fff;font-size:1rem;margin-bottom:0.75rem"
      );

      var btn = document.createElement("button");
      btn.type = "submit";
      btn.textContent = "Entrar";
      btn.setAttribute(
        "style",
        "width:100%;padding:0.65rem;border:none;border-radius:8px;background:#0059d5;color:#fff;font-weight:600;font-size:0.95rem;cursor:pointer"
      );

      label.appendChild(document.createElement("br"));
      label.appendChild(input);
      form.appendChild(label);
      form.appendChild(btn);

      card.appendChild(title);
      card.appendChild(sub);
      card.appendChild(err);
      card.appendChild(form);
      overlay.appendChild(card);
      document.body.appendChild(overlay);
      input.focus();
    }

    if (document.body) {
      buildOverlay();
    } else {
      document.addEventListener("DOMContentLoaded", buildOverlay, { once: true });
    }
  }

  if (isAuthed()) {
    return;
  }

  showGate();
})();
