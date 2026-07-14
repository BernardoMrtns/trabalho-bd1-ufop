from __future__ import annotations

import tkinter as tk
from tkinter import ttk

import repositories as rep
from .util import to_int
from .widgets import Tabela, avisar


class AbaConsultas(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=8)

        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True)

        self._resumo = self._aba_resumo()
        self._classificacao = self._aba_classificacao()
        self._artilharia = self._aba_artilharia()
        self._cartoes = self._aba_cartoes()
        self._confrontos = self._aba_confrontos()
        self._elenco = self._aba_elenco()

    def _seletor_temporada(self, parent):
        frame = ttk.Frame(parent)
        ttk.Label(frame, text="Temporada:").pack(side="left")
        cb = ttk.Combobox(frame, state="readonly", width=40)
        cb.pack(side="left", padx=4)
        try:
            temps = rep.listar_temporadas()
            cb["values"] = [f'{t["id_temporada"]} - {t["nome"]} ({t["ano"]})'
                            for t in temps]
        except Exception:
            cb["values"] = []
        return frame, cb

    @staticmethod
    def _id_temp(cb_value):
        if not cb_value:
            return None
        return to_int(cb_value.split(" - ")[0])

    def _aba_resumo(self):
        f = ttk.Frame(self.nb, padding=6)
        self.nb.add(f, text="📊 Resumo")
        ttk.Label(f, text="Visão geral de todas as temporadas",
                  font=("Segoe UI", 10, "italic")).pack(anchor="w")
        ttk.Button(f, text="Atualizar", command=lambda: self._gerar_resumo()).pack(anchor="w", pady=4)
        self.t_resumo = Tabela(
            f,
            colunas=[("temporada", "Temporada", 180),
                     ("ano", "Ano", 60),
                     ("modalidade", "Modalidade", 120),
                     ("n_equipes", "Equipes", 70),
                     ("n_partidas", "Partidas", 70),
                     ("n_encerradas", "Encerradas", 90),
                     ("total_gols", "Gols", 60)],
        )
        self.t_resumo.pack(fill="both", expand=True, pady=4)
        self.after(80, self._gerar_resumo)
        return f

    def _gerar_resumo(self):
        try:
            self.t_resumo.preencher(rep.resumo_temporadas())
        except Exception as e:
            avisar("Erro", f"{e}")

    def _aba_classificacao(self):
        f = ttk.Frame(self.nb, padding=6)
        self.nb.add(f, text="🏆 Classificação")
        sel, self.cb_class = self._seletor_temporada(f)
        sel.pack(anchor="w")
        ttk.Button(f, text="Gerar", command=self._gerar_classificacao).pack(anchor="w", pady=4)
        self.t_class = Tabela(
            f,
            colunas=[("posicao", "#", 40),
                     ("equipe", "Equipe", 200),
                     ("sigla", "Sigla", 60),
                     ("jogos", "J", 40),
                     ("vitorias", "V", 40),
                     ("empates", "E", 40),
                     ("derrotas", "D", 40),
                     ("gols_pro", "GP", 40),
                     ("gols_contra", "GC", 40),
                     ("saldo_gols", "SG", 50),
                     ("pontos", "Pts", 50)],
        )
        self.t_class.pack(fill="both", expand=True, pady=4)
        return f

    def _gerar_classificacao(self):
        id_t = self._id_temp(self.cb_class.get())
        if id_t is None:
            avisar("Selecionar", "Escolha uma temporada.")
            return
        try:
            self.t_class.preencher(rep.classificacao(id_t))
        except Exception as e:
            avisar("Erro", f"{e}")

    def _aba_artilharia(self):
        f = ttk.Frame(self.nb, padding=6)
        self.nb.add(f, text="⚽ Artilharia")
        sel, self.cb_art = self._seletor_temporada(f)
        sel.pack(anchor="w")
        ttk.Button(f, text="Gerar", command=self._gerar_artilharia).pack(anchor="w", pady=4)
        self.t_art = Tabela(
            f,
            colunas=[("atleta", "Atleta", 250),
                     ("equipe", "Equipe", 180),
                     ("sigla", "Sigla", 60),
                     ("gols", "Gols", 60)],
        )
        self.t_art.pack(fill="both", expand=True, pady=4)
        return f

    def _gerar_artilharia(self):
        id_t = self._id_temp(self.cb_art.get())
        if id_t is None:
            avisar("Selecionar", "Escolha uma temporada.")
            return
        try:
            self.t_art.preencher(rep.artilharia(id_t))
        except Exception as e:
            avisar("Erro", f"{e}")

    def _aba_cartoes(self):
        f = ttk.Frame(self.nb, padding=6)
        self.nb.add(f, text="🟨🟥 Cartões")
        sel, self.cb_cart = self._seletor_temporada(f)
        sel.pack(anchor="w")
        ttk.Button(f, text="Gerar", command=self._gerar_cartoes).pack(anchor="w", pady=4)
        self.t_cart = Tabela(
            f,
            colunas=[("atleta", "Atleta", 250),
                     ("equipe", "Equipe", 180),
                     ("amarelos", "Amarelos", 80),
                     ("vermelhos", "Vermelhos", 90)],
        )
        self.t_cart.pack(fill="both", expand=True, pady=4)
        return f

    def _gerar_cartoes(self):
        id_t = self._id_temp(self.cb_cart.get())
        if id_t is None:
            avisar("Selecionar", "Escolha uma temporada.")
            return
        try:
            self.t_cart.preencher(rep.cartoes(id_t))
        except Exception as e:
            avisar("Erro", f"{e}")

    def _aba_confrontos(self):
        f = ttk.Frame(self.nb, padding=6)
        self.nb.add(f, text="⚔️ Confrontos")

        sel = ttk.Frame(f)
        sel.pack(anchor="w", fill="x")
        ttk.Label(sel, text="Equipe A:").pack(side="left")
        self.cb_conf_a = ttk.Combobox(sel, state="readonly", width=30)
        self.cb_conf_a.pack(side="left", padx=4)
        ttk.Label(sel, text="Equipe B:").pack(side="left")
        self.cb_conf_b = ttk.Combobox(sel, state="readonly", width=30)
        self.cb_conf_b.pack(side="left", padx=4)
        ttk.Button(f, text="Gerar", command=self._gerar_confrontos).pack(anchor="w", pady=4)

        try:
            equips = rep.listar_equipes()
            valores = [f'{e["id_equipe"]} - {e["nome"]}' for e in equips]
            self.cb_conf_a["values"] = valores
            self.cb_conf_b["values"] = valores
        except Exception:
            pass

        self.t_conf = Tabela(
            f,
            colunas=[("temporada", "Temporada", 160),
                     ("data_hora", "Data", 140),
                     ("mandante", "Mandante", 150),
                     ("visitante", "Visitante", 150),
                     ("gols_mandante", "GM", 40),
                     ("gols_visitante", "GV", 40),
                     ("resultado", "Vencedor", 140)],
        )
        self.t_conf.pack(fill="both", expand=True, pady=4)
        return f

    def _gerar_confrontos(self):
        a = to_int(self.cb_conf_a.get().split(" - ")[0]) if self.cb_conf_a.get() else None
        b = to_int(self.cb_conf_b.get().split(" - ")[0]) if self.cb_conf_b.get() else None
        if a is None or b is None:
            avisar("Selecionar", "Escolha as duas equipes.")
            return
        try:
            self.t_conf.preencher(rep.confrontos(a, b))
        except Exception as e:
            avisar("Erro", f"{e}")

    def _aba_elenco(self):
        f = ttk.Frame(self.nb, padding=6)
        self.nb.add(f, text="👥 Elenco")

        sel = ttk.Frame(f)
        sel.pack(anchor="w", fill="x")
        ttk.Label(sel, text="Temporada:").pack(side="left")
        self.cb_elo_t = ttk.Combobox(sel, state="readonly", width=35)
        self.cb_elo_t.pack(side="left", padx=4)
        ttk.Label(sel, text="Equipe:").pack(side="left")
        self.cb_elo_e = ttk.Combobox(sel, state="readonly", width=30)
        self.cb_elo_e.pack(side="left", padx=4)
        ttk.Button(f, text="Gerar", command=self._gerar_elenco).pack(anchor="w", pady=4)

        try:
            temps = rep.listar_temporadas()
            equips = rep.listar_equipes()
            self.cb_elo_t["values"] = [f'{t["id_temporada"]} - {t["nome"]} ({t["ano"]})'
                                       for t in temps]
            self.cb_elo_e["values"] = [f'{e["id_equipe"]} - {e["nome"]}' for e in equips]
        except Exception:
            pass

        self.t_elo = Tabela(
            f,
            colunas=[("num_camisa", "Nº", 50),
                     ("atleta", "Atleta", 250),
                     ("altura", "Altura", 80),
                     ("peso", "Peso", 70)],
        )
        self.t_elo.pack(fill="both", expand=True, pady=4)
        return f

    def _gerar_elenco(self):
        id_t = to_int(self.cb_elo_t.get().split(" - ")[0]) if self.cb_elo_t.get() else None
        id_e = to_int(self.cb_elo_e.get().split(" - ")[0]) if self.cb_elo_e.get() else None
        if id_t is None or id_e is None:
            avisar("Selecionar", "Escolha temporada e equipe.")
            return
        try:
            self.t_elo.preencher(rep.elenco(id_t, id_e))
        except Exception as e:
            avisar("Erro", f"{e}")
