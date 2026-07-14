from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from .widgets import Tabela, avisar, confirmar, informar
from .util import to_str


class CrudFrame(ttk.Frame):
    def __init__(
        self,
        master,
        colunas: list[tuple[str, str, int]],
        on_listar: Callable[[], list[dict]],
        on_novo_form: Callable[[], dict | None] | None = None,
        on_inserir: Callable[[dict], None] | None = None,
        on_editar_form: Callable[[dict], dict | None] | None = None,
        on_atualizar: Callable[[dict], None] | None = None,
        on_excluir: Callable[[dict], None] | None = None,
        chave_exclusao: str = "id",
        label_entidade: str = "registro",
    ):
        super().__init__(master, padding=8)

        self._on_listar = on_listar
        self._on_novo = on_novo_form
        self._on_inserir = on_inserir
        self._on_editar = on_editar_form
        self._on_atualizar = on_atualizar
        self._on_excluir = on_excluir
        self._chave = chave_exclusao
        self._label = label_entidade

        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 6))

        if on_novo_form:
            ttk.Button(barra, text="➕ Novo", command=self._novo).pack(side="left")
        if on_editar_form:
            ttk.Button(barra, text="✏️ Editar", command=self._editar).pack(side="left", padx=4)
        ttk.Button(barra, text="🗑️ Excluir", command=self._excluir).pack(side="left", padx=4)
        ttk.Button(barra, text="🔄 Atualizar", command=self.atualizar).pack(side="left", padx=4)

        self.tabela = Tabela(self, colunas, on_duplo_clique=self._on_duplo_clique)
        self.tabela.pack(fill="both", expand=True)

    def _on_duplo_clique(self, _linha):
        if self._on_editar:
            self._editar()

    def atualizar(self) -> None:
        try:
            dados = self._on_listar()
        except Exception as e:
            avisar("Erro ao carregar", f"{e}")
            dados = []
        self.tabela.preencher(dados)

    def _novo(self) -> None:
        if not self._on_novo or not self._on_inserir:
            return
        try:
            dados = self._on_novo()
        except Exception as e:
            avisar("Erro no formulário", f"{e}")
            return
        if dados is None:
            return
        try:
            self._on_inserir(dados)
            self.atualizar()
            informar("Sucesso", f"{self._label.capitalize()} cadastrado.")
        except Exception as e:
            avisar("Erro ao inserir", f"{e}")

    def _editar(self) -> None:
        if not self._on_editar or not self._on_atualizar:
            return
        linha = self.tabela.linha_selecionada()
        if not linha:
            avisar("Selecionar", f"Selecione um {self._label} na tabela.")
            return
        try:
            dados = self._on_editar(linha)
        except Exception as e:
            avisar("Erro no formulário", f"{e}")
            return
        if dados is None:
            return
        try:
            dados["_linha"] = linha
            self._on_atualizar(dados)
            self.atualizar()
            informar("Sucesso", f"{self._label.capitalize()} atualizado.")
        except Exception as e:
            avisar("Erro ao atualizar", f"{e}")

    def _excluir(self) -> None:
        if not self._on_excluir:
            return
        linha = self.tabela.linha_selecionada()
        if not linha:
            avisar("Selecionar", f"Selecione um {self._label} na tabela.")
            return
        chave = to_str(linha.get(self._chave, ""))
        if not confirmar("Confirmar exclusão",
                         f"Excluir {self._label} '{chave}'?\nEsta ação não pode ser desfeita."):
            return
        try:
            self._on_excluir(linha)
            self.atualizar()
            informar("Sucesso", f"{self._label.capitalize()} excluído.")
        except Exception as e:
            avisar("Erro ao excluir", f"{e}")
