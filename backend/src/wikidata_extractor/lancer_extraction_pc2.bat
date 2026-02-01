@echo off
REM ================================================================================
REM EXTRACTION PC2 - Lancement automatique
REM Données stockées sur F:\extraction_quartz\extracted_by_domain\
REM ================================================================================

echo ================================================================================
echo LANCEMENT EXTRACTION PC2 - 21 DOMAINES
echo ================================================================================
echo.
echo Disque externe: F:\
echo Repertoire code: F:\extraction_quartz\wikidata_extractor\
echo Repertoire sortie: F:\extraction_quartz\extracted_by_domain\
echo.
echo ================================================================================
pause

REM Se placer dans le répertoire du code sur F:\
cd /d F:\extraction_quartz\wikidata_extractor

REM Lancer l'extraction
python extract_pc2_external.py

pause
