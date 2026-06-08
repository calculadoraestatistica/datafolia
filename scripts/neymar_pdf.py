"""
Gera um PDF com 4 correlacoes envolvendo Neymar (proximas a Copa do Mundo).
Sorteia aleatoriamente entre as candidatas com |r| > 0.7 envolvendo
'neymar-contusoes' (unica serie disponivel) e respeitando supertopicos.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import random
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parent.parent
SERIES_DIR = ROOT / "data" / "series"
MANIFEST_PATH = SERIES_DIR / "_manifest.json"
ALL_CORR = ROOT / "data" / "correlations_all.csv"
PDF_OUT = ROOT / "data" / "DataFolia_neymar_copa_4_candidatas.pdf"

NEYMAR_SLUG = "neymar-contusoes"
MIN_ABS_R = 0.70

# Seed pra reprodutibilidade (mas com timestamp pra ter variedade entre runs)
random.seed(dt.datetime.now().strftime("%Y%m%d-%H"))


def load_series_data() -> dict:
    data = {}
    for csv_path in SERIES_DIR.glob("*.csv"):
        slug = csv_path.stem
        if slug.startswith("_"):
            continue
        rows = {}
        with csv_path.open(encoding="utf-8") as f:
            for line in csv.DictReader(f):
                try:
                    rows[int(line["ano"])] = float(line["valor"])
                except (TypeError, ValueError):
                    continue
        if rows:
            data[slug] = rows
    return data


def _short(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n - 1] + "…"


def _fmt_num(v: float) -> str:
    if abs(v) >= 1000:
        return f"{v:,.0f}".replace(",", ".")
    if abs(v) >= 10:
        return f"{v:.1f}"
    if abs(v) >= 0.01:
        return f"{v:.3f}"
    return f"{v:.5g}"


def render_page(pdf: PdfPages, idx: int, row: dict,
                series: dict, manifest: dict) -> None:
    sa = row["serie_a"]; sb = row["serie_b"]
    info_a = manifest["series"].get(sa, {})
    info_b = manifest["series"].get(sb, {})
    label_a = info_a.get("label", sa)
    label_b = info_b.get("label", sb)
    fonte_a = info_a.get("fonte_nome", "?")
    fonte_b = info_b.get("fonte_nome", "?")
    da = series[sa]; db = series[sb]
    anos = [y for y in sorted(set(da) & set(db))
            if int(row["ano_inicio"]) <= y <= int(row["ano_fim"])]
    xs = [da[y] for y in anos]
    ys = [db[y] for y in anos]

    fig = plt.figure(figsize=(8.5, 11))
    fig.suptitle(f"Candidata #{idx}  ·  Data Folia × Copa do Mundo",
                 fontsize=14, fontweight="bold", color="#0f172a", y=0.975)

    ax_h = fig.add_axes([0.06, 0.78, 0.88, 0.16])
    ax_h.axis("off")
    sign = "positiva" if row["r"] > 0 else "negativa"
    p_str = f"{row['p']:.4f}" if row["p"] >= 0.0001 else "< 0,0001"
    header = (
        f"r = {row['r']:+.4f}   R² = {row['r']**2:.3f}   "
        f"p = {p_str}   n = {row['n']}   "
        f"janela {row['ano_inicio']}–{row['ano_fim']}   correlação {sign}"
    )
    body = (
        header + "\n\n"
        f"Série A (linha azul)  ▸ {label_a}\n"
        f"    fonte: {fonte_a}\n\n"
        f"Série B (linha laranja, escala à direita)  ▸ {label_b}\n"
        f"    fonte: {fonte_b}"
    )
    ax_h.text(0, 1, body, va="top", ha="left", fontsize=9.5)

    color_a = "#1d4ed8"; color_b = "#ea580c"
    ax = fig.add_axes([0.10, 0.36, 0.78, 0.36])
    ax2 = ax.twinx()
    line_a, = ax.plot(anos, xs, color=color_a, linewidth=2.4,
                      linestyle="-", marker="o", markersize=8,
                      markerfacecolor=color_a, markeredgecolor="white",
                      markeredgewidth=1.5, zorder=4,
                      label="A — " + _short(label_a, 60))
    line_b, = ax2.plot(anos, ys, color=color_b, linewidth=2.8,
                       linestyle=(0, (6, 3)), marker="s", markersize=9,
                       markerfacecolor="white", markeredgecolor=color_b,
                       markeredgewidth=2.2, zorder=3,
                       label="B — " + _short(label_b, 60))
    ax.set_xlabel("Ano", fontsize=10, color="#334155")
    ax.set_ylabel(_short(label_a, 45), fontsize=10,
                  color=color_a, fontweight="bold")
    ax.tick_params(axis="y", labelcolor=color_a)
    ax2.set_ylabel(_short(label_b, 45), fontsize=10,
                   color=color_b, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=color_b)
    ax.grid(True, alpha=0.25, linestyle="--", zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=min(len(anos), 12)))
    for axis, vals in ((ax, xs), (ax2, ys)):
        vmin, vmax = min(vals), max(vals)
        if vmin == vmax: vmin -= 0.5; vmax += 0.5
        pad = (vmax - vmin) * 0.10
        axis.set_ylim(vmin - pad, vmax + pad)
    ax.legend([line_a, line_b],
              ["A — " + _short(label_a, 70), "B — " + _short(label_b, 70)],
              loc="upper center", bbox_to_anchor=(0.5, -0.13),
              fontsize=8.5, frameon=False, ncol=1)

    ax_tab = fig.add_axes([0.06, 0.04, 0.88, 0.20])
    ax_tab.axis("off")
    col_a = _short(label_a, 40); col_b = _short(label_b, 40)
    headers = ["Ano", col_a, col_b]
    table_rows = [[str(y), _fmt_num(da[y]), _fmt_num(db[y])] for y in anos]
    tab = ax_tab.table(cellText=table_rows, colLabels=headers,
                       loc="upper center", cellLoc="center",
                       colWidths=[0.10, 0.42, 0.42])
    tab.auto_set_font_size(False); tab.set_fontsize(8); tab.scale(1.0, 1.15)
    for j in range(len(headers)):
        cell = tab[(0, j)]
        cell.set_facecolor("#fed7aa")  # laranja claro pra marcar tema Copa
        cell.set_text_props(weight="bold")

    fig.text(0.5, 0.012,
             "Data Folia — datafolia.com.br · Especial Copa do Mundo (Neymar)",
             ha="center", fontsize=8, color="#64748b")
    pdf.savefig(fig); plt.close(fig)


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    series = load_series_data()
    # Le todas as correlacoes que envolvem Neymar
    candidates = []
    with ALL_CORR.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if NEYMAR_SLUG not in (r["serie_a"], r["serie_b"]):
                continue
            absr = abs(float(r["r"]))
            if absr < MIN_ABS_R:
                continue
            # Pega o melhor janelamento por par (slug_a, slug_b)
            r["r"] = float(r["r"]); r["p"] = float(r["p"])
            r["n"] = int(r["n"]); r["abs_r"] = absr
            r["ano_inicio"] = int(r["ano_inicio"]); r["ano_fim"] = int(r["ano_fim"])
            candidates.append(r)
    # Pra cada serie parceira, fica so com a janela de maior |r|
    best_per_pair: dict = {}
    for c in candidates:
        other = c["serie_a"] if c["serie_b"] == NEYMAR_SLUG else c["serie_b"]
        if other not in best_per_pair or best_per_pair[other]["abs_r"] < c["abs_r"]:
            best_per_pair[other] = c
    pool = list(best_per_pair.values())
    print(f"Candidatas Neymar com |r|>={MIN_ABS_R}: {len(pool)} pares unicos")

    if len(pool) < 4:
        print("AVISO: menos de 4 candidatas disponiveis")
        chosen = pool
    else:
        chosen = random.sample(pool, 4)

    # Ordena pelo |r| desc apenas para apresentacao
    chosen.sort(key=lambda x: -x["abs_r"])

    with PdfPages(PDF_OUT) as pdf:
        # Capa
        fig = plt.figure(figsize=(8.5, 11))
        fig.text(0.5, 0.70, "Data Folia", ha="center", fontsize=44,
                 fontweight="bold", color="#2563eb")
        fig.text(0.5, 0.62, "Especial Copa do Mundo", ha="center",
                 fontsize=20, color="#0f172a")
        fig.text(0.5, 0.56, "4 correlações aleatórias envolvendo o Neymar",
                 ha="center", fontsize=14, color="#64748b")
        fig.text(0.5, 0.46,
                 f"Gerado em {dt.datetime.now().strftime('%d/%m/%Y %H:%M')}",
                 ha="center", fontsize=10, color="#64748b")
        fig.text(0.5, 0.40,
                 f"Selecionadas aleatoriamente entre {len(pool)} pares com "
                 f"|r| ≥ {MIN_ABS_R:.2f}\n"
                 "envolvendo a série 'Contusões registradas do Neymar no ano'",
                 ha="center", fontsize=10, color="#94a3b8")
        fig.text(0.5, 0.20,
                 "Escolha 2 destas para entrar nas publicações da temporada Copa.\n"
                 "Correlação não implica causa — estes pares servem para rir.",
                 ha="center", fontsize=10, color="#94a3b8", style="italic")
        pdf.savefig(fig); plt.close(fig)

        for i, row in enumerate(chosen, 1):
            la = manifest["series"][row["serie_a"]]["label"]
            lb = manifest["series"][row["serie_b"]]["label"]
            print(f"  Cand #{i}  r={row['r']:+.4f}  "
                  f"{row['serie_a']} x {row['serie_b']}")
            print(f"      A: {la}")
            print(f"      B: {lb}")
            render_page(pdf, i, row, series, manifest)

    print(f"\nPDF: {PDF_OUT} ({PDF_OUT.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
