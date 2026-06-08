"""Roda as séries hand-curadas de extras.py e anexa ao manifest."""
from __future__ import annotations
import csv
import datetime as dt
import json
from pathlib import Path

from extras import EXTRAS

ROOT = Path(__file__).resolve().parent.parent
SERIES_DIR = ROOT / "data" / "series"
MANIFEST_PATH = SERIES_DIR / "_manifest.json"


def main() -> None:
    manifest = (
        json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        if MANIFEST_PATH.exists()
        else {"series": {}}
    )
    manifest.setdefault("series", {})

    for slug, entry in EXTRAS.items():
        dados = entry["dados"]
        pairs = sorted(((int(y), float(v)) for y, v in dados.items()), key=lambda p: p[0])
        path = SERIES_DIR / f"{slug}.csv"
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["ano", "valor"])
            for ano, valor in pairs:
                w.writerow([ano, valor])
        anos = [p[0] for p in pairs]
        manifest["series"][slug] = {
            "label": entry["label"],
            "categoria": entry["categoria"],
            "fonte_nome": entry["fonte_nome"],
            "fonte_url": entry["fonte_url"],
            "status": "ok",
            "n": len(pairs),
            "ano_min": min(anos),
            "ano_max": max(anos),
            "coletado_em": dt.datetime.utcnow().isoformat() + "Z",
        }
        print(f"> {slug} OK ({len(pairs)} pts, {min(anos)}-{max(anos)})")

    manifest["gerado_em"] = dt.datetime.utcnow().isoformat() + "Z"
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Total agora: {len(manifest['series'])} séries no manifest")


if __name__ == "__main__":
    main()
