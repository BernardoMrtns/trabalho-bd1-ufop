from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import repositories as rep
from .crud import CrudFrame
from .util import to_int, to_float, to_str, to_optional_str
from .widgets import perguntar


class AbaTemporada(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_temporada", "ID", 50),
                     ("nome", "Nome", 200),
                     ("ano", "Ano", 70),
                     ("data_inicio", "Início", 110),
                     ("data_fim", "Fim", 110),
                     ("modalidade", "Modalidade", 140)],
            on_listar=rep.listar_temporadas,
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_editar_form=self._form_editar,
            on_atualizar=self._atualizar,
            on_excluir=self._excluir,
            chave_exclusao="id_temporada",
            label_entidade="temporada",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _opcoes_modalidade(self):
        return [f'{m["id_modalidade"]} - {m["nome"]}' for m in rep.listar_modalidades()]

    def _form_novo(self):
        return perguntar(self, "Nova Temporada", [
            {"chave": "nome", "rotulo": "Nome:", "obrigatorio": True},
            {"chave": "ano", "rotulo": "Ano:", "tipo": "numero", "obrigatorio": True},
            {"chave": "data_inicio", "rotulo": "Início (AAAA-MM-DD):", "obrigatorio": True},
            {"chave": "data_fim", "rotulo": "Fim (AAAA-MM-DD):", "obrigatorio": True},
            {"chave": "modalidade", "rotulo": "Modalidade:",
             "tipo": "combo", "opcoes": self._opcoes_modalidade()},
        ])

    def _form_editar(self, linha):
        return perguntar(self, "Editar Temporada", [
            {"chave": "nome", "rotulo": "Nome:", "valor": linha["nome"]},
            {"chave": "ano", "rotulo": "Ano:", "tipo": "numero", "valor": linha["ano"]},
            {"chave": "data_inicio", "rotulo": "Início (AAAA-MM-DD):",
             "valor": linha["data_inicio"]},
            {"chave": "data_fim", "rotulo": "Fim (AAAA-MM-DD):",
             "valor": linha["data_fim"]},
            {"chave": "modalidade", "rotulo": "Modalidade:",
             "tipo": "combo", "opcoes": self._opcoes_modalidade()},
        ])

    def _inserir(self, dados):
        id_mod = to_int(dados["modalidade"].split(" - ")[0])
        rep.inserir_temporada(to_str(dados["nome"]), int(dados["ano"]),
                              dados["data_inicio"], dados["data_fim"], id_mod)

    def _atualizar(self, dados):
        linha = dados["_linha"]
        id_mod = to_int(dados["modalidade"].split(" - ")[0])
        rep.atualizar_temporada(int(linha["id_temporada"]),
                                to_str(dados["nome"]), int(dados["ano"]),
                                dados["data_inicio"], dados["data_fim"], id_mod)

    def _excluir(self, linha):
        rep.remover_temporada(int(linha["id_temporada"]))


class AbaAtletas(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_pessoa", "ID", 50),
                     ("nome", "Nome", 250),
                     ("cpf", "CPF", 110),
                     ("data_nasc", "Nascimento", 120),
                     ("nacionalidade", "Nacionalidade", 130)],
            on_listar=lambda: rep.listar_pessoas("ATLETA"),
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_excluir=self._excluir,
            chave_exclusao="id_pessoa",
            label_entidade="atleta",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _form_novo(self):
        return perguntar(self, "Novo Atleta", [
            {"chave": "nome", "rotulo": "Nome:", "obrigatorio": True},
            {"chave": "cpf", "rotulo": "CPF (11 dígitos):", "obrigatorio": True},
            {"chave": "data_nasc", "rotulo": "Nasc. (AAAA-MM-DD):", "obrigatorio": True},
            {"chave": "nacionalidade", "rotulo": "Nacionalidade:", "valor": "Brasileira"},
            {"chave": "altura", "rotulo": "Altura (m):", "tipo": "numero"},
            {"chave": "peso", "rotulo": "Peso (kg):", "tipo": "numero"},
            {"chave": "num_camisa", "rotulo": "Nº camisa:", "tipo": "numero"},
        ])

    def _inserir(self, dados):
        rep.inserir_atleta(
            to_str(dados["nome"]), to_str(dados["cpf"]),
            dados["data_nasc"], to_str(dados.get("nacionalidade", "Brasileira")),
            float(dados["altura"]) if dados.get("altura") else 0.0,
            float(dados["peso"]) if dados.get("peso") else 0.0,
            to_int(dados.get("num_camisa")),
        )

    def _excluir(self, linha):
        rep.remover_pessoa(int(linha["id_pessoa"]))


class AbaArbitros(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_pessoa", "ID", 50),
                     ("nome", "Nome", 250),
                     ("cpf", "CPF", 110),
                     ("data_nasc", "Nascimento", 120),
                     ("nacionalidade", "Nacionalidade", 130)],
            on_listar=lambda: rep.listar_pessoas("ARBITRO"),
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_excluir=self._excluir,
            chave_exclusao="id_pessoa",
            label_entidade="árbitro",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _form_novo(self):
        return perguntar(self, "Novo Árbitro", [
            {"chave": "nome", "rotulo": "Nome:", "obrigatorio": True},
            {"chave": "cpf", "rotulo": "CPF:", "obrigatorio": True},
            {"chave": "data_nasc", "rotulo": "Nasc. (AAAA-MM-DD):", "obrigatorio": True},
            {"chave": "nacionalidade", "rotulo": "Nacionalidade:", "valor": "Brasileira"},
            {"chave": "categoria", "rotulo": "Categoria:"},
        ])

    def _inserir(self, dados):
        rep.inserir_arbitro(
            to_str(dados["nome"]), to_str(dados["cpf"]),
            dados["data_nasc"], to_str(dados.get("nacionalidade", "Brasileira")),
            to_optional_str(dados.get("categoria")),
        )

    def _excluir(self, linha):
        rep.remover_pessoa(int(linha["id_pessoa"]))


class AbaTecnicos(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_pessoa", "ID", 50),
                     ("nome", "Nome", 250),
                     ("cpf", "CPF", 110),
                     ("data_nasc", "Nascimento", 120),
                     ("nacionalidade", "Nacionalidade", 130)],
            on_listar=lambda: rep.listar_pessoas("TECNICO"),
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_excluir=self._excluir,
            chave_exclusao="id_pessoa",
            label_entidade="técnico",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _form_novo(self):
        return perguntar(self, "Novo Técnico", [
            {"chave": "nome", "rotulo": "Nome:", "obrigatorio": True},
            {"chave": "cpf", "rotulo": "CPF:", "obrigatorio": True},
            {"chave": "data_nasc", "rotulo": "Nasc. (AAAA-MM-DD):", "obrigatorio": True},
            {"chave": "nacionalidade", "rotulo": "Nacionalidade:", "valor": "Brasileira"},
            {"chave": "registro", "rotulo": "Registro federação:"},
        ])

    def _inserir(self, dados):
        rep.inserir_tecnico(
            to_str(dados["nome"]), to_str(dados["cpf"]),
            dados["data_nasc"], to_str(dados.get("nacionalidade", "Brasileira")),
            to_optional_str(dados.get("registro")),
        )

    def _excluir(self, linha):
        rep.remover_pessoa(int(linha["id_pessoa"]))


class AbaInscricao(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_temporada", "ID Temp.", 80),
                     ("temporada", "Temporada", 200),
                     ("id_equipe", "ID Eq.", 70),
                     ("equipe", "Equipe", 220)],
            on_listar=rep.listar_inscricoes,
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_excluir=self._excluir,
            chave_exclusao="id_temporada",
            label_entidade="inscrição",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _form_novo(self):
        temps = [f'{t["id_temporada"]} - {t["nome"]} ({t["ano"]})'
                 for t in rep.listar_temporadas()]
        equips = [f'{e["id_equipe"]} - {e["nome"]}' for e in rep.listar_equipes()]
        return perguntar(self, "Nova Inscrição", [
            {"chave": "temporada", "rotulo": "Temporada:",
             "tipo": "combo", "opcoes": temps},
            {"chave": "equipe", "rotulo": "Equipe:",
             "tipo": "combo", "opcoes": equips},
        ])

    def _inserir(self, dados):
        id_t = to_int(dados["temporada"].split(" - ")[0])
        id_e = to_int(dados["equipe"].split(" - ")[0])
        rep.inserir_inscricao(id_t, id_e)

    def _excluir(self, linha):
        rep.remover_inscricao(int(linha["id_temporada"]), int(linha["id_equipe"]))


class AbaContrato(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.crud = CrudFrame(
            self,
            colunas=[("id_contrato", "ID", 50),
                     ("atleta", "Atleta", 200),
                     ("equipe", "Equipe", 170),
                     ("temporada", "Temporada", 160),
                     ("salario", "Salário", 110),
                     ("data_inicio", "Início", 100),
                     ("data_fim", "Fim", 100)],
            on_listar=rep.listar_contratos,
            on_novo_form=self._form_novo,
            on_inserir=self._inserir,
            on_excluir=self._excluir,
            chave_exclusao="id_contrato",
            label_entidade="contrato",
        )
        self.crud.pack(fill="both", expand=True)
        self.after(50, self.crud.atualizar)

    def _opcoes(self):
        atletas = [f'{a["id_pessoa"]} - {a["nome"]}'
                   for a in rep.listar_pessoas("ATLETA")]
        equips = [f'{e["id_equipe"]} - {e["nome"]}' for e in rep.listar_equipes()]
        temps = [f'{t["id_temporada"]} - {t["nome"]} ({t["ano"]})'
                 for t in rep.listar_temporadas()]
        return atletas, equips, temps

    def _form_novo(self):
        atletas, equips, temps = self._opcoes()
        return perguntar(self, "Novo Contrato", [
            {"chave": "atleta", "rotulo": "Atleta:", "tipo": "combo", "opcoes": atletas},
            {"chave": "equipe", "rotulo": "Equipe:", "tipo": "combo", "opcoes": equips},
            {"chave": "temporada", "rotulo": "Temporada:",
             "tipo": "combo", "opcoes": temps},
            {"chave": "salario", "rotulo": "Salário:", "tipo": "numero"},
            {"chave": "data_inicio", "rotulo": "Início (AAAA-MM-DD):"},
            {"chave": "data_fim", "rotulo": "Fim (AAAA-MM-DD): (vazio=ativo)"},
        ])

    def _inserir(self, dados):
        rep.inserir_contrato(
            to_int(dados["atleta"].split(" - ")[0]),
            to_int(dados["equipe"].split(" - ")[0]),
            to_int(dados["temporada"].split(" - ")[0]),
            float(dados["salario"]) if dados.get("salario") else 0.0,
            dados["data_inicio"],
            to_optional_str(dados.get("data_fim")),
        )

    def _excluir(self, linha):
        rep.remover_contrato(int(linha["id_contrato"]))
