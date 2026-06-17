"""
Utilidades de conversão de tipos para a GUI.

Os formulários devolvem strings. As funções SQL esperam int/float/None.
Estes helpers fazem a normalização mantendo o código das abas legível.
"""
from __future__ import annotations

from typing import Any


def to_int(valor: Any, default: int | None = None) -> int | None:
    if valor is None or valor == "":
        return default
    try:
        return int(str(valor).strip())
    except (ValueError, TypeError):
        return default


def to_float(valor: Any, default: float | None = None) -> float | None:
    if valor is None or valor == "":
        return default
    try:
        return float(str(valor).strip())
    except (ValueError, TypeError):
        return default


def to_str(valor: Any) -> str:
    if valor is None:
        return ""
    return str(valor).strip()


def to_optional_str(valor: Any) -> str | None:
    if valor is None:
        return None
    s = str(valor).strip()
    return s if s else None
