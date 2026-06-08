"""
Top 30 correlações: dedupe agressivo (1 por tópico), composite scoring
(prioriza correlações negativas e séries não-lineares no tempo), gera PDF
com APENAS o gráfico de duas séries em eixos Y duplos e tabela com
nomes reais. Email com PDF anexo.
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator

ROOT = Path(__file__).resolve().parent.parent
SERIES_DIR = ROOT / "data" / "series"
MANIFEST_PATH = SERIES_DIR / "_manifest.json"
ALL_CORR = ROOT / "data" / "correlations_all.csv"
TOP_CSV = ROOT / "data" / "correlations_top40.csv"
PDF_OUT = ROOT / "data" / "DataFolia_top40_correlacoes.pdf"

TOP_N = 40
MAX_PER_TOPIC = 3                  # 40 com 1x e impossivel, 2x e apertado; 3x da espaco
LINEARITY_NONLIN = 0.85            # max(linearidade) < isso = altamente nao-linear
LINEARITY_LINEAR = 0.80            # max(linearidade) >= isso = "mais linear"

# Series explicitamente excluidas do estudo (pedido do Vinicius)
SLUGS_EXCLUIDOS: set[str] = {
    "populacao-costa-rica-milhoes",
    "trends-vira-lata-caramelo",
}

# Topicos com alto potencial de comedia / surpresa (cultura pop, celebridades,
# animais, alimentos, esportes simbolicos). Usados pra rankear "engracadice".
FUNNY_TOPICS: set[str] = {
    # Animais
    "capivara-tiete", "coelhos-au", "vira-lata",
    # Celebridades
    "ana-maria-braga", "katy-perry", "virginia", "trump", "musk", "eike",
    "messi", "neymar", "milei",
    # Pop culture brasileiro
    "bbb", "roberto-carlos", "mega-sena", "evidencias", "carnaval", "f1-brasil",
    # Comidas / consumo curioso
    "ovo-pascoa", "sorvete-baunilha", "pistache", "havaianas",
    # Esportes simbolicos (eventos pontuais)
    "copa-mundo", "olimpiadas",
    # Times de futebol como personagens
    "flamengo", "palmeiras", "corinthians", "sao-paulo", "santos", "vasco",
    "fluminense", "botafogo", "atletico-mg", "cruzeiro", "internacional", "gremio",
    "brasileirao-artilheiro", "flamengo-x-palmeiras",
    # Nomes (curiosidade onomastica)
    "nome-valentina", "nome-enzo", "nome-kely", "nome-riquelme",
    # Trends culturais
    "trends-bbb", "trends-enem", "trends-pix", "trends-mega-sena",
    "trends-milei", "capivara-trend", "dieta",
    # Eventos sociais
    "eleicoes-br",
    # Internacional "exotico"
    "japao", "panama", "guatemala", "honduras",
    "desemprego-ru", "desemprego-ar",
    # Eike é icone do "boom e queda" — sempre rende
    "alpargatas",  # marca cultural
}

BONUS_FUN_BOTH = 0.20
BONUS_FUN_ONE = 0.10
PENALTY_FUN_NONE = 0.15

# Quotas para o top 40:
QUOTAS = [
    ("highly_nonlin", 30),         # altamente nao-linear (qualquer sinal)
    ("linear_neg",    10),         # mais linear E correlacao negativa
]

# "Supertopicos" — pares de topicos no mesmo supertopico sao DESCARTADOS
# porque suas correlacoes refletem o mesmo fenomeno (Dolar x Ibovespa = mercado).
SUPERTOPIC = {
    # Mercado financeiro brasileiro (movem juntos)
    "dolar": "mercado-financeiro-br",
    "ibovespa": "mercado-financeiro-br",
    "selic": "mercado-financeiro-br",
    # Inflacao (todos os indices se movem juntos)
    "ipca": "inflacao",
    "igpm": "inflacao",
    "salario-minimo": "inflacao",
    "cesta-basica": "inflacao",
    "gasolina": "inflacao",
    # Brasileirao (clubes/competicao mesma realidade)
    "flamengo": "brasileirao",
    "palmeiras": "brasileirao",
    "corinthians": "brasileirao",
    "sao-paulo": "brasileirao",
    "santos": "brasileirao",
    "vasco": "brasileirao",
    "fluminense": "brasileirao",
    "botafogo": "brasileirao",
    "atletico-mg": "brasileirao",
    "cruzeiro": "brasileirao",
    "internacional": "brasileirao",
    "gremio": "brasileirao",
    "brasileirao-artilheiro": "brasileirao",
    "flamengo-x-palmeiras": "brasileirao",
    # Agro brasileiro (cresce junto)
    "soja": "agro-br",
    "cafe": "agro-br",
    "gado": "agro-br",
    # Ambiente Amazonia (mesmo fenomeno)
    "queimadas": "ambiente-amazonia",
    "desmatamento": "ambiente-amazonia",
    # Demografia BR (todas crescem com populacao)
    "populacao-br": "demografia-br",
    "casamentos-br": "demografia-br",
    "divorcios-br": "demografia-br",
    "acidentes-br": "demografia-br",
}


# ===========================================================================
# Carregamento
# ===========================================================================
def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_series_data() -> dict[str, dict[int, float]]:
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


def pearson_r(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx = sum(xs) / n; my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    if sxx == 0 or syy == 0:
        return 0.0
    return sxy / math.sqrt(sxx * syy)


def linearity_score(series_data: dict[int, float]) -> float:
    """|corr(ano, valor)| — quanto mais perto de 1, mais linear no tempo."""
    anos = sorted(series_data)
    if len(anos) < 3:
        return 0.0
    xs = anos
    ys = [series_data[a] for a in anos]
    return abs(pearson_r(xs, ys))


# ===========================================================================
# Dedup + scoring
# ===========================================================================
def load_all_rows() -> list[dict]:
    rows = []
    with ALL_CORR.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["r"] = float(r["r"])
            r["p"] = float(r["p"])
            r["n"] = int(r["n"])
            r["abs_r"] = float(r["abs_r"])
            r["ano_inicio"] = int(r["ano_inicio"])
            r["ano_fim"] = int(r["ano_fim"])
            rows.append(r)
    return rows


def categorize(r: dict) -> str:
    """
    Categoriza para as quotas atuais (top 40):
      - highly_nonlin: max(linearity_a, linearity_b) < LINEARITY_NONLIN
        Pelo menos uma das duas series tem oscilacao bem clara
        (nao e simplesmente "tudo cresce").
      - linear_neg:   max(linearity) >= LINEARITY_LINEAR  e  r < 0
        Series mais monotonicas, mas correlacao negativa (uma sobe enquanto
        a outra cai), o que ja garante uma narrativa visual interessante.
      - other:        sobra (positivas lineares — nao entram nas quotas).
    """
    la = r["linearity_a"]; lb = r["linearity_b"]
    max_lin = max(la, lb)
    if max_lin < LINEARITY_NONLIN:
        return "highly_nonlin"
    if r["r"] < 0 and max_lin >= LINEARITY_LINEAR:
        return "linear_neg"
    return "other"


def annotate(rows: list[dict], linearity: dict[str, float]) -> list[dict]:
    out = []
    for r in rows:
        # Descartar pares com series excluidas
        if r["serie_a"] in SLUGS_EXCLUIDOS or r["serie_b"] in SLUGS_EXCLUIDOS:
            continue
        r["linearity_a"] = linearity.get(r["serie_a"], 0)
        r["linearity_b"] = linearity.get(r["serie_b"], 0)
        r["is_negative"] = r["r"] < 0
        r["both_linear"] = (
            r["linearity_a"] >= LINEARITY_LINEAR
            and r["linearity_b"] >= LINEARITY_LINEAR
        )
        r["categoria"] = categorize(r)
        # Score "engracadice"
        fa = r["topic_a"] in FUNNY_TOPICS
        fb = r["topic_b"] in FUNNY_TOPICS
        fun_bonus = 0.0
        if fa and fb:
            fun_bonus = BONUS_FUN_BOTH
        elif fa or fb:
            fun_bonus = BONUS_FUN_ONE
        else:
            fun_bonus = -PENALTY_FUN_NONE
        r["fun_bonus"] = fun_bonus
        r["fun_score"] = r["abs_r"] + fun_bonus
        r["fun_a"] = fa
        r["fun_b"] = fb
        out.append(r)
    # Ordem: fun_score descendente (DENTRO DE CADA categoria a quota selecionara)
    out.sort(key=lambda x: -x["fun_score"])
    return out


def select_with_quotas(all_rows: list[dict]) -> list[dict]:
    seen_pairs: set = set()
    topic_count: dict[str, int] = {}
    out: list[dict] = []

    def pair_ok(r: dict) -> bool:
        ta = r["topic_a"]; tb = r["topic_b"]
        if ta == tb:
            return False
        # Mesmo supertopico = correlacao real, descarta
        sa = SUPERTOPIC.get(ta); sb = SUPERTOPIC.get(tb)
        if sa is not None and sa == sb:
            return False
        pair = tuple(sorted((ta, tb)))
        if pair in seen_pairs:
            return False
        if topic_count.get(ta, 0) >= MAX_PER_TOPIC:
            return False
        if topic_count.get(tb, 0) >= MAX_PER_TOPIC:
            return False
        return True

    for category, n_target in QUOTAS:
        picked = 0
        for r in all_rows:
            if r["categoria"] != category:
                continue
            if not pair_ok(r):
                continue
            ta = r["topic_a"]; tb = r["topic_b"]
            seen_pairs.add(tuple(sorted((ta, tb))))
            topic_count[ta] = topic_count.get(ta, 0) + 1
            topic_count[tb] = topic_count.get(tb, 0) + 1
            out.append(r)
            picked += 1
            if picked >= n_target:
                break
        if picked < n_target:
            print(f"  AVISO: categoria '{category}' só conseguiu {picked}/{n_target}")

    # Reordena: altamente nao-lineares primeiro, depois lineares negativas
    cat_order = {"highly_nonlin": 0, "linear_neg": 1, "other": 2}
    out.sort(key=lambda r: (cat_order.get(r["categoria"], 99), -r["abs_r"]))
    return out


# ===========================================================================
# PDF
# ===========================================================================
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
    win_years = [y for y in sorted(set(da) & set(db))
                 if row["ano_inicio"] <= y <= row["ano_fim"]]
    xs = [da[y] for y in win_years]
    ys = [db[y] for y in win_years]

    fig = plt.figure(figsize=(8.5, 11))
    # ---- Título e header ------------------------------------------------
    fig.suptitle(f"#{idx:02d}  Correlação espúria — Data Folia",
                 fontsize=14, fontweight="bold", color="#0f172a", y=0.975)

    ax_h = fig.add_axes([0.06, 0.78, 0.88, 0.16])
    ax_h.axis("off")
    sign = "positiva" if row["r"] > 0 else "negativa"
    p_str = f"{row['p']:.4f}" if row["p"] >= 0.0001 else "< 0,0001"
    cat_human = {
        "highly_nonlin": "ALTAMENTE NÃO-LINEAR (oscilação clara em pelo menos uma das séries)",
        "linear_neg":    "MAIS LINEAR, CORRELAÇÃO NEGATIVA (uma sobe, a outra cai)",
        "other":         "—",
    }
    header = (
        f"r = {row['r']:+.4f}   R² = {row['r']**2:.3f}   "
        f"p = {p_str}   n = {row['n']}   "
        f"janela {row['ano_inicio']}–{row['ano_fim']}\n"
        f"categoria: {cat_human.get(row.get('categoria','?'),'?')}"
    )
    body = (
        header + "\n\n"
        f"Série A (linha azul)  ▸ {label_a}\n"
        f"    fonte: {fonte_a}\n\n"
        f"Série B (linha laranja, escala à direita)  ▸ {label_b}\n"
        f"    fonte: {fonte_b}"
    )
    ax_h.text(0, 1, body, va="top", ha="left", fontsize=9.5)

    # ---- Gráfico ÚNICO: duas séries em eixos duplos ---------------------
    color_a = "#1d4ed8"   # azul profundo
    color_b = "#ea580c"   # laranja quente
    ax = fig.add_axes([0.10, 0.36, 0.78, 0.36])
    ax2 = ax.twinx()

    # Linha A: sólida, marcador cheio (círculo)
    line_a, = ax.plot(win_years, xs, color=color_a, linewidth=2.4,
                      linestyle="-",
                      marker="o", markersize=8, markerfacecolor=color_a,
                      markeredgecolor="white", markeredgewidth=1.5,
                      label="A — " + _short(label_a, 60), zorder=4)
    # Linha B: tracejada (dash), marcador VAZADO (quadrado oco) para
    # diferenciar mesmo quando se sobrepõe à linha A
    line_b, = ax2.plot(win_years, ys, color=color_b, linewidth=2.8,
                       linestyle=(0, (6, 3)),     # dash 6 / gap 3
                       marker="s", markersize=9, markerfacecolor="white",
                       markeredgecolor=color_b, markeredgewidth=2.2,
                       label="B — " + _short(label_b, 60), zorder=3)

    ax.set_xlabel("Ano", fontsize=10, color="#334155")
    ax.set_ylabel(_short(label_a, 45), fontsize=10, color=color_a, fontweight="bold")
    ax.tick_params(axis="y", labelcolor=color_a)
    ax2.set_ylabel(_short(label_b, 45), fontsize=10, color=color_b, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=color_b)
    ax.grid(True, alpha=0.25, linestyle="--", zorder=0)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)
    # Eixo X com ticks inteiros (anos)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True, nbins=min(len(win_years), 12)))

    # Ajusta margens para que as duas séries fiquem visualmente comparáveis:
    # cada eixo ganha ~10% de folga acima e abaixo do seu próprio range.
    for axis, vals in ((ax, xs), (ax2, ys)):
        vmin, vmax = min(vals), max(vals)
        if vmin == vmax:
            vmin -= 0.5; vmax += 0.5
        pad = (vmax - vmin) * 0.10
        axis.set_ylim(vmin - pad, vmax + pad)

    # Legenda combinada abaixo do gráfico
    ax.legend([line_a, line_b],
              ["A — " + _short(label_a, 70), "B — " + _short(label_b, 70)],
              loc="upper center", bbox_to_anchor=(0.5, -0.13), fontsize=8.5,
              frameon=False, ncol=1)

    # ---- Tabela com nomes reais nas colunas -----------------------------
    ax_tab = fig.add_axes([0.06, 0.04, 0.88, 0.20])
    ax_tab.axis("off")
    col_a = _short(label_a, 40)
    col_b = _short(label_b, 40)
    headers = ["Ano", col_a, col_b]
    table_rows = [[str(y), _fmt_num(da[y]), _fmt_num(db[y])] for y in win_years]
    tab = ax_tab.table(cellText=table_rows, colLabels=headers,
                       loc="upper center", cellLoc="center",
                       colWidths=[0.10, 0.42, 0.42])
    tab.auto_set_font_size(False)
    tab.set_fontsize(8)
    tab.scale(1.0, 1.15)
    for j in range(len(headers)):
        cell = tab[(0, j)]
        cell.set_facecolor("#e0e7ff")
        cell.set_text_props(weight="bold")

    fig.text(0.5, 0.012,
             "Data Folia — datafolia.com.br · correlações espúrias por entretenimento",
             ha="center", fontsize=8, color="#64748b")

    pdf.savefig(fig)
    plt.close(fig)


def _short(s: str, maxlen: int) -> str:
    if len(s) <= maxlen:
        return s
    return s[: maxlen - 1] + "…"


def _fmt_num(v: float) -> str:
    if abs(v) >= 1000:
        return f"{v:,.0f}".replace(",", ".")
    if abs(v) >= 10:
        return f"{v:.1f}"
    if abs(v) >= 0.01:
        return f"{v:.3f}"
    return f"{v:.5g}"


# ===========================================================================
# Main
# ===========================================================================
def main() -> None:
    manifest = load_manifest()
    series = load_series_data()
    print(f"Series carregadas: {len(series)}")

    # Linearidade no tempo de cada serie
    linearity = {slug: linearity_score(data) for slug, data in series.items()}
    very_linear = sorted(
        ((s, l) for s, l in linearity.items() if l > LINEARITY_LINEAR),
        key=lambda x: -x[1],
    )
    print(f"Series 'lineares no tempo' (|corr(ano,valor)| > {LINEARITY_LINEAR}): "
          f"{len(very_linear)} de {len(linearity)}")

    rows = load_all_rows()
    print(f"Total de janelas carregadas: {len(rows)}")
    rows = annotate(rows, linearity)
    top = select_with_quotas(rows)
    print(f"Top selecionado por quotas (1 por tópico + filtro de supertópicos): {len(top)}")

    # Salva CSV top
    with TOP_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "categoria", "label_a", "label_b",
                    "serie_a", "serie_b", "topic_a", "topic_b",
                    "ano_inicio", "ano_fim", "n", "r", "p",
                    "linearity_a", "linearity_b"])
        for i, r in enumerate(top, 1):
            la = manifest["series"][r["serie_a"]]["label"]
            lb = manifest["series"][r["serie_b"]]["label"]
            w.writerow([i, r["categoria"], la, lb,
                        r["serie_a"], r["serie_b"], r["topic_a"], r["topic_b"],
                        r["ano_inicio"], r["ano_fim"], r["n"],
                        f"{r['r']:.4f}", f"{r['p']:.6f}",
                        f"{r['linearity_a']:.3f}", f"{r['linearity_b']:.3f}"])

    # Estatísticas do top
    n_hnl = sum(1 for r in top if r["categoria"] == "highly_nonlin")
    n_lneg = sum(1 for r in top if r["categoria"] == "linear_neg")

    # PDF
    with PdfPages(PDF_OUT) as pdf:
        # Capa
        fig = plt.figure(figsize=(8.5, 11))
        fig.text(0.5, 0.70, "Data Folia", ha="center", fontsize=48,
                 fontweight="bold", color="#2563eb")
        fig.text(0.5, 0.62, "Top 40 correlações espúrias", ha="center",
                 fontsize=18, color="#0f172a")
        fig.text(0.5, 0.55, "Brasil + alguns vizinhos curiosos",
                 ha="center", fontsize=13, color="#64748b")
        fig.text(0.5, 0.42,
                 f"Gerado em {dt.datetime.now().strftime('%d/%m/%Y %H:%M')}",
                 ha="center", fontsize=10, color="#64748b")
        fig.text(0.5, 0.36,
                 f"{len(series)} séries · {len(rows):,} janelas com |r|≥0,80"
                 .replace(",", "."),
                 ha="center", fontsize=10, color="#64748b")
        fig.text(0.5, 0.32,
                 "Distribuição alvo: 30 altamente não-lineares + 10 mais lineares e negativas\n"
                 "Pares onde ambos os tópicos pertencem ao mesmo supertópico\n"
                 "(ex.: Dólar × Ibovespa = mercado financeiro) foram descartados",
                 ha="center", fontsize=9, color="#94a3b8")
        fig.text(0.5, 0.22,
                 f"Composição real do top 40: "
                 f"{n_hnl} altamente não-lineares · {n_lneg} mais lineares com r<0",
                 ha="center", fontsize=10, color="#0f172a")
        fig.text(0.5, 0.10,
                 "Correlação não implica causa. Estes pares foram encontrados\n"
                 "por força bruta entre séries de assuntos não relacionados —\n"
                 "servem para rir, não para concluir.",
                 ha="center", fontsize=10, color="#94a3b8", style="italic")
        pdf.savefig(fig); plt.close(fig)

        for i, row in enumerate(top, 1):
            la = manifest["series"][row["serie_a"]]["label"]
            lb = manifest["series"][row["serie_b"]]["label"]
            print(f"  #{i:02d}  r={row['r']:+.4f}  cat={row['categoria']:11s}  "
                  f"lin=({row['linearity_a']:.2f},{row['linearity_b']:.2f})")
            print(f"       A: {la}")
            print(f"       B: {lb}")
            render_page(pdf, i, row, series, manifest)

    print(f"\nPDF: {PDF_OUT}  ({PDF_OUT.stat().st_size/1024:.1f} KB)")


if __name__ == "__main__":
    main()
