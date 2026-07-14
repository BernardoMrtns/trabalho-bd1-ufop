CREATE OR REPLACE VIEW vw_classificacao AS
WITH mandante AS (
    SELECT id_temporada, id_mandante AS id_equipe,
           gols_mandante AS gols_pro, gols_visitante AS gols_contra
    FROM partida
    WHERE status = 'ENCERRADA'
),
visitante AS (
    SELECT id_temporada, id_visitante AS id_equipe,
           gols_visitante AS gols_pro, gols_mandante AS gols_contra
    FROM partida
    WHERE status = 'ENCERRADA'
),
jogos AS (
    SELECT id_temporada, id_equipe, gols_pro, gols_contra FROM mandante
    UNION ALL
    SELECT id_temporada, id_equipe, gols_pro, gols_contra FROM visitante
)
SELECT j.id_temporada,
       j.id_equipe,
       e.nome       AS equipe,
       e.sigla,
       COUNT(*)     AS jogos,
       SUM(CASE WHEN j.gols_pro > j.gols_contra THEN 1 ELSE 0 END) AS vitorias,
       SUM(CASE WHEN j.gols_pro = j.gols_contra THEN 1 ELSE 0 END) AS empates,
       SUM(CASE WHEN j.gols_pro < j.gols_contra THEN 1 ELSE 0 END) AS derrotas,
       SUM(j.gols_pro)    AS gols_pro,
       SUM(j.gols_contra) AS gols_contra,
       SUM(j.gols_pro) - SUM(j.gols_contra) AS saldo_gols,
       SUM(CASE WHEN j.gols_pro > j.gols_contra THEN 3
                WHEN j.gols_pro = j.gols_contra THEN 1
                ELSE 0 END) AS pontos
FROM jogos j
JOIN equipe e ON e.id_equipe = j.id_equipe
GROUP BY j.id_temporada, j.id_equipe, e.nome, e.sigla;

CREATE OR REPLACE VIEW vw_artilharia AS
SELECT p.id_temporada,
       e.id_atleta,
       pes.nome    AS atleta,
       eq.nome     AS equipe,
       eq.sigla,
       COUNT(*)    AS gols
FROM evento e
JOIN partida  p   ON p.id_partida  = e.id_partida
JOIN atleta   a   ON a.id_pessoa   = e.id_atleta
JOIN pessoa   pes ON pes.id_pessoa = a.id_pessoa
LEFT JOIN contrato c ON c.id_atleta = e.id_atleta AND c.id_temporada = p.id_temporada
LEFT JOIN equipe  eq ON eq.id_equipe = c.id_equipe
WHERE e.tipo = 'GOL' AND p.status = 'ENCERRADA'
GROUP BY p.id_temporada, e.id_atleta, pes.nome, eq.nome, eq.sigla;

CREATE OR REPLACE VIEW vw_cartoes AS
SELECT p.id_temporada,
       e.id_atleta,
       pes.nome AS atleta,
       eq.nome  AS equipe,
       SUM(CASE WHEN e.tipo = 'CARTAO_AMARELO'   THEN 1 ELSE 0 END) AS amarelos,
       SUM(CASE WHEN e.tipo = 'CARTAO_VERMELHO'  THEN 1 ELSE 0 END) AS vermelhos
FROM evento e
JOIN partida  p   ON p.id_partida  = e.id_partida
JOIN pessoa   pes ON pes.id_pessoa = e.id_atleta
LEFT JOIN contrato c ON c.id_atleta = e.id_atleta AND c.id_temporada = p.id_temporada
LEFT JOIN equipe  eq ON eq.id_equipe = c.id_equipe
WHERE e.tipo IN ('CARTAO_AMARELO','CARTAO_VERMELHO')
GROUP BY p.id_temporada, e.id_atleta, pes.nome, eq.nome;

CREATE OR REPLACE VIEW vw_confrontos AS
SELECT p.id_temporada,
       t.nome AS temporada,
       p.data_hora,
       em.nome AS mandante,   ev.nome AS visitante,
       p.gols_mandante, p.gols_visitante,
       CASE
           WHEN p.gols_mandante > p.gols_visitante THEN em.nome
           WHEN p.gols_mandante < p.gols_visitante THEN ev.nome
           ELSE 'EMPATE'
       END AS resultado
FROM partida p
JOIN equipe em ON em.id_equipe = p.id_mandante
JOIN equipe ev ON ev.id_equipe = p.id_visitante
JOIN temporada t ON t.id_temporada = p.id_temporada
WHERE p.status = 'ENCERRADA';

CREATE OR REPLACE VIEW vw_elenco AS
SELECT c.id_temporada,
       c.id_equipe,
       eq.nome AS equipe,
       c.id_atleta,
       pes.nome AS atleta,
       a.num_camisa,
       a.altura,
       a.peso
FROM contrato c
JOIN equipe  eq  ON eq.id_equipe   = c.id_equipe
JOIN atleta  a   ON a.id_pessoa    = c.id_atleta
JOIN pessoa  pes ON pes.id_pessoa  = c.id_atleta;

CREATE OR REPLACE VIEW vw_partidas_detalhadas AS
SELECT p.id_partida,
       p.data_hora,
       p.status,
       t.nome  AS temporada,
       em.nome AS mandante,
       ev.nome AS visitante,
       em.sigla AS sigla_mandante,
       ev.sigla AS sigla_visitante,
       p.gols_mandante,
       p.gols_visitante,
       es.nome AS estadio,
       es.cidade
FROM partida p
JOIN temporada t  ON t.id_temporada = p.id_temporada
JOIN equipe    em ON em.id_equipe   = p.id_mandante
JOIN equipe    ev ON ev.id_equipe   = p.id_visitante
JOIN estadio   es ON es.id_estadio  = p.id_estadio;

CREATE OR REPLACE VIEW vw_resumo_temporada AS
SELECT t.id_temporada,
       t.nome  AS temporada,
       t.ano,
       m.nome  AS modalidade,
       (SELECT COUNT(*) FROM inscricao_temporada i WHERE i.id_temporada = t.id_temporada) AS n_equipes,
       (SELECT COUNT(*) FROM partida p WHERE p.id_temporada = t.id_temporada)              AS n_partidas,
       (SELECT COUNT(*) FROM partida p WHERE p.id_temporada = t.id_temporada AND p.status = 'ENCERRADA') AS n_encerradas,
       (SELECT COALESCE(SUM(gols_mandante + gols_visitante),0)
          FROM partida p WHERE p.id_temporada = t.id_temporada AND p.status = 'ENCERRADA') AS total_gols
FROM temporada t
JOIN modalidade m ON m.id_modalidade = t.id_modalidade;
