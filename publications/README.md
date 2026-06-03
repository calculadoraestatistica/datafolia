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
