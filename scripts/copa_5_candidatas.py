"""
Gera um PDF com 5 candidatas espurias envolvendo gols dos 3 craques
(CR7, Messi, Neymar) para o tematica Copa do Mundo 2026.

Critério de seleção:
- cada candidato envolve UM dos slugs de gols
- |r| >= 0.85
- n >= 6 anos
- pelo menos um candidato de cada craque, se houver pool

Usuário escolhe 2 das 5.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
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
PDF_OUT = ROOT / "data" / "DataFolia_copa_5_candidatas_gols.pdf"

CRAQUES = {
    "cr7-gols-ano-civil":    ("CR7",    "Gols do Cristiano Ronaldo no ano"),
    "messi-gols-ano-civil":  ("Messi",  "Gols do Messi no ano"),
    "neymar-gols-ano-civil": ("Neymar", "Gols do Neymar no ano"),
}

# slugs ja usados nas 22 publicacoes finais (para evitar repetir)
JA_USADOS = set()
PUBLICATIONS_DIR = ROOT / "publications"
if PUBLICATIONS_DIR.exists():
    for meta_path in PUBLICATIONS_DIR.glob("pub-*/metadata.json"):
        try:
            m = json.loads(meta_path.read_text(encoding="utf-8"))
            JA_USADOS.add(m.get("serie_a"))
            JA_USADOS.add(m.get("serie_b"))
        except Exception:
            pass

MIN_ABS_R = 0.85
MIN_N = 6
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
                series: dict, manifest: dict, craque_label: str) -> None:
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
    fig.suptitle(f"Candidata #{idx}  ·  {craque_label}",
                 fontsize=14, fontweight="bold", color="#0f172a", y=0.975)

    ax_h = fig.add_axes([0.06, 0.78, 0.88, 0.16])
    ax_h.axis("off")
    sign = "positiva" if row["r"] > 0 else "negativa"
    p_str = f"{row['p']:.4f}" if row["p"] >= 0.0001 else "< 0,0001"
    header = (
        f"r = {row['r']:+.4f}   R² = {row['r']**2:.3f}   "
        f"p = {p_str}   n = {row['n']}   "
        f"janela {row['ano_inicio']}-{row['ano_fim']}   correlação {sign}"
    )
    body = (
        header + "\n\n"
        f"Série A (verde, círculo)  ▸ {label_a}\n"
        f"    fonte: {fonte_a}\n\n"
        f"Série B (laranja, quadrado, escala à direita)  ▸ {label_b}\n"
        f"    fonte: {fonte_b}"
    )
    ax_h.text(0, 1, body, va="top", ha="left", fontsize=9.5)

    color_a = "#009C3B"  # verde bandeira
    color_b = "#F97316"  # laranja festa
    ax = fig.add_axes([0.10, 0.36, 0.78, 0.36])
    ax2 = ax.twinx()
    line_a, = ax.plot(anos, xs, color=color_a, linewidth=2.4,
                      linestyle="-", marker="o", markersize=9,
                      markerfacecolor=color_a, markeredgecolor="white",
                      markeredgewidth=1.5, zorder=4,
                      label="A — " + _short(label_a, 60))
    line_b, = ax2.plot(anos, ys, color=color_b, linewidth=2.6,
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
        cell.set_facecolor("#FACC15")  # amarelo bandeira
        cell.set_text_props(weight="bold")

    fig.text(0.5, 0.012,
             "Data Folia — datafolia.com.br · Copa do Mundo 2026 · gols dos craques",
             ha="center", fontsize=8, color="#64748b")
    pdf.savefig(fig); plt.close(fig)


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    series = load_series_data()

    # Le todas as correlacoes envolvendo gols dos 3 craques
    by_craque: dict[str, list[dict]] = {k: [] for k in CRAQUES}
    with ALL_CORR.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            craque = None
            if r["serie_a"] in CRAQUES:
                craque = r["serie_a"]
            elif r["serie_b"] in CRAQUES:
                craque = r["serie_b"]
            if not craque:
                continue
            absr = abs(float(r["r"]))
            n = int(r["n"])
            if absr < MIN_ABS_R or n < MIN_N:
                continue
            other = r["serie_a"] if r["serie_b"] == craque else r["serie_b"]
            # Evitar pares ja publicados
            if other in JA_USADOS:
                continue
            r["r"] = float(r["r"]); r["p"] = float(r["p"])
            r["n"] = n; r["abs_r"] = absr
            r["ano_inicio"] = int(r["ano_inicio"]); r["ano_fim"] = int(r["ano_fim"])
            r["_other"] = other
            r["_craque_slug"] = craque
            by_craque[craque].append(r)

    # Para cada craque, fica so com a melhor janela por par
    pools: dict[str, list[dict]] = {}
    for craque, rows in by_craque.items():
        best_per_pair: dict[str, dict] = {}
        for c in rows:
            o = c["_other"]
            if o not in best_per_pair or best_per_pair[o]["abs_r"] < c["abs_r"]:
                best_per_pair[o] = c
        # ordena por |r| desc
        ranked = sorted(best_per_pair.values(), key=lambda x: -x["abs_r"])
        pools[craque] = ranked
        nome = CRAQUES[craque][0]
        print(f"{nome}: {len(ranked)} pares candidatos (top {min(5,len(ranked))}:)")
        for c in ranked[:5]:
            print(f"   r={c['r']:+.3f} n={c['n']} {c['_other']}")
        print()

    # Seleciona 5 com variedade: ao menos 1 de cada craque, depois embaralha
    chosen: list[dict] = []
    used_others: set[str] = set()
    # Round 1: top de cada craque
    for craque in CRAQUES:
        for c in pools[craque]:
            if c["_other"] not in used_others:
                chosen.append(c)
                used_others.add(c["_other"])
                break
    # Round 2: completa ate 5 com top dos pools que ainda tem material
    all_remaining = []
    for craque, ranked in pools.items():
        for c in ranked:
            if c["_other"] not in used_others:
                all_remaining.append(c)
    # ordena por |r| desc + embaralha um pouco para variedade
    all_remaining.sort(key=lambda x: -x["abs_r"])
    # toma os top 12 e sorteia
    top_pool = all_remaining[:12]
    random.shuffle(top_pool)
    for c in top_pool:
        if len(chosen) >= 5:
            break
        if c["_other"] in used_others:
            continue
        chosen.append(c)
        used_others.add(c["_other"])

    print("\n=== 5 candidatas escolhidas ===")
    for i, c in enumerate(chosen, 1):
        nome = CRAQUES[c["_craque_slug"]][0]
        print(f"#{i}  {nome:<6}  r={c['r']:+.3f} n={c['n']}  vs  {c['_other']}")

    with PdfPages(PDF_OUT) as pdf:
        # Capa
        fig = plt.figure(figsize=(8.5, 11))
        fig.text(0.5, 0.72, "Data Folia", ha="center", fontsize=44,
                 fontweight="bold", color="#009C3B")
        fig.text(0.5, 0.65, "Copa do Mundo 2026", ha="center",
                 fontsize=22, color="#0f172a")
        fig.text(0.5, 0.58, "5 candidatas envolvendo gols de CR7, Messi e Neymar",
                 ha="center", fontsize=13, color="#64748b")
        fig.text(0.5, 0.48,
                 f"Gerado em {dt.datetime.now().strftime('%d/%m/%Y %H:%M')}",
                 ha="center", fontsize=10, color="#64748b")
        fig.text(0.5, 0.42,
                 f"Selecionadas entre pares com |r| ≥ {MIN_ABS_R:.2f} e n ≥ {MIN_N}\n"
                 "Pelo menos 1 de cada craque + variedade",
                 ha="center", fontsize=10, color="#94a3b8")
        fig.text(0.5, 0.20,
                 "Escolha 2 destas para entrar no calendário da Copa.\n"
                 "Correlação não implica causa — estes pares servem para rir.",
                 ha="center", fontsize=10, color="#94a3b8", style="italic")
        pdf.savefig(fig); plt.close(fig)

        for i, row in enumerate(chosen, 1):
            craque_label = CRAQUES[row["_craque_slug"]][1]
            render_page(pdf, i, row, series, manifest, craque_label)

    print(f"\nPDF: {PDF_OUT} ({PDF_OUT.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
