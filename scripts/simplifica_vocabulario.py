"""
Aplica substituicoes de vocabulario rebuscado em artigo-site.md.
Lista vinda da auditoria.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"

# (pub_id, [(velho, novo), ...])
TROCAS = [
    ("pub-01-trump-x-neymar-copa-do-mundo", [
        ("reservas simbólicas de confiança", "símbolos de confiança"),
        ("pirâmide financeira", "topo das fortunas"),
    ]),
    ("pub-03-palmeiras-x-nome-enzo", [
        ("planejamento geracional", "pensar nas próximas gerações"),
        ("imaginário familiar", "as famílias"),
        ("candidatos simbólicos para o amanhã", "futuras promessas"),
    ]),
    ("pub-06-cr7-x-desemprego-alemanha", [
        ("libera capacidade ociosa", "destrava vaga parada"),
        ("memorando europeu", "comunicado europeu"),
    ]),
    ("pub-07-brasileirao-artilheiro-x-olimpiadas", [
        ("comoção nacional", "emoção do país"),
    ]),
    ("pub-08-gremio-x-nome-riquelme", [
        ("bússola de ordem", "referência de ordem"),
        ("referências continentais de serenidade", "calma vinda de fora"),
        ("válvula de consulta coletiva", "referência que todo mundo busca"),
    ]),
    ("pub-09-carnaval-x-coelhos-au", [
        ("fenômeno de ocupação urbana", "tomada das ruas"),
        ("princípio territorial", "instinto de marcar território"),
        ("densidade festiva", "aglomeração da festa"),
    ]),
    ("pub-10-desemprego-ar-x-capivara-trend", [
        ("baixa volatilidade", "tranquilidade"),
    ]),
    ("pub-11-ana-maria-braga-x-japao", [
        ("estrutura etária", "envelhecimento da população"),
        ("dimensão demográfica do envelhecimento", "o envelhecimento do país"),
        ("pirâmide etária", "envelhecimento"),
    ]),
    ("pub-12-cruzeiro-x-capivara-trend", [
        ("baixa turbulência", "que acalma"),
        ("autorregulação coletiva", "alívio coletivo"),
    ]),
    ("pub-15-alpargatas-x-trump", [
        ("imaginário patrimonial de luxo", "mundo do luxo"),
    ]),
    ("pub-16-atletico-mg-x-mega-sena-2", [
        ("administração da ansiedade", "controle da ansiedade"),
        ("cálculo emocional", "jogo de cintura emocional"),
    ]),
    ("pub-17-coelhos-au-x-desemprego-ar", [
        ("indicador antecedente", "sinal de alerta"),
    ]),
    ("pub-18-corinthians-x-nome-riquelme", [
        ("leitura tática do continente", "entender o futebol do continente"),
        ("biblioteca emocional", "memória afetiva"),
        ("verbete obrigatório da educação sul-americana corintiana",
          "leitura obrigatória do corintiano sul-americano"),
    ]),
    ("pub-19-eleicoes-br-x-nome-kely", [
        ("padrão operacional", "padrão do sistema"),
        ("alfabeto para ser mais administrativo", "alfabeto para caber no sistema"),
    ]),
    ("pub-20-bbb-x-desemprego-ar", [
        ("infraestrutura emocional", "base emocional"),
        ("humor regional", "clima da região"),
    ]),
    ("pub-22-alpargatas-x-sao-paulo", [
        ("cadência própria", "ritmo próprio"),
        ("marcha mais contemplativa", "passo mais calmo"),
        ("índice de maciez social", "termômetro do conforto do país"),
    ]),
    ("pub-23-cruzeiro-x-eike", [
        ("ambiente simbólico", "clima ao redor"),
        ("fortunas espetaculares", "fortunas gigantes"),
        ("disputa de grandiosidade", "disputa de grandeza"),
    ]),
]


def main() -> None:
    total_applied = 0
    total_skipped = 0
    for pub_id, trocas in TROCAS:
        path = PUB / pub_id / "artigo-site.md"
        if not path.exists():
            print(f"  ! {pub_id}: artigo-site.md nao encontrado")
            continue
        text = path.read_text(encoding="utf-8")
        original = text
        applied: list[str] = []
        skipped: list[str] = []
        for old, new in trocas:
            if old in text:
                text = text.replace(old, new)
                applied.append(old)
            else:
                skipped.append(old)
        if text != original:
            path.write_text(text, encoding="utf-8")
        print(f"  [{pub_id}] +{len(applied)} -{len(skipped)}")
        for s in skipped:
            print(f"     not found: '{s}'")
        total_applied += len(applied)
        total_skipped += len(skipped)
    print(f"\nTotal: {total_applied} aplicadas, {total_skipped} nao encontradas")


if __name__ == "__main__":
    main()
