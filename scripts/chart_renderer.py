"""
chart_renderer.py — layout padrão Data Folia.

Paleta brasileira, fontes uniformes, dois tamanhos:
  - render_chart_site(...)     → 1200x600 (chart wide pro site)
  - render_table_site(...)     → 1200xN   (tabela dos dados brutos)
  - render_chart_instagram(...) → 1080x1080 (quadrado pro feed do IG)

Cores:
  - SÉRIE A: verde bandeira       #009C3B
  - SÉRIE B: laranja festa         #F97316
  - acento amarelo (header strips) #FACC15
  - tinta                          #1A1A1A
  - muted                          #6B7280
"""
from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.ticker import MaxNLocator

# ─── Paleta ────────────────────────────────────────────────────────────────
C_A          = "#009C3B"   # verde bandeira brasileira
C_B          = "#F97316"   # laranja festa
C_YELLOW     = "#FACC15"   # amarelo bandeira (acento, header strips)
C_INK        = "#1A1A1A"
C_INK_SOFT   = "#374151"
C_MUTED      = "#6B7280"
C_GRID       = "#E5E7EB"
C_HEADER_BG  = "#FEF3C7"   # amarelo bem claro (table header bg)
C_TABLE_ALT  = "#FFF7ED"   # laranja bem claro (linhas alternadas)
C_BG         = "#FFFFFF"

# ─── Fontes (uniformes em todos os posts) ──────────────────────────────────
# Tamanhos absolutos em pt para os layouts do SITE.
SITE_FS_TITLE      = 17
SITE_FS_SUBTITLE   = 12
SITE_FS_AXIS_LABEL = 13
SITE_FS_TICK       = 11
SITE_FS_LEGEND     = 12
SITE_FS_TABLE_HDR  = 13
SITE_FS_TABLE_CELL = 12
SITE_FS_FOOTER     = 10

# Tamanhos absolutos em pt para o layout do INSTAGRAM (figura menor em px
# mas fontes maiores em pt pra ficar legível no feed mobile).
IG_FS_TITLE       = 26
IG_FS_R           = 32
IG_FS_AXIS_LABEL  = 16
IG_FS_TICK        = 14
IG_FS_LEGEND      = 14
IG_FS_FOOTER      = 12

# ─── Helpers ───────────────────────────────────────────────────────────────
def _wrap_label(label: str, width: int) -> str:
    """Quebra rótulo de eixo em 2 linhas se ultrapassar `width` chars."""
    if len(label) <= width:
        return label
    lines = textwrap.wrap(label, width=width, break_long_words=False)
    if len(lines) > 2:
        # 2 linhas máximas; truncamento elegante se ainda exceder
        lines = lines[:2]
        if len(lines[1]) > width - 1:
            lines[1] = lines[1][: width - 1] + "…"
    return "\n".join(lines)


def _fmt_num(v: float) -> str:
    if abs(v) >= 1000:
        return f"{v:,.0f}".replace(",", ".")
    if abs(v) >= 10:
        return f"{v:.1f}"
    if abs(v) >= 0.01:
        return f"{v:.3f}"
    return f"{v:.5g}"


# ─── 1) CHART SITE (1200×600 px) ──────────────────────────────────────────
def render_chart_site(out_path: Path, label_a: str, label_b: str,
                       anos: list[int], xs: list[float], ys: list[float],
                       r: float, p: float, n: int,
                       fonte_a: str | None = None,
                       fonte_b: str | None = None) -> None:
    fig, ax = plt.subplots(figsize=(12, 6), dpi=120, facecolor=C_BG)
    ax.set_facecolor(C_BG)
    ax2 = ax.twinx()

    # Header strip verde com r-value (barra fininha no topo)
    fig.subplots_adjust(left=0.10, right=0.90, top=0.86, bottom=0.18)
    fig.text(0.06, 0.94, "Data Folia", fontsize=SITE_FS_TITLE,
             fontweight="bold", color=C_INK, va="center")
    fig.text(0.94, 0.94, f"r = {r:+.3f}", fontsize=SITE_FS_TITLE,
             fontweight="bold", color=(C_A if r > 0 else C_B),
             va="center", ha="right")

    # Linhas
    line_a, = ax.plot(anos, xs, color=C_A, linewidth=2.8, linestyle="-",
                      marker="o", markersize=9,
                      markerfacecolor=C_A, markeredgecolor="white",
                      markeredgewidth=1.6, zorder=4)
    line_b, = ax2.plot(anos, ys, color=C_B, linewidth=2.8,
                       linestyle=(0, (6, 3)),
                       marker="s", markersize=9,
                       markerfacecolor="white", markeredgecolor=C_B,
                       markeredgewidth=2.4, zorder=3)

    # Eixos
    ax.set_xlabel("Ano", fontsize=SITE_FS_AXIS_LABEL, color=C_INK_SOFT)
    ax.set_ylabel(_wrap_label(label_a, 40),
                  fontsize=SITE_FS_AXIS_LABEL, fontweight="bold",
                  color=C_A, labelpad=10)
    ax2.set_ylabel(_wrap_label(label_b, 40),
                   fontsize=SITE_FS_AXIS_LABEL, fontweight="bold",
                   color=C_B, labelpad=10, rotation=270, va="bottom")
    ax.tick_params(axis="x", labelsize=SITE_FS_TICK)
    ax.tick_params(axis="y", labelsize=SITE_FS_TICK, colors=C_A)
    ax2.tick_params(axis="y", labelsize=SITE_FS_TICK, colors=C_B)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True,
                                            nbins=min(len(anos), 12)))

    # Grid
    ax.grid(True, color=C_GRID, linestyle="--", linewidth=0.7, alpha=0.9)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("top", "left"):
        ax2.spines[sp].set_visible(False)

    # Folga em cada eixo Y
    for axis, vals in ((ax, xs), (ax2, ys)):
        vmin, vmax = min(vals), max(vals)
        if vmin == vmax:
            vmin -= 0.5; vmax += 0.5
        pad = (vmax - vmin) * 0.12
        axis.set_ylim(vmin - pad, vmax + pad)

    # Legenda abaixo do gráfico (rótulos completos)
    fig.legend([line_a, line_b],
               [f"● {label_a}", f"□ {label_b}"],
               loc="lower center",
               bbox_to_anchor=(0.5, 0.005),
               fontsize=SITE_FS_LEGEND, frameon=False, ncol=1,
               handlelength=0, handletextpad=0)

    # Subtítulo discreto com p-valor e n
    p_str = f"{p:.4f}" if p >= 0.0001 else "< 0,0001"
    fig.text(0.5, 0.89,
             f"correlação de Pearson  ·  n = {n}  ·  p = {p_str}  ·  "
             f"janela {anos[0]}–{anos[-1]}",
             ha="center", fontsize=SITE_FS_SUBTITLE, color=C_MUTED)

    fig.savefig(out_path, dpi=120, bbox_inches="tight",
                facecolor=C_BG, edgecolor="none")
    plt.close(fig)


# ─── 2) TABLE SITE (1200x dinâmico) ────────────────────────────────────────
def render_table_site(out_path: Path, label_a: str, label_b: str,
                       anos: list[int], xs: list[float], ys: list[float]) -> None:
    # Quebra rotulos longos em até 3 linhas pro cabeçalho.
    hdr_a = _wrap_label(label_a, 32)
    hdr_b = _wrap_label(label_b, 32)
    n_lines_hdr = max(hdr_a.count("\n"), hdr_b.count("\n")) + 1

    rows_data = len(anos)
    # altura: header (escala com numero de linhas) + linhas de dados + padding
    h_inches = 0.42 * n_lines_hdr + 0.45 + 0.36 * rows_data
    fig, ax = plt.subplots(figsize=(12, h_inches), dpi=120, facecolor=C_BG)
    ax.set_facecolor(C_BG)
    ax.axis("off")

    headers = ["Ano", hdr_a, hdr_b]
    table_rows = [[str(y), _fmt_num(xs[i]), _fmt_num(ys[i])]
                  for i, y in enumerate(anos)]
    tab = ax.table(cellText=table_rows, colLabels=headers,
                   cellLoc="center", colLoc="center",
                   colWidths=[0.10, 0.45, 0.45],
                   loc="center")
    tab.auto_set_font_size(False)
    tab.set_fontsize(SITE_FS_TABLE_CELL)
    tab.scale(1.0, 1.4)
    # Header expandido para acomodar multilinhas
    for (i, j), cell in tab.get_celld().items():
        cell.set_edgecolor(C_GRID)
        cell.set_linewidth(0.8)
        if i == 0:
            cell.set_facecolor(C_HEADER_BG)
            cell.set_text_props(weight="bold", fontsize=SITE_FS_TABLE_HDR,
                                color=C_INK, ha="center", va="center")
            cell.set_height(cell.get_height() * (1.1 + 0.5 * (n_lines_hdr - 1)))
        else:
            cell.set_facecolor(C_TABLE_ALT if (i % 2 == 0) else C_BG)
            if j == 0:
                cell.set_text_props(weight="bold", color=C_INK)
            elif j == 1:
                cell.set_text_props(color=C_A, weight="bold")
            elif j == 2:
                cell.set_text_props(color=C_B, weight="bold")

    fig.savefig(out_path, dpi=120, bbox_inches="tight",
                facecolor=C_BG, edgecolor="none", pad_inches=0.2)
    plt.close(fig)


# ─── 3) CHART INSTAGRAM (1080×1080 px = 1:1) ──────────────────────────────
def render_chart_instagram(out_path: Path, label_a: str, label_b: str,
                            anos: list[int], xs: list[float], ys: list[float],
                            r: float, p: float, n: int) -> None:
    # 9x9 inches @ 120 dpi = 1080x1080
    fig = plt.figure(figsize=(9, 9), dpi=120, facecolor=C_BG)

    # ── Header strip verde (top 12%) ─────────────────────────────────
    head_ax = fig.add_axes([0, 0.88, 1, 0.12])
    head_ax.axis("off")
    head_ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=C_A,
                                  transform=head_ax.transAxes, zorder=0))
    head_ax.text(0.04, 0.55, "Data Folia",
                 fontsize=IG_FS_TITLE, fontweight="bold", color="white",
                 va="center", transform=head_ax.transAxes)
    head_ax.text(0.96, 0.55, f"r = {r:+.3f}",
                 fontsize=IG_FS_R, fontweight="bold", color=C_YELLOW,
                 va="center", ha="right", transform=head_ax.transAxes)
    head_ax.text(0.04, 0.16, "correlação espúria",
                 fontsize=IG_FS_FOOTER, color="white",
                 va="center", transform=head_ax.transAxes, style="italic")

    # ── Chart no meio (60-65% da altura) ─────────────────────────────
    ax = fig.add_axes([0.13, 0.21, 0.74, 0.55])
    ax.set_facecolor(C_BG)
    ax2 = ax.twinx()

    line_a, = ax.plot(anos, xs, color=C_A, linewidth=3.0, linestyle="-",
                      marker="o", markersize=11,
                      markerfacecolor=C_A, markeredgecolor="white",
                      markeredgewidth=2.0, zorder=4)
    line_b, = ax2.plot(anos, ys, color=C_B, linewidth=3.0,
                       linestyle=(0, (6, 3)),
                       marker="s", markersize=11,
                       markerfacecolor="white", markeredgecolor=C_B,
                       markeredgewidth=2.8, zorder=3)

    # Rótulos curtos para IG (espaço limitado)
    short_a = _wrap_label(label_a, 28)
    short_b = _wrap_label(label_b, 28)
    ax.set_xlabel("Ano", fontsize=IG_FS_AXIS_LABEL, color=C_INK_SOFT)
    ax.set_ylabel(short_a, fontsize=IG_FS_AXIS_LABEL, fontweight="bold",
                  color=C_A, labelpad=8)
    ax2.set_ylabel(short_b, fontsize=IG_FS_AXIS_LABEL, fontweight="bold",
                   color=C_B, labelpad=8, rotation=270, va="bottom")
    ax.tick_params(axis="x", labelsize=IG_FS_TICK)
    ax.tick_params(axis="y", labelsize=IG_FS_TICK, colors=C_A)
    ax2.tick_params(axis="y", labelsize=IG_FS_TICK, colors=C_B)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True,
                                            nbins=min(len(anos), 8)))
    ax.grid(True, color=C_GRID, linestyle="--", linewidth=0.7, alpha=0.9)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("top", "left"):
        ax2.spines[sp].set_visible(False)
    for axis, vals in ((ax, xs), (ax2, ys)):
        vmin, vmax = min(vals), max(vals)
        if vmin == vmax:
            vmin -= 0.5; vmax += 0.5
        pad = (vmax - vmin) * 0.14
        axis.set_ylim(vmin - pad, vmax + pad)

    # ── Footer amarelo com legenda completa (bottom 18%) ─────────────
    foot_ax = fig.add_axes([0, 0, 1, 0.18])
    foot_ax.axis("off")
    foot_ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=C_YELLOW,
                                  transform=foot_ax.transAxes, zorder=0))
    foot_ax.text(0.04, 0.78, "● " + _wrap_label(label_a, 70),
                 fontsize=IG_FS_LEGEND, color=C_INK, fontweight="bold",
                 va="top", transform=foot_ax.transAxes)
    foot_ax.text(0.04, 0.40, "□ " + _wrap_label(label_b, 70),
                 fontsize=IG_FS_LEGEND, color=C_INK, fontweight="bold",
                 va="top", transform=foot_ax.transAxes)
    p_str = f"{p:.3f}" if p >= 0.001 else "< 0,001"
    foot_ax.text(0.96, 0.10,
                 f"n = {n}   p = {p_str}   janela {anos[0]}–{anos[-1]}   "
                 "·   datafolia.com.br",
                 fontsize=IG_FS_FOOTER, color=C_INK_SOFT,
                 va="center", ha="right", transform=foot_ax.transAxes)

    fig.savefig(out_path, dpi=120, facecolor=C_BG, edgecolor="none")
    plt.close(fig)


# ─── 4) CHART IG CAROUSEL (1080x1080) — sem stats, com TITULO ──────────────
def render_chart_ig_carousel(out_path: Path, titulo: str,
                              label_a: str, label_b: str,
                              anos: list[int], xs: list[float],
                              ys: list[float]) -> None:
    """Versao 1:1 (1080x1080) com TITULO do post visivel + eixos + legenda.
    SEM r/p/n — usuario nao quer stats no feed."""
    fig = plt.figure(figsize=(9, 9), dpi=120, facecolor=C_BG)

    # Header verde (top 20%) com brand pequena + titulo grande
    head = fig.add_axes([0, 0.80, 1, 0.20])
    head.axis("off")
    head.add_patch(Rectangle((0, 0), 1, 1, facecolor=C_A,
                              transform=head.transAxes, zorder=0))
    head.text(0.5, 0.84, "DATA FOLIA",
              fontsize=14, fontweight="bold", color=C_YELLOW,
              va="center", ha="center", transform=head.transAxes)
    titulo_wrap = _wrap_label(titulo, 36)
    head.text(0.5, 0.42, titulo_wrap,
              fontsize=24, fontweight="bold", color="white",
              va="center", ha="center", transform=head.transAxes)

    # Chart no meio (50% da altura)
    ax = fig.add_axes([0.14, 0.24, 0.72, 0.50])
    ax.set_facecolor(C_BG)
    ax2 = ax.twinx()

    line_a, = ax.plot(anos, xs, color=C_A, linewidth=3.0, linestyle="-",
                      marker="o", markersize=11,
                      markerfacecolor=C_A, markeredgecolor="white",
                      markeredgewidth=2.0, zorder=4)
    line_b, = ax2.plot(anos, ys, color=C_B, linewidth=3.0,
                       linestyle=(0, (6, 3)),
                       marker="s", markersize=11,
                       markerfacecolor="white", markeredgecolor=C_B,
                       markeredgewidth=2.8, zorder=3)

    short_a = _wrap_label(label_a, 28)
    short_b = _wrap_label(label_b, 28)
    # SEM xlabel "Ano" — os ticks ja sao anos, evita conflito com footer
    ax.set_ylabel(short_a, fontsize=IG_FS_AXIS_LABEL, fontweight="bold",
                  color=C_A, labelpad=8)
    ax2.set_ylabel(short_b, fontsize=IG_FS_AXIS_LABEL, fontweight="bold",
                   color=C_B, labelpad=8, rotation=270, va="bottom")
    ax.tick_params(axis="x", labelsize=IG_FS_TICK)
    ax.tick_params(axis="y", labelsize=IG_FS_TICK, colors=C_A)
    ax2.tick_params(axis="y", labelsize=IG_FS_TICK, colors=C_B)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True,
                                            nbins=min(len(anos), 8)))
    ax.grid(True, color=C_GRID, linestyle="--", linewidth=0.7, alpha=0.9)
    ax.set_axisbelow(True)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    for sp in ("top", "left"):
        ax2.spines[sp].set_visible(False)
    for axis, vals in ((ax, xs), (ax2, ys)):
        vmin, vmax = min(vals), max(vals)
        if vmin == vmax:
            vmin -= 0.5; vmax += 0.5
        pad = (vmax - vmin) * 0.14
        axis.set_ylim(vmin - pad, vmax + pad)

    # Footer amarelo (bottom 20%) com legenda centralizada
    foot = fig.add_axes([0, 0, 1, 0.20])
    foot.axis("off")
    foot.add_patch(Rectangle((0, 0), 1, 1, facecolor=C_YELLOW,
                              transform=foot.transAxes, zorder=0))
    foot.text(0.5, 0.78, "● " + _wrap_label(label_a, 60),
              fontsize=IG_FS_LEGEND, color=C_INK, fontweight="bold",
              va="top", ha="center", transform=foot.transAxes)
    foot.text(0.5, 0.40, "□ " + _wrap_label(label_b, 60),
              fontsize=IG_FS_LEGEND, color=C_INK, fontweight="bold",
              va="top", ha="center", transform=foot.transAxes)
    foot.text(0.5, 0.08, "datafolia.com.br",
              fontsize=IG_FS_FOOTER, color=C_INK_SOFT, fontweight="bold",
              va="center", ha="center", transform=foot.transAxes)

    fig.savefig(out_path, dpi=120, facecolor=C_BG, edgecolor="none")
    plt.close(fig)
