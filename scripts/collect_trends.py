"""
Coleta de Google Trends via pytrends. Roda em separado do collect.py
porque tem rate-limit muito mais agressivo (429) e pode falhar.
Salva diretamente em data/series/<slug>.csv e atualiza _manifest.json.
"""
from __future__ import annotations
import csv
import datetime as dt
import json
import time
from pathlib import Path

from pytrends.request import TrendReq

ROOT = Path(__file__).resolve().parent.parent
SERIES_DIR = ROOT / "data" / "series"
MANIFEST_PATH = SERIES_DIR / "_manifest.json"

# Termos: cada um vira uma série anual (interest_over_time agregado por ano).
TERMS = [
    {
        "slug": "trends-vira-lata-caramelo",
        "label": "Interesse no Google por 'vira lata caramelo' (média anual, escala 0–100)",
        "categoria": "cultura",
        "termo": "vira lata caramelo",
        "geo": "BR",
    },
    {
        "slug": "trends-bbb",
        "label": "Interesse no Google por 'BBB' (média anual, escala 0–100)",
        "categoria": "midia",
        "termo": "BBB",
        "geo": "BR",
    },
    {
        "slug": "trends-enem",
        "label": "Interesse no Google por 'enem' (média anual, escala 0–100)",
        "categoria": "educacao",
        "termo": "enem",
        "geo": "BR",
    },
    {
        "slug": "trends-mega-sena",
        "label": "Interesse no Google por 'mega sena' (média anual, escala 0–100)",
        "categoria": "cultura",
        "termo": "mega sena",
        "geo": "BR",
    },
    {
        "slug": "trends-pix",
        "label": "Interesse no Google por 'pix' (média anual, escala 0–100)",
        "categoria": "economia",
        "termo": "pix",
        "geo": "BR",
    },
    {
        "slug": "trends-dieta",
        "label": "Interesse no Google por 'dieta' (média anual, escala 0–100)",
        "categoria": "saude",
        "termo": "dieta",
        "geo": "BR",
    },
    {
        "slug": "trends-nome-valentina",
        "label": "Interesse no Google por 'Valentina' no Brasil — proxy do nome (escala 0–100)",
        "categoria": "cultura",
        "termo": "Valentina",
        "geo": "BR",
    },
    {
        "slug": "trends-nome-enzo",
        "label": "Interesse no Google por 'Enzo' no Brasil — proxy do nome (escala 0–100)",
        "categoria": "cultura",
        "termo": "Enzo",
        "geo": "BR",
    },
    {
        "slug": "trends-nome-kely",
        "label": "Interesse no Google por 'Kely' no Brasil — proxy do nome (escala 0–100)",
        "categoria": "cultura",
        "termo": "Kely",
        "geo": "BR",
    },
    {
        "slug": "trends-nome-riquelme",
        "label": "Interesse no Google por 'Riquelme' no Brasil — proxy do nome (escala 0–100)",
        "categoria": "cultura",
        "termo": "Riquelme",
        "geo": "BR",
    },
    {
        "slug": "trends-capivaras",
        "label": "Interesse no Google por 'capivara' no Brasil (escala 0–100)",
        "categoria": "cultura",
        "termo": "capivara",
        "geo": "BR",
    },
    {
        "slug": "trends-milei",
        "label": "Interesse no Google por 'Milei' no Brasil (escala 0–100)",
        "categoria": "internacional",
        "termo": "Milei",
        "geo": "BR",
    },
]


def coletar() -> None:
    py = TrendReq(hl="pt-BR", tz=180)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8")) if MANIFEST_PATH.exists() else {"series": {}}
    manifest.setdefault("series", {})

    for entry in TERMS:
        slug = entry["slug"]
        termo = entry["termo"]
        print(f"> {slug} (termo='{termo}')")
        try:
            # Janela ampla; o Google agrega automaticamente. Para series anuais
            # passamos timeframe 'all' (~ desde 2004).
            py.build_payload([termo], cat=0, timeframe="all", geo=entry["geo"])
            df = py.interest_over_time()
            if df.empty:
                raise RuntimeError("DataFrame vazio")
            # Agrega por ano (média de valores mensais)
            df = df.drop(columns=["isPartial"], errors="ignore")
            df["ano"] = df.index.year
            anual = df.groupby("ano")[termo].mean().round(1)
            pairs = [(int(y), float(v)) for y, v in anual.items()]
            # Salva CSV
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
                "fonte_nome": "Google Trends (pytrends)",
                "fonte_url": f"https://trends.google.com/trends/explore?geo={entry['geo']}&q={termo.replace(' ', '%20')}",
                "status": "ok",
                "n": len(pairs),
                "ano_min": min(anos),
                "ano_max": max(anos),
                "coletado_em": dt.datetime.utcnow().isoformat() + "Z",
            }
            print(f"   OK — {len(pairs)} anos ({min(anos)}–{max(anos)})")
        except Exception as e:
            print(f"   FALHA: {e}")
            manifest["series"][slug] = {
                "label": entry["label"],
                "categoria": entry["categoria"],
                "fonte_nome": "Google Trends (pytrends)",
                "fonte_url": "https://trends.google.com/",
                "status": "error",
                "erro": str(e),
                "coletado_em": dt.datetime.utcnow().isoformat() + "Z",
            }
        # Rate limit: 4-8s entre queries
        time.sleep(6)

    manifest["gerado_em"] = dt.datetime.utcnow().isoformat() + "Z"
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    ok = sum(1 for s in manifest["series"].values() if s.get("status") == "ok")
    err = sum(1 for s in manifest["series"].values() if s.get("status") != "ok")
    print(f"=== Manifest agora: {ok} ok / {err} falhas ===")


if __name__ == "__main__":
    coletar()
