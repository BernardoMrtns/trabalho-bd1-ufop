-- =====================================================================
-- SportsLeagueDB — Índices e Gatilhos (Triggers)
-- Etapa 4
-- =====================================================================

-- ---------------------------------------------------------------------
-- ÍNDICES (para acelerar consultas comuns)
-- ---------------------------------------------------------------------
CREATE INDEX idx_partida_temporada  ON partida(id_temporada);
CREATE INDEX idx_partida_mandante   ON partida(id_mandante);
CREATE INDEX idx_partida_visitante  ON partida(id_visitante);
CREATE INDEX idx_partida_data       ON partida(data_hora);
CREATE INDEX idx_evento_partida     ON evento(id_partida);
CREATE INDEX idx_evento_atleta      ON evento(id_atleta);
CREATE INDEX idx_evento_tipo        ON evento(tipo);
CREATE INDEX idx_contrato_atleta    ON contrato(id_atleta);
CREATE INDEX idx_contrato_temporada ON contrato(id_temporada);
CREATE INDEX idx_pessoa_nome        ON pessoa(nome);
CREATE INDEX idx_pessoa_cpf         ON pessoa(cpf);

-- ---------------------------------------------------------------------
-- EXTENSÃO pg_trgm (busca aproximada por nome) — opcional.
-- Tenta criar; se faltar privilégio, cai no ILIKE simples (ver views/consultas).
-- ---------------------------------------------------------------------
DO $
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm') THEN
        CREATE EXTENSION IF NOT EXISTS pg_trgm;
        CREATE INDEX IF NOT EXISTS idx_pessoa_nome_trgm ON pessoa USING gin (nome gin_trgm_ops);
    END IF;
EXCEPTION WHEN insufficient_privilege OR feature_not_supported THEN
    RAISE NOTICE 'Extensão pg_trgm não pôde ser criada (sem privilégio). Consultas por nome usarão ILIKE.';
END $;

-- ---------------------------------------------------------------------
-- TRIGGER 1: R3 — impedir contrato ativo duplicado na mesma temporada
-- (atleta não pode jogar por duas equipes ao mesmo tempo)
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION chk_contrato_atleta_unico() RETURNS TRIGGER AS $$
DECLARE
    conflito_id INTEGER;
BEGIN
    SELECT c.id_contrato INTO conflito_id
    FROM contrato c
    WHERE c.id_atleta = NEW.id_atleta
      AND c.id_temporada = NEW.id_temporada
      AND c.id_equipe <> NEW.id_equipe
      AND (c.data_fim IS NULL OR c.data_fim >= COALESCE(NEW.data_inicio, CURRENT_DATE))
    LIMIT 1;

    IF conflito_id IS NOT NULL THEN
        RAISE EXCEPTION 'Atleta % já possui contrato ativo (contrato %) com outra equipe na temporada %',
            NEW.id_atleta, conflito_id, NEW.id_temporada
            USING ERRCODE = 'check_violation';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_contrato_atleta_unico
    BEFORE INSERT OR UPDATE ON contrato
    FOR EACH ROW EXECUTE FUNCTION chk_contrato_atleta_unico();

-- ---------------------------------------------------------------------
-- TRIGGER 2: R4 — equipes da partida devem estar inscritas na temporada
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION chk_partida_inscricoes() RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM inscricao_temporada
                   WHERE id_temporada = NEW.id_temporada AND id_equipe = NEW.id_mandante) THEN
        RAISE EXCEPTION 'Equipe mandante % não está inscrita na temporada %',
            NEW.id_mandante, NEW.id_temporada USING ERRCODE = 'foreign_key_violation';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM inscricao_temporada
                   WHERE id_temporada = NEW.id_temporada AND id_equipe = NEW.id_visitante) THEN
        RAISE EXCEPTION 'Equipe visitante % não está inscrita na temporada %',
            NEW.id_visitante, NEW.id_temporada USING ERRCODE = 'foreign_key_violation';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_partida_inscricoes
    BEFORE INSERT OR UPDATE ON partida
    FOR EACH ROW EXECUTE FUNCTION chk_partida_inscricoes();

-- ---------------------------------------------------------------------
-- TRIGGER 3: sincronizar placar da partida com a contagem de gols
-- (quando status = ENCERRADA e há gols registrados como eventos)
-- ---------------------------------------------------------------------
CREATE OR REPLACE FUNCTION sync_placar_partida() RETURNS TRIGGER AS $$
DECLARE
    g_mandante INTEGER;
    g_visitante INTEGER;
    v_id_mandante INTEGER;
    v_id_visitante INTEGER;
BEGIN
    SELECT id_mandante, id_visitante INTO v_id_mandante, v_id_visitante
    FROM partida WHERE id_partida = NEW.id_partida;

    -- Conta gols por equipe: gols marcados por atletas de cada equipe.
    SELECT COUNT(*) INTO g_mandante
    FROM evento e
    JOIN contrato c ON c.id_atleta = e.id_atleta
    WHERE e.id_partida = NEW.id_partida
      AND e.tipo = 'GOL'
      AND c.id_equipe = v_id_mandante;

    SELECT COUNT(*) INTO g_visitante
    FROM evento e
    JOIN contrato c ON c.id_atleta = e.id_atleta
    WHERE e.id_partida = NEW.id_partida
      AND e.tipo = 'GOL'
      AND c.id_equipe = v_id_visitante;

    UPDATE partida
       SET gols_mandante = g_mandante, gols_visitante = g_visitante
     WHERE id_partida = NEW.id_partida;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_sync_placar
    AFTER INSERT OR UPDATE OF id_atleta, tipo ON evento
    FOR EACH ROW WHEN (NEW.tipo = 'GOL')
    EXECUTE FUNCTION sync_placar_partida();
