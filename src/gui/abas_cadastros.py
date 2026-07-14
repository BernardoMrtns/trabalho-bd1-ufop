from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import repositories as rep
from .crud import CrudFrame
from .util import to_int, to_str, to_optional_str
from .widgets import perguntar


class AbaModalidade(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_modalidade", "ID", 60),
                     ("nome", "Nome", 250),
                     ("n_jogadores_por_time", "Jogadores", 100)],
            on_listar=rep.listar_modalidades,
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_editar_form=self._form_editar,
            on_atualizar=self._atualizar,
            on_excluir=self._excluir,
            chave_exclusao="id_modalidade",
            label_entidade="modalidade",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _form_novo(self):
        return perguntar(self, "Nova Modalidade", [
            {"chave": "nome", "rotulo": "Nome:", "obrigatorio": True},
            {"chave": "n_jogadores", "rotulo": "Jogadores/time:",
             "tipo": "numero", "obrigatorio": True},
        ])

    def _form_editar(self, linha):
        return perguntar(self, "Editar Modalidade", [
            {"chave": "nome", "rotulo": "Nome:", "valor": linha["nome"]},
            {"chave": "n_jogadores", "rotulo": "Jogadores/time:",
             "tipo": "numero", "valor": linha["n_jogadores_por_time"]},
        ])

    def _inserir(self, dados):
        rep.inserir_modalidade(to_str(dados["nome"]), int(dados["n_jogadores"]))

    def _atualizar(self, dados):
        linha = dados["_linha"]
        rep.atualizar_modalidade(int(linha["id_modalidade"]),
                                 to_str(dados["nome"]),
                                 int(dados["n_jogadores"]))

    def _excluir(self, linha):
        rep.remover_modalidade(int(linha["id_modalidade"]))


class AbaPosicao(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_posicao", "ID", 60),
                     ("nome", "Posição", 200),
                     ("modalidade", "Modalidade", 200)],
            on_listar=rep.listar_posicoes,
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_excluir=self._excluir,
            chave_exclusao="id_posicao",
            label_entidade="posição",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _opcoes_modalidade(self):
        return [f'{m["id_modalidade"]} - {m["nome"]}' for m in rep.listar_modalidades()]

    def _form_novo(self):
        return perguntar(self, "Nova Posição", [
            {"chave": "nome", "rotulo": "Posição:", "obrigatorio": True},
            {"chave": "modalidade", "rotulo": "Modalidade:",
             "tipo": "combo", "opcoes": self._opcoes_modalidade()},
        ])

    def _inserir(self, dados):
        id_mod = to_int(dados["modalidade"].split(" - ")[0])
        rep.inserir_posicao(to_str(dados["nome"]), id_mod)

    def _excluir(self, linha):
        rep.remover_posicao(int(linha["id_posicao"]))


class AbaEstadio(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_estadio", "ID", 60),
                     ("nome", "Nome", 250),
                     ("cidade", "Cidade", 160),
                     ("capacidade", "Capacidade", 110)],
            on_listar=rep.listar_estadios,
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_editar_form=self._form_editar,
            on_atualizar=self._atualizar,
            on_excluir=self._excluir,
            chave_exclusao="id_estadio",
            label_entidade="estádio",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _form_novo(self):
        return perguntar(self, "Novo Estádio", [
            {"chave": "nome", "rotulo": "Nome:", "obrigatorio": True},
            {"chave": "cidade", "rotulo": "Cidade:", "obrigatorio": True},
            {"chave": "capacidade", "rotulo": "Capacidade:",
             "tipo": "numero", "obrigatorio": True},
        ])

    def _form_editar(self, linha):
        return perguntar(self, "Editar Estádio", [
            {"chave": "nome", "rotulo": "Nome:", "valor": linha["nome"]},
            {"chave": "cidade", "rotulo": "Cidade:", "valor": linha["cidade"]},
            {"chave": "capacidade", "rotulo": "Capacidade:",
             "tipo": "numero", "valor": linha["capacidade"]},
        ])

    def _inserir(self, dados):
        rep.inserir_estadio(to_str(dados["nome"]), to_str(dados["cidade"]),
                            int(dados["capacidade"]))

    def _atualizar(self, dados):
        linha = dados["_linha"]
        rep.atualizar_estadio(int(linha["id_estadio"]),
                              to_str(dados["nome"]),
                              to_str(dados["cidade"]),
                              int(dados["capacidade"]))

    def _excluir(self, linha):
        rep.remover_estadio(int(linha["id_estadio"]))


class AbaEquipe(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_equipe", "ID", 60),
                     ("nome", "Nome", 220),
                     ("sigla", "Sigla", 70),
                     ("cidade", "Cidade", 150),
                     ("estadio_sede", "Estádio Sede", 200)],
            on_listar=rep.listar_equipes,
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_editar_form=self._form_editar,
            on_atualizar=self._atualizar,
            on_excluir=self._excluir,
            chave_exclusao="id_equipe",
            label_entidade="equipe",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _opcoes_estadio(self):
        opcoes = ["(nenhum)"]
        opcoes += [f'{e["id_estadio"]} - {e["nome"]}' for e in rep.listar_estadios()]
        return opcoes

    def _form_novo(self):
        return perguntar(self, "Nova Equipe", [
            {"chave": "nome", "rotulo": "Nome:", "obrigatorio": True},
            {"chave": "sigla", "rotulo": "Sigla (até 5):", "obrigatorio": True},
            {"chave": "cidade", "rotulo": "Cidade:", "obrigatorio": True},
            {"chave": "estadio", "rotulo": "Estádio sede:",
             "tipo": "combo", "opcoes": self._opcoes_estadio()},
        ])

    def _form_editar(self, linha):
        return perguntar(self, "Editar Equipe", [
            {"chave": "nome", "rotulo": "Nome:", "valor": linha["nome"]},
            {"chave": "sigla", "rotulo": "Sigla (até 5):", "valor": linha["sigla"]},
            {"chave": "cidade", "rotulo": "Cidade:", "valor": linha["cidade"]},
            {"chave": "estadio", "rotulo": "Estádio sede:",
             "tipo": "combo", "opcoes": self._opcoes_estadio()},
        ])

    def _id_estadio(self, valor):
        if not valor or valor.startswith("("):
            return None
        return to_int(valor.split(" - ")[0])

    def _inserir(self, dados):
        rep.inserir_equipe(to_str(dados["nome"]), to_str(dados["sigla"]),
                           to_str(dados["cidade"]),
                           self._id_estadio(dados["estadio"]))

    def _atualizar(self, dados):
        linha = dados["_linha"]
        rep.atualizar_equipe(int(linha["id_equipe"]),
                             to_str(dados["nome"]), to_str(dados["sigla"]),
                             to_str(dados["cidade"]),
                             self._id_estadio(dados["estadio"]))

    def _excluir(self, linha):
        rep.remover_equipe(int(linha["id_equipe"]))
