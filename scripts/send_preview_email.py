"""
Envia o PDF preview do proximo post por email via Gmail API.

Credenciais via env vars (workflow GH Actions injeta dos secrets):
  GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN, MAIL_FROM

Destinatarios fixos (mas pode override via env MAIL_TO):
  - v178334@dac.unicamp.br (Vinicius)
  - g268952@dac.unicamp.br (Giovana)
"""
from __future__ import annotations
import argparse
import base64
import datetime as dt
import json
import mimetypes
import os
import sys
from email.message import EmailMessage
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_TO = ["v178334@dac.unicamp.br", "g268952@dac.unicamp.br"]


def fresh_access_token() -> str:
    cid = os.environ["GMAIL_CLIENT_ID"]
    cs  = os.environ["GMAIL_CLIENT_SECRET"]
    rt  = os.environ["GMAIL_REFRESH_TOKEN"]
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": cid, "client_secret": cs,
        "refresh_token": rt, "grant_type": "refresh_token",
    }, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def build_message(sender: str, to: list[str], subject: str, body: str,
                   attach: Path) -> str:
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = ", ".join(to)
    msg["Subject"] = subject
    msg.set_content(body)
    ctype, _ = mimetypes.guess_type(str(attach))
    maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
    msg.add_attachment(attach.read_bytes(), maintype=maintype,
                        subtype=subtype, filename=attach.name)
    return base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")


def send(access_token: str, raw_b64: str) -> dict:
    r = requests.post(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        headers={"Authorization": f"Bearer {access_token}",
                  "Content-Type": "application/json"},
        json={"raw": raw_b64}, timeout=60)
    if r.status_code >= 400:
        sys.exit(f"Gmail API erro {r.status_code}: {r.text[:500]}")
    return r.json()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True, help="caminho do PDF")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--body", required=True)
    ap.add_argument("--to", nargs="*", default=None,
                     help="lista de destinatarios; default=Vini+Giovana")
    args = ap.parse_args()

    pdf = Path(args.pdf)
    if not pdf.exists():
        sys.exit(f"PDF nao encontrado: {pdf}")
    to = args.to or DEFAULT_TO
    sender = os.environ.get("MAIL_FROM") or to[0]

    print(f"De:        {sender}")
    print(f"Para:      {', '.join(to)}")
    print(f"Assunto:   {args.subject}")
    print(f"Anexo:     {pdf.name} ({pdf.stat().st_size/1024:.1f} KB)")

    tok = fresh_access_token()
    raw = build_message(sender, to, args.subject, args.body, pdf)
    res = send(tok, raw)
    print(f"\nEnviado: messageId={res.get('id')}")


if __name__ == "__main__":
    main()
