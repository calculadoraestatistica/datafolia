"""
Troca o post-zero: Desemp.RU x Havaianas vira o novo pub-00 (estreia).
Ana Maria x Japao vai para a vaga de 17/08/2026 (pub-11 atual).

Mecanica: troca os IDs e renomeia as pastas com prefixo _tmp_ para evitar colisao.
"""
from __future__ import annotations
import json
from pathlib import Path
import datetime as dt

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"

OLD_ZERO = "pub-00-ana-maria-braga-x-japao"
OLD_11   = "pub-11-desemprego-ru-x-havaianas"

NEW_ZERO = "pub-00-desemprego-ru-x-havaianas"
NEW_11   = "pub-11-ana-maria-braga-x-japao"


def main() -> None:
    a = PUB / OLD_ZERO
    b = PUB / OLD_11
    assert a.exists() and b.exists(), "pastas de origem nao encontradas"

    # Fase 1: tmp
    ta = PUB / "_tmp_zero"; a.rename(ta)
    tb = PUB / "_tmp_eleven"; b.rename(tb)

    # Fase 2: nomes finais
    ta.rename(PUB / NEW_11)        # ana maria -> pub-11
    tb.rename(PUB / NEW_ZERO)      # desemprego ru -> pub-00

    # Metadata da nova pub-00 (Desemp RU = post-zero)
    p0 = PUB / NEW_ZERO / "metadata.json"
    m0 = json.loads(p0.read_text(encoding="utf-8"))
    m0["id"] = NEW_ZERO
    m0["ordem_curadoria"] = 0
    m0["post_zero"] = True
    m0["data_post"] = None
    m0["data_post_dia_semana"] = None
    m0["tema_calendario"] = None
    m0["data_estreia"] = dt.date.today().isoformat()
    # remove campos antigos que nao se aplicam
    m0.pop("ordem_calendario", None)
    p0.write_text(json.dumps(m0, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {NEW_ZERO}: novo POST ZERO (data_estreia={m0['data_estreia']})")

    # Metadata da nova pub-11 (Ana Maria = 17/08/2026)
    p11 = PUB / NEW_11 / "metadata.json"
    m11 = json.loads(p11.read_text(encoding="utf-8"))
    m11["id"] = NEW_11
    m11["ordem_curadoria"] = 11
    m11.pop("post_zero", None)
    m11.pop("data_estreia", None)
    m11["data_post"] = "2026-08-17"
    m11["data_post_dia_semana"] = "monday"
    m11["tema_calendario"] = "dia-dos-pais"
    m11["ordem_calendario"] = 11
    p11.write_text(json.dumps(m11, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  {NEW_11}: agora calendario (17/08/2026)")

    # Regerar _index.json a partir de todas as pubs
    new_idx: list[dict] = []
    for d in sorted(PUB.glob("pub-*")):
        m = json.loads((d / "metadata.json").read_text(encoding="utf-8"))
        new_idx.append({
            "id": m["id"],
            "titulo": m.get("titulo", ""),
            "status": m.get("status", ""),
            "label_a": m["serie_a"]["label"],
            "label_b": m["serie_b"]["label"],
            "data_post": m.get("data_post"),
            "post_zero": bool(m.get("post_zero")),
        })
    idx = {
        "gerado_em": dt.datetime.utcnow().isoformat() + "Z",
        "total": len(new_idx),
        "publicacoes": new_idx,
    }
    (PUB / "_index.json").write_text(json.dumps(idx, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
    print(f"\n_index.json regenerado ({len(new_idx)} pubs)")


if __name__ == "__main__":
    main()
