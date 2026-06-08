"""
Adiciona 2 publicacoes da Copa do Mundo escolhidas pelo usuario:
- pub-28-cr7-x-desemprego-alemanha  -> Quinta 09/07/2026 (entre quartas e semifinal)
- pub-29-neymar-x-salario-minimo    -> Quinta 25/06/2026 (entre fase de grupos e oitavas)

Gera tudo o que as outras pubs ja tem: metadata, csv, charts, artigo, caption,
prompt e atualiza publications/_index.json.
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from statistics import mean

from chart_renderer import (
    render_chart_site, render_table_site, render_chart_instagram,
)

ROOT = Path(__file__).resolve().parent.parent
SERIES_DIR = ROOT / "data" / "series"
MANIFEST_PATH = SERIES_DIR / "_manifest.json"
PUB_DIR = ROOT / "publications"

# ----------------------------------------------------------------------
NOVAS_PUBS = [
    {
        "id":            "pub-28-cr7-x-desemprego-alemanha",
        "slug_a":        "cr7-gols-ano-civil",
        "slug_b":        "desemprego-alemanha-pct",
        "topic_a":       "cr7",
        "topic_b":       "alemanha",
        "ano_inicio":    2004,
        "ano_fim":       2013,
        "data_post":     "2026-07-09",   # Quinta entre quartas e semis
        "data_post_dia_semana": "thursday",
        "tema_calendario":      "copa-do-mundo-bonus-rota-alemanha",
        "titulo":        "A Rota Alemã do Bicampeão Português",
        "ordem_curadoria":     28,
        "rank_no_top40":       None,
        "categoria":           "highly_nonlin",
        "story": (
            "A teoria começa numa observação descontextualizada: enquanto Cristiano "
            "Ronaldo subia de 11 para 69 gols por ano civil, o desemprego alemão caía "
            "ininterruptamente de 10,4% para 5,2%. Dois fenômenos sem qualquer "
            "vizinhança causal — e ainda assim, perfeitamente coreografados.\n\n"
            "A explicação fictícia favorita por aqui é a doutrina do *efeito Mannschaft "
            "invertido*. Cada gol do português obrigaria os tecnocratas alemães a "
            "recalibrar a economia, reforçando a Reforma Hartz com mais determinação "
            "germânica, só para não admitir que um lusitano marcou o tempo histórico da "
            "Europa.\n\n"
            "Nessa leitura, o craque luso é variável macroeconômica disfarçada de "
            "ponta. Cada finalização sua aciona um conselho silencioso em Frankfurt que "
            "imediatamente abre vagas em Stuttgart. A correlação durou exatos dez anos, "
            "exatamente o tempo entre Ronaldo virar profissional e a Alemanha vencer a "
            "Copa de 2014.\n\n"
            "É claro que crescimento alemão se explica por demografia, reformas "
            "trabalhistas e o ciclo expansivo da década. Mas a coreografia é tão "
            "perfeita que dá vontade de pedir um café preto em Munique e dedicar a "
            "próxima vaga aberta a Cristiano."
        ),
    },
    {
        "id":            "pub-29-neymar-x-salario-minimo",
        "slug_a":        "neymar-gols-ano-civil",
        "slug_b":        "salario-minimo",
        "topic_a":       "neymar",
        "topic_b":       "salario-minimo",
        "ano_inicio":    2015,
        "ano_fim":       2021,
        "data_post":     "2026-06-25",   # Quinta entre grupos e oitavas
        "data_post_dia_semana": "thursday",
        "tema_calendario":      "copa-do-mundo-bonus-fim-de-grupos",
        "titulo":        "A Inflação que Engole o Camisa Dez",
        "ordem_curadoria":     29,
        "rank_no_top40":       None,
        "categoria":           "highly_nonlin",
        "story": (
            "Entre 2015 e 2021 o salário mínimo brasileiro foi corrigido de R$ 788 para "
            "R$ 1.100. No mesmo período Neymar saiu de 49 gols por ano para 14. Subiu "
            "uma curva, desabou a outra, e o coeficiente parece desenhado a régua.\n\n"
            "A teoria espúria favorita é a *hipótese do contrapeso fiscal*. Em algum "
            "balanço imaginário da economia brasileira, cada centavo a mais no piso "
            "salarial seria descontado da finalização do camisa 10 — como se Brasília "
            "estivesse usando o pé direito do craque como fundo de equalização "
            "monetária.\n\n"
            "É só a teoria não funcionar para Neymar marcar três contra a Suécia. Para "
            "rebaixar a inflação, basta ele acertar o ângulo. Política monetária "
            "ortodoxa, mas com chuteira.\n\n"
            "Na vida real, a queda dos gols tem causas conhecidas: lesões repetidas, "
            "transferência ao PSG, calendário travado. Mas para quem gosta de "
            "explicações cruzadas, a curva parece dizer que o Plano Real e o departamento "
            "médico do Parque dos Príncipes assinaram o mesmo memorando."
        ),
    },
]


# ----------------------------------------------------------------------
def pearson(xs: list[float], ys: list[float]) -> tuple[float, float]:
    n = len(xs); mx = mean(xs); my = mean(ys)
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    r = sxy / math.sqrt(sxx * syy)
    if abs(r) >= 0.99999:
        return (r, 0.0)
    df = n - 2
    t = r * math.sqrt(df) / math.sqrt(1 - r * r)
    p = 2 * (1 - _t_cdf(abs(t), df))
    return (r, p)


def _gammaln(x):
    coef = [76.18009172947146, -86.50532032941677, 24.01409824083091,
            -1.231739572450155, 0.1208650973866179e-2, -0.5395239384953e-5]
    y = x; tmp = x + 5.5; tmp -= (x + 0.5) * math.log(tmp); ser = 1.000000000190015
    for j in range(6):
        y += 1; ser += coef[j] / y
    return -tmp + math.log(2.5066282746310005 * ser / x)

def _betacf(a, b, x):
    MAXIT=200; EPS=3e-12; FPMIN=1e-300
    qab=a+b; qap=a+1; qam=a-1; c=1; d=1-qab*x/qap
    if abs(d)<FPMIN: d=FPMIN
    d=1/d; h=d
    for m in range(1, MAXIT+1):
        m2=2*m
        aa=m*(b-m)*x/((qam+m2)*(a+m2)); d=1+aa*d
        if abs(d)<FPMIN: d=FPMIN
        c=1+aa/c
        if abs(c)<FPMIN: c=FPMIN
        d=1/d; h*=d*c
        aa=-(a+m)*(qab+m)*x/((a+m2)*(qap+m2)); d=1+aa*d
        if abs(d)<FPMIN: d=FPMIN
        c=1+aa/c
        if abs(c)<FPMIN: c=FPMIN
        d=1/d; delta=d*c; h*=delta
        if abs(delta-1)<EPS: break
    return h

def _betai(a, b, x):
    if x<=0: return 0
    if x>=1: return 1
    bt = math.exp(_gammaln(a+b)-_gammaln(a)-_gammaln(b)+a*math.log(x)+b*math.log(1-x))
    if x<(a+1)/(a+b+2): return bt*_betacf(a,b,x)/a
    return 1-bt*_betacf(b,a,1-x)/b

def _t_cdf(t, df):
    x = df/(df+t*t); ib = _betai(df/2, 0.5, x)
    return 1-0.5*ib if t>0 else 0.5*ib


def load_csv_series(slug: str) -> dict[int, float]:
    rows = {}
    with (SERIES_DIR / f"{slug}.csv").open(encoding="utf-8") as f:
        for line in csv.DictReader(f):
            try:
                rows[int(line["ano"])] = float(line["valor"])
            except (TypeError, ValueError):
                continue
    return rows


def build_caption(pub: dict, label_a: str, label_b: str, r: float) -> str:
    sinal = "negativa" if r < 0 else "positiva"
    return (
        f"# {pub['titulo']}\n\n"
        f"> Copa 2026 · edição bônus durante o torneio\n\n"
        f"Duas curvas que ninguém pediu para se encontrarem decidiram conversar "
        f"de **{pub['ano_inicio']} a {pub['ano_fim']}**.\n\n"
        f"**{label_a}** vs **{label_b}** — correlação {sinal} de manual "
        f"de espúrias.\n\n"
        f"A teoria por trás está no site (link na bio).\n\n"
        f"#datafolia #copa2026 #correlacoes #brasil #futebol\n"
    )


def build_image_prompt(pub: dict) -> str:
    return (
        f"Editorial illustration in Brazilian carnival palette (green #009C3B, "
        f"yellow #FACC15, orange #F97316), warm humor.\n\n"
        f"Theme: '{pub['titulo']}'. The image should poke fun at the absurd "
        f"theory linking the two data series — soccer + macroeconomy mashup.\n\n"
        f"Mood: bossa-nova-meets-spreadsheet. No real player likenesses. "
        f"Composition fits 1200x630 hero crop and works as Instagram square.\n"
    )


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    index_path = PUB_DIR / "_index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    existing_ids = {p["id"] for p in index["publicacoes"]}

    for pub in NOVAS_PUBS:
        info_a = manifest["series"][pub["slug_a"]]
        info_b = manifest["series"][pub["slug_b"]]
        da = load_csv_series(pub["slug_a"])
        db = load_csv_series(pub["slug_b"])
        anos = sorted(set(da) & set(db) & set(range(pub["ano_inicio"], pub["ano_fim"]+1)))
        xs = [da[y] for y in anos]
        ys = [db[y] for y in anos]
        r, p = pearson(xs, ys)
        r2 = r * r
        n = len(anos)

        pdir = PUB_DIR / pub["id"]
        pdir.mkdir(exist_ok=True)
        print(f"\n== {pub['id']} ==")
        print(f"   r={r:+.4f} R2={r2:.4f} p={p:.4g} n={n}")
        print(f"   dir={pdir.relative_to(ROOT)}")

        # 1. serie_data.csv (so a janela)
        with (pdir / "serie_data.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ano", pub["slug_a"], pub["slug_b"]])
            for y, va, vb in zip(anos, xs, ys):
                w.writerow([y, va, vb])

        # 2. metadata.json
        meta = {
            "id": pub["id"],
            "ordem_curadoria": pub["ordem_curadoria"],
            "rank_no_top40": pub["rank_no_top40"],
            "status": "text_done",
            "data_post": pub["data_post"],
            "data_post_dia_semana": pub["data_post_dia_semana"],
            "tema_calendario": pub["tema_calendario"],
            "titulo": pub["titulo"],
            "caption_ig_path": "caption-ig.md",
            "artigo_site_path": "artigo-site.md",
            "image_prompt_path": "image-prompt.txt",
            "image_path": "image.jpg",
            "correlacao": {
                "r": round(r, 4),
                "r2": round(r2, 6),
                "p": float(f"{p:.6g}"),
                "n": n,
                "categoria": pub["categoria"],
                "ano_inicio": pub["ano_inicio"],
                "ano_fim": pub["ano_fim"],
                "anos": anos,
                "valores_a": xs,
                "valores_b": ys,
            },
            "serie_a": {
                "slug": pub["slug_a"],
                "label": info_a["label"],
                "fonte": info_a["fonte_nome"],
                "url": info_a["fonte_url"],
                "topic": pub["topic_a"],
            },
            "serie_b": {
                "slug": pub["slug_b"],
                "label": info_b["label"],
                "fonte": info_b["fonte_nome"],
                "url": info_b["fonte_url"],
                "topic": pub["topic_b"],
            },
            "ordem_calendario": None,
            "chart_site_path": "chart.png",
            "table_site_path": "table.png",
            "chart_instagram_path": "instagram.png",
        }
        (pdir / "metadata.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

        # 3. Renderizar charts
        render_chart_site(pdir / "chart.png", info_a["label"], info_b["label"],
                          anos, xs, ys, r, p, n,
                          fonte_a=info_a["fonte_nome"], fonte_b=info_b["fonte_nome"])
        render_table_site(pdir / "table.png", info_a["label"], info_b["label"],
                          anos, xs, ys)
        render_chart_instagram(pdir / "instagram.png", info_a["label"], info_b["label"],
                               anos, xs, ys, r, p, n)
        print(f"   charts OK")

        # 4. artigo-site.md
        p_str = f"{p:.4f}" if p >= 0.0001 else "< 0,0001"
        artigo = (
            f"# {pub['titulo']}\n\n"
            f"## A \"história\"\n\n"
            f"{pub['story']}\n\n"
            f"## Os dados\n\n"
            f"- **{info_a['label']}** ({n} pontos, {pub['ano_inicio']}-{pub['ano_fim']})\n"
            f"  Fonte: [{info_a['fonte_nome']}]({info_a['fonte_url']})\n\n"
            f"- **{info_b['label']}** ({n} pontos, {pub['ano_inicio']}-{pub['ano_fim']})\n"
            f"  Fonte: [{info_b['fonte_nome']}]({info_b['fonte_url']})\n\n"
            f"## A estatística\n\n"
            f"| Métrica | Valor |\n|---|---|\n"
            f"| Coeficiente de Pearson (r) | {r:+.4f} |\n"
            f"| R² (variação explicada) | {r2:.4f} ({r2*100:.1f}%) |\n"
            f"| Valor-p (bicaudal) | {p_str} |\n"
            f"| Tamanho da amostra (n) | {n} pares |\n"
            f"| Janela | {pub['ano_inicio']}-{pub['ano_fim']} |\n\n"
            f"Quer testar a correlação de duas séries suas?\n"
            f"[Use a calculadora de correlação aqui](https://calculadoraestatistica.com.br/correlacao.html).\n\n"
            f"## Lembrete\n\n"
            f"Correlação não é causa. Estas séries provavelmente não têm nenhuma relação real entre si; a coincidência matemática é o ponto. Para mais correlações espúrias brasileiras, [veja todas](/) ou siga [@datafolia no Instagram](https://instagram.com/datafolia).\n"
        )
        (pdir / "artigo-site.md").write_text(artigo, encoding="utf-8")
        (pdir / "caption-ig.md").write_text(
            build_caption(pub, info_a["label"], info_b["label"], r),
            encoding="utf-8")
        (pdir / "image-prompt.txt").write_text(
            build_image_prompt(pub), encoding="utf-8")
        print(f"   textos OK")

        # 5. atualizar _index.json
        if pub["id"] not in existing_ids:
            index["publicacoes"].append({
                "id": pub["id"],
                "titulo": pub["titulo"],
                "status": "text_done",
                "label_a": info_a["label"],
                "label_b": info_b["label"],
            })
            existing_ids.add(pub["id"])

    index["total"] = len(index["publicacoes"])
    import datetime as dt
    index["gerado_em"] = dt.datetime.utcnow().isoformat() + "Z"
    index_path.write_text(json.dumps(index, ensure_ascii=False, indent=2),
                          encoding="utf-8")
    print(f"\n_index.json atualizado: {index['total']} publicacoes")


if __name__ == "__main__":
    main()
