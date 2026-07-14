from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

import db
from config import DBConfig
from .widgets import aplicar_estilo, informar, avisar
from .abas_cadastros import (
    AbaModalidade, AbaPosicao, AbaEstadio, AbaEquipe,
)
from .abas_operacionais import (
    AbaTemporada, AbaAtletas, AbaArbitros, AbaTecnicos,
    AbaInscricao, AbaContrato,
)
from .aba_partidas import AbaPartidas
from .aba_consultas import AbaConsultas


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SportsLeagueDB — Sistema de Gestão de Liga Esportiva")
        self.geometry("1100x720")
        self.minsize(900, 600)

        aplicar_estilo(self)

        self.barra_status = ttk.Frame(self, relief="sunken", padding=(6, 2))
        self.barra_status.pack(side="bottom", fill="x")
        self.lbl_status = ttk.Label(self.barra_status, text="Conectando...")
        self.lbl_status.pack(side="left")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=6, pady=6)

        self._montar_abas()
        self._montar_menu()

        self.after(100, self._verificar_conexao)

    def _montar_abas(self):
        self.aba_cadastros = self._grupo("📋 Cadastros", [
            ("Modalidades", AbaModalidade),
            ("Posições", AbaPosicao),
            ("Estádios", AbaEstadio),
            ("Equipes", AbaEquipe),
        ])
        self.aba_pessoas = self._grupo("👥 Pessoas", [
            ("Atletas", AbaAtletas),
            ("Árbitros", AbaArbitros),
            ("Técnicos", AbaTecnicos),
        ])
        self.aba_operacoes = self._grupo("🗓️ Operações", [
            ("Temporadas", AbaTemporada),
            ("Inscrições", AbaInscricao),
            ("Contratos", AbaContrato),
        ])
        self.aba_partidas = AbaPartidas(self.notebook)
        self.notebook.add(self.aba_partidas, text="⚽ Partidas")
        self.aba_consultas = AbaConsultas(self.notebook)
        self.notebook.add(self.aba_consultas, text="📈 Consultas")

    def _grupo(self, titulo: str, itens: list[tuple[str, type]]) -> ttk.Notebook:
        externa = ttk.Frame(self.notebook)
        self.notebook.add(externa, text=titulo)
        interna = ttk.Notebook(externa)
        interna.pack(fill="both", expand=True, padx=4, pady=4)
        for nome, classe in itens:
            aba = classe(interna)
            interna.add(aba, text=nome)
        return interna

    def _montar_menu(self):
        menubar = tk.Menu(self)

        m_banco = tk.Menu(menubar, tearoff=0)
        m_banco.add_command(label="Testar conexão", command=self._testar_conexao)
        m_banco.add_command(label="(Re)criar banco e popular com dados de exemplo",
                            command=self._bootstrap)
        m_banco.add_separator()
        m_banco.add_command(label="Sair", command=self.quit)
        menubar.add_cascade(label="Banco", menu=m_banco)

        m_ajuda = tk.Menu(menubar, tearoff=0)
        m_ajuda.add_command(label="Sobre", command=self._sobre)
        menubar.add_cascade(label="Ajuda", menu=m_ajuda)

        self.config(menu=menubar)

    def _verificar_conexao(self):
        ok = db.test_connection()
        if ok:
            self.lbl_status.config(
                text=f"✅ Conectado a {DBConfig.HOST}:{DBConfig.PORT}/"
                     f"{DBConfig.DATABASE}  (usuário: {DBConfig.USER})"
            )
        else:
            self.lbl_status.config(text="❌ Sem conexão — use o menu Banco > "
                                        "(Re)criar banco... após instalar/configurar o PostgreSQL.")
            messagebox.showwarning(
                "Sem conexão com o PostgreSQL",
                f"Não foi possível conectar a {DBConfig.HOST}:{DBConfig.PORT}/"
                f"{DBConfig.DATABASE}\n\n"
                "Verifique se:\n"
                "  1. O PostgreSQL está instalado e em execução;\n"
                "  2. As credenciais em .env (ou variáveis de ambiente) estão corretas;\n"
                "  3. O usuário tem permissão para criar banco de dados.\n\n"
                "Use o menu Banco > (Re)criar banco... depois de corrigir."
            )

    def _testar_conexao(self):
        ok = db.test_connection()
        if ok:
            informar("Conexão", "Conexão com o PostgreSQL bem-sucedida!")
        else:
            avisar("Conexão", "Falha na conexão. Veja a barra de status.")

    def _bootstrap(self):
        if not messagebox.askyesno(
            "Confirmar",
            "Isto irá APAGAR e recriar o banco de dados, executando todos os\n"
            "scripts SQL (schema, triggers, views e dados de exemplo).\n\nContinuar?"
        ):
            return
        try:
            log = db.bootstrap()
            informar("Bootstrap concluído", "\n".join(log))
            self._verificar_conexao()
            for aba in self._todas_abas():
                if hasattr(aba, "crud"):
                    aba.crud.atualizar()
                elif hasattr(aba, "_atualizar"):
                    aba._atualizar()
        except Exception as e:
            avisar("Erro no bootstrap", f"{e}")

    def _todas_abas(self):
        abas = []
        def percorrer(nb):
            for tab_id in nb.tabs():
                widget = nb.nametowidget(tab_id)
                if isinstance(widget, ttk.Notebook):
                    percorrer(widget)
                else:
                    abas.append(widget)
        percorrer(self.notebook)
        return abas

    def _sobre(self):
        informar(
            "Sobre",
            "SportsLeagueDB\n"
            "Sistema de Gestão de Liga Esportiva\n\n"
            "Projeto Prático — CSI440 / CSI602 (Banco de Dados)\n"
            "Tecnologias: PostgreSQL + Python + tkinter\n"
            "Acesso via SQL puro (sem ORM)."
        )


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
