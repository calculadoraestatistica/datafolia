"""Guarda de regressao das fontes usadas nas imagens do Instagram.

Roda no mesmo runner Linux do post semanal e falha se a fonte escolhida
para o TITULO nao tiver os glifos acentuados do portugues — que foi o
defeito do post de 2026-08-17 ("O Caf# da Manh# Demogr#fico"): a lista
de candidatas do negrito so tinha nomes de Arial, ausentes no Ubuntu, e
o titulo caia no bitmap embutido do Pillow, sem acentos.

Alem do teste, salva as imagens em _fontcheck/ para inspecao visual
pelo artifact do workflow.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ig_post_test import _font, make_text_slide_feed  # noqa: E402

ACENTOS = "áàâãéêíóôõúüçÁÀÂÃÉÊÍÓÔÕÚÜÇºª"
TITULO = "O Café da Manhã Demográfico"
CORPO = ("A população do Japão diminui porque a apresentadora insiste em "
         "fazer aniversário. Todo 1º de abril sopra velinhas em rede "
         "nacional, e Tóquio fecha o ano com menos gente.")


def cobertura(font) -> tuple[str, list[str]]:
    """Retorna (caminho da fonte, lista de acentos sem glifo)."""
    path = getattr(font, "path", None)
    if not path:
        return "load_default() [bitmap embutido]", list(ACENTOS)
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("   (fontTools indisponivel — checagem so visual)")
        return path, []
    cmap = TTFont(path).getBestCmap()
    return path, [c for c in ACENTOS if ord(c) not in cmap]


def main() -> int:
    falhou = False
    for rotulo, bold in (("titulo (negrito)", True), ("corpo (regular)", False)):
        path, faltando = cobertura(_font(64, bold=bold))
        if faltando:
            print(f"ERRO {rotulo}: {path} nao tem {''.join(faltando)}", file=sys.stderr)
            falhou = True
        else:
            print(f"OK   {rotulo}: {path}")

    out = Path(__file__).resolve().parent.parent / "_fontcheck"
    out.mkdir(exist_ok=True)
    make_text_slide_feed(out / "feed_text.png", TITULO, CORPO)
    print(f"OK   slide de teste renderizado -> {out / 'feed_text.png'}")
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main())
