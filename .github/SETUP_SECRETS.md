# Configurar secrets do GitHub Actions

O workflow `.github/workflows/post-weekly.yml` precisa de dois secrets no repositório `calculadoraestatistica/datafolia`:

1. `IG_TOKEN` — o long-lived user access token da Meta Graph API (começa com `EAA...`)
2. `IG_USER_ID` — o ID do IG Business Account (atual: `17841433145266122`)

## Como adicionar

1. Abra https://github.com/calculadoraestatistica/datafolia/settings/secrets/actions
2. Clique **New repository secret**
3. Nome: `IG_TOKEN`, valor: cole o token (a linha que começa com `EAA...` no arquivo `token instagram` local)
4. **Add secret**
5. Repita para `IG_USER_ID` = `17841433145266122`

## Como testar a cron sem esperar segunda

1. https://github.com/calculadoraestatistica/datafolia/actions
2. Clique no workflow **Post weekly to Instagram**
3. Botão **Run workflow** (canto direito)
4. No campo `pub_id` digite a pub que quer testar (ex: `pub-23-ana-maria-braga-x-japao`).
   Deixe em branco se quiser usar a pub agendada para a data de hoje.
5. **Run workflow**

## Cadência automática

- Cron: toda segunda às **12:00 UTC** (≈ 09:00 BRT)
- Lê `publications/pub-*/metadata.json`, acha a pub cuja `data_post` == hoje
- Pula se nenhuma bate (sem erro)
- Ignora a pub marcada com `post_zero: true`

## Token expira

O token long-lived da Meta dura ~60 dias. Renovar via Graph API Explorer ou via
`POST /oauth/access_token?grant_type=fb_exchange_token&...` antes de expirar e
atualizar o secret `IG_TOKEN`.
