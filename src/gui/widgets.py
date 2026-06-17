"""
Widgets reutilizáveis da GUI — SportsLeagueDB.

Componentes usados pelas abas:
  - Tabela:   Treeview com colunas configuráveis, ordenação e barra de rolagem.
  - Formulario: janela modal (Toplevel) que monta campos a partir de uma definição
                e devolve um dicionário com os valores digitados.
  - ComboBoxSearch: Combobox com auto-preenchimento de opções.
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any, Callable


# ---------------------------------------------------------------------------
# Estilo visual centralizado
# ---------------------------------------------------------------------------
def aplicar_estilo(root: tk.Tk) -> None:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass
    style.configure("Treeview", rowheight=24, font=("Segoe UI", 10))
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("TButton", font=("Segoe UI", 10), padding=4)
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TLabelframe.Label", font=("Segoe UI", 10, "bold"))
    style.configure("TCombobox", font=("Segoe UI", 10))


# ---------------------------------------------------------------------------
# Tabela (Treeview) com colunas, cabeçalho clicável e ordenação
# ---------------------------------------------------------------------------
class Tabela(ttk.Frame):
    """Treeview empacotado com scrollbar e suporte a duplo-clique em linha."""

    def __init__(
        self,
        master,
        colunas: list[tuple[str, str, int]],  # (chave, título, largura)
        on_duplo_clique: Callable[[dict], None] | None = None,
    ):
        super().__init__(master)
        self._col_keys = [c[0] for c in colunas]
        self._on_duplo = on_duplo_clique

        self.tree = ttk.Treeview(
            self, columns=self._col_keys, show="headings", selectmode="browse"
        )
        for chave, titulo, largura in colunas:
            self.tree.heading(chave, text=titulo,
                              command=lambda c=chave: self._ordenar(c))
            self.tree.column(chave, width=largura, minwidth=40, stretch=True)

        scroll_y = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scroll_x = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set,
                            xscrollcommand=scroll_x.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        if on_duplo_clique:
            self.tree.bind("<Double-Button-1>", self._handle_duplo)

        self._sort_reverse: dict[str, bool] = {}

    def _ordenar(self, coluna: str) -> None:
        dados = self._dados_atuais()
        reverse = self._sort_reverse.get(coluna, False)
        try:
            dados.sort(key=lambda r: (r.get(coluna) is None, r.get(coluna)),
                       reverse=reverse)
        except TypeError:
            dados.sort(key=lambda r: str(r.get(coluna)), reverse=reverse)
        self._sort_reverse[coluna] = not reverse
        self.preencher(dados)

    def _dados_atuais(self) -> list[dict]:
        dados = []
        for iid in self.tree.get_children(""):
            valores = self.tree.item(iid, "values")
            dados.append(dict(zip(self._col_keys, valores)))
        return dados

    def preencher(self, linhas: list[dict]) -> None:
        self.tree.delete(*self.tree.get_children(""))
        for i, linha in enumerate(linhas):
            valores = [linha.get(c, "") for c in self._col_keys]
            iid = self.tree.insert("", "end", iid=str(i), values=valores)

    def linha_selecionada(self) -> dict | None:
        sel = self.tree.selection()
        if not sel:
            return None
        valores = self.tree.item(sel[0], "values")
        return dict(zip(self._col_keys, valores))

    def _handle_duplo(self, _event):
        if self._on_duplo and self.linha_selecionada():
            self._on_duplo(self.linha_selecionada())


# ---------------------------------------------------------------------------
# Diálogo de formulário genérico
# ---------------------------------------------------------------------------
class Formulario(tk.Toplevel):
    """
    Janela modal que monta campos a partir de uma especificação.

    campos: lista de dicts:
        { "chave": str, "rotulo": str, "tipo": "texto"|"numero"|"data"|"combo",
          "opcoes": [...] (se combo), "obrigatorio": bool, "valor": inicial }
    """

    def __init__(self, master, titulo: str, campos: list[dict]):
        super().__init__(master)
        self.title(titulo)
        self.grab_set()
        self.transient(master)
        self.resizable(True, True)

        self._entradas: dict[str, tk.Widget] = {}
        self.resultado: dict[str, Any] | None = None
        self._valores_iniciais = {c["chave"]: c.get("valor", "") for c in campos}

        cont = ttk.Frame(self, padding=12)
        cont.pack(fill="both", expand=True)

        for i, campo in enumerate(campos):
            ttk.Label(cont, text=campo["rotulo"]).grid(
                row=i, column=0, sticky="e", padx=(0, 8), pady=3
            )
            tipo = campo.get("tipo", "texto")
            if tipo == "combo":
                widget = ttk.Combobox(cont, values=campo.get("opcoes", []),
                                      state="readonly", width=32)
            else:
                widget = ttk.Entry(cont, width=34)
                if tipo == "numero":
                    widget.config(validate="key")
                    widget.config(
                        validatecommand=(self.register(self._valida_numero), "%P")
                    )
            widget.grid(row=i, column=1, pady=3, sticky="ew")
            if campo.get("valor") is not None:
                widget.insert(0, str(campo["valor"]))
            self._entradas[campo["chave"]] = widget

        cont.columnconfigure(1, weight=1)

        barra = ttk.Frame(cont)
        barra.grid(row=len(campos), column=0, columnspan=2, pady=(12, 0))
        ttk.Button(barra, text="Cancelar", command=self._cancelar).pack(side="right")
        ttk.Button(barra, text="Salvar", command=self._salvar).pack(side="right",
                                                                    padx=4)
        self.bind("<Return>", lambda _e: self._salvar())
        self.bind("<Escape>", lambda _e: self._cancelar())

        # Centraliza
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"+{(sw - w)//2}+{(sh - h)//2}")

    @staticmethod
    def _valida_numero(valor: str) -> bool:
        if valor == "" or valor == "-":
            return True
        try:
            float(valor)
            return True
        except ValueError:
            return False

    def _salvar(self) -> None:
        resultado: dict[str, Any] = {}
        for chave, widget in self._entradas.items():
            if isinstance(widget, ttk.Combobox):
                resultado[chave] = widget.get()
            else:
                resultado[chave] = widget.get().strip()
        self.resultado = resultado
        self.destroy()

    def _cancelar(self) -> None:
        self.resultado = None
        self.destroy()


def perguntar(master, titulo: str, campos: list[dict]) -> dict | None:
    """Abre Formulario e devolve o dict preenchido (ou None se cancelado)."""
    form = Formulario(master, titulo, campos)
    master.wait_window(form)
    return form.resultado


def confirmar(titulo: str, mensagem: str) -> bool:
    return messagebox.askyesno(titulo, mensagem)


def avisar(titulo: str, mensagem: str) -> None:
    messagebox.showwarning(titulo, mensagem)


def informar(titulo: str, mensagem: str) -> None:
    messagebox.showinfo(titulo, mensagem)
