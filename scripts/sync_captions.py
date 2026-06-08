"""
Sincroniza caption-ig.md com a secao 'A teoria' (ou A historia) do artigo-site.md
para garantir que o texto do site e do IG sao identicos.

Formato da caption gerada:
    {titulo}
    {historia inteira}
    Mais detalhes em datafolia.com.br
    #datafolia #correlacoes #brasil #estatistica
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUB = ROOT / "publications"

HASHTAGS = "#datafolia #correlacoes #brasil #estatistica"


def extract_historia(md: str) -> str:
    for header in ["A teoria", 'A "história"', "A história"]:
        m = re.search(rf'^##\s+{re.escape(header)}\s*\n+(.+?)(?=\n##|\Z)',
                       md, re.M | re.S)
        if m:
            return m.group(1).strip()
    return ""


def main() -> None:
    n_synced = 0
    n_skipped = 0
    for pdir in sorted(PUB.glob("pub-*")):
        artigo_path = pdir / "artigo-site.md"
        caption_path = pdir / "caption-ig.md"
        if not artigo_path.exists():
            continue
        meta = json.loads((pdir / "metadata.json").read_text(encoding="utf-8"))
        titulo = meta.get("titulo", "")
        artigo = artigo_path.read_text(encoding="utf-8")
        historia = extract_historia(artigo)
        if not historia:
            print(f"  ! {pdir.name}: nenhuma secao 'A teoria/historia' encontrada")
            n_skipped += 1
            continue
        new_caption = (
            f"{titulo}\n\n"
            f"{historia}\n\n"
            f"Mais detalhes em datafolia.com.br\n\n"
            f"{HASHTAGS}\n"
        )
        old = caption_path.read_text(encoding="utf-8") if caption_path.exists() else ""
        if old.strip() == new_caption.strip():
            continue
        caption_path.write_text(new_caption, encoding="utf-8")
        print(f"  sync {pdir.name}")
        n_synced += 1
    print(f"\n{n_synced} captions sincronizadas, {n_skipped} sem fonte.")


if __name__ == "__main__":
    main()
