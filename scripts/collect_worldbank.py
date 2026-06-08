"""Coletor World Bank — PIB (USD bilhoes) + desemprego (%) por pais.

Especifico para os paises da Copa: campeoes mundiais + sede 2026 + Curacao.
Grava CSVs em data/series/ e atualiza _manifest.json.
"""
from __future__ import annotations
import csv
import datetime as dt
import json
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SERIES_DIR = ROOT / "data" / "series"
MANIFEST_PATH = SERIES_DIR / "_manifest.json"

# Paises World Bank ISO3 + nome PT
COUNTRIES = {
    "URY": ("Uruguai",     "uruguai"),
    "ITA": ("Italia",      "italia"),
    "DEU": ("Alemanha",    "alemanha"),
    "GBR": ("Inglaterra",  "inglaterra"),   # GBR cobre o Reino Unido
    "FRA": ("Franca",      "franca"),
    "ESP": ("Espanha",     "espanha"),
    "MEX": ("Mexico",      "mexico"),
    "CAN": ("Canada",      "canada"),
    "CUW": ("Curacao",     "curacao"),
    "ARG": ("Argentina",   "argentina"),
    "BRA": ("Brasil",      "brasil"),
}

INDICATORS = {
    # slug_template, label_template, fonte_nome, fonte_url, transform
    "pib": {
        "code": "NY.GDP.MKTP.CD",
        "label_fmt": "PIB da {nome} (USD bilhoes)",
        "slug_fmt": "pib-{slug}-bilhoes-usd",
        "fonte_nome": "World Bank — World Development Indicators",
        "fonte_url_fmt": "https://data.worldbank.org/indicator/NY.GDP.MKTP.CD?locations={iso}",
        "scale": 1e-9,   # USD -> USD bilhoes
        "round_to": 1,
    },
    "desemprego": {
        "code": "SL.UEM.TOTL.ZS",
        "label_fmt": "Taxa de desemprego na {nome} (%, ILO modelado)",
        "slug_fmt": "desemprego-{slug}-pct",
        "fonte_nome": "World Bank — ILO modelled estimate",
        "fonte_url_fmt": "https://data.worldbank.org/indicator/SL.UEM.TOTL.ZS?locations={iso}",
        "scale": 1.0,
        "round_to": 2,
    },
}

# Series ja existentes no projeto que NAO devo sobrescrever
SKIP = {
    "pib-brasil-bilhoes-usd",         # ja temos pib-brasil-bilhoes (BCB)
    "desemprego-brasil-pct",          # ja temos desemprego-pnadc (PNADC)
    "desemprego-argentina-pct",       # ja existe (hand-curado)
}

YEAR_FROM, YEAR_TO = 2003, 2024
SLEEP_BETWEEN = 0.4  # respeitar a API


def fetch_wb(iso: str, indicator: str) -> dict[int, float]:
    url = (f"https://api.worldbank.org/v2/country/{iso}/indicator/{indicator}"
           f"?format=json&date={YEAR_FROM}:{YEAR_TO}&per_page=200")
    req = urllib.request.Request(url, headers={"User-Agent": "data-folia/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if not isinstance(data, list) or len(data) < 2 or not data[1]:
        return {}
    out: dict[int, float] = {}
    for row in data[1]:
        v = row.get("value")
        if v is None:
            continue
        out[int(row["date"])] = float(v)
    return out


def write_series(slug: str, label: str, fonte_nome: str, fonte_url: str,
                 dados: dict[int, float], manifest: dict) -> None:
    pairs = sorted(dados.items())
    path = SERIES_DIR / f"{slug}.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ano", "valor"])
        for ano, valor in pairs:
            w.writerow([ano, valor])
    anos = [p[0] for p in pairs]
    manifest["series"][slug] = {
        "label": label,
        "categoria": "internacional",
        "fonte_nome": fonte_nome,
        "fonte_url": fonte_url,
        "status": "ok",
        "n": len(pairs),
        "ano_min": min(anos) if anos else None,
        "ano_max": max(anos) if anos else None,
        "coletado_em": dt.datetime.utcnow().isoformat() + "Z",
    }
    print(f"  > {slug}: {len(pairs)} pts ({min(anos)}-{max(anos)})")


def main() -> None:
    manifest = (
        json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        if MANIFEST_PATH.exists()
        else {"series": {}}
    )
    manifest.setdefault("series", {})

    for iso, (nome, slug_pais) in COUNTRIES.items():
        for ind_key, spec in INDICATORS.items():
            slug = spec["slug_fmt"].format(slug=slug_pais)
            if slug in SKIP:
                print(f"  - skip {slug}")
                continue
            try:
                raw = fetch_wb(iso, spec["code"])
                if not raw:
                    print(f"  ! {slug}: API retornou vazio")
                    continue
                dados = {ano: round(v * spec["scale"], spec["round_to"])
                         for ano, v in raw.items()}
                label = spec["label_fmt"].format(nome=nome)
                fonte_url = spec["fonte_url_fmt"].format(iso=iso)
                write_series(slug, label, spec["fonte_nome"], fonte_url,
                             dados, manifest)
            except Exception as e:
                print(f"  ! {slug}: erro {e}")
            time.sleep(SLEEP_BETWEEN)

    manifest["gerado_em"] = dt.datetime.utcnow().isoformat() + "Z"
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nTotal agora: {len(manifest['series'])} series no manifest")


if __name__ == "__main__":
    main()
