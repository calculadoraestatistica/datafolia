"""
Renomeia as pastas e ids das publicacoes para sequencial:
  pub-00-* = post de estreia (Ana Maria)
  pub-01-* = primeiro post agendado (08/06)
  pub-02-* = segundo (15/06)
  ... ate pub-23-* (09/11/2026)

Atualiza tambem:
  - id dentro de metadata.json
  - ordem_curadoria
  - publications/_index.json
"""
from __future__ import annotations
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"

# Ordem desejada: pub-00 = post-zero, pub-01..pub-23 = calendario
NOVA_ORDEM = [
    ("pub-23-ana-maria-braga-x-japao",          "ana-maria-braga-x-japao"),         # 00
    ("pub-27-trump-x-neymar-copa-do-mundo",     "trump-x-neymar-copa-do-mundo"),    # 01
    ("pub-16-bbb-x-messi",                       "bbb-x-messi"),                     # 02
    ("pub-19-palmeiras-x-nome-enzo",             "palmeiras-x-nome-enzo"),           # 03
    ("pub-20-messi-x-roberto-carlos",            "messi-x-roberto-carlos"),          # 04
    ("pub-29-neymar-x-salario-minimo",           "neymar-x-salario-minimo"),         # 05
    ("pub-28-cr7-x-desemprego-alemanha",         "cr7-x-desemprego-alemanha"),       # 06
    ("pub-25-brasileirao-artilheiro-x-olimpiadas", "brasileirao-artilheiro-x-olimpiadas"),  # 07
    ("pub-03-gremio-x-nome-riquelme",            "gremio-x-nome-riquelme"),          # 08
    ("pub-10-carnaval-x-coelhos-au",             "carnaval-x-coelhos-au"),           # 09
    ("pub-12-desemprego-ar-x-capivara-trend",    "desemprego-ar-x-capivara-trend"),  # 10
    ("pub-26-desemprego-ru-x-havaianas",         "desemprego-ru-x-havaianas"),       # 11
    ("pub-09-cruzeiro-x-capivara-trend",         "cruzeiro-x-capivara-trend"),       # 12
    ("pub-21-atletico-mg-x-pistache",            "atletico-mg-x-pistache"),          # 13
    ("pub-04-corinthians-x-mega-sena",           "corinthians-x-mega-sena"),         # 14
    ("pub-08-alpargatas-x-trump",                "alpargatas-x-trump"),              # 15
    ("pub-06-atletico-mg-x-mega-sena",           "atletico-mg-x-mega-sena-2"),       # 16 (mesmo time, evita duplicidade)
    ("pub-02-coelhos-au-x-desemprego-ar",        "coelhos-au-x-desemprego-ar"),      # 17
    ("pub-13-corinthians-x-nome-riquelme",       "corinthians-x-nome-riquelme"),     # 18
    ("pub-22-eleicoes-br-x-nome-kely",           "eleicoes-br-x-nome-kely"),         # 19
    ("pub-15-bbb-x-desemprego-ar",               "bbb-x-desemprego-ar"),             # 20
    ("pub-14-flamengo-x-olimpiadas",             "flamengo-x-olimpiadas"),           # 21
    ("pub-11-alpargatas-x-sao-paulo",            "alpargatas-x-sao-paulo"),          # 22
    ("pub-18-cruzeiro-x-eike",                   "cruzeiro-x-eike"),                 # 23
]


def main() -> None:
    # 1. Verificar que todas as pastas antigas existem
    missing = [old for old, _ in NOVA_ORDEM if not (PUB / old).exists()]
    if missing:
        raise SystemExit(f"Pastas faltando: {missing}")

    # 2. Renomear em duas fases: primeiro pra prefixo temporario, depois pro nome final.
    #    Isso evita colisoes (ex.: se pub-06 -> pub-16, mas pub-16 existe).
    print("--- fase 1: renomeia pra _tmp_NNN_slug ---")
    tmp_paths: list[tuple[int, Path, str]] = []
    for idx, (old, slug) in enumerate(NOVA_ORDEM):
        src = PUB / old
        tmp = PUB / f"_tmp_{idx:03d}_{slug}"
        src.rename(tmp)
        tmp_paths.append((idx, tmp, slug))
        print(f"   {old}  ->  {tmp.name}")

    print("\n--- fase 2: rename final pub-NN-slug ---")
    new_pubs: list[dict] = []
    for idx, tmp, slug in tmp_paths:
        new_id = f"pub-{idx:02d}-{slug}"
        dst = PUB / new_id
        tmp.rename(dst)

        # Atualizar metadata.json
        meta_path = dst / "metadata.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        old_id = meta.get("id")
        meta["id"] = new_id
        meta["ordem_curadoria"] = idx
        meta_path.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

        new_pubs.append({
            "id": new_id,
            "titulo": meta.get("titulo", ""),
            "status": meta.get("status", ""),
            "label_a": meta["serie_a"]["label"],
            "label_b": meta["serie_b"]["label"],
            "data_post": meta.get("data_post"),
            "post_zero": bool(meta.get("post_zero")),
        })
        marker = " [post-zero]" if meta.get("post_zero") else ""
        print(f"   {old_id:<48} -> {new_id}{marker}")

    # 3. Regerar _index.json
    import datetime as dt
    idx_path = PUB / "_index.json"
    index = {
        "gerado_em": dt.datetime.utcnow().isoformat() + "Z",
        "total": len(new_pubs),
        "publicacoes": new_pubs,
    }
    idx_path.write_text(json.dumps(index, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"\n_index.json regenerado: {len(new_pubs)} publicacoes")


if __name__ == "__main__":
    main()
