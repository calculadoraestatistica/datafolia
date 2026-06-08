"""
Gera index.html a partir das publicacoes em publications/.

Por padrao mostra apenas publicacoes cujo `data_post` ja chegou.
Use --all para incluir tambem as futuras (preview/teste).

Os posts ficam empilhados, o mais recente no topo, com badge "Último post".
Cada post mostra: data, titulo, hero (image.jpg), historia (artigo-site.md),
chart, e <details> expandivel com tabela + fontes + CTA pra calculadora.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"
OUT = ROOT / "index.html"


# ─── Markdown -> HTML (minimo) ────────────────────────────────────────────
def md_to_html(md: str) -> str:
    """Converte markdown simples (paragrafos, h2, h3, bold, italic, links, listas)."""
    out: list[str] = []
    in_ul = False
    for line in md.splitlines():
        s = line.rstrip()
        if not s:
            if in_ul:
                out.append("</ul>"); in_ul = False
            out.append("")
            continue
        # Headings
        if s.startswith("### "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h3>{_inline(s[4:].strip())}</h3>")
        elif s.startswith("## "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<h2>{_inline(s[3:].strip())}</h2>")
        elif s.startswith("# "):
            if in_ul: out.append("</ul>"); in_ul = False
            # h1 ficou no titulo do post, ignora aqui
        elif s.startswith("> "):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<blockquote><p>{_inline(s[2:].strip())}</p></blockquote>")
        elif s.startswith("- "):
            if not in_ul:
                out.append("<ul>"); in_ul = True
            out.append(f"<li>{_inline(s[2:].strip())}</li>")
        elif s.startswith("|") and "|" in s[1:]:
            # tabela markdown — pulamos (vamos mostrar table.png em vez disso)
            continue
        elif s.startswith("---"):
            if in_ul: out.append("</ul>"); in_ul = False
            out.append("<hr>")
        else:
            if in_ul: out.append("</ul>"); in_ul = False
            out.append(f"<p>{_inline(s)}</p>")
    if in_ul: out.append("</ul>")
    # Junta paragrafos consecutivos: o "" entre eles ja separa
    return "\n".join([x for x in out if x is not None])


_INLINE_PATTERNS = [
    (re.compile(r"\*\*([^*]+)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"\*([^*]+)\*"),     r"<em>\1</em>"),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2" target="_blank" rel="noopener">\1</a>'),
]
def _inline(text: str) -> str:
    """Aplica conversoes inline. Texto ja deve estar HTML-escaped quando possivel."""
    # Tomamos cuidado: nao escape o HTML pra deixar links/bold passarem
    for pat, rep in _INLINE_PATTERNS:
        text = pat.sub(rep, text)
    return text


# ─── Extracao de pedacos do artigo-site.md ────────────────────────────────
def extract_section(md: str, heading: str) -> str:
    """Pega texto entre `## heading` e o proximo `## ...` (sem o cabecalho)."""
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    m = pattern.search(md)
    if not m:
        return ""
    rest = md[m.end():]
    nxt = re.search(r"^##\s+", rest, re.MULTILINE)
    return rest[: nxt.start()].strip() if nxt else rest.strip()


def extract_titulo(md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


# ─── Carrega publicacoes ─────────────────────────────────────────────────
def load_pubs() -> list[dict]:
    pubs = []
    for d in PUB.glob("pub-*"):
        if not d.is_dir(): continue
        meta = json.loads((d / "metadata.json").read_text(encoding="utf-8"))
        meta["_dir"] = d
        meta["_artigo_md"] = (d / "artigo-site.md").read_text(encoding="utf-8") \
                              if (d / "artigo-site.md").exists() else ""
        meta["_caption_md"] = (d / "caption-ig.md").read_text(encoding="utf-8") \
                                if (d / "caption-ig.md").exists() else ""
        pubs.append(meta)
    return pubs


# ─── Render ──────────────────────────────────────────────────────────────
ADSENSE = ('<script async src="https://pagead2.googlesyndication.com/'
           'pagead/js/adsbygoogle.js?client=ca-pub-7516029395999799" '
           'crossorigin="anonymous"></script>')


def render_post(p: dict, is_latest: bool, idx: int) -> str:
    d = p["_dir"]
    rel = d.relative_to(ROOT).as_posix()
    md = p["_artigo_md"]
    titulo = extract_titulo(md) or f"{p['serie_a']['label'][:35]} × {p['serie_b']['label'][:35]}"
    historia = (
        extract_section(md, "A teoria")
        or extract_section(md, 'A "história"')
        or extract_section(md, "A história")
    )
    historia_html = md_to_html(historia) if historia else ""

    # Caption como fallback se a historia estiver vazia
    if not historia_html and p["_caption_md"]:
        # tira cabecalhos de template, pega so o corpo
        body = "\n".join(
            l for l in p["_caption_md"].splitlines()
            if l.strip() and not l.startswith("#") and not l.startswith(">") and not l.startswith("---")
        )
        historia_html = md_to_html(body)

    c = p["correlacao"]
    data_post = p.get("data_post") or ""
    is_post_zero = bool(p.get("post_zero"))
    # Formata data BR (DD/MM/YYYY) — post-zero usa data_estreia se houver
    if is_post_zero:
        d_str = p.get("data_estreia") or dt.date.today().isoformat()
        try:
            data_br = dt.date.fromisoformat(d_str).strftime("%d/%m/%Y")
        except Exception:
            data_br = d_str
    else:
        try:
            data_br = dt.date.fromisoformat(data_post).strftime("%d/%m/%Y")
        except Exception:
            data_br = data_post
    # Badge "Último post" so para o mais recente nao-post-zero
    badge = '<span class="post__badge">Último post</span>' if (is_latest and not is_post_zero) else ""
    # Tema/categoria nao aparece mais na UI (so a data importa)
    tema_html = ""

    # Hero (image.jpg)
    img_path = d / "image.jpg"
    img_url = f"/{rel}/image.jpg" if img_path.exists() and img_path.stat().st_size > 1000 else None
    hero_html = (f'<img class="post__hero" src="{img_url}" alt="Ilustração: {escape(titulo)}" loading="lazy">'
                  if img_url else "")

    # Chart e table
    chart_url = f"/{rel}/chart.png"
    table_url = f"/{rel}/table.png"

    # Fontes
    fa = p["serie_a"]; fb = p["serie_b"]

    return f"""
<article class="post {'post--latest' if is_latest else ''}" id="{d.name}">
  <header class="post__head">
    <span class="post__date">{escape(data_br)}{badge}{tema_html}</span>
    <h2 class="post__title">{escape(titulo)}</h2>
  </header>
  <div class="post__body">
    <div class="post__chart">
      <img src="{chart_url}" alt="Gráfico das duas séries" loading="lazy">
    </div>
    {hero_html}
    <div class="post__caption">
      {historia_html}
    </div>
    <details class="post__details">
      <summary>Ver tabela completa e fontes</summary>
      <div class="post__details-body">
        <img src="{table_url}" alt="Tabela com os valores anuais" loading="lazy">
        <p class="post__source">
          <strong>Fonte A:</strong> <a href="{escape(fa['url'])}" target="_blank" rel="noopener">{escape(fa['fonte'])}</a><br>
          <strong>Fonte B:</strong> <a href="{escape(fb['url'])}" target="_blank" rel="noopener">{escape(fb['fonte'])}</a>
        </p>
      </div>
    </details>
  </div>
</article>
"""


def render_index(pubs: list[dict], show_all: bool, with_image_only: bool = False) -> str:
    today = dt.date.today()
    post_zero = [p for p in pubs if p.get("post_zero")]
    rest      = [p for p in pubs if not p.get("post_zero")]

    # Filtra: por padrao só posts cuja data ja passou
    if show_all:
        visible = list(rest)
    elif with_image_only:
        # Apenas posts que ja tem image.jpg pronta (modo preview/validacao)
        def has_img(p: dict) -> bool:
            img = p["_dir"] / "image.jpg"
            return img.exists() and img.stat().st_size > 5000
        visible = [p for p in rest if has_img(p)]
    else:
        visible = [p for p in rest
                    if p.get("data_post") and dt.date.fromisoformat(p["data_post"]) <= today]

    # Post-zero entra na ordenacao geral usando data_estreia como data efetiva
    # (assim o mais recente fica sempre no topo — feed estilo timeline)
    visible = post_zero + visible
    def _effective_date(p: dict) -> str:
        return p.get("data_post") or p.get("data_estreia") or "1900-01-01"
    visible.sort(key=_effective_date, reverse=True)

    posts_html = ""
    if visible:
        for i, p in enumerate(visible):
            posts_html += render_post(p, is_latest=(i == 0), idx=i)
    else:
        next_pub = sorted(
            (p for p in pubs if p.get("data_post")),
            key=lambda p: p["data_post"],
        )
        next_one = next_pub[0] if next_pub else None
        if next_one:
            data_br = dt.date.fromisoformat(next_one["data_post"]).strftime("%d/%m/%Y")
            posts_html = f"""
<div class="empty">
  <h2>O primeiro post vai ao ar em {data_br}</h2>
  <p>Toda segunda-feira a partir daí, uma correlação espúria nova.</p>
  <p>Enquanto isso, <a href="/sobre.html">leia sobre o projeto</a> ou
     visite o <a href="https://www.instagram.com/datafolia" target="_blank" rel="noopener">@datafolia</a>.</p>
</div>
"""
        else:
            posts_html = '<div class="empty"><p>Ainda nenhum post agendado.</p></div>'

    n_visible = len(visible)
    n_total = len(pubs)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- Google AdSense -->
{ADSENSE}
<title>Data Folia — correlações espúrias do Brasil, todas as segundas</title>
<meta name="description" content="Toda segunda-feira tem uma correlação espúria nova, brasileira, com gráfico, dados, fontes e uma história inventada que costura as duas séries.">
<link rel="canonical" href="https://datafolia.com.br/">
<meta name="theme-color" content="#009C3B">
<meta property="og:type" content="website">
<meta property="og:locale" content="pt_BR">
<meta property="og:site_name" content="Data Folia">
<meta property="og:title" content="Data Folia — correlações espúrias do Brasil">
<meta property="og:description" content="Correlações espúrias brasileiras, todas as segundas-feiras.">
<meta property="og:url" content="https://datafolia.com.br/">
<meta property="og:image" content="https://datafolia.com.br/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/datafolia_final.png" type="image/png">
<link rel="apple-touch-icon" href="/datafolia_final.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="stylesheet" href="/css/style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Data Folia",
  "url": "https://datafolia.com.br/",
  "inLanguage": "pt-BR",
  "description": "Correlações espúrias brasileiras, todas as segundas-feiras."
}}
</script>
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>

<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="/" aria-label="Data Folia — página inicial">
      <img class="brand__mark" src="/datafolia_final.png" alt="" width="42" height="42">
      <span class="brand__name">Data <em>Folia</em></span>
    </a>
    <nav class="main-nav" aria-label="Menu principal">
      <ul>
        <li><a href="/">Posts</a></li>
        <li><a href="/sobre.html">Sobre</a></li>
        <li><a class="nav-ig" href="https://www.instagram.com/datafolia" target="_blank" rel="noopener" aria-label="Instagram @datafolia">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <rect x="2" y="2" width="20" height="20" rx="5"/>
            <circle cx="12" cy="12" r="4.5"/>
            <circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>
          </svg>
          @datafolia
        </a></li>
      </ul>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="container">
    <h1>Explicando o Brasil por dados.</h1>
    <p class="hero__tagline">Dos mesmos criadores de <strong>Taylor Swift</strong> e <strong>Corinthians</strong>…</p>
    <p>Toda segunda-feira, dois números brasileiros se encontram por acaso —
       e a gente conta a teoria fictícia que costura os dois. Pura folia, puro entretenimento.</p>
    <a class="hero__ig" href="https://www.instagram.com/datafolia" target="_blank" rel="noopener">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <rect x="2" y="2" width="20" height="20" rx="5"/>
        <circle cx="12" cy="12" r="4.5"/>
        <circle cx="17.5" cy="6.5" r="1" fill="currentColor"/>
      </svg>
      Siga no Instagram · @datafolia
    </a>
  </div>
</section>

<main id="conteudo" class="feed">
  <div class="container">
    {posts_html}
    <div class="ad-slot" data-ad-slot=""></div>
  </div>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/">
          <img class="brand__mark" src="/datafolia_final.png" alt="" width="42" height="42">
          <span class="brand__name">Data <em>Folia</em></span>
        </a>
        <p>Explicando o Brasil por dados, todas as segundas-feiras. Por entretenimento.</p>
      </div>
      <div>
        <h3>Site</h3>
        <ul>
          <li><a href="/">Posts</a></li>
          <li><a href="/sobre.html">Sobre</a></li>
          <li><a href="/contato.html">Contato</a></li>
        </ul>
      </div>
      <div>
        <h3>Estatística</h3>
        <ul>
          <li><a href="https://calculadoraestatistica.com.br/correlacao.html" target="_blank" rel="noopener">Teste sua correlação</a></li>
          <li><a href="https://www.instagram.com/datafolia" target="_blank" rel="noopener">@datafolia</a></li>
          <li><a href="/privacidade.html">Privacidade</a></li>
          <li><a href="/termos.html">Termos</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <p>Os gráficos são correlações estatisticamente verdadeiras, mas as histórias que os acompanham são ficcionais. Correlação não implica causalidade.</p>
      <p>© <span data-year>2026</span> Data Folia · Feito no Brasil 🇧🇷 · {n_visible}/{n_total} posts publicados</p>
    </div>
  </div>
</footer>
<script>document.querySelectorAll('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());</script>
</body>
</html>
"""


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--all", action="store_true",
                    help="Inclui posts futuros (preview)")
    p.add_argument("--with-image-only", action="store_true",
                    help="Apenas posts que ja tem image.jpg pronta (validacao)")
    args = p.parse_args()
    pubs = load_pubs()
    html = render_index(pubs, show_all=args.all, with_image_only=args.with_image_only)
    OUT.write_text(html, encoding="utf-8")
    print(f"OK  {OUT.relative_to(ROOT)}  ({len(html)//1024} KB, {len(pubs)} pubs total)")


if __name__ == "__main__":
    main()
