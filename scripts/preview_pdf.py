"""
Preview PDF: mostra 2 publicações em ambos formatos (site e instagram).

Por pub: 2 paginas
  - SITE: mockup da pagina do artigo (titulo, hero image.jpg, intro,
    chart.png, table.png, corpo + fontes)
  - INSTAGRAM: mockup do post no feed (image.jpg como slide 1 e
    instagram.png como slide 2 do carousel) + caption a direita

Uso: python scripts/preview_pdf.py pub-08-... pub-02-...
"""
from __future__ import annotations

import sys
import datetime as dt
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
import matplotlib.image as mpimg

from chart_renderer import (
    C_A, C_B, C_YELLOW, C_INK, C_INK_SOFT, C_MUTED, C_GRID,
    C_HEADER_BG, C_TABLE_ALT, C_BG, _wrap_label,
)

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"
OUT = ROOT / "data" / "DataFolia_preview_2_posts.pdf"


def _load_meta(d: Path) -> dict:
    return json.loads((d / "metadata.json").read_text(encoding="utf-8"))


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8") if p.exists() else ""


def _wrap_paragraph(text: str, width: int) -> list[str]:
    """Quebra paragrafos em linhas <= width chars (palavras inteiras)."""
    import textwrap
    out: list[str] = []
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        # remove cabecalhos markdown e separadores
        if para.startswith("#") or para.startswith("---") or para.startswith(">"):
            continue
        lines = textwrap.wrap(para, width=width, break_long_words=False)
        out.extend(lines)
        out.append("")  # paragraph break
    return out


def render_site_page(pdf: PdfPages, sub: Path, meta: dict) -> None:
    label_a = meta["serie_a"]["label"]; label_b = meta["serie_b"]["label"]
    fonte_a = meta["serie_a"]["fonte"]; fonte_b = meta["serie_b"]["fonte"]
    c = meta["correlacao"]
    r = c["r"]; p = c["p"]; n = c["n"]
    artigo = _read_text(sub / "artigo-site.md")
    # Extrai titulo (primeira linha # ...)
    titulo = ""
    for line in artigo.splitlines():
        if line.startswith("# "):
            titulo = line[2:].strip()
            break
    if not titulo:
        titulo = f"{label_a[:35]} × {label_b[:35]}"

    # Pega o trecho da "história" (entre ## A "história" e ## Os dados)
    historia = ""
    if "## A \"história\"" in artigo or "## A " in artigo:
        try:
            after = artigo.split("## A \"história\"", 1)[1]
        except IndexError:
            after = artigo.split("## A ", 1)[1]
        historia = after.split("##", 1)[0].strip()

    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")  # A4 portrait

    # ── Header: barra verde com "Data Folia · datafolia.com.br" ─────────
    head = fig.add_axes([0, 0.95, 1, 0.05])
    head.axis("off")
    head.add_patch(Rectangle((0, 0), 1, 1, transform=head.transAxes,
                                facecolor=C_A))
    head.text(0.04, 0.5, "Data Folia", fontsize=14, fontweight="bold",
              color="white", va="center", transform=head.transAxes)
    head.text(0.50, 0.5, "PREVIEW · formato SITE", fontsize=10,
              color=C_YELLOW, va="center", ha="center", style="italic",
              transform=head.transAxes)
    head.text(0.96, 0.5, "datafolia.com.br", fontsize=10, color="white",
              va="center", ha="right", transform=head.transAxes)

    # ── Titulo do artigo ────────────────────────────────────────────────
    fig.text(0.06, 0.91, titulo, fontsize=18, fontweight="bold",
             color=C_INK, ha="left", va="top", wrap=True)
    p_str = f"{p:.4f}" if p >= 0.0001 else "< 0,0001"
    fig.text(0.06, 0.875,
             f"correlação de Pearson  ·  r = {r:+.3f}  ·  R² = {r*r:.3f}  ·  "
             f"n = {n}  ·  p = {p_str}  ·  janela {c['ano_inicio']}–{c['ano_fim']}",
             fontsize=9, color=C_MUTED, ha="left", va="top")

    # ── Hero image (image.jpg) ──────────────────────────────────────────
    img_path = sub / "image.jpg"
    if img_path.exists() and img_path.stat().st_size > 1000:
        hero = fig.add_axes([0.06, 0.62, 0.88, 0.24])
        hero.axis("off")
        try:
            im = mpimg.imread(str(img_path))
            hero.imshow(im, aspect="auto")
        except Exception as e:
            hero.text(0.5, 0.5, f"(imagem nao carregou: {e})",
                      ha="center", va="center", transform=hero.transAxes)

    # ── Chart embedded ─────────────────────────────────────────────────
    chart_path = sub / "chart.png"
    if chart_path.exists():
        ch = fig.add_axes([0.06, 0.36, 0.88, 0.24])
        ch.axis("off")
        im = mpimg.imread(str(chart_path))
        ch.imshow(im, aspect="auto")

    # ── Texto (historia, abreviado) ────────────────────────────────────
    if historia:
        lines = _wrap_paragraph(historia, 95)[:14]   # 14 linhas no maximo
        text_block = "\n".join(lines)
        fig.text(0.06, 0.33, text_block, fontsize=9, color=C_INK_SOFT,
                 ha="left", va="top", linespacing=1.5)

    # ── Tabela embedded ────────────────────────────────────────────────
    table_path = sub / "table.png"
    if table_path.exists():
        tb = fig.add_axes([0.06, 0.06, 0.88, 0.10])
        tb.axis("off")
        im = mpimg.imread(str(table_path))
        tb.imshow(im, aspect="auto")

    # ── Footer: fontes ─────────────────────────────────────────────────
    foot = fig.add_axes([0, 0, 1, 0.04])
    foot.axis("off")
    foot.add_patch(Rectangle((0, 0), 1, 1, transform=foot.transAxes,
                                facecolor=C_HEADER_BG))
    foot.text(0.04, 0.5, f"Fonte A: {fonte_a[:50]}",
              fontsize=8, color=C_INK, va="center",
              transform=foot.transAxes)
    foot.text(0.96, 0.5, f"Fonte B: {fonte_b[:50]}",
              fontsize=8, color=C_INK, va="center", ha="right",
              transform=foot.transAxes)

    pdf.savefig(fig, facecolor="white")
    plt.close(fig)


def render_ig_page(pdf: PdfPages, sub: Path, meta: dict) -> None:
    label_a = meta["serie_a"]["label"]; label_b = meta["serie_b"]["label"]
    c = meta["correlacao"]
    r = c["r"]
    caption = _read_text(sub / "caption-ig.md").strip()

    fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")

    # ── Header verde
    head = fig.add_axes([0, 0.95, 1, 0.05])
    head.axis("off")
    head.add_patch(Rectangle((0, 0), 1, 1, transform=head.transAxes,
                                facecolor=C_A))
    head.text(0.04, 0.5, "Data Folia", fontsize=14, fontweight="bold",
              color="white", va="center", transform=head.transAxes)
    head.text(0.50, 0.5, "PREVIEW · formato INSTAGRAM",
              fontsize=10, color=C_YELLOW, va="center", ha="center",
              style="italic", transform=head.transAxes)
    head.text(0.96, 0.5, "@datafolia", fontsize=10, color="white",
              va="center", ha="right", transform=head.transAxes)

    # ── Lado esquerdo: dois slides do carousel (image.jpg + instagram.png)
    fig.text(0.06, 0.92, "Carrossel (2 slides)", fontsize=11,
             fontweight="bold", color=C_INK, va="top")

    # Slide 1: image.jpg — eixo "limpo" mas com imshow normal
    s1_label = fig.add_axes([0.03, 0.87, 0.40, 0.02]); s1_label.axis("off")
    s1_label.text(0.5, 0.5, "slide 1 · image.jpg", fontsize=9, color=C_MUTED,
                  ha="center", va="center", transform=s1_label.transAxes)
    s1 = fig.add_axes([0.03, 0.55, 0.40, 0.32])
    s1.set_xticks([]); s1.set_yticks([])
    for spine in s1.spines.values():
        spine.set_edgecolor(C_GRID); spine.set_linewidth(1)
    img_path = sub / "image.jpg"
    if img_path.exists() and img_path.stat().st_size > 1000:
        try:
            im = mpimg.imread(str(img_path))
            s1.imshow(im, aspect="auto")
        except Exception as e:
            s1.text(0.5, 0.5, f"erro: {e}", ha="center", va="center",
                     transform=s1.transAxes)

    # Slide 2: instagram.png
    s2_label = fig.add_axes([0.03, 0.49, 0.40, 0.02]); s2_label.axis("off")
    s2_label.text(0.5, 0.5, "slide 2 · instagram.png (chart)", fontsize=9,
                  color=C_MUTED, ha="center", va="center",
                  transform=s2_label.transAxes)
    s2 = fig.add_axes([0.03, 0.17, 0.40, 0.32])
    s2.set_xticks([]); s2.set_yticks([])
    for spine in s2.spines.values():
        spine.set_edgecolor(C_GRID); spine.set_linewidth(1)
    ig_path = sub / "instagram.png"
    if ig_path.exists():
        im = mpimg.imread(str(ig_path))
        s2.imshow(im, aspect="auto")

    # ── Lado direito: caption do post (texto)
    fig.text(0.48, 0.92, "Caption do post", fontsize=11, fontweight="bold",
             color=C_INK, va="top")
    cap_ax = fig.add_axes([0.48, 0.10, 0.49, 0.81])
    cap_ax.axis("off")
    cap_ax.add_patch(Rectangle((0, 0), 1, 1, transform=cap_ax.transAxes,
                                  facecolor="#fafafa",
                                  edgecolor=C_GRID, linewidth=1))
    # Renderiza caption como texto. Tira o "# Caption do Instagram..." se vier de template.
    cap_clean = []
    for ln in caption.splitlines():
        if ln.startswith("#") or ln.startswith(">") or ln.startswith("---"):
            continue
        cap_clean.append(ln)
    txt = "\n".join(cap_clean).strip()
    # Quebra cada linha que ficar muito longa
    import textwrap
    wrapped = []
    for ln in txt.splitlines():
        if not ln.strip():
            wrapped.append("")
            continue
        wrapped.extend(textwrap.wrap(ln, width=48, break_long_words=False)
                        or [""])
    body = "\n".join(wrapped[:40])
    cap_ax.text(0.04, 0.97, body, fontsize=9.5, color=C_INK,
                 ha="left", va="top", transform=cap_ax.transAxes,
                 linespacing=1.45, wrap=True)

    # ── Footer com r e data
    foot = fig.add_axes([0, 0, 1, 0.04])
    foot.axis("off")
    foot.add_patch(Rectangle((0, 0), 1, 1, transform=foot.transAxes,
                                facecolor=C_HEADER_BG))
    data_post = meta.get("data_post") or "—"
    tema = meta.get("tema_calendario") or "—"
    foot.text(0.04, 0.5,
              f"r = {r:+.3f}  ·  data prevista: {data_post}  ·  tema: {tema}",
              fontsize=8, color=C_INK, va="center", transform=foot.transAxes)
    foot.text(0.96, 0.5, sub.name, fontsize=8, color=C_MUTED,
              va="center", ha="right", transform=foot.transAxes)

    pdf.savefig(fig, facecolor="white")
    plt.close(fig)


def main(slugs: list[str]) -> None:
    if not slugs:
        slugs = ["pub-08", "pub-02"]
    # Encontra cada pub pelo prefixo
    pubs: list[Path] = []
    for s in slugs:
        matches = sorted(PUB.glob(s + "*"))
        if not matches:
            print(f"AVISO: nao achei nada para '{s}'")
            continue
        pubs.append(matches[0])

    if not pubs:
        raise SystemExit("Nenhuma pub encontrada")

    print(f"Gerando preview de {len(pubs)} pubs em {OUT}")
    with PdfPages(OUT) as pdf:
        # ── Capa
        fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        fig.text(0.5, 0.70, "Data Folia", ha="center", fontsize=42,
                 fontweight="bold", color=C_A)
        fig.text(0.5, 0.64, "Preview de 2 publicações", ha="center",
                 fontsize=18, color=C_INK)
        fig.text(0.5, 0.58, "site + Instagram", ha="center", fontsize=14,
                 color=C_MUTED, style="italic")
        fig.text(0.5, 0.45,
                 f"Gerado em {dt.datetime.now().strftime('%d/%m/%Y %H:%M')}",
                 ha="center", fontsize=10, color=C_MUTED)
        fig.text(0.5, 0.40, "Publicações incluídas:",
                 ha="center", fontsize=11, color=C_INK_SOFT)
        for i, sub in enumerate(pubs):
            meta = _load_meta(sub)
            label = f"{i+1}. {sub.name}"
            fig.text(0.5, 0.36 - i * 0.04, label, ha="center",
                     fontsize=10, color=C_INK)
            fig.text(0.5, 0.34 - i * 0.04,
                     f"   {meta['serie_a']['label'][:50]}",
                     ha="center", fontsize=8, color=C_A)
            fig.text(0.5, 0.32 - i * 0.04,
                     f"   × {meta['serie_b']['label'][:50]}",
                     ha="center", fontsize=8, color=C_B)
        pdf.savefig(fig, facecolor="white"); plt.close(fig)

        for sub in pubs:
            meta = _load_meta(sub)
            print(f"  {sub.name}")
            render_site_page(pdf, sub, meta)
            render_ig_page(pdf, sub, meta)

    print(f"PDF: {OUT}  ({OUT.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main(sys.argv[1:])
