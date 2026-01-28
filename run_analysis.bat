@echo off
REM ============================================================
REM Script de lancement local pour l'analyse des tags
REM Compatible avec GitHub Actions (memes chemins)
REM ============================================================

echo.
echo ========================================
echo    ANALYSE LOCALE DES TAGS
echo ========================================
echo.

REM Se positionner dans le repertoire du projet
cd /d "%~dp0"

REM Verifier que Python est disponible
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    pause
    exit /b 1
)

REM Creer les repertoires necessaires si absents
if not exist "backend\data" mkdir "backend\data"
if not exist "content\emergent-tags" mkdir "content\emergent-tags"

REM Definir PYTHONPATH
set PYTHONPATH=%cd%

echo [1/2] Verification des dependances...
pip show sentence-transformers >nul 2>&1
if errorlevel 1 (
    echo     Installation des dependances...
    pip install -r backend\requirements.txt
) else (
    echo     Dependances OK
)

echo.
echo [2/2] Lancement de l'analyse...
echo.

python -m backend.src.main ^
    --vault-path ./content ^
    --output content/emergent-tags/suggestions.json ^
    --db-path backend/data/tags.db ^
    --decisions content/emergent-tags/decisions.json ^
    --verbose

echo.
echo ========================================
if errorlevel 1 (
    echo    ANALYSE TERMINEE AVEC ERREURS
) else (
    echo    ANALYSE TERMINEE AVEC SUCCES
)
echo ========================================
echo.
echo Fichier genere: content\emergent-tags\suggestions.json
echo.

pause
