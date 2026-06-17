"""
Aba de Partidas e seus Eventos.

Layout: lista de partidas em cima; ao selecionar uma, os eventos dela aparecem
embaixo, com botões para adicionar/remover eventos (gols, cartões, substituições).
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import repositories as rep
from .util import to_int, to_str, to_optional_str
from .widgets import Tabela, perguntar, avisar, confirmar, informar

STATUS_OPCOES = ["AGENDADA", "EM_ANDAMENTO", "ENCERRADA", "CANCELADA"]
TIPO_EVENTO = ["GOL", "CARTAO_AMARELO", "CARTAO_VERMELHO", "SUBSTITUICAO"]


class AbaPartidas(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)

        # ---------- Parte superior: partidas ----------
        top = ttk.LabelFrame(self, text="Partidas")
        top.pack(fill="both", expand=True, pady=(0, 6))

        barra = ttk.Frame(top)
        barra.pack(fill="x", pady=(6, 4), padx=6)
        ttk.Button(barra, text="➕ Nova partida", command=self._nova_partida).pack(side="left")
        ttk.Button(barra, text="🔄 Atualizar", command=self._atualizar).pack(side="left", padx=4)
        ttk.Button(barra, text="✏️ Alterar status", command=self._alterar_status).pack(side="left", padx=4)
        ttk.Button(barra, text="🗑️ Excluir partida", command=self._excluir_partida).pack(side="left", padx=4)

        self.tab_partidas = Tabela(
            top,
            colunas=[("id_partida", "ID", 50),
                     ("data_hora", "Data/Hora", 140),
                     ("status", "Status", 120),
                     ("temporada", "Temporada", 160),
                     ("mandante", "Mandante", 150),
                     ("visitante", "Visitante", 150),
                     ("gols_mandante", "GM", 40),
                     ("gols_visitante", "GV", 40),
                     ("estadio", "Estádio", 150)],
        )
        self.tab_partidas.pack(fill="both", expand=True, padx=6, pady=(0, 6))
        self.tab_partidas.tree.bind("<<TreeviewSelect>>", lambda _e: self._carregar_eventos())

        # ---------- Parte inferior: eventos da partida selecionada ----------
        bottom = ttk.LabelFrame(self, text="Eventos da partida selecionada")
        bottom.pack(fill="both", expand=True)

        barra_ev = ttk.Frame(bottom)
        barra_ev.pack(fill="x", pady=(6, 4), padx=6)
        ttk.Button(barra_ev, text="➕ Novo evento", command=self._novo_evento).pack(side="left")
        ttk.Button(barra_ev, text="🗑️ Remover evento", command=self._remover_evento).pack(side="left", padx=4)
        ttk.Button(barra_ev, text="🔄 Atualizar eventos", command=self._carregar_eventos).pack(side="left", padx=4)

        self.tab_eventos = Tabela(
            bottom,
            colunas=[("id_evento", "ID", 50),
                     ("minuto", "Min", 50),
                     ("tipo", "Tipo", 140),
                     ("atleta", "Atleta", 200),
                     ("atleta2", "Subst. por", 200),
                     ("descricao", "Descrição", 240)],
        )
        self.tab_eventos.pack(fill="both", expand=True, padx=6, pady=(0, 6))

        self.after(50, self._atualizar)

    # ---------------- Partidas ----------------
    def _atualizar(self):
        try:
            partidas = rep.listar_partidas()
        except Exception as e:
            avisar("Erro ao carregar partidas", f"{e}")
            partidas = []
        self.tab_partidas.preencher(partidas)

    def _partida_selecionada(self) -> dict | None:
        return self.tab_partidas.linha_selecionada()

    def _nova_partida(self):
        temps = [f'{t["id_temporada"]} - {t["nome"]} ({t["ano"]})'
                 for t in rep.listar_temporadas()]
        equips = [f'{e["id_equipe"]} - {e["nome"]}' for e in rep.listar_equipes()]
        estadios = [f'{s["id_estadio"]} - {s["nome"]}' for s in rep.listar_estadios()]
        dados = perguntar(self, "Nova Partida", [
            {"chave": "data_hora", "rotulo": "Data/Hora (AAAA-MM-DD HH:MM):"},
            {"chave": "status", "rotulo": "Status:", "tipo": "combo",
             "opcoes": STATUS_OPCOES, "valor": "AGENDADA"},
            {"chave": "gols_mandante", "rotulo": "Gols mandante:", "tipo": "numero", "valor": "0"},
            {"chave": "gols_visitante", "rotulo": "Gols visitante:", "tipo": "numero", "valor": "0"},
            {"chave": "temporada", "rotulo": "Temporada:", "tipo": "combo", "opcoes": temps},
            {"chave": "mandante", "rotulo": "Mandante:", "tipo": "combo", "opcoes": equips},
            {"chave": "visitante", "rotulo": "Visitante:", "tipo": "combo", "opcoes": equips},
            {"chave": "estadio", "rotulo": "Estádio:", "tipo": "combo", "opcoes": estadios},
        ])
        if not dados:
            return
        try:
            rep.inserir_partida(
                dados["data_hora"], dados["status"],
                int(dados["gols_mandante"]), int(dados["gols_visitante"]),
                to_int(dados["temporada"].split(" - ")[0]),
                to_int(dados["mandante"].split(" - ")[0]),
                to_int(dados["visitante"].split(" - ")[0]),
                to_int(dados["estadio"].split(" - ")[0]),
            )
            self._atualizar()
            informar("Sucesso", "Partida cadastrada.")
        except Exception as e:
            avisar("Erro ao inserir partida", f"{e}")

    def _alterar_status(self):
        linha = self._partida_selecionada()
        if not linha:
            avisar("Selecionar", "Selecione uma partida.")
            return
        dados = perguntar(self, "Alterar status", [
            {"chave": "status", "rotulo": "Novo status:", "tipo": "combo",
             "opcoes": STATUS_OPCOES, "valor": linha["status"]},
        ])
        if not dados:
            return
        try:
            rep.atualizar_status_partida(int(linha["id_partida"]), dados["status"])
            self._atualizar()
        except Exception as e:
            avisar("Erro ao alterar status", f"{e}")

    def _excluir_partida(self):
        linha = self._partida_selecionada()
        if not linha:
            avisar("Selecionar", "Selecione uma partida.")
            return
        if not confirmar("Confirmar", "Excluir a partida e todos os seus eventos?"):
            return
        try:
            rep.remover_partida(int(linha["id_partida"]))
            self._atualizar()
        except Exception as e:
            avisar("Erro ao excluir", f"{e}")

    # ---------------- Eventos ----------------
    def _carregar_eventos(self):
        linha = self._partida_selecionada()
        if not linha:
            self.tab_eventos.preencher([])
            return
        try:
            evs = rep.listar_eventos(int(linha["id_partida"]))
        except Exception as e:
            avisar("Erro ao carregar eventos", f"{e}")
            evs = []
        self.tab_eventos.preencher(evs)

    def _novo_evento(self):
        linha = self._partida_selecionada()
        if not linha:
            avisar("Selecionar", "Selecione uma partida.")
            return
        atletas = [f'{a["id_pessoa"]} - {a["nome"]}'
                   for a in rep.listar_pessoas("ATLETA")]
        # Pré-formata lista com "(nenhum)" para segundo atleta
        atletas2 = ["(nenhum)"] + atletas
        dados = perguntar(self, "Novo Evento", [
            {"chave": "tipo", "rotulo": "Tipo:", "tipo": "combo",
             "opcoes": TIPO_EVENTO, "valor": "GOL"},
            {"chave": "minuto", "rotulo": "Minuto (0-130):", "tipo": "numero"},
            {"chave": "atleta", "rotulo": "Atleta:", "tipo": "combo", "opcoes": atletas},
            {"chave": "atleta2", "rotulo": "Subst. entra (se SUBSTITUICAO):",
             "tipo": "combo", "opcoes": atletas2},
            {"chave": "descricao", "rotulo": "Descrição:"},
        ])
        if not dados:
            return
        # Se tipo != SUBSTITUICAO, ignora atleta2
        id_atleta2 = None
        if dados["tipo"] == "SUBSTITUICAO" and not dados["atleta2"].startswith("("):
            id_atleta2 = to_int(dados["atleta2"].split(" - ")[0])
        try:
            rep.inserir_evento(
                dados["tipo"], int(dados["minuto"]),
                int(linha["id_partida"]),
                to_int(dados["atleta"].split(" - ")[0]),
                id_atleta2,
                to_optional_str(dados.get("descricao")),
            )
            self._carregar_eventos()
            self._atualizar()  # placar pode ter mudado via trigger
            informar("Sucesso", "Evento registrado.")
        except Exception as e:
            avisar("Erro ao inserir evento", f"{e}")

    def _remover_evento(self):
        ev = self.tab_eventos.linha_selecionada()
        if not ev:
            avisar("Selecionar", "Selecione um evento.")
            return
        if not confirmar("Confirmar", "Remover o evento selecionado?"):
            return
        try:
            rep.remover_evento(int(ev["id_evento"]))
            self._carregar_eventos()
            self._atualizar()
        except Exception as e:
            avisar("Erro ao remover", f"{e}")
