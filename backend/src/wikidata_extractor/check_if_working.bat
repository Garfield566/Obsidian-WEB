@echo off
echo ========================================
echo VERIFICATION: Le nouveau code fonctionne-t-il?
echo ========================================
echo.

cd "C:\Users\robin tual\quartz\backend\src\wikidata_extractor\extracted_by_domain\mathematiques"

if exist mathematiques_specialized_terms.json (
    echo [OK] Le fichier specialized_terms.json EXISTE!
    echo [OK] Le nouveau code fonctionne correctement!
    echo.
    dir mathematiques_specialized_terms.json
    echo.
    echo Contenu (premieres lignes):
    type mathematiques_specialized_terms.json | more /E
) else (
    echo [ERREUR] Le fichier specialized_terms.json N'EXISTE PAS
    echo.
    echo Cela signifie:
    echo - Soit l'extraction n'a pas encore atteint la phase 2
    echo - Soit l'extraction utilise encore l'ancien code
    echo.
    echo Solution: Arretez l'extraction (Ctrl+C) et relancez-la
)

echo.
echo ========================================
pause
