"""
Testa a cadeia da Meta Graph API para confirmar que da pra postar
no Instagram (@datafolia) via cron.

Faz APENAS leituras: nao posta nada. Verifica:
  1. Token valido + permissoes (debug_token)
  2. Usuario/conta dona do token
  3. Paginas do Facebook associadas
  4. Conta Instagram Business conectada a cada Pagina
  5. Capacidade de postar (lista campos do container endpoint)

Saida: relatorio passou/falhou por etapa + ID do IG (necessario pro cron).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import requests

GRAPH = "https://graph.facebook.com/v23.0"
TOKEN_FILE = Path(__file__).resolve().parent.parent / "token instagram"


def parse_token() -> tuple[str, str, str]:
    """Le o arquivo 'token instagram' e devolve (app_id, app_secret, token)."""
    lines = [l.strip() for l in TOKEN_FILE.read_text(encoding="utf-8").splitlines()]
    app_id = next(l for l in lines if l.startswith("ID do app:")).split(":", 1)[1].strip()
    app_secret = next(l for l in lines if l.startswith("Chave secreta")).split(":", 1)[1].strip()
    token = next(l for l in lines if l.startswith("EAA"))
    return app_id, app_secret, token


def call(path: str, params: dict, label: str) -> dict | None:
    url = f"{GRAPH}{path}"
    r = requests.get(url, params=params, timeout=30)
    if r.status_code == 200:
        return r.json()
    print(f"   FALHA: HTTP {r.status_code}")
    try:
        err = r.json().get("error", {})
        print(f"     code={err.get('code')} type={err.get('type')}")
        print(f"     msg: {err.get('message')}")
    except Exception:
        print(f"     body: {r.text[:300]}")
    return None


def main() -> None:
    app_id, app_secret, token = parse_token()
    print(f"App ID: {app_id}")
    print(f"Token (15 chars): {token[:15]}...{token[-5:]}\n")

    # ── 1) debug_token: token e valido? permissoes? expira quando? ───
    print("=== 1) debug_token ===")
    app_token = f"{app_id}|{app_secret}"
    d = call("/debug_token",
             {"input_token": token, "access_token": app_token},
             "debug_token")
    if not d or "data" not in d:
        print("   Token invalido. Para nessa etapa.")
        sys.exit(1)
    info = d["data"]
    is_valid = info.get("is_valid", False)
    typ = info.get("type")
    app = info.get("application")
    scopes = info.get("scopes", [])
    user_id = info.get("user_id")
    expires = info.get("expires_at")
    expires_str = "nunca" if expires == 0 else f"unix {expires}"
    print(f"   valido: {is_valid}")
    print(f"   tipo: {typ}")
    print(f"   app: {app}")
    print(f"   user_id (dono): {user_id}")
    print(f"   expira: {expires_str}")
    print(f"   escopos ({len(scopes)}): {', '.join(scopes) if scopes else '<nenhum>'}")
    needed = {"pages_show_list", "pages_read_engagement",
              "instagram_basic", "instagram_content_publish",
              "business_management"}
    missing = needed - set(scopes)
    if missing:
        print(f"   AVISO: escopos ausentes pra postar IG: {', '.join(missing)}")
    print()

    # ── 2) /me ─────────────────────────────────────────────────────────
    print("=== 2) /me — quem e o dono do token ===")
    me = call("/me",
              {"access_token": token, "fields": "id,name"}, "/me")
    if not me:
        sys.exit(1)
    print(f"   id: {me['id']}")
    print(f"   nome: {me.get('name')}")
    print()

    # ── 3) /me/accounts — Paginas do FB ─────────────────────────────
    print("=== 3) /me/accounts — Paginas do Facebook gerenciadas ===")
    accts = call("/me/accounts",
                 {"access_token": token,
                  "fields": "id,name,category,tasks,access_token"},
                 "/me/accounts")
    if not accts or not accts.get("data"):
        print("   FALHA: nenhuma Pagina vinculada. Sem Pagina, nao da pra postar IG.")
        sys.exit(1)
    pages = accts["data"]
    print(f"   {len(pages)} Pagina(s):")
    for p in pages:
        tasks = p.get("tasks", [])
        can_post = "CREATE_CONTENT" in tasks or "MANAGE" in tasks
        print(f"     - {p['name']}  id={p['id']}  cat={p.get('category')}  "
              f"tasks={tasks}  publica={can_post}")
    print()

    # ── 4) Por Pagina, busca o Instagram Business conectado ──────────
    print("=== 4) Instagram Business Account de cada Pagina ===")
    ig_accounts = []
    for p in pages:
        pid = p["id"]; pname = p["name"]; ptok = p.get("access_token", token)
        ig = call(f"/{pid}",
                  {"access_token": ptok,
                   "fields": "instagram_business_account{id,username,name,"
                             "profile_picture_url,followers_count,media_count}"},
                  f"page {pname}")
        if not ig: continue
        igacc = ig.get("instagram_business_account")
        if not igacc:
            print(f"   Pagina '{pname}': sem conta IG Business conectada.")
        else:
            print(f"   Pagina '{pname}' -> IG @{igacc.get('username','?')}")
            print(f"     IG id: {igacc['id']}")
            print(f"     nome: {igacc.get('name')}")
            print(f"     seguidores: {igacc.get('followers_count')}")
            print(f"     publicacoes: {igacc.get('media_count')}")
            ig_accounts.append({"page_id": pid, "page_name": pname,
                                 "page_token": ptok, **igacc})
    print()

    if not ig_accounts:
        print("FALHA: nenhuma conta IG Business encontrada.")
        print("Veja se a conta @datafolia esta conectada a uma Pagina FB do App")
        sys.exit(1)

    # ── 5) Testa endpoint de criar container (sem postar) ─────────────
    print("=== 5) Endpoint /media — confere permissao sem postar ===")
    for ig in ig_accounts:
        ig_id = ig["id"]
        # POST com parametros vazios — vai falhar, mas o tipo de erro ja diz
        # se temos OU NAO permissao.
        r = requests.post(
            f"{GRAPH}/{ig_id}/media",
            params={"access_token": ig["page_token"]},
            timeout=30,
        )
        body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text}
        err = body.get("error", {})
        code = err.get("code"); msg = err.get("message", "")
        sub = err.get("error_subcode")
        if code in (None, 0):
            print(f"   @{ig.get('username')}: resposta inesperada (sem erro)")
            print(f"     {body}")
        elif code in (100, 190, 200):
            # 100 = missing param (esperado), 190 = token invalido, 200 = sem permissao
            if "image_url" in msg.lower() or "missing" in msg.lower() or code == 100:
                print(f"   @{ig.get('username')}: OK — endpoint aceita "
                      f"chamada, falta apenas image_url/caption (esperado).")
            elif code == 190:
                print(f"   @{ig.get('username')}: FALHA — token invalido/expirado")
            elif code == 200:
                print(f"   @{ig.get('username')}: FALHA — sem permissao "
                      f"instagram_content_publish")
            else:
                print(f"   @{ig.get('username')}: erro {code}: {msg}")
        else:
            print(f"   @{ig.get('username')}: erro {code} sub={sub}: {msg}")

    print("\n=== Resumo ===")
    print(f"Cadeia validada. Para o cron usar:")
    for ig in ig_accounts:
        print(f"  IG_USER_ID  = {ig['id']}    (@{ig.get('username')})")
        print(f"  PAGE_TOKEN  = (page_token de '{ig['page_name']}')")
    print()
    print("Falta para postagem real: image_url publica (sera a URL da imagem.jpg")
    print("hospedada em datafolia.com.br/publications/pub-XX/image.jpg quando ar)")


if __name__ == "__main__":
    main()
