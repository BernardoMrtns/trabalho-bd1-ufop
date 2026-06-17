@echo off
REM ============================================================
REM  SportsLeagueDB — inicializador (Windows)
REM  Instala dependências (se necessário) e abre a aplicação.
REM ============================================================
setlocal
cd /d "%~dp0\src"

echo Verificando psycopg2...
python -c "import psycopg2" 2>nul
if errorlevel 1 (
    echo psycopg2 nao encontrado. Instalando dependencias...
    python -m pip install -r "%~dp0requirements.txt"
)

echo Iniciando SportsLeagueDB...
python app.py
endlocal
