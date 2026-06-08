"""
Atribui data e tema a cada publicacao em publications/.

Janela: 22 segundas-feiras a partir de Mon 08/06/2026.
Cada pub recebe metadata.data_post e metadata.tema_calendario.

Contexto brasileiro Jun-Nov 2026:
  - Jun 8/15/22/29, Jul 6/13: Copa do Mundo FIFA (11/jun-19/jul, USA-CAN-MEX)
  - Jul 20/27: ferias escolares
  - Aug 3: volta as aulas (algumas regioes)
  - Aug 10: Dia dos Pais (dom 9/ago)
  - Sep 7: Independencia (segunda feriado nacional!)
  - Sep 21: primavera comeca (22/set)
  - Oct 4 dom: ELEICOES GERAIS 1o turno -> Mon 5/out: comentario dos resultados
  - Oct 12: N. Sra. Aparecida (feriado) + Dia das Criancas
  - Oct 25 dom: ELEICOES 2o turno -> Mon 26/out: resultados
  - Nov 2 segunda: Finados (feriado) + vespera ENEM (Nov 8)
"""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"

# (slug_partial, data, tema_calendario)
# slug_partial = inicio do nome da pasta, identifica univocamente
PLAN: list[tuple[str, str, str | None]] = [
    # Bloco Copa do Mundo (Jun 11 - Jul 19)
    ("pub-27-trump-x-neymar",            "2026-06-08", "copa-do-mundo-abertura"),
    ("pub-16-bbb-x-messi",               "2026-06-15", "copa-do-mundo-fase-grupos-messi"),
    ("pub-19-palmeiras-x-nome-enzo",     "2026-06-22", "copa-do-mundo-grupos-argentina-festas-juninas"),
    ("pub-20-messi-x-roberto-carlos",    "2026-06-29", "copa-do-mundo-oitavas"),
    ("pub-25-brasileirao-artilheiro-x-olimpiadas", "2026-07-06", "copa-do-mundo-quartas"),
    ("pub-03-gremio-x-nome-riquelme",    "2026-07-13", "copa-do-mundo-final-argentina"),

    # Pos-Copa / ferias escolares
    ("pub-10-carnaval-x-coelhos-au",     "2026-07-20", "ferias-escolares-descontracao"),
    ("pub-23-ana-maria-braga-x-japao",   "2026-07-27", "ferias-escolares"),

    # Volta as aulas e Dia dos Pais
    ("pub-12-desemprego-ar-x-capivara-trend", "2026-08-03", "volta-as-aulas"),
    ("pub-26-desemprego-ru-x-havaianas", "2026-08-10", "dia-dos-pais"),

    # Meio de agosto e fim de mes (futebol-pesado, brasileirao em ritmo)
    ("pub-09-cruzeiro-x-capivara-trend", "2026-08-17", None),
    ("pub-21-atletico-mg-x-pistache",    "2026-08-24", None),
    ("pub-04-corinthians-x-mega-sena",   "2026-08-31", None),

    # Setembro: Independencia + corrida eleitoral
    ("pub-08-alpargatas-x-trump",        "2026-09-07", "feriado-independencia-marca-br-vs-figura-internacional"),
    ("pub-06-atletico-mg-x-mega-sena",   "2026-09-14", None),
    ("pub-02-coelhos-au-x-desemprego-ar","2026-09-21", "primavera"),
    ("pub-13-corinthians-x-nome-riquelme","2026-09-28", "vespera-eleicoes"),

    # Outubro: eleicoes e feriados
    ("pub-22-eleicoes-br-x-nome-kely",   "2026-10-05", "pos-eleicoes-1t"),
    ("pub-15-bbb-x-desemprego-ar",       "2026-10-12", "dia-das-criancas-nossa-senhora-aparecida"),
    ("pub-14-flamengo-x-olimpiadas",     "2026-10-19", None),
    ("pub-11-alpargatas-x-sao-paulo",    "2026-10-26", "pos-eleicoes-2t"),

    # Novembro: vespera ENEM
    ("pub-18-cruzeiro-x-eike",           "2026-11-02", "vespera-enem-finados-drama"),
]


def main() -> None:
    if not PUB.exists():
        raise SystemExit("publications/ nao existe")

    # Validar: cada slug parcial mapeia a uma unica pasta existente?
    found_paths: dict[str, Path] = {}
    for slug_partial, _, _ in PLAN:
        matches = list(PUB.glob(slug_partial + "*"))
        if len(matches) != 1:
            raise SystemExit(f"slug_partial '{slug_partial}' achou {len(matches)} pastas: {matches}")
        found_paths[slug_partial] = matches[0]

    # Confere que cobre todas as 22 publicacoes existentes
    pubs_no_disco = sorted(d.name for d in PUB.glob("pub-*") if d.is_dir())
    pubs_no_plano = sorted(found_paths[s].name for s in found_paths)
    sobrando = sorted(set(pubs_no_disco) - set(pubs_no_plano))
    if sobrando:
        print(f"AVISO: publicacoes sem data atribuida ({len(sobrando)}): {sobrando}")

    # Aplica
    for ordem, (slug_partial, data_str, tema) in enumerate(PLAN, 1):
        sub = found_paths[slug_partial]
        meta_path = sub / "metadata.json"
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        # Confirma que e segunda
        d = dt.date.fromisoformat(data_str)
        assert d.weekday() == 0, f"{data_str} nao e segunda-feira"
        meta["data_post"] = data_str
        meta["data_post_dia_semana"] = d.strftime("%A").lower()
        meta["tema_calendario"] = tema
        meta["ordem_calendario"] = ordem
        if meta.get("status") == "draft":
            pass  # mantem draft; status muda quando texto/imagem ficam prontos
        meta_path.write_text(
            json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
        d_pt = d.strftime("%d/%m/%Y")
        print(f"  {ordem:2d}. {d_pt}  ({d.strftime('%a')})  {sub.name}")
        if tema:
            print(f"      tema: {tema}")
        print()

    # Atualiza _index.json: agora com data
    ix_path = PUB / "_index.json"
    ix = json.loads(ix_path.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in ix["publicacoes"]}
    for slug_partial, data_str, tema in PLAN:
        nome = found_paths[slug_partial].name
        if nome in by_id:
            by_id[nome]["data_post"] = data_str
            by_id[nome]["tema_calendario"] = tema
    ix["publicacoes"] = sorted(ix["publicacoes"],
                                key=lambda p: p.get("data_post") or "9999")
    ix_path.write_text(json.dumps(ix, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Total: {len(PLAN)} publicacoes datadas, de "
          f"{PLAN[0][1]} ate {PLAN[-1][1]}")


if __name__ == "__main__":
    main()
