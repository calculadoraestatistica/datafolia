"""
Regenera chart.png, table.png e instagram.png em TODAS as pastas
publications/pub-*/ usando o layout padrao em chart_renderer.py.

Nao toca em metadata.json, caption-ig.md, artigo-site.md, image-prompt.txt
nem em image.jpg do usuario.

Tambem adiciona/atualiza os campos *_path no metadata.json para refletir
os 3 arquivos de imagem.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

from chart_renderer import (
    render_chart_site,
    render_table_site,
    render_chart_instagram,
)

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"


def main() -> None:
    pubs = sorted(d for d in PUB.glob("pub-*") if d.is_dir())
    print(f"Regenerando {len(pubs)} publicacoes...")
    for sub in pubs:
        meta_path = sub / "metadata.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        c = meta["correlacao"]
        label_a = meta["serie_a"]["label"]
        label_b = meta["serie_b"]["label"]
        anos = c["anos"]; xs = c["valores_a"]; ys = c["valores_b"]
        r = c["r"]; p = c["p"]; n = c["n"]

        render_chart_site(sub / "chart.png", label_a, label_b,
                          anos, xs, ys, r, p, n,
                          fonte_a=meta["serie_a"]["fonte"],
                          fonte_b=meta["serie_b"]["fonte"])
        render_table_site(sub / "table.png", label_a, label_b, anos, xs, ys)
        render_chart_instagram(sub / "instagram.png",
                                label_a, label_b, anos, xs, ys, r, p, n)

        # Atualiza caminhos no meta (limpa chart_path antigo se existir)
        meta.pop("chart_path", None)
        meta["chart_site_path"] = "chart.png"
        meta["table_site_path"] = "table.png"
        meta["chart_instagram_path"] = "instagram.png"
        meta_path.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  OK  {sub.name}")
    print("\nDone.")


if __name__ == "__main__":
    main()
