"""
Ponto de entrada da aplicação SportsLeagueDB.

Execute com:
    python app.py
ou
    python -m app

A partir da pasta src/.
"""
import sys
import os

# Garante que a pasta src/ esteja no sys.path quando executado direto.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main import main


if __name__ == "__main__":
    main()
