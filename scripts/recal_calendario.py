"""
Reorganiza o calendario: remove pub-23 (vira post 0), elimina quintas-bonus,
move pub-29 e pub-28 para segundas, cascateia o resto +2 semanas.
"""
from __future__ import annotations
import json
from pathlib import Path
import datetime as dt

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"

# Ordem final (segundas consecutivas a partir de 08/06)
ORDEM = [
    "pub-27-trump-x-neymar-copa-do-mundo",
    "pub-16-bbb-x-messi",
    "pub-19-palmeiras-x-nome-enzo",
    "pub-20-messi-x-roberto-carlos",
    "pub-29-neymar-x-salario-minimo",
    "pub-28-cr7-x-desemprego-alemanha",
    "pub-25-brasileirao-artilheiro-x-olimpiadas",
    "pub-03-gremio-x-nome-riquelme",
    "pub-10-carnaval-x-coelhos-au",
    "pub-12-desemprego-ar-x-capivara-trend",
    "pub-26-desemprego-ru-x-havaianas",
    "pub-09-cruzeiro-x-capivara-trend",
    "pub-21-atletico-mg-x-pistache",
    "pub-04-corinthians-x-mega-sena",
    "pub-08-alpargatas-x-trump",
    "pub-06-atletico-mg-x-mega-sena",
    "pub-02-coelhos-au-x-desemprego-ar",
    "pub-13-corinthians-x-nome-riquelme",
    "pub-22-eleicoes-br-x-nome-kely",
    "pub-15-bbb-x-desemprego-ar",
    "pub-14-flamengo-x-olimpiadas",
    "pub-11-alpargatas-x-sao-paulo",
    "pub-18-cruzeiro-x-eike",
]

# Temas atualizados (alguns ja existiam, ajustamos os que mudaram)
TEMAS = {
    "pub-27-trump-x-neymar-copa-do-mundo":        "copa-do-mundo-abertura",
    "pub-16-bbb-x-messi":                          "copa-do-mundo-fase-grupos-messi",
    "pub-19-palmeiras-x-nome-enzo":                "copa-do-mundo-grupos-argentina-festas-juninas",
    "pub-20-messi-x-roberto-carlos":               "copa-do-mundo-oitavas",
    "pub-29-neymar-x-salario-minimo":              "copa-do-mundo-quartas-neymar",
    "pub-28-cr7-x-desemprego-alemanha":            "copa-do-mundo-final-alemanha",
    "pub-25-brasileirao-artilheiro-x-olimpiadas":  "pos-copa-brasileirao",
    "pub-03-gremio-x-nome-riquelme":               "pos-copa-resaca-argentina",
    "pub-10-carnaval-x-coelhos-au":                "ferias-escolares-descontracao",
    "pub-12-desemprego-ar-x-capivara-trend":       "volta-as-aulas",
    "pub-26-desemprego-ru-x-havaianas":            "dia-dos-pais",
    "pub-09-cruzeiro-x-capivara-trend":            None,
    "pub-21-atletico-mg-x-pistache":               None,
    "pub-04-corinthians-x-mega-sena":              None,
    "pub-08-alpargatas-x-trump":                   "feriado-independencia-marca-br-vs-figura-internacional",
    "pub-06-atletico-mg-x-mega-sena":              None,
    "pub-02-coelhos-au-x-desemprego-ar":           "primavera",
    "pub-13-corinthians-x-nome-riquelme":          "vespera-eleicoes",
    "pub-22-eleicoes-br-x-nome-kely":              "pos-eleicoes-1t",
    "pub-15-bbb-x-desemprego-ar":                  "dia-das-criancas-nossa-senhora-aparecida",
    "pub-14-flamengo-x-olimpiadas":                None,
    "pub-11-alpargatas-x-sao-paulo":               "pos-eleicoes-2t",
    "pub-18-cruzeiro-x-eike":                      "vespera-enem-finados-drama",
}

INICIO = dt.date(2026, 6, 8)  # primeira segunda
POST_ZERO_ID = "pub-23-ana-maria-braga-x-japao"


def main() -> None:
    # 1. Atualizar metadata.json de cada pub
    for idx, pid in enumerate(ORDEM):
        data = INICIO + dt.timedelta(weeks=idx)
        pdir = PUB / pid
        meta_path = pdir / "metadata.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        old = meta.get("data_post")
        meta["data_post"] = data.isoformat()
        meta["data_post_dia_semana"] = "monday"
        meta["tema_calendario"] = TEMAS.get(pid)
        meta["ordem_calendario"] = idx + 1
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2),
                              encoding="utf-8")
        if old != meta["data_post"]:
            print(f"  {pid}: {old} -> {meta['data_post']}")
        else:
            print(f"  {pid}: {meta['data_post']} (igual)")

    # 2. Marcar pub-23 como post 0 (data null + flag)
    pdir = PUB / POST_ZERO_ID
    meta = json.loads((pdir / "metadata.json").read_text(encoding="utf-8"))
    meta["data_post"] = None
    meta["data_post_dia_semana"] = None
    meta["tema_calendario"] = "post-zero-estreia"
    meta["ordem_calendario"] = 0
    meta["post_zero"] = True
    (pdir / "metadata.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  {POST_ZERO_ID}: marcado como POST ZERO (sem data, sempre topo)")

    # 3. Resumo
    print(f"\nCalendario: {len(ORDEM)} pubs de {INICIO} a "
          f"{INICIO + dt.timedelta(weeks=len(ORDEM)-1)}")


if __name__ == "__main__":
    main()
