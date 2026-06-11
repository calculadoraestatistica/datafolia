"""
Constroi a pasta publications/ a partir das escolhas do Vinicius no top 40.

Para cada correlacao escolhida cria uma subpasta com:
  - metadata.json    : todos os campos (correlacao, fontes, status, datas, textos)
  - chart.png        : grafico das duas series (mesmo estilo do PDF)
  - serie_data.csv   : dados brutos das duas series na janela
  - caption-ig.md    : caption a redigir para o Instagram
  - artigo-site.md   : texto a redigir para a pagina do site
  - image-prompt.txt : prompt do Picsart a redigir
  - image.jpg        : placeholder (gerar e salvar manualmente)
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Renderer padrao Data Folia (paleta brasileira + fontes uniformes)
from chart_renderer import (
    render_chart_site,
    render_table_site,
    render_chart_instagram,
)

ROOT = Path(__file__).resolve().parent.parent
SERIES_DIR = ROOT / "data" / "series"
MANIFEST_PATH = SERIES_DIR / "_manifest.json"
TOP_CSV = ROOT / "data" / "correlations_top40.csv"
PUB_DIR = ROOT / "publications"

# Numeros escolhidos pelo Vinicius
PICKS = [3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 17, 19, 20, 22, 23,
         25, 27, 28, 29, 30, 32, 34, 35, 37, 39]


def slugify(s: str, maxlen: int = 40) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s[:maxlen]


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


def render_chart(out_path: Path, label_a: str, label_b: str,
                 anos: list[int], xs: list[float], ys: list[float],
                 r: float) -> None:
    """Mesmo estilo do PDF: dual-axis, solida vs tracejada vazada."""
    color_a = "#1d4ed8"
    color_b = "#ea580c"
    fig, ax = plt.subplots(figsize=(10, 5.5), dpi=140)
    ax2 = ax.twinx()
    # Linha A: solida circulos cheios
    line_a, = ax.plot(anos, xs, color=color_a, linewidth=2.6,
                      linestyle="-",
                      marker="o", markersize=8, markerfacecolor=color_a,
                      markeredgecolor="white", markeredgewidth=1.5,
                      zorder=4, label="A — " + _short(label_a, 60))
    # Linha B: tracejada quadrados vazados
    line_b, = ax2.plot(anos, ys, color=color_b, linewidth=2.8,
                       linestyle=(0, (6, 3)),
                       marker="s", markersize=9, markerfacecolor="white",
                       markeredgecolor=color_b, markeredgewidth=2.2,
                       zorder=3, label="B — " + _short(label_b, 60))
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
        if vmin == vmax:
            vmin -= 0.5; vmax += 0.5
        pad = (vmax - vmin) * 0.10
        axis.set_ylim(vmin - pad, vmax + pad)
    ax.legend([line_a, line_b],
              ["A — " + _short(label_a, 70), "B — " + _short(label_b, 70)],
              loc="upper center", bbox_to_anchor=(0.5, -0.13),
              fontsize=9, frameon=False, ncol=1)
    fig.suptitle(f"Data Folia · r = {r:+.3f}",
                 fontsize=11, color="#0f172a", fontweight="bold")
    fig.tight_layout()
    fig.savefig(out_path, dpi=140, bbox_inches="tight")
    plt.close(fig)


def _short(s: str, n: int) -> str:
    return s if len(s) <= n else s[:n - 1] + "…"


CAPTION_TEMPLATE = """\
# Caption do Instagram (a redigir)

> Para preencher antes da publicação. Sugestão de tom: divertido, com a
> "explicação" inventada (não real) que conecta as duas séries — no estilo
> Tyler Vigen. Termina com chamada para o site.

---

[GANCHO EM 1 LINHA — algo intrigante]

[2-3 frases costurando uma "explicação" lúdica entre os dois fenômenos]

Coincidência ou conspiração? Você decide.

⚠️ A teoria é ficção: a correlação é real, a história que costura os dois é puro entretenimento.

📊 r = {r:+.3f} · n = {n} · janela {anos}
🔗 Veja os dados completos em datafolia.com.br/{slug}/

#estatistica #datafolia #correlacaoespurea #brasil
"""

ARTIGO_TEMPLATE = """\
# {titulo_temp}

> Texto para a página individual no site. Mais longo que o caption do IG,
> com as fontes citadas, gráfico, tabela e link para a calculadora de
> correlação (calculadoraestatistica.com.br/correlacao.html).

---

## A "história"

[Aqui entra a narrativa engraçada — 3-5 parágrafos costurando uma explicação
inventada entre as duas séries. Lembrar: NÃO afirmar causalidade real.]

## Os dados

- **{label_a}** ({n} pontos, {ano_inicio}–{ano_fim})
  Fonte: [{fonte_a}]({fonte_a_url})

- **{label_b}** ({n} pontos, {ano_inicio}–{ano_fim})
  Fonte: [{fonte_b}]({fonte_b_url})

## A estatística

| Métrica | Valor |
|---|---|
| Coeficiente de Pearson (r) | {r:+.4f} |
| R² (variação explicada) | {r2:.4f} ({r2_pct:.1f}%) |
| Valor-p (bicaudal) | {p_str} |
| Tamanho da amostra (n) | {n} pares |
| Janela | {ano_inicio}–{ano_fim} |

Quer testar a correlação de duas séries suas?
[Use a calculadora de correlação aqui](https://calculadoraestatistica.com.br/correlacao.html).

## Lembrete

Correlação não é causa. Estas séries provavelmente não têm nenhuma relação
real entre si — a coincidência matemática é o ponto. Para mais correlações
espúrias brasileiras, [veja todas](/) ou siga [@datafolia no Instagram](https://instagram.com/datafolia).
"""

IMAGE_PROMPT_TEMPLATE = """\
# Prompt do Picsart (a redigir)

> Estilo visual fixo para a marca Data Folia (definir uma vez e replicar).
> Sugestão: ilustração editorial flat com personagens dos dois lados se
> encontrando, paleta vibrante, fundo neutro.

ESTILO FIXO (preencher uma vez):
- Paleta: ___
- Tipo: ___ (flat illustration / cartoon / colagem / etc.)
- Aspecto: 1:1 (Instagram feed)

PROMPT PARA ESTA PUBLICAÇÃO:
[Personagem A: representação visual de "{label_a}"]
[Personagem B: representação visual de "{label_b}"]
[Cenário/Composição: algo que sugira a conexão impossível entre os dois]
Sem texto na imagem (o texto fica no caption).
"""


def main() -> None:
    PUB_DIR.mkdir(exist_ok=True)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    series = load_series_data()
    rows = list(csv.DictReader(TOP_CSV.open(encoding="utf-8")))
    rows_by_rank = {int(r["rank"]): r for r in rows}

    # README explicando a estrutura
    (PUB_DIR / "README.md").write_text(_README, encoding="utf-8")

    salvos = []
    for ordem, rank in enumerate(PICKS, 1):
        r = rows_by_rank[rank]
        sa = r["serie_a"]; sb = r["serie_b"]
        info_a = manifest["series"][sa]
        info_b = manifest["series"][sb]
        label_a = info_a["label"]; label_b = info_b["label"]

        # Slug da pasta: pub-NN-topica-x-topica
        slug = f"pub-{ordem:02d}-{slugify(r['topic_a'])}-x-{slugify(r['topic_b'])}"
        sub = PUB_DIR / slug
        sub.mkdir(exist_ok=True)

        # Dados na janela
        da = series[sa]; db = series[sb]
        anos = [y for y in sorted(set(da) & set(db))
                if int(r["ano_inicio"]) <= y <= int(r["ano_fim"])]
        xs = [da[y] for y in anos]
        ys = [db[y] for y in anos]

        # Charts (3 imagens com o layout padrao Data Folia)
        r_v = float(r["r"]); p_v = float(r["p"])
        render_chart_site(sub / "chart.png",
                          label_a, label_b, anos, xs, ys,
                          r_v, p_v, len(anos),
                          fonte_a=info_a["fonte_nome"],
                          fonte_b=info_b["fonte_nome"])
        render_table_site(sub / "table.png",
                          label_a, label_b, anos, xs, ys)
        render_chart_instagram(sub / "instagram.png",
                               label_a, label_b, anos, xs, ys,
                               r_v, p_v, len(anos))

        # Serie data CSV
        with (sub / "serie_data.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ano", "valor_a", "valor_b"])
            for i, y in enumerate(anos):
                w.writerow([y, xs[i], ys[i]])

        # Metadata
        meta = {
            "id": slug,
            "ordem_curadoria": ordem,
            "rank_no_top40": rank,
            "status": "draft",
            "data_post": None,
            "data_post_dia_semana": "monday",
            "tema_calendario": None,
            "titulo": None,
            "caption_ig_path": "caption-ig.md",
            "artigo_site_path": "artigo-site.md",
            "image_prompt_path": "image-prompt.txt",
            "image_path": "image.jpg",
            "chart_site_path": "chart.png",
            "table_site_path": "table.png",
            "chart_instagram_path": "instagram.png",
            "correlacao": {
                "r": float(r["r"]),
                "r2": float(r["r"]) ** 2,
                "p": float(r["p"]),
                "n": len(anos),
                "categoria": r["categoria"],
                "ano_inicio": int(r["ano_inicio"]),
                "ano_fim": int(r["ano_fim"]),
                "anos": anos,
                "valores_a": xs,
                "valores_b": ys,
            },
            "serie_a": {
                "slug": sa, "label": label_a,
                "fonte": info_a["fonte_nome"], "url": info_a["fonte_url"],
                "topic": r["topic_a"],
            },
            "serie_b": {
                "slug": sb, "label": label_b,
                "fonte": info_b["fonte_nome"], "url": info_b["fonte_url"],
                "topic": r["topic_b"],
            },
        }
        (sub / "metadata.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

        # Texts (templates a preencher)
        anos_str = f"{anos[0]}–{anos[-1]}"
        r_val = float(r["r"])
        r2 = r_val ** 2
        p = float(r["p"])
        p_str = f"{p:.4f}" if p >= 0.0001 else "< 0,0001"
        (sub / "caption-ig.md").write_text(CAPTION_TEMPLATE.format(
            r=r_val, n=len(anos), anos=anos_str, slug=slug), encoding="utf-8")
        (sub / "artigo-site.md").write_text(ARTIGO_TEMPLATE.format(
            titulo_temp=f"{_short(label_a, 35)} × {_short(label_b, 35)}",
            label_a=label_a, label_b=label_b,
            fonte_a=info_a["fonte_nome"], fonte_a_url=info_a["fonte_url"],
            fonte_b=info_b["fonte_nome"], fonte_b_url=info_b["fonte_url"],
            n=len(anos), ano_inicio=anos[0], ano_fim=anos[-1],
            r=r_val, r2=r2, r2_pct=r2 * 100, p_str=p_str
        ), encoding="utf-8")
        (sub / "image-prompt.txt").write_text(IMAGE_PROMPT_TEMPLATE.format(
            label_a=label_a, label_b=label_b), encoding="utf-8")

        salvos.append((slug, label_a, label_b))
        print(f"OK  {slug}  ({label_a[:30]} × {label_b[:30]})")

    # Indice geral
    indice = {
        "gerado_em": dt.datetime.utcnow().isoformat() + "Z",
        "total": len(salvos),
        "publicacoes": [{"id": s, "label_a": la, "label_b": lb}
                        for s, la, lb in salvos],
    }
    (PUB_DIR / "_index.json").write_text(
        json.dumps(indice, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nTotal salvo: {len(salvos)} publicacoes em {PUB_DIR}")


_README = """\
# publications/ — Pasta de publicações Data Folia

Cada subpasta `pub-NN-...` é uma **publicação pronta para a Etapa 6 (calendário)
e Etapa 7 (cron de postagem)**. A pasta contém TUDO que o post precisa:

```
pub-NN-topica-x-topica/
├── metadata.json     # correlação, fontes, status, datas (todas as flags)
├── chart.png         # gráfico dual-axis (já gerado, pronto pro site)
├── serie_data.csv    # dados brutos das duas séries na janela usada
├── caption-ig.md     # caption do Instagram — A REDIGIR
├── artigo-site.md    # texto do site (mais longo) — A REDIGIR
├── image-prompt.txt  # prompt do Picsart — A REDIGIR
└── image.jpg         # imagem gerada no Picsart — A SALVAR
```

## Campos do metadata.json

- `status`: `draft` → `text_done` → `image_done` → `scheduled` → `published`
- `data_post`: `YYYY-MM-DD` da segunda-feira em que vai ar (atribuída na Etapa 6)
- `tema_calendario`: ex. `"copa-do-mundo"`, `"bbb-final"`, `"enem"` (opcional)
- `correlacao.*`: r, p, n, valores, janela
- `serie_a` / `serie_b`: slug, label, fonte, url, topic

## Fluxo de trabalho

1. Para cada `pub-NN`, escrever `caption-ig.md` e `artigo-site.md` →
   `status: text_done`
2. Escrever `image-prompt.txt`, gerar no Picsart, salvar `image.jpg` →
   `status: image_done`
3. Etapa 6 (calendário): preencher `data_post` e `tema_calendario` para cada →
   `status: scheduled`
4. Etapa 7 (cron GitHub Actions): a cada segunda-feira, lê todos os
   `metadata.json` com `status: scheduled` e `data_post == hoje`, e posta
   no Instagram (Graph API) + commit do post novo no site.

## Status atual

Esta pasta foi gerada pelo `scripts/build_publications.py` na primeira
curadoria do Vinícius (26 correlações escolhidas a partir do top 40).
Todos os arquivos `*.md` e `image-prompt.txt` estão como templates a
preencher; `chart.png`, `serie_data.csv` e `metadata.json` já estão
prontos.
"""


if __name__ == "__main__":
    main()
