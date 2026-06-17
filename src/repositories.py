"""
Repositórios — SportsLeagueDB.

Camada fina entre a GUI e o db.py. Cada função encapsula uma consulta SQL
específica (escrita à mão, sem ORM). Os parâmetros são sempre passados de
forma parametrizada (placeholder %s) para evitar injeção de SQL.
"""
from __future__ import annotations

from typing import Any

import db

# =============================================================================
#  Modalidade
# =============================================================================
def listar_modalidades() -> list[dict]:
    return db.fetch_all(
        "SELECT id_modalidade, nome, n_jogadores_por_time "
        "FROM modalidade ORDER BY nome"
    )


def inserir_modalidade(nome: str, n_jogadores: int) -> dict:
    return db.execute_returning(
        "INSERT INTO modalidade (nome, n_jogadores_por_time) "
        "VALUES (%s, %s) RETURNING id_modalidade, nome, n_jogadores_por_time",
        (nome, n_jogadores),
    )


def atualizar_modalidade(id_modalidade: int, nome: str, n_jogadores: int) -> int:
    return db.execute(
        "UPDATE modalidade SET nome=%s, n_jogadores_por_time=%s "
        "WHERE id_modalidade=%s",
        (nome, n_jogadores, id_modalidade),
    )


def remover_modalidade(id_modalidade: int) -> int:
    return db.execute("DELETE FROM modalidade WHERE id_modalidade=%s", (id_modalidade,))


# =============================================================================
#  Posição
# =============================================================================
def listar_posicoes() -> list[dict]:
    return db.fetch_all(
        "SELECT p.id_posicao, p.nome, m.nome AS modalidade "
        "FROM posicao p JOIN modalidade m ON m.id_modalidade = p.id_modalidade "
        "ORDER BY m.nome, p.nome"
    )


def inserir_posicao(nome: str, id_modalidade: int) -> dict:
    return db.execute_returning(
        "INSERT INTO posicao (nome, id_modalidade) VALUES (%s, %s) "
        "RETURNING id_posicao",
        (nome, id_modalidade),
    )


def remover_posicao(id_posicao: int) -> int:
    return db.execute("DELETE FROM posicao WHERE id_posicao=%s", (id_posicao,))


# =============================================================================
#  Estadio
# =============================================================================
def listar_estadios() -> list[dict]:
    return db.fetch_all(
        "SELECT id_estadio, nome, cidade, capacidade "
        "FROM estadio ORDER BY nome"
    )


def inserir_estadio(nome: str, cidade: str, capacidade: int) -> dict:
    return db.execute_returning(
        "INSERT INTO estadio (nome, cidade, capacidade) "
        "VALUES (%s, %s, %s) RETURNING id_estadio",
        (nome, cidade, capacidade),
    )


def atualizar_estadio(id_estadio: int, nome: str, cidade: str, capacidade: int) -> int:
    return db.execute(
        "UPDATE estadio SET nome=%s, cidade=%s, capacidade=%s WHERE id_estadio=%s",
        (nome, cidade, capacidade, id_estadio),
    )


def remover_estadio(id_estadio: int) -> int:
    return db.execute("DELETE FROM estadio WHERE id_estadio=%s", (id_estadio,))


# =============================================================================
#  Equipe
# =============================================================================
def listar_equipes() -> list[dict]:
    return db.fetch_all(
        "SELECT e.id_equipe, e.nome, e.sigla, e.cidade, "
        "       es.nome AS estadio_sede "
        "FROM equipe e LEFT JOIN estadio es ON es.id_estadio = e.id_estadio_sede "
        "ORDER BY e.nome"
    )


def inserir_equipe(nome: str, sigla: str, cidade: str, id_estadio_sede: int | None) -> dict:
    return db.execute_returning(
        "INSERT INTO equipe (nome, sigla, cidade, id_estadio_sede) "
        "VALUES (%s, %s, %s, %s) RETURNING id_equipe",
        (nome, sigla.upper(), cidade, id_estadio_sede),
    )


def atualizar_equipe(
    id_equipe: int, nome: str, sigla: str, cidade: str, id_estadio_sede: int | None
) -> int:
    return db.execute(
        "UPDATE equipe SET nome=%s, sigla=%s, cidade=%s, id_estadio_sede=%s "
        "WHERE id_equipe=%s",
        (nome, sigla.upper(), cidade, id_estadio_sede, id_equipe),
    )


def remover_equipe(id_equipe: int) -> int:
    return db.execute("DELETE FROM equipe WHERE id_equipe=%s", (id_equipe,))


# =============================================================================
#  Temporada
# =============================================================================
def listar_temporadas() -> list[dict]:
    return db.fetch_all(
        "SELECT t.id_temporada, t.nome, t.ano, t.data_inicio, t.data_fim, "
        "       m.nome AS modalidade "
        "FROM temporada t JOIN modalidade m ON m.id_modalidade = t.id_modalidade "
        "ORDER BY t.ano DESC, t.nome"
    )


def inserir_temporada(
    nome: str, ano: int, data_inicio: str, data_fim: str, id_modalidade: int
) -> dict:
    return db.execute_returning(
        "INSERT INTO temporada (nome, ano, data_inicio, data_fim, id_modalidade) "
        "VALUES (%s, %s, %s, %s, %s) RETURNING id_temporada",
        (nome, ano, data_inicio, data_fim, id_modalidade),
    )


def atualizar_temporada(
    id_temporada: int, nome: str, ano: int, data_inicio: str, data_fim: str,
    id_modalidade: int,
) -> int:
    return db.execute(
        "UPDATE temporada SET nome=%s, ano=%s, data_inicio=%s, data_fim=%s, "
        "id_modalidade=%s WHERE id_temporada=%s",
        (nome, ano, data_inicio, data_fim, id_modalidade, id_temporada),
    )


def remover_temporada(id_temporada: int) -> int:
    return db.execute("DELETE FROM temporada WHERE id_temporada=%s", (id_temporada,))


# =============================================================================
#  Pessoas (Atleta / Árbitro / Técnico) — generalização
# =============================================================================
def listar_pessoas(tipo: str | None = None) -> list[dict]:
    if tipo:
        return db.fetch_all(
            "SELECT id_pessoa, nome, cpf, data_nasc, nacionalidade, tipo "
            "FROM pessoa WHERE tipo = %s ORDER BY nome",
            (tipo,),
        )
    return db.fetch_all(
        "SELECT id_pessoa, nome, cpf, data_nasc, nacionalidade, tipo "
        "FROM pessoa ORDER BY nome"
    )


def inserir_atleta(
    nome: str, cpf: str, data_nasc: str, nacionalidade: str,
    altura: float, peso: float, num_camisa: int | None,
) -> dict:
    """Insere em pessoa + atleta numa transação."""
    with db.get_connection() as conn:
        try:
            with conn.cursor(cursor_factory=__real_dict()) as cur:
                cur.execute(
                    "INSERT INTO pessoa (nome, cpf, data_nasc, nacionalidade, tipo) "
                    "VALUES (%s, %s, %s, %s, 'ATLETA') "
                    "RETURNING id_pessoa",
                    (nome, cpf, data_nasc, nacionalidade),
                )
                id_pessoa = cur.fetchone()["id_pessoa"]
                cur.execute(
                    "INSERT INTO atleta (id_pessoa, altura, peso, num_camisa) "
                    "VALUES (%s, %s, %s, %s)",
                    (id_pessoa, altura, peso, num_camisa),
                )
            conn.commit()
            return {"id_pessoa": id_pessoa}
        except Exception:
            conn.rollback()
            raise


def inserir_arbitro(
    nome: str, cpf: str, data_nasc: str, nacionalidade: str, categoria: str
) -> dict:
    with db.get_connection() as conn:
        try:
            with conn.cursor(cursor_factory=__real_dict()) as cur:
                cur.execute(
                    "INSERT INTO pessoa (nome, cpf, data_nasc, nacionalidade, tipo) "
                    "VALUES (%s, %s, %s, %s, 'ARBITRO') "
                    "RETURNING id_pessoa",
                    (nome, cpf, data_nasc, nacionalidade),
                )
                id_pessoa = cur.fetchone()["id_pessoa"]
                cur.execute(
                    "INSERT INTO arbitro (id_pessoa, categoria) VALUES (%s, %s)",
                    (id_pessoa, categoria),
                )
            conn.commit()
            return {"id_pessoa": id_pessoa}
        except Exception:
            conn.rollback()
            raise


def inserir_tecnico(
    nome: str, cpf: str, data_nasc: str, nacionalidade: str, registro: str
) -> dict:
    with db.get_connection() as conn:
        try:
            with conn.cursor(cursor_factory=__real_dict()) as cur:
                cur.execute(
                    "INSERT INTO pessoa (nome, cpf, data_nasc, nacionalidade, tipo) "
                    "VALUES (%s, %s, %s, %s, 'TECNICO') "
                    "RETURNING id_pessoa",
                    (nome, cpf, data_nasc, nacionalidade),
                )
                id_pessoa = cur.fetchone()["id_pessoa"]
                cur.execute(
                    "INSERT INTO tecnico (id_pessoa, registro_federacao) "
                    "VALUES (%s, %s)",
                    (id_pessoa, registro),
                )
            conn.commit()
            return {"id_pessoa": id_pessoa}
        except Exception:
            conn.rollback()
            raise


def remover_pessoa(id_pessoa: int) -> int:
    # ON DELETE CASCADE remove a especialização automaticamente.
    return db.execute("DELETE FROM pessoa WHERE id_pessoa=%s", (id_pessoa,))


# atalho para não repetir o import dentro das funções
def __real_dict():
    from psycopg2.extras import RealDictCursor
    return RealDictCursor


# =============================================================================
#  Contrato
# =============================================================================
def listar_contratos() -> list[dict]:
    return db.fetch_all(
        "SELECT c.id_contrato, pes.nome AS atleta, eq.nome AS equipe, "
        "       t.nome AS temporada, c.salario, c.data_inicio, c.data_fim "
        "FROM contrato c "
        "JOIN atleta   a   ON a.id_pessoa   = c.id_atleta "
        "JOIN pessoa   pes ON pes.id_pessoa = c.id_atleta "
        "JOIN equipe   eq  ON eq.id_equipe  = c.id_equipe "
        "JOIN temporada t  ON t.id_temporada= c.id_temporada "
        "ORDER BY t.ano DESC, eq.nome, pes.nome"
    )


def inserir_contrato(
    id_atleta: int, id_equipe: int, id_temporada: int,
    salario: float, data_inicio: str, data_fim: str | None,
) -> dict:
    return db.execute_returning(
        "INSERT INTO contrato (id_atleta, id_equipe, id_temporada, salario, "
        "                      data_inicio, data_fim) "
        "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_contrato",
        (id_atleta, id_equipe, id_temporada, salario, data_inicio, data_fim),
    )


def remover_contrato(id_contrato: int) -> int:
    return db.execute("DELETE FROM contrato WHERE id_contrato=%s", (id_contrato,))


# =============================================================================
#  Inscrição de equipe em temporada
# =============================================================================
def listar_inscricoes() -> list[dict]:
    return db.fetch_all(
        "SELECT i.id_temporada, t.nome AS temporada, "
        "       i.id_equipe, e.nome AS equipe "
        "FROM inscricao_temporada i "
        "JOIN temporada t ON t.id_temporada = i.id_temporada "
        "JOIN equipe    e ON e.id_equipe    = i.id_equipe "
        "ORDER BY t.ano DESC, e.nome"
    )


def inserir_inscricao(id_temporada: int, id_equipe: int) -> None:
    db.execute(
        "INSERT INTO inscricao_temporada (id_temporada, id_equipe) VALUES (%s, %s)",
        (id_temporada, id_equipe),
    )


def remover_inscricao(id_temporada: int, id_equipe: int) -> int:
    return db.execute(
        "DELETE FROM inscricao_temporada WHERE id_temporada=%s AND id_equipe=%s",
        (id_temporada, id_equipe),
    )


# =============================================================================
#  Partida
# =============================================================================
def listar_partidas() -> list[dict]:
    return db.fetch_all(
        "SELECT * FROM vw_partidas_detalhadas ORDER BY data_hora DESC"
    )


def inserir_partida(
    data_hora: str, status: str, gols_mandante: int, gols_visitante: int,
    id_temporada: int, id_mandante: int, id_visitante: int, id_estadio: int,
) -> dict:
    return db.execute_returning(
        "INSERT INTO partida (data_hora, status, gols_mandante, gols_visitante, "
        "                     id_temporada, id_mandante, id_visitante, id_estadio) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_partida",
        (data_hora, status, gols_mandante, gols_visitante,
         id_temporada, id_mandante, id_visitante, id_estadio),
    )


def atualizar_status_partida(id_partida: int, status: str) -> int:
    return db.execute(
        "UPDATE partida SET status=%s WHERE id_partida=%s",
        (status, id_partida),
    )


def remover_partida(id_partida: int) -> int:
    return db.execute("DELETE FROM partida WHERE id_partida=%s", (id_partida,))


# =============================================================================
#  Evento de partida
# =============================================================================
def listar_eventos(id_partida: int | None = None) -> list[dict]:
    if id_partida is None:
        return db.fetch_all(
            "SELECT ev.id_evento, ev.tipo, ev.minuto, p.data_hora, "
            "       pa.nome AS atleta, pa2.nome AS atleta2, ev.descricao, "
            "       em.nome AS mandante, vi.nome AS visitante "
            "FROM evento ev "
            "JOIN partida pt ON pt.id_partida = ev.id_partida "
            "JOIN equipe em  ON em.id_equipe  = pt.id_mandante "
            "JOIN equipe vi  ON vi.id_equipe  = pt.id_visitante "
            "LEFT JOIN pessoa pa  ON pa.id_pessoa  = ev.id_atleta "
            "LEFT JOIN pessoa pa2 ON pa2.id_pessoa = ev.id_atleta2 "
            "ORDER BY pt.data_hora DESC, ev.minuto"
        )
    return db.fetch_all(
        "SELECT ev.id_evento, ev.tipo, ev.minuto, "
        "       pa.nome AS atleta, pa2.nome AS atleta2, ev.descricao "
        "FROM evento ev "
        "LEFT JOIN pessoa pa  ON pa.id_pessoa  = ev.id_atleta "
        "LEFT JOIN pessoa pa2 ON pa2.id_pessoa = ev.id_atleta2 "
        "WHERE ev.id_partida = %s "
        "ORDER BY ev.minuto",
        (id_partida,),
    )


def inserir_evento(
    tipo: str, minuto: int, id_partida: int,
    id_atleta: int | None, id_atleta2: int | None, descricao: str | None,
) -> dict:
    return db.execute_returning(
        "INSERT INTO evento (tipo, minuto, id_partida, id_atleta, id_atleta2, descricao) "
        "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_evento",
        (tipo, minuto, id_partida, id_atleta, id_atleta2, descricao),
    )


def remover_evento(id_evento: int) -> int:
    return db.execute("DELETE FROM evento WHERE id_evento=%s", (id_evento,))


# =============================================================================
#  Consultas pré-definidas (relatórios)
# =============================================================================
def classificacao(id_temporada: int) -> list[dict]:
    return db.fetch_all(
        "SELECT posicao, equipe, sigla, jogos, vitorias, empates, derrotas, "
        "       gols_pro, gols_contra, saldo_gols, pontos "
        "FROM ( "
        "  SELECT *, ROW_NUMBER() OVER (ORDER BY pontos DESC, saldo_gols DESC, "
        "           gols_pro DESC, equipe) AS posicao "
        "  FROM vw_classificacao WHERE id_temporada = %s "
        ") x ORDER BY posicao",
        (id_temporada,),
    )


def artilharia(id_temporada: int) -> list[dict]:
    return db.fetch_all(
        "SELECT atleta, equipe, sigla, gols FROM vw_artilharia "
        "WHERE id_temporada = %s ORDER BY gols DESC, atleta",
        (id_temporada,),
    )


def cartoes(id_temporada: int) -> list[dict]:
    return db.fetch_all(
        "SELECT atleta, equipe, amarelos, vermelhos FROM vw_cartoes "
        "WHERE id_temporada = %s "
        "ORDER BY (vermelhos*2 + amarelos) DESC, atleta",
        (id_temporada,),
    )


def confrontos(id_equipe_a: int, id_equipe_b: int) -> list[dict]:
    """Histórico entre duas equipes (considera ambos os mandos)."""
    return db.fetch_all(
        "SELECT temporada, data_hora, mandante, visitante, "
        "       gols_mandante, gols_visitante, resultado "
        "FROM vw_confrontos "
        "WHERE (mandante = (SELECT nome FROM equipe WHERE id_equipe=%s) "
        "   AND visitante = (SELECT nome FROM equipe WHERE id_equipe=%s)) "
        "   OR (mandante = (SELECT nome FROM equipe WHERE id_equipe=%s) "
        "   AND visitante = (SELECT nome FROM equipe WHERE id_equipe=%s)) "
        "ORDER BY data_hora DESC",
        (id_equipe_a, id_equipe_b, id_equipe_b, id_equipe_a),
    )


def elenco(id_temporada: int, id_equipe: int) -> list[dict]:
    return db.fetch_all(
        "SELECT num_camisa, atleta, altura, peso FROM vw_elenco "
        "WHERE id_temporada = %s AND id_equipe = %s "
        "ORDER BY num_camisa NULLS LAST, atleta",
        (id_temporada, id_equipe),
    )


def resumo_temporadas() -> list[dict]:
    return db.fetch_all(
        "SELECT temporada, ano, modalidade, n_equipes, n_partidas, "
        "       n_encerradas, total_gols FROM vw_resumo_temporada "
        "ORDER BY ano DESC, temporada"
    )
