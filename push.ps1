# Uso: .\push.ps1 "mensagem do commit"
# Faz add -A, commit com a mensagem e push pro GitHub via helper.

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$Message
)

$ErrorActionPreference = "Stop"

# 1. Status
Write-Host ">>> git status" -ForegroundColor Cyan
git status -s
if (-not $?) { exit 1 }

# Aborta se nao tem nada pra commitar
$changes = git status --porcelain
if ([string]::IsNullOrWhiteSpace($changes)) {
    Write-Host "Nada para commitar." -ForegroundColor Yellow
    exit 0
}

# 2. Add + commit
Write-Host ">>> git add + commit" -ForegroundColor Cyan
git add -A
if (-not $?) { exit 1 }
git commit -m $Message
if (-not $?) { exit 1 }

# 3. Push via helper
Write-Host ">>> git push (autenticado via helper)" -ForegroundColor Cyan
& "C:/Users/vinyn/miniconda3/python.exe" `
  "C:/Users/vinyn/Desktop/Vinícius/claude_infos/claude_github/use_account.py" `
  --account site_calculadora_estatistica `
  -- git push origin main
if (-not $?) { exit 1 }

Write-Host "OK — pushed." -ForegroundColor Green
