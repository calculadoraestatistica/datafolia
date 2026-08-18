"""
Postagem no Instagram @datafolia para uma publicacao do Data Folia.

Pipeline:
  1. (generate) Gera assets em publications/<pub>/ig/:
     - feed_chart.png   (1080x1080)  chart com titulo+eixos+legenda, sem stats
     - feed_text.png    (1080x1080)  slide texto do post
     - story_chart.png  (1080x1920)  chart vertical, limpo
     - story_image.png  (1080x1920)  imagem vertical, limpa
     - story_text.png   (1080x1920)  texto COMPLETO do post
  2. (push)     Commit + push para publicar URLs no GH Pages
  3. (wait)     Espera CDN servir os novos arquivos
  4. (post)     Posta no IG:
                 - Feed CAROUSEL: chart -> image -> text
                 - 3 Stories: chart -> image -> text-completo

Uso:
    python ig_post_test.py <pub-id>                  # ciclo completo (local)
    python ig_post_test.py <pub-id> --generate-only  # so gera assets
    python ig_post_test.py <pub-id> --post-only      # so posta (assets ja online)
    python ig_post_test.py <pub-id> --no-push        # gera + posta, sem git
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import requests
from PIL import Image, ImageDraw, ImageFont

from chart_renderer import render_chart_ig_carousel

ROOT = Path(__file__).resolve().parent.parent
TOKEN_FILE = ROOT / "token instagram"
GRAPH = "https://graph.facebook.com/v23.0"
SITE_BASE = "https://datafolia.com.br"

C_GREEN  = "#009C3B"
C_YELLOW = "#FACC15"
C_ORANGE = "#F97316"
C_INK    = "#0F172A"
C_WHITE  = "#FFFFFF"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ─── Auth ──────────────────────────────────────────────────────────────────
def parse_token() -> str:
    """Le o token do arquivo OU da env IG_TOKEN (para GitHub Actions)."""
    if os.environ.get("IG_TOKEN"):
        return os.environ["IG_TOKEN"].strip()
    if not TOKEN_FILE.exists():
        sys.exit(f"token nao encontrado: {TOKEN_FILE} nem IG_TOKEN env")
    for ln in TOKEN_FILE.read_text(encoding="utf-8").splitlines():
        if ln.strip().startswith("EAA"):
            return ln.strip()
    sys.exit("token EAA... nao encontrado")


def get_ig_user_id(token: str) -> str:
    if os.environ.get("IG_USER_ID"):
        return os.environ["IG_USER_ID"].strip()
    r = requests.get(f"{GRAPH}/me/accounts",
                     params={"access_token": token,
                             "fields": "id,name,instagram_business_account"},
                     timeout=30)
    r.raise_for_status()
    for page in r.json().get("data", []):
        iba = page.get("instagram_business_account")
        if iba:
            print(f"   FB Page '{page['name']}' -> IG user_id={iba['id']}")
            return iba["id"]
    sys.exit("Nenhuma Pagina FB tem IG Business conectado")


# ─── Helpers de texto / imagem ─────────────────────────────────────────────
# Diretorios varridos, na ordem: cwd, Windows (dev local), Linux (runner CI).
_FONT_DIRS = ["", "C:/Windows/Fonts/",
              "/usr/share/fonts/truetype/dejavu/",
              "/usr/share/fonts/truetype/liberation/",
              "/usr/share/fonts/truetype/msttcorefonts/",
              "/usr/share/fonts/truetype/noto/"]

# Nomes reais dos arquivos em cada plataforma. DejaVu-Bold e obrigatorio na
# lista do negrito: sem ele o runner Linux nao achava NENHUM candidato (so
# havia nomes de Arial, ausentes no Ubuntu, e o mapeamento p/ Liberation
# gerava "LiberationSans-bd.ttf", que nao existe). O titulo entao caia no
# load_default(), sem glifos acentuados, e saia com quadrados no lugar de
# a/e/o — foi o que aconteceu no post de 2026-08-17.
_FONT_NAMES = {
    True:  ["arialbd.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf",
            "NotoSans-Bold.ttf", "DejaVuSans.ttf", "arial.ttf"],
    False: ["arial.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf",
            "NotoSans-Regular.ttf"],
}


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    for name in _FONT_NAMES[bold]:
        for d in _FONT_DIRS:
            try:
                return ImageFont.truetype(d + name, size)
            except OSError:
                continue
    # Ultimo recurso: o bitmap embutido do Pillow renderiza sem acentos.
    print(f"AVISO: nenhuma fonte TrueType encontrada (bold={bold}); "
          f"acentos podem sair como quadrados.", file=sys.stderr)
    return ImageFont.load_default(size=size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont,
          max_width: int) -> list[str]:
    out: list[str] = []
    for para in text.split("\n"):
        if not para.strip():
            out.append("")
            continue
        words = para.split()
        cur = ""
        for w in words:
            cand = (cur + " " + w).strip()
            bb = draw.textbbox((0, 0), cand, font=font)
            if bb[2] - bb[0] <= max_width:
                cur = cand
            else:
                if cur:
                    out.append(cur)
                cur = w
        if cur:
            out.append(cur)
    return out


def _draw_brand_bar_top(draw: ImageDraw.ImageDraw, W: int, height: int = 110) -> None:
    draw.rectangle([0, 0, W, height], fill=C_GREEN)
    f = _font(int(height * 0.45), bold=True)
    bb = draw.textbbox((0, 0), "DATA FOLIA", font=f)
    draw.text(((W - (bb[2] - bb[0])) / 2, (height - (bb[3] - bb[1])) / 2 - 6),
              "DATA FOLIA", font=f, fill=C_WHITE)


def make_text_slide_feed(out: Path, titulo: str, snippet: str) -> None:
    """Slide texto do feed 1080x1080: titulo + snippet + 'Mais detalhes em datafolia.com.br'."""
    W, H = 1080, 1080
    img = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(img)
    _draw_brand_bar_top(draw, W, 110)

    margin = 80
    y = 200
    f_title = _font(64, bold=True)
    f_body  = _font(36)

    for ln in _wrap(draw, titulo, f_title, W - 2 * margin):
        draw.text((margin, y), ln, font=f_title, fill=C_INK)
        y += 76
    y += 30
    draw.rectangle([margin, y, margin + 200, y + 8], fill=C_YELLOW)
    y += 50

    for ln in _wrap(draw, snippet, f_body, W - 2 * margin):
        draw.text((margin, y), ln, font=f_body, fill=C_INK)
        y += 52
        if y > H - 160:
            break

    # Footer com link discreto (uma linha)
    draw.rectangle([0, H - 110, W, H], fill=C_YELLOW)
    f_link = _font(34, bold=True)
    msg = "Mais detalhes em datafolia.com.br"
    bb = draw.textbbox((0, 0), msg, font=f_link)
    draw.text(((W - (bb[2] - bb[0])) / 2, H - 110 + (110 - (bb[3] - bb[1])) / 2 - 5),
              msg, font=f_link, fill=C_INK)
    img.save(out, "PNG", optimize=True)
    print(f"   feed_text -> {out.relative_to(ROOT)}")


def make_story_from_square(out: Path, square_path: Path) -> None:
    """Story 1080x1920 SEM banner inferior. Brand bar minima no topo."""
    W, H = 1080, 1920
    canvas = Image.new("RGB", (W, H), C_GREEN)
    img = Image.open(square_path).convert("RGB")
    if img.size != (W, W):
        img = img.resize((W, W), Image.LANCZOS)
    band = (H - W) // 2
    canvas.paste(img, (0, band))
    # Banda topo: so brand pequena
    draw = ImageDraw.Draw(canvas)
    f = _font(60, bold=True)
    bb = draw.textbbox((0, 0), "DATA FOLIA", font=f)
    draw.text(((W - (bb[2] - bb[0])) / 2, band // 2 - 30),
              "DATA FOLIA", font=f, fill=C_WHITE)
    # Banda inferior: SEM nada (verde solido, segundo o pedido)
    canvas.save(out, "PNG", optimize=True)
    print(f"   story -> {out.relative_to(ROOT)}")


def make_text_story_full(out: Path, titulo: str, texto_full: str) -> None:
    """Story 1080x1920 com TEXTO COMPLETO da pub. Sem banner de link."""
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), C_WHITE)
    draw = ImageDraw.Draw(img)
    _draw_brand_bar_top(draw, W, 170)

    margin = 80
    y = 240
    f_title = _font(64, bold=True)
    f_body  = _font(38)

    for ln in _wrap(draw, titulo, f_title, W - 2 * margin):
        draw.text((margin, y), ln, font=f_title, fill=C_INK)
        y += 76
    y += 24
    draw.rectangle([margin, y, margin + 200, y + 10], fill=C_YELLOW)
    y += 50

    body_max_y = H - 100
    for ln in _wrap(draw, texto_full, f_body, W - 2 * margin):
        if y + 52 > body_max_y:
            # Trunca elegante
            draw.text((margin, y), "(…) cont. em datafolia.com.br",
                      font=f_body, fill=C_INK)
            break
        if ln == "":
            y += 24
        else:
            draw.text((margin, y), ln, font=f_body, fill=C_INK)
            y += 50
    img.save(out, "PNG", optimize=True)
    print(f"   story text -> {out.relative_to(ROOT)}")


# ─── Texto / caption ───────────────────────────────────────────────────────
def extract_historia(artigo_md: str) -> str:
    """Extrai a secao 'A historia'/A teoria do artigo (todo o corpo)."""
    for header in ['A "história"', "A história", "A teoria"]:
        m = re.search(rf'^##\s+{re.escape(header)}\s*\n+(.+?)(?=\n##|\Z)',
                       artigo_md, re.M | re.S)
        if m:
            return m.group(1).strip()
    return ""


def build_caption(titulo: str, historia_full: str) -> str:
    """Caption do feed = MESMO texto do site (titulo + historia) + link simples."""
    return f"{titulo}\n\n{historia_full}\n\nMais detalhes em datafolia.com.br"


# ─── Git ───────────────────────────────────────────────────────────────────
def git_push_assets(paths: list[Path]) -> None:
    rel = [str(p.relative_to(ROOT).as_posix()) for p in paths]
    subprocess.run(["git", "add", *rel], cwd=ROOT, check=True)
    res = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if res.returncode == 0:
        print("   nada novo p/ commitar")
        return
    subprocess.run(
        ["git", "commit", "-m", "IG assets auto-gerados"],
        cwd=ROOT, check=True)

    # Em GitHub Actions: usa GITHUB_TOKEN configurado pelo workflow.
    # Local: usa helper claude_github.
    if os.environ.get("GITHUB_ACTIONS") == "true":
        subprocess.run(["git", "push", "origin", "HEAD"], cwd=ROOT, check=True)
    else:
        subprocess.run(
            ["C:/Users/vinyn/miniconda3/python.exe",
             "C:/Vinicius/claude_infos/claude_github/use_account.py",
             "--account", "site_calculadora_estatistica",
             "--", "git", "push", "origin", "main"],
            cwd=ROOT, check=True)
    print("   git push OK")


def wait_for_url(url: str, timeout: int = 360) -> bool:
    """Espera ate URL responder 200. Padrao 6 min pra dar folga ao GH Pages.
    Se DNS local falhar mas conseguirmos resolver via 185.199.108.153 (GH Pages),
    tentamos via IP+Host header — verifica que o GH Pages ja serviu o asset."""
    import socket
    print(f"   esperando CDN: {url}")
    t0 = time.time()
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc

    while time.time() - t0 < timeout:
        try:
            r = requests.get(url, timeout=10, allow_redirects=True,
                              headers={"User-Agent": "datafolia-cron"})
            if r.status_code == 200:
                print(f"   OK em {time.time()-t0:.0f}s (DNS local)")
                return True
        except requests.exceptions.ConnectionError:
            # DNS local fudido — tenta via IP do GH Pages com Host header
            try:
                path = parsed.path + (f"?{parsed.query}" if parsed.query else "")
                for gh_ip in ("185.199.108.153", "185.199.109.153"):
                    r = requests.get(f"https://{gh_ip}{path}", timeout=10,
                                      headers={"Host": host,
                                               "User-Agent": "datafolia-cron"},
                                      verify=False)
                    if r.status_code == 200:
                        print(f"   OK em {time.time()-t0:.0f}s (via {gh_ip} + Host header)")
                        return True
            except Exception:
                pass
        except Exception:
            pass
        time.sleep(10)
    print(f"   TIMEOUT {timeout}s para {url}")
    return False


# ─── Meta Graph API ────────────────────────────────────────────────────────
def ig_post(token: str, ig_user_id: str, params: dict) -> dict:
    url = f"{GRAPH}/{ig_user_id}/media"
    p = {**params, "access_token": token}
    r = requests.post(url, params=p, timeout=60)
    if r.status_code != 200:
        print(f"FAIL POST /media: {r.status_code}\n{r.text[:500]}")
        r.raise_for_status()
    return r.json()


def ig_publish(token: str, ig_user_id: str, creation_id: str, retries: int = 3) -> dict:
    """POST /media_publish com retry exponencial.

    A Instagram Graph API às vezes retorna 'Media ID is not available' mesmo
    depois de o container reportar status_code=FINISHED — race condition do
    lado da Meta. 3 tentativas com backoff (4s, 8s, 16s) cobrem essa janela.
    """
    url = f"{GRAPH}/{ig_user_id}/media_publish"
    last_err = None
    for attempt in range(1, retries + 1):
        r = requests.post(url, params={"creation_id": creation_id,
                                       "access_token": token}, timeout=60)
        if r.status_code == 200:
            return r.json()
        last_err = (r.status_code, r.text[:300])
        # Erros transient comuns: 9007 (not available), 2207027, 4 (rate limit)
        body = r.text.lower()
        transient = ("media id is not available" in body or
                     "not ready" in body or
                     '"code":4,' in body or
                     '"code":190' in body)  # token issues are not transient, but log
        if attempt < retries and (r.status_code in (400, 500, 502, 503) and transient):
            sleep_s = 4 * (2 ** (attempt - 1))
            print(f"   publish attempt {attempt}/{retries} got {r.status_code}; retry em {sleep_s}s")
            time.sleep(sleep_s)
            continue
        break
    print(f"FAIL POST /media_publish: {last_err[0]}\n{last_err[1]}")
    r.raise_for_status()
    return r.json()


def wait_container_ready(token: str, cid: str, timeout: int = 120) -> None:
    t0 = time.time()
    while time.time() - t0 < timeout:
        r = requests.get(f"{GRAPH}/{cid}",
                         params={"fields": "status_code", "access_token": token},
                         timeout=30)
        st = r.json().get("status_code", "UNKNOWN") if r.status_code == 200 else "ERR"
        if st == "FINISHED":
            return
        if st == "ERROR":
            sys.exit(f"   container {cid} ERROR")
        time.sleep(4)
    sys.exit(f"   container {cid} nao ficou READY em {timeout}s")


# ─── Pipeline ──────────────────────────────────────────────────────────────
def generate_assets(pdir: Path, meta: dict, artigo_md: str) -> list[Path]:
    ig_dir = pdir / "ig"
    ig_dir.mkdir(exist_ok=True)
    titulo = meta["titulo"]
    historia = extract_historia(artigo_md)
    snippet  = historia.split("\n\n", 1)[0].strip()

    corr = meta["correlacao"]
    label_a = meta["serie_a"]["label"]
    label_b = meta["serie_b"]["label"]
    anos = corr["anos"]; xs = corr["valores_a"]; ys = corr["valores_b"]

    feed_chart = ig_dir / "feed_chart.png"
    feed_text  = ig_dir / "feed_text.png"
    story_image = ig_dir / "story_image.png"
    story_text_full = ig_dir / "story_text.png"

    print("--- gerando assets ---")
    _f = _font(48, bold=True)
    print(f"   fonte do titulo: {getattr(_f, 'path', 'load_default (SEM ACENTOS)')}")
    # 1) Feed chart 1080x1080 com titulo+eixos+legenda
    render_chart_ig_carousel(feed_chart, titulo, label_a, label_b, anos, xs, ys)
    print(f"   feed_chart -> {feed_chart.relative_to(ROOT)}")

    # 2) Feed text slide
    make_text_slide_feed(feed_text, titulo, snippet)

    # 3) Story image (1080x1920)
    make_story_from_square(story_image, pdir / "image.jpg")

    # 4) Story text COMPLETO
    make_text_story_full(story_text_full, titulo, historia)

    # 5) Story chart usa o MESMO feed_chart (1080x1080 -> centralizado em 1920)
    story_chart = ig_dir / "story_chart.png"
    make_story_from_square(story_chart, feed_chart)

    return [feed_chart, feed_text, story_chart, story_image, story_text_full]


def post_to_ig(pub_id: str, pdir: Path, meta: dict, artigo_md: str) -> None:
    titulo = meta["titulo"]
    historia = extract_historia(artigo_md)
    caption = build_caption(titulo, historia)
    print(f"\n--- caption ({len(caption)} chars) ---\n{caption}\n---")

    rel = pdir.relative_to(ROOT).as_posix()
    base = f"{SITE_BASE}/{rel}/ig"
    feed_chart_url = f"{base}/feed_chart.png"
    feed_image_url = f"{SITE_BASE}/{rel}/image.jpg"  # reaproveita
    feed_text_url  = f"{base}/feed_text.png"
    story_chart_url = f"{base}/story_chart.png"
    story_image_url = f"{base}/story_image.png"
    story_text_url  = f"{base}/story_text.png"

    print("\n--- aguardando GH Pages ---")
    for url in [feed_chart_url, feed_text_url, story_chart_url,
                 story_image_url, story_text_url]:
        if not wait_for_url(url, timeout=360):
            sys.exit(f"asset nao publicou no CDN: {url}")

    print("\n--- auth IG ---")
    token = parse_token()
    ig_user_id = get_ig_user_id(token)

    # Feed carousel
    print("\n=== POSTANDO FEED CARROSSEL ===")
    children = []
    for url in [feed_chart_url, feed_image_url, feed_text_url]:
        res = ig_post(token, ig_user_id,
                      {"image_url": url, "is_carousel_item": "true"})
        wait_container_ready(token, res["id"])
        children.append(res["id"])
        print(f"   child OK ({url.rsplit('/',1)[-1]})")
    car = ig_post(token, ig_user_id,
                  {"media_type": "CAROUSEL",
                   "children": ",".join(children), "caption": caption})
    wait_container_ready(token, car["id"], timeout=120)
    pub = ig_publish(token, ig_user_id, car["id"])
    print(f"   FEED publicado  media_id={pub.get('id')}")

    # Stories — tolerante a falhas parciais. O feed principal já foi
    # publicado; se 1 story extra falhar (timing da Meta API), não vale
    # abortar o workflow inteiro nem bloquear o Rebuild do site.
    print("\n=== POSTANDO STORIES ===")
    story_targets = [
        ("chart", story_chart_url),
        ("image", story_image_url),
        ("text",  story_text_url),
    ]
    success_count = 0
    for label, url in story_targets:
        try:
            res = ig_post(token, ig_user_id,
                          {"media_type": "STORIES", "image_url": url})
            wait_container_ready(token, res["id"], timeout=90)
            pub = ig_publish(token, ig_user_id, res["id"])
            print(f"   story '{label}' publicado  media_id={pub.get('id')}")
            success_count += 1
            time.sleep(6)  # antes era 3 — mais folga entre stories
        except Exception as exc:
            print(f"   story '{label}' FALHOU: {type(exc).__name__}: {str(exc)[:200]}")

    print(f"\n=== STORIES: {success_count}/{len(story_targets)} publicados ===")
    if success_count == 0:
        # Tudo falhou: sinaliza erro pra cron alertar.
        sys.exit("Nenhum story publicado — possivel problema sistemico (token, rede).")
    print(f"\nFeed publicado + {success_count} story(s). https://www.instagram.com/datafolia/")


# ─── Entrypoint ────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pub_id")
    ap.add_argument("--generate-only", action="store_true")
    ap.add_argument("--post-only", action="store_true")
    ap.add_argument("--no-push", action="store_true")
    args = ap.parse_args()

    pdir = ROOT / "publications" / args.pub_id
    if not pdir.exists():
        sys.exit(f"Pub nao encontrada: {pdir}")
    meta = json.loads((pdir / "metadata.json").read_text(encoding="utf-8"))
    artigo = (pdir / "artigo-site.md").read_text(encoding="utf-8")

    print(f"\n=== pub: {args.pub_id} ===")
    print(f"titulo: {meta['titulo']}")

    if not args.post_only:
        assets = generate_assets(pdir, meta, artigo)
        if not args.no_push:
            print("\n--- push assets ---")
            git_push_assets(assets)

    if args.generate_only:
        return

    post_to_ig(args.pub_id, pdir, meta, artigo)


if __name__ == "__main__":
    main()
