# Cron externo confiável para DataFolia

GitHub Actions schedule é unreliable: pode atrasar até 1h e silenciosamente pular
se a carga estiver alta. Em 4 semanas, **o cron `post-weekly` nunca disparou via
schedule** — todos os posts foram feitos com `workflow_dispatch` manual.

A solução padrão é usar um **scheduler externo** (cron-job.org) que faz POST
autenticado no endpoint `workflow_dispatch` da GitHub API. Uptime histórico
~99.95% + e-mail automático se uma execução falhar.

## Passos (~5 min)

### 1. Criar Personal Access Token fine-grained
1. Acesse <https://github.com/settings/personal-access-tokens/new>
2. Token name: `datafolia-cron-external`
3. Expiration: 1 ano (ou "No expiration" se preferir)
4. Resource owner: `calculadoraestatistica`
5. Repository access: **Only select repositories** → `datafolia`
6. Permissions → Repository permissions:
   - **Actions**: Read and write
   - **Contents**: Read-only (necessário pra triggers em `workflow_dispatch`)
   - **Metadata**: Read-only (vem automático)
7. Generate token. **Copia o token agora** (não vai aparecer de novo).

### 2. Cadastrar no cron-job.org
1. Sign up grátis em <https://cron-job.org>
2. Confirma email
3. Configurações → Notifications → habilita "Email on failure"

### 3. Criar 2 cron jobs

#### Job 1: Preview de quinta
- **Title**: `DataFolia · preview de quinta`
- **URL**: `https://api.github.com/repos/calculadoraestatistica/datafolia/actions/workflows/preview-thursday.yml/dispatches`
- **Schedule**: aba "Schedule" → Common schedules → "Every Thursday at 12:07 UTC"
  (ou Custom: Day of week = Thursday, Hour = 12, Minute = 7)
- **Request method**: POST
- **Request body**: `{"ref":"main"}`
- **Headers**:
  ```
  Authorization: Bearer <SEU_TOKEN_DO_PASSO_1>
  Accept: application/vnd.github.v3+json
  X-GitHub-Api-Version: 2022-11-28
  Content-Type: application/json
  ```
- **Treat redirects as success**: Off
- **Save**

Resposta esperada do GitHub: **HTTP 204 No Content** (success, workflow disparado).

#### Job 2: Post de segunda
Mesma config, só muda:
- **Title**: `DataFolia · post de segunda`
- **URL**: troca `preview-thursday.yml` por `post-weekly.yml`
- **Schedule**: Monday at 22:07 UTC

### 4. Teste imediato
- Em cada job no cron-job.org clica "**Test run**" → confirma HTTP 204
- Volta em <https://github.com/calculadoraestatistica/datafolia/actions> → vê o
  workflow rodando com `event: workflow_dispatch`

### 5. (Opcional) Manter cron interno como backup
Os blocos `on: schedule` nos dois workflows YAML podem ficar — quando o cron
do GitHub roda (raramente), o `Determinar pub_id` simplesmente pega a próxima
publicação não-postada. Como `post-weekly` checa se a `data_post == today()`
antes de postar, nunca posta a mesma pub 2x mesmo se ambos os schedulers
dispararem.

## Por que isso é mais confiável

- **cron-job.org**: schedules ficam em servidores dedicados; uptime 99.95%
  histórico; envia email se uma execução der erro.
- **GitHub Actions schedule**: roda em best-effort. Doc oficial diz:
  > scheduled workflows are paused during high load; if not run within 1h, are skipped silently
- A combinação dos dois (interno + externo) reduz a chance de skip a quase zero.

## Manutenção

- O token PAT do passo 1 expira (se você definiu prazo). Anote pra renovar.
- Se trocar a senha do GitHub não afeta o token, mas se for revogado no
  settings, o cron começa a falhar com HTTP 401 (que cron-job.org alerta por
  email).
- Pra mudar o horário: editar direto no painel do cron-job.org, sem touch no
  repo.
