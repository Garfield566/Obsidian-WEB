# ============================================================
# Script PowerShell de lancement local pour l'analyse des tags
# Compatible avec GitHub Actions (memes chemins)
# ============================================================

param(
    [switch]$Quick,      # Mode rapide (sans pause)
    [switch]$SkipDeps,   # Ne pas verifier les dependances
    [int]$MaxNotes = 0   # Limiter le nombre de notes (0 = toutes)
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   ANALYSE LOCALE DES TAGS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Se positionner dans le repertoire du projet
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

# Verifier Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] Python non trouve!" -ForegroundColor Red
    exit 1
}

# Creer les repertoires
New-Item -ItemType Directory -Path "backend\data" -Force | Out-Null
New-Item -ItemType Directory -Path "content\emergent-tags" -Force | Out-Null

# PYTHONPATH
$env:PYTHONPATH = $ProjectRoot

# Dependances
if (-not $SkipDeps) {
    Write-Host "[1/2] Verification des dependances..." -ForegroundColor Yellow
    $hasDeps = pip show sentence-transformers 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "     Installation des dependances..." -ForegroundColor Yellow
        pip install -r backend\requirements.txt
    } else {
        Write-Host "     Dependances OK" -ForegroundColor Green
    }
}

# Lancement
Write-Host ""
Write-Host "[2/2] Lancement de l'analyse..." -ForegroundColor Yellow
Write-Host ""

$startTime = Get-Date

python -m backend.src.main `
    --vault-path ./content `
    --output content/emergent-tags/suggestions.json `
    --db-path backend/data/tags.db `
    --decisions content/emergent-tags/decisions.json `
    --verbose

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($LASTEXITCODE -eq 0) {
    Write-Host "   ANALYSE TERMINEE AVEC SUCCES" -ForegroundColor Green
} else {
    Write-Host "   ANALYSE TERMINEE AVEC ERREURS" -ForegroundColor Red
}
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Duree: $($duration.ToString('mm\:ss'))" -ForegroundColor Gray
Write-Host "Fichier: content\emergent-tags\suggestions.json" -ForegroundColor Gray
Write-Host ""

if (-not $Quick) {
    Read-Host "Appuyez sur Entree pour fermer"
}
