-- =====================================================================
-- SportsLeagueDB — Esquema do banco de dados (DDL)
-- Etapa 4 — Scripts SQL
-- SGBD: PostgreSQL 15+
-- =====================================================================

-- Limpeza (idempotente — cuidado em produção)
DROP TABLE IF EXISTS evento                CASCADE;
DROP TABLE IF EXISTS partida_arbitro       CASCADE;
DROP TABLE IF EXISTS contrato              CASCADE;
DROP TABLE IF EXISTS inscricao_temporada   CASCADE;
DROP TABLE IF EXISTS atleta_posicao        CASCADE;
DROP TABLE IF EXISTS partida               CASCADE;
DROP TABLE IF EXISTS atleta                CASCADE;
DROP TABLE IF EXISTS arbitro               CASCADE;
DROP TABLE IF EXISTS tecnico               CASCADE;
DROP TABLE IF EXISTS pessoa                CASCADE;
DROP TABLE IF EXISTS equipe                CASCADE;
DROP TABLE IF EXISTS temporada             CASCADE;
DROP TABLE IF EXISTS posicao               CASCADE;
DROP TABLE IF EXISTS estadio               CASCADE;
DROP TABLE IF EXISTS modalidade            CASCADE;

-- ---------------------------------------------------------------------
-- 1. MODALIDADE
-- ---------------------------------------------------------------------
CREATE TABLE modalidade (
    id_modalidade         SERIAL PRIMARY KEY,
    nome                  VARCHAR(80)  NOT NULL UNIQUE,
    n_jogadores_por_time  SMALLINT     NOT NULL CHECK (n_jogadores_por_time > 0)
);

-- ---------------------------------------------------------------------
-- 2. POSICAO
-- ---------------------------------------------------------------------
CREATE TABLE posicao (
    id_posicao   SERIAL PRIMARY KEY,
    nome         VARCHAR(60) NOT NULL,
    id_modalidade INTEGER     NOT NULL REFERENCES modalidade(id_modalidade) ON DELETE CASCADE,
    UNIQUE (nome, id_modalidade)
);

-- ---------------------------------------------------------------------
-- 3. ESTADIO
-- ---------------------------------------------------------------------
CREATE TABLE estadio (
    id_estadio   SERIAL PRIMARY KEY,
    nome         VARCHAR(120) NOT NULL,
    cidade       VARCHAR(80)  NOT NULL,
    capacidade   INTEGER      NOT NULL CHECK (capacidade > 0)
);

-- ---------------------------------------------------------------------
-- 4. EQUIPE
-- ---------------------------------------------------------------------
CREATE TABLE equipe (
    id_equipe       SERIAL PRIMARY KEY,
    nome            VARCHAR(120) NOT NULL,
    sigla           VARCHAR(5)   NOT NULL UNIQUE,
    cidade          VARCHAR(80)  NOT NULL,
    id_estadio_sede INTEGER      REFERENCES estadio(id_estadio) ON DELETE SET NULL
);

-- ---------------------------------------------------------------------
-- 5. TEMPORADA
-- ---------------------------------------------------------------------
CREATE TABLE temporada (
    id_temporada  SERIAL PRIMARY KEY,
    nome          VARCHAR(80)  NOT NULL,
    ano           SMALLINT     NOT NULL CHECK (ano BETWEEN 1900 AND 2100),
    data_inicio   DATE         NOT NULL,
    data_fim      DATE         NOT NULL,
    id_modalidade INTEGER      NOT NULL REFERENCES modalidade(id_modalidade) ON DELETE RESTRICT,
    CHECK (data_fim > data_inicio),
    UNIQUE (nome, ano)
);

-- ---------------------------------------------------------------------
-- 6. PESSOA  (superclasse da generalização)
-- ---------------------------------------------------------------------
CREATE TABLE pessoa (
    id_pessoa     SERIAL PRIMARY KEY,
    nome          VARCHAR(120) NOT NULL,
    cpf           CHAR(11)     NOT NULL UNIQUE,
    data_nasc     DATE         NOT NULL CHECK (data_nasc <= CURRENT_DATE),
    nacionalidade VARCHAR(60)  NOT NULL DEFAULT 'Brasileira',
    tipo          VARCHAR(10)  NOT NULL CHECK (tipo IN ('ATLETA','ARBITRO','TECNICO'))
);

-- ---------------------------------------------------------------------
-- 7. ATLETA / ARBITRO / TECNICO  (especializações)
-- ---------------------------------------------------------------------
CREATE TABLE atleta (
    id_pessoa  INTEGER PRIMARY KEY REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    altura     NUMERIC(3,2) CHECK (altura > 0 AND altura < 3),
    peso       NUMERIC(5,2) CHECK (peso > 0),
    num_camisa INTEGER CHECK (num_camisa IS NULL OR num_camisa BETWEEN 1 AND 99)
);

CREATE TABLE arbitro (
    id_pessoa  INTEGER PRIMARY KEY REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    categoria  VARCHAR(40)
);

CREATE TABLE tecnico (
    id_pessoa          INTEGER PRIMARY KEY REFERENCES pessoa(id_pessoa) ON DELETE CASCADE,
    registro_federacao VARCHAR(30)
);

-- ---------------------------------------------------------------------
-- 8. ATLETA_POSICAO  (N:N)
-- ---------------------------------------------------------------------
CREATE TABLE atleta_posicao (
    id_atleta   INTEGER NOT NULL REFERENCES atleta(id_pessoa)   ON DELETE CASCADE,
    id_posicao  INTEGER NOT NULL REFERENCES posicao(id_posicao) ON DELETE CASCADE,
    PRIMARY KEY (id_atleta, id_posicao)
);

-- ---------------------------------------------------------------------
-- 9. INSCRICAO_TEMPORADA  (N:N equipe×temporada)
-- ---------------------------------------------------------------------
CREATE TABLE inscricao_temporada (
    id_temporada INTEGER NOT NULL REFERENCES temporada(id_temporada) ON DELETE CASCADE,
    id_equipe    INTEGER NOT NULL REFERENCES equipe(id_equipe)       ON DELETE CASCADE,
    PRIMARY KEY (id_temporada, id_equipe)
);

-- ---------------------------------------------------------------------
-- 10. PARTIDA
-- ---------------------------------------------------------------------
CREATE TABLE partida (
    id_partida      SERIAL PRIMARY KEY,
    data_hora       TIMESTAMP NOT NULL,
    status          VARCHAR(15) NOT NULL DEFAULT 'AGENDADA'
                       CHECK (status IN ('AGENDADA','EM_ANDAMENTO','ENCERRADA','CANCELADA')),
    gols_mandante   INTEGER NOT NULL DEFAULT 0 CHECK (gols_mandante   >= 0),
    gols_visitante  INTEGER NOT NULL DEFAULT 0 CHECK (gols_visitante  >= 0),
    id_temporada    INTEGER NOT NULL REFERENCES temporada(id_temporada) ON DELETE RESTRICT,
    id_mandante     INTEGER NOT NULL REFERENCES equipe(id_equipe),
    id_visitante    INTEGER NOT NULL REFERENCES equipe(id_equipe),
    id_estadio      INTEGER NOT NULL REFERENCES estadio(id_estadio),
    CHECK (id_mandante <> id_visitante),
    UNIQUE (id_estadio, data_hora)
);

-- ---------------------------------------------------------------------
-- 11. PARTIDA_ARBITRO  (N:N com atributo "papel")
-- ---------------------------------------------------------------------
CREATE TABLE partida_arbitro (
    id_partida  INTEGER NOT NULL REFERENCES partida(id_partida)   ON DELETE CASCADE,
    id_arbitro  INTEGER NOT NULL REFERENCES arbitro(id_pessoa),
    papel       VARCHAR(15) NOT NULL DEFAULT 'PRINCIPAL'
                   CHECK (papel IN ('PRINCIPAL','ASSISTENTE','QUARTO')),
    PRIMARY KEY (id_partida, id_arbitro)
);

-- ---------------------------------------------------------------------
-- 12. CONTRATO  (entidade associativa atleta × equipe × temporada)
-- ---------------------------------------------------------------------
CREATE TABLE contrato (
    id_contrato   SERIAL PRIMARY KEY,
    salario       NUMERIC(12,2) NOT NULL CHECK (salario >= 0),
    data_inicio   DATE NOT NULL,
    data_fim      DATE,
    id_atleta     INTEGER NOT NULL REFERENCES atleta(id_pessoa),
    id_equipe     INTEGER NOT NULL REFERENCES equipe(id_equipe),
    id_temporada  INTEGER NOT NULL REFERENCES temporada(id_temporada),
    CHECK (data_fim IS NULL OR data_fim >= data_inicio),
    UNIQUE (id_atleta, id_temporada, data_inicio)
);

-- ---------------------------------------------------------------------
-- 13. EVENTO  (eventos de uma partida)
-- ---------------------------------------------------------------------
CREATE TABLE evento (
    id_evento   SERIAL PRIMARY KEY,
    tipo        VARCHAR(20) NOT NULL
                   CHECK (tipo IN ('GOL','CARTAO_AMARELO','CARTAO_VERMELHO','SUBSTITUICAO')),
    minuto      SMALLINT NOT NULL CHECK (minuto BETWEEN 0 AND 130),
    id_partida  INTEGER NOT NULL REFERENCES partida(id_partida) ON DELETE CASCADE,
    id_atleta   INTEGER REFERENCES atleta(id_pessoa),
    id_atleta2  INTEGER REFERENCES atleta(id_pessoa),
    descricao   VARCHAR(200),
    CHECK ((tipo = 'SUBSTITUICAO') = (id_atleta2 IS NOT NULL)),
    CHECK (id_atleta IS NOT NULL OR tipo <> 'GOL')
);
