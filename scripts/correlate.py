"""
Motor de correlações Data Folia.

Para cada par de séries:
  - Inner-join por ano (apenas anos onde as duas têm valor)
  - Se a sobreposição é "densa" (gap mediano = 1 ano): janelas consecutivas de 7, 8, 9 e 10 anos
  - Se a sobreposição é "esparsa" (gap > 1, ex.: Copa/Olimpíadas/eleições): janelas de 4 eventos consecutivos
  - Calcula Pearson em cada janela, salva em correlations_all.parquet (ou csv)

Filtros: n >= 5, p < 0.05, |r| >= 0.85. Dedupe por (topic_a, topic_b)
mantendo apenas o maior |r| de cada combinação de tópicos.
"""
from __future__ import annotations

import csv
import itertools
import json
import math
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
SERIES_DIR = ROOT / "data" / "series"
OUT_ALL = ROOT / "data" / "correlations_all.csv"
OUT_TOP = ROOT / "data" / "correlations_top.csv"

WIN_DENSE = [10, 9, 8, 7]
WIN_SPARSE_EVENTS = 4
MIN_N = 5
MIN_ABS_R = 0.80
MAX_P = 0.05


# ===========================================================================
# Mapeamento slug -> topico (para dedupe)
# Series que falam do mesmo "assunto" compartilham o mesmo topic.
# ===========================================================================
TOPICS: dict[str, str] = {
    # Esporte — clubes
    "brasileirao-pontos-flamengo": "flamengo",
    "brasileirao-pontos-palmeiras": "palmeiras",
    "brasileirao-pontos-corinthians": "corinthians",
    "brasileirao-pontos-sao-paulo": "sao-paulo",
    "brasileirao-pontos-santos": "santos",
    "brasileirao-pontos-vasco": "vasco",
    "brasileirao-pontos-fluminense": "fluminense",
    "brasileirao-pontos-botafogo": "botafogo",
    "brasileirao-pontos-atletico-mg": "atletico-mg",
    "brasileirao-pontos-cruzeiro": "cruzeiro",
    "brasileirao-pontos-internacional": "internacional",
    "brasileirao-pontos-gremio": "gremio",
    "flamengo-vitorias-sobre-palmeiras": "flamengo-x-palmeiras",
    "vasco-anos-serie-b-acumulado": "vasco",
    "corinthians-fiel-torcedor-mil": "corinthians",
    "brasileirao-artilheiro-gols": "brasileirao-artilheiro",
    # Esporte — pessoas / eventos
    "neymar-contusoes": "neymar",
    "neymar-gols-ano-civil": "neymar",
    "messi-gols-ano-civil": "messi",
    "cr7-gols-ano-civil": "cr7",
    "copa-mundo-brasil-posicao": "copa-mundo",
    "copa-mundo-brasil-gols": "copa-mundo",
    "olimpiadas-brasil-medalhas": "olimpiadas",
    "olimpiadas-brasil-ouros": "olimpiadas",
    "f1-gp-brasil-publico-mil": "f1-brasil",
    # Pessoas (cultura)
    "idade-ana-maria-braga": "ana-maria-braga",
    "katy-perry-albuns-acumulado": "katy-perry",
    "virginia-seguidores-milhoes": "virginia",
    # Fortunas
    "fortuna-trump-bilhoes-usd": "trump",
    "fortuna-musk-bilhoes-usd": "musk",
    "fortuna-eike-bilhoes-usd": "eike",
    # Mídia / eventos brasileiros
    "bbb-audiencia-final": "bbb",
    "bbb-rejeicao-maxima": "bbb",
    "trends-bbb": "bbb",
    "roberto-carlos-especial-globo": "roberto-carlos",
    "enem-inscritos-milhoes": "enem",
    "enem-abstencao-pct": "enem",
    "enem-abstencao-absoluto-milhoes": "enem",
    "trends-enem": "enem",
    "mega-sena-virada-premio-milhoes": "mega-sena",
    "trends-mega-sena": "mega-sena",
    "evidencias-youtube-views-milhoes": "evidencias",
    "carnaval-rio-publico-milhoes": "carnaval",
    "eleicoes-eleitores-milhoes": "eleicoes-br",
    # Internet / tendências
    "internet-usuarios-pct": "internet-br",
    "trends-vira-lata-caramelo": "vira-lata",
    "trends-pix": "pix",
    "trends-dieta": "dieta",
    "trends-nome-valentina": "nome-valentina",
    "trends-nome-enzo": "nome-enzo",
    "trends-nome-kely": "nome-kely",
    "trends-nome-riquelme": "nome-riquelme",
    "trends-capivaras": "capivara-trend",
    "trends-milei": "milei",
    # Economia / financeiro
    "ipca-acumulado-ano": "ipca",
    "igpm-acumulado-ano": "igpm",
    "selic-fim-de-ano": "selic",
    "dolar-fechamento-ano": "dolar",
    "salario-minimo": "salario-minimo",
    "preco-gasolina": "gasolina",
    "pib-brasil-bilhoes": "pib-br",
    "ibovespa-fechamento-ano": "ibovespa",
    "credito-total-pib": "credito",
    "desemprego-pnadc": "desemprego-br",
    "endividamento-familias": "endividamento",
    "mei-estoque-milhoes": "mei",
    "cesta-basica-dieese-sp": "cesta-basica",
    "alpargatas-receita-bilhoes-rs": "alpargatas",
    # Demografia / saúde
    "populacao-brasil": "populacao-br",
    "casamentos-brasil-mil": "casamentos-br",
    "divorcios-brasil-mil": "divorcios-br",
    "acidentes-transito-obitos": "acidentes-br",
    "inss-fila-milhoes": "inss",
    # Agro / ambiente
    "soja-exportada-milhoes-ton": "soja",
    "cafe-exportado-milhoes-sacas": "cafe",
    "gado-cabecas-milhoes": "gado",
    "queimadas-brasil-focos": "queimadas",
    "desmatamento-amazonia-km2": "desmatamento",
    "capivaras-tiete-mil": "capivara-tiete",
    # Consumo
    "turistas-estrangeiros-milhoes": "turistas-br",
    "veiculos-vendidos-milhoes": "veiculos",
    "motos-vendidas-mil": "motos",
    "ovo-pascoa-preco-medio-rs": "ovo-pascoa",
    "havaianas-vendidas-br-milhoes": "havaianas",
    "havaianas-vendidas-ext-milhoes": "havaianas",
    "sorvete-baunilha-mundo-bilhoes-usd": "sorvete-baunilha",
    "pistache-mundo-mil-toneladas": "pistache",
    "bitcoin-fechamento-usd": "bitcoin",
    # Internacional
    "coelhos-australia-milhoes": "coelhos-au",
    "desemprego-russia-pct": "desemprego-ru",
    "desemprego-argentina-pct": "desemprego-ar",
    "populacao-japao-milhoes": "japao",
    "populacao-costa-rica-milhoes": "costa-rica",
    "populacao-panama-milhoes": "panama",
    "populacao-guatemala-milhoes": "guatemala",
    "populacao-honduras-milhoes": "honduras",
    "milei-aprovacao-pct": "milei",
    # Internacional — World Bank (Copa do Mundo)
    "pib-uruguai-bilhoes-usd":     "uruguai",
    "desemprego-uruguai-pct":      "uruguai",
    "pib-italia-bilhoes-usd":      "italia",
    "desemprego-italia-pct":       "italia",
    "pib-alemanha-bilhoes-usd":    "alemanha",
    "desemprego-alemanha-pct":     "alemanha",
    "pib-inglaterra-bilhoes-usd":  "inglaterra",
    "desemprego-inglaterra-pct":   "inglaterra",
    "pib-franca-bilhoes-usd":      "franca",
    "desemprego-franca-pct":       "franca",
    "pib-espanha-bilhoes-usd":     "espanha",
    "desemprego-espanha-pct":      "espanha",
    "pib-mexico-bilhoes-usd":      "mexico",
    "desemprego-mexico-pct":       "mexico",
    "pib-canada-bilhoes-usd":      "canada",
    "desemprego-canada-pct":       "canada",
    "pib-curacao-bilhoes-usd":     "curacao",
    "pib-argentina-bilhoes-usd":   "argentina",
}


def load_series() -> dict[str, dict[int, float]]:
    out = {}
    for csv_path in sorted(SERIES_DIR.glob("*.csv")):
        slug = csv_path.stem
        if slug.startswith("_"):
            continue
        rows = {}
        with csv_path.open(encoding="utf-8") as f:
            r = csv.DictReader(f)
            for line in r:
                try:
                    rows[int(line["ano"])] = float(line["valor"])
                except (TypeError, ValueError):
                    continue
        if rows:
            out[slug] = rows
    return out


def pearson(xs: list[float], ys: list[float]) -> tuple[float, float] | None:
    """Pearson r + t-test p-valor bicaudal. None se variância zero."""
    n = len(xs)
    if n < 3:
        return None
    mx = mean(xs); my = mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    if sxx == 0 or syy == 0:
        return None
    r = sxy / math.sqrt(sxx * syy)
    if r > 1: r = 1
    if r < -1: r = -1
    # t-statistic e p-valor via aproximação Student-t cdf usando beta incompleta
    if abs(r) >= 0.99999:
        return (r, 0.0)
    df = n - 2
    t = r * math.sqrt(df) / math.sqrt(1 - r * r)
    p = 2 * (1 - _t_cdf(abs(t), df))
    return (r, p)


# ---- distribuição t de Student (cdf) via beta incompleta -----------------
def _gammaln(x: float) -> float:
    coef = [76.18009172947146, -86.50532032941677, 24.01409824083091,
            -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5]
    y = x; tmp = x + 5.5
    tmp -= (x + 0.5) * math.log(tmp)
    ser = 1.000000000190015
    for j in range(6):
        y += 1; ser += coef[j] / y
    return -tmp + math.log(2.5066282746310005 * ser / x)


def _betacf(a: float, b: float, x: float) -> float:
    MAXIT = 200; EPS = 3e-12; FPMIN = 1e-300
    qab = a + b; qap = a + 1; qam = a - 1
    c = 1; d = 1 - qab * x / qap
    if abs(d) < FPMIN: d = FPMIN
    d = 1 / d
    h = d
    for m in range(1, MAXIT + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1 + aa * d
        if abs(d) < FPMIN: d = FPMIN
        c = 1 + aa / c
        if abs(c) < FPMIN: c = FPMIN
        d = 1 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1 + aa * d
        if abs(d) < FPMIN: d = FPMIN
        c = 1 + aa / c
        if abs(c) < FPMIN: c = FPMIN
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < EPS:
            break
    return h


def _betai(a: float, b: float, x: float) -> float:
    if x <= 0: return 0
    if x >= 1: return 1
    bt = math.exp(_gammaln(a + b) - _gammaln(a) - _gammaln(b)
                  + a * math.log(x) + b * math.log(1 - x))
    if x < (a + 1) / (a + b + 2):
        return bt * _betacf(a, b, x) / a
    return 1 - bt * _betacf(b, a, 1 - x) / b


def _t_cdf(t: float, df: float) -> float:
    x = df / (df + t * t)
    ib = _betai(df / 2, 0.5, x)
    return 1 - 0.5 * ib if t > 0 else 0.5 * ib


# ---- janelas -------------------------------------------------------------
def windows_for(years: list[int]) -> list[list[int]]:
    """Gera janelas baseado na densidade da sobreposição."""
    if len(years) < MIN_N:
        return []
    ys = sorted(years)
    gaps = [ys[i + 1] - ys[i] for i in range(len(ys) - 1)]
    median_gap = sorted(gaps)[len(gaps) // 2]
    out = []
    if median_gap <= 1:
        # Densa: janelas de WIN_DENSE anos consecutivos
        for k in WIN_DENSE:
            if k > len(ys):
                continue
            for i in range(len(ys) - k + 1):
                sub = ys[i:i + k]
                # Aceitamos janelas com 1 ou 2 anos faltando (gap>1) — densas mas com furos
                if sub[-1] - sub[0] <= k + 2:
                    out.append(sub)
    else:
        # Esparsa: WIN_SPARSE_EVENTS eventos consecutivos
        k = WIN_SPARSE_EVENTS
        if k <= len(ys):
            for i in range(len(ys) - k + 1):
                out.append(ys[i:i + k])
    # Sempre incluir a sobreposição completa se for >= MIN_N
    if len(ys) >= MIN_N and ys not in out:
        out.append(ys)
    return out


# ---- run -----------------------------------------------------------------
def main() -> None:
    series = load_series()
    print(f"Series carregadas: {len(series)}")
    rows = []
    slugs = sorted(series.keys())
    for i, sa in enumerate(slugs):
        for sb in slugs[i + 1:]:
            ta = TOPICS.get(sa)
            tb = TOPICS.get(sb)
            if ta is None or tb is None:
                continue
            if ta == tb:
                continue  # mesma topica = correlação óbvia, pula
            da = series[sa]
            db = series[sb]
            common = sorted(set(da) & set(db))
            wins = windows_for(common)
            for win in wins:
                xs = [da[y] for y in win]
                ys = [db[y] for y in win]
                res = pearson(xs, ys)
                if res is None:
                    continue
                r, p = res
                if abs(r) < MIN_ABS_R or p > MAX_P:
                    continue
                rows.append((sa, sb, ta, tb, win[0], win[-1], len(win), r, p, abs(r)))
        if (i + 1) % 10 == 0:
            print(f"  ... processado {i+1}/{len(slugs)} series, rows acumulados {len(rows)}")

    rows.sort(key=lambda r: -r[-1])
    # Salva TODOS
    with OUT_ALL.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["serie_a", "serie_b", "topic_a", "topic_b",
                    "ano_inicio", "ano_fim", "n", "r", "p", "abs_r"])
        for row in rows:
            w.writerow(row)
    print(f"Total de janelas com |r|>={MIN_ABS_R} e p<{MAX_P}: {len(rows)}")
    print(f"Salvo em {OUT_ALL}")


if __name__ == "__main__":
    main()
