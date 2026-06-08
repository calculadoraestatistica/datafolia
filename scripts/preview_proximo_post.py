"""
Preview do PROXIMO post agendado em PDF de UMA pagina A4.

Layout:
  - Topo: titulo do post + data de publicacao
  - Meio:  grafico (chart.png) lado a lado com imagem (image.jpg)
  - Base:  texto integral da 'A teoria' do artigo-site.md

Uso:
    python scripts/preview_proximo_post.py
    python scripts/preview_proximo_post.py --pub pub-01-trump-x-neymar-copa-do-mundo
    python scripts/preview_proximo_post.py --out preview.pdf

Cron: rodar quintas a noite, gera PDF e envia por email pra Vini + Giovana.
"""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"

C_GREEN  = "#009C3B"
C_YELLOW = "#FACC15"
C_INK    = "#0F172A"
C_MUTED  = "#64748B"


def extract_section(md: str, heading: str) -> str:
    m = re.search(rf'^##\s+{re.escape(heading)}\s*\n+(.+?)(?=\n##|\Z)',
                   md, re.M | re.S)
    return m.group(1).strip() if m else ""


def extract_historia(md: str) -> str:
    for h in ["A teoria", 'A "história"', "A história"]:
        s = extract_section(md, h)
        if s:
            return s
    return ""


def find_next_pub() -> Path | None:
    """Acha a pub com data_post >= hoje, menor data."""
    today = dt.date.today()
    candidates: list[tuple[dt.date, Path]] = []
    for d in PUB.glob("pub-*"):
        if not d.is_dir():
            continue
        meta = json.loads((d / "metadata.json").read_text(encoding="utf-8"))
        if meta.get("post_zero"):
            continue
        dp = meta.get("data_post")
        if not dp:
            continue
        try:
            data = dt.date.fromisoformat(dp)
        except Exception:
            continue
        if data >= today:
            candidates.append((data, d))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][1]


def render_pdf(pdir: Path, out: Path) -> None:
    meta = json.loads((pdir / "metadata.json").read_text(encoding="utf-8"))
    artigo = (pdir / "artigo-site.md").read_text(encoding="utf-8")
    titulo = meta["titulo"]
    data_post = meta.get("data_post", "—")
    dias_pt = ["segunda-feira", "terça-feira", "quarta-feira",
                "quinta-feira", "sexta-feira", "sábado", "domingo"]
    try:
        d_obj = dt.date.fromisoformat(data_post)
        data_br = f"{d_obj.strftime('%d/%m/%Y')} ({dias_pt[d_obj.weekday()]})"
    except Exception:
        data_br = data_post
    label_a = meta["serie_a"]["label"]
    label_b = meta["serie_b"]["label"]
    historia = extract_historia(artigo)

    chart_path = pdir / "chart.png"
    image_path = pdir / "image.jpg"

    # A4 portrait: 8.27 x 11.69 inches
    fig = plt.figure(figsize=(8.27, 11.69), dpi=100, facecolor="white")

    # ── Banda topo verde (10%): brand + data ──────────────────────────
    ax_top = fig.add_axes([0, 0.92, 1, 0.08])
    ax_top.axis("off")
    ax_top.add_patch(Rectangle((0, 0), 1, 1, facecolor=C_GREEN,
                                 transform=ax_top.transAxes, zorder=0))
    ax_top.text(0.04, 0.55, "DATA FOLIA",
                fontsize=14, fontweight="bold", color=C_YELLOW,
                va="center", transform=ax_top.transAxes)
    ax_top.text(0.96, 0.55, f"Próximo post · {data_br}",
                fontsize=11, color="white",
                va="center", ha="right", transform=ax_top.transAxes)

    # ── Titulo (5%): grande, abaixo da banda ──────────────────────────
    ax_titulo = fig.add_axes([0, 0.85, 1, 0.06])
    ax_titulo.axis("off")
    ax_titulo.text(0.5, 0.5, titulo,
                    fontsize=20, fontweight="bold", color=C_INK,
                    va="center", ha="center", transform=ax_titulo.transAxes)

    # ── Linha amarela divisoria ───────────────────────────────────────
    ax_div = fig.add_axes([0.10, 0.835, 0.80, 0.004])
    ax_div.axis("off")
    ax_div.add_patch(Rectangle((0, 0), 1, 1, facecolor=C_YELLOW,
                                 transform=ax_div.transAxes))

    # ── Grafico e imagem lado a lado (30% da altura) ──────────────────
    # Cada um ocupa 44% da largura, separados por 4% de gap
    if chart_path.exists():
        ax_chart = fig.add_axes([0.05, 0.50, 0.43, 0.32])
        ax_chart.axis("off")
        try:
            ax_chart.imshow(mpimg.imread(chart_path), aspect="equal")
        except Exception as e:
            ax_chart.text(0.5, 0.5, f"[chart.png erro]\n{e}",
                          ha="center", va="center")

    if image_path.exists() and image_path.stat().st_size > 5000:
        ax_img = fig.add_axes([0.52, 0.50, 0.43, 0.32])
        ax_img.axis("off")
        try:
            ax_img.imshow(mpimg.imread(image_path), aspect="equal")
        except Exception as e:
            ax_img.text(0.5, 0.5, f"[image.jpg erro]\n{e}",
                        ha="center", va="center")
    else:
        ax_img = fig.add_axes([0.52, 0.50, 0.43, 0.32])
        ax_img.axis("off")
        ax_img.add_patch(Rectangle((0, 0), 1, 1, facecolor="#F1F5F9",
                                     transform=ax_img.transAxes))
        ax_img.text(0.5, 0.5, "(imagem nao gerada ainda)",
                    ha="center", va="center", color=C_MUTED, fontstyle="italic",
                    transform=ax_img.transAxes)

    # ── Texto da teoria (parte inferior, ~40% da altura) ──────────────
    ax_txt = fig.add_axes([0.07, 0.05, 0.86, 0.42])
    ax_txt.axis("off")
    # Cabecalho do texto
    ax_txt.text(0, 1.0, "A TEORIA",
                fontsize=10, fontweight="bold", color=C_MUTED,
                va="top", transform=ax_txt.transAxes)
    # Texto quebrado em paragrafos
    paragrafos = [p.strip() for p in historia.split("\n\n") if p.strip()]
    y = 0.92
    line_h = 0.034
    for para in paragrafos:
        # quebra cada paragrafo manualmente em ~95 chars
        import textwrap
        lines = textwrap.wrap(para, width=95)
        for ln in lines:
            if y < 0.05:
                break
            ax_txt.text(0, y, ln, fontsize=10, color=C_INK,
                        va="top", transform=ax_txt.transAxes)
            y -= line_h
        y -= line_h * 0.6   # espaco entre paragrafos
        if y < 0.05:
            break

    # Series ao fim (rodape)
    ax_txt.text(0, 0.02,
                f"Série A: {label_a}\nSérie B: {label_b}",
                fontsize=8, color=C_MUTED, fontstyle="italic",
                va="bottom", transform=ax_txt.transAxes)

    # ── Rodape ────────────────────────────────────────────────────────
    fig.text(0.5, 0.015, "datafolia.com.br  ·  @datafolia  ·  preview gerado em "
             f"{dt.datetime.now().strftime('%d/%m/%Y %H:%M')}",
             ha="center", fontsize=8, color=C_MUTED)

    with PdfPages(out) as pdf:
        pdf.savefig(fig, facecolor="white")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pub", help="pub-id especifico (default: proximo agendado)")
    ap.add_argument("--out", default=str(ROOT / "data" / "preview_proximo.pdf"))
    args = ap.parse_args()

    if args.pub:
        pdir = PUB / args.pub
        if not pdir.exists():
            raise SystemExit(f"Pub nao encontrada: {pdir}")
    else:
        pdir = find_next_pub()
        if not pdir:
            raise SystemExit("Nenhuma pub agendada com data >= hoje")
    print(f"Pub: {pdir.name}")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    render_pdf(pdir, out)
    size_kb = out.stat().st_size / 1024
    print(f"PDF: {out.relative_to(ROOT)}  ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
