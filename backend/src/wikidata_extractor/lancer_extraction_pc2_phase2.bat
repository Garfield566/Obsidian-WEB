@echo off
REM ================================================================================
REM EXTRACTION PC2 PHASE 2 - Lancement automatique
REM Données stockées sur E:\extraction_quartz\extracted_by_domain\
REM ================================================================================

echo ================================================================================
echo LANCEMENT EXTRACTION PC2 PHASE 2 - 11 DOMAINES RESTANTS
echo ================================================================================
echo.
echo Disque externe: E:\
echo Repertoire code: E:\extraction_quartz\wikidata_extractor\
echo Repertoire sortie: E:\extraction_quartz\extracted_by_domain\
echo.
echo ================================================================================
pause

REM Se placer dans le répertoire du code sur E:\
cd /d E:\extraction_quartz\wikidata_extractor

REM Lancer l'extraction Phase 2
python extract_pc2_phase2.py

pause
