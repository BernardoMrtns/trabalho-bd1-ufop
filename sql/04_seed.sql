INSERT INTO modalidade (nome, n_jogadores_por_time) VALUES
    ('Futebol', 11),
    ('Basquete', 5),
    ('Vôlei',   6);

INSERT INTO posicao (nome, id_modalidade) VALUES
    ('Goleiro',  1),
    ('Zagueiro', 1),
    ('Lateral',  1),
    ('Meio-Campo', 1),
    ('Atacante', 1);

INSERT INTO estadio (nome, cidade, capacidade) VALUES
    ('Arena Tubarão',     'São Paulo', 45000),
    ('Estádio Solar',     'Rio de Janeiro', 38000),
    ('Arena Pampas',      'Porto Alegre', 52000),
    ('Estádio Mangueiral','Recife', 30000);

INSERT INTO equipe (nome, sigla, cidade, id_estadio_sede) VALUES
    ('Tubarões FC',      'TUB', 'São Paulo',      1),
    ('Solar EC',         'SOL', 'Rio de Janeiro', 2),
    ('Pampas SC',        'PMP', 'Porto Alegre',   3),
    ('Mangueiral FC',    'MNG', 'Recife',         4);

INSERT INTO temporada (nome, ano, data_inicio, data_fim, id_modalidade) VALUES
    ('Brasileirão Amador', 2026, '2026-03-01', '2026-11-30', 1);

INSERT INTO inscricao_temporada (id_temporada, id_equipe) VALUES
    (1,1),(1,2),(1,3),(1,4);

INSERT INTO pessoa (nome, cpf, data_nasc, nacionalidade, tipo) VALUES
    ('Carlos Mendes',    '11111111111', '1998-04-12', 'Brasileira', 'ATLETA'),
    ('João Silva',       '22222222222', '2000-07-30', 'Brasileira', 'ATLETA'),
    ('Pedro Alves',      '33333333333', '1999-12-01', 'Brasileira', 'ATLETA'),
    ('Lucas Ribeiro',    '44444444444', '2001-02-18', 'Brasileira', 'ATLETA'),
    ('Marcos Lima',      '55555555555', '1997-09-09', 'Brasileira', 'ATLETA'),
    ('Diego Souza',      '66666666666', '1996-01-25', 'Brasileira', 'ATLETA'),
    ('Rafael Costa',     '77777777777', '2002-06-14', 'Brasileira', 'ATLETA'),
    ('Bruno Nunes',      '88888888888', '2000-03-21', 'Brasileira', 'ATLETA'),
    ('Felipe Rocha',     '99999999999', '1998-11-02', 'Brasileira', 'ATLETA'),
    ('Gustavo Pinto',    '10101010101', '2001-08-19', 'Brasileira', 'ATLETA'),
    ('Henrique Dias',    '12121212121', '1999-05-07', 'Brasileira', 'ATLETA'),
    ('André Moraes',     '13131313131', '1997-10-28', 'Brasileira', 'ATLETA'),
    ('Wagner Lopes',     '14141414141', '1985-02-10', 'Brasileira', 'ARBITRO'),
    ('Paulo Camargo',    '15151515151', '1980-12-15', 'Brasileira', 'ARBITRO'),
    ('Mário Schmidt',    '16161616161', '1975-04-22', 'Brasileira', 'TECNICO'),
    ('Fernando Bernardes','17171717171','1978-09-03', 'Brasileira', 'TECNICO');

INSERT INTO atleta (id_pessoa, altura, peso, num_camisa) VALUES
    (1,1.82,79,1),(2,1.75,72,10),(3,1.80,78,5),
    (4,1.78,74,9),(5,1.85,82,7),(6,1.70,68,11),
    (7,1.88,85,3),(8,1.83,80,8),(9,1.77,73,6),
    (10,1.90,88,4),(11,1.74,70,2),(12,1.86,84,12);

INSERT INTO arbitro (id_pessoa, categoria) VALUES
    (13,'FIFA'), (14,'Estadual');

INSERT INTO tecnico (id_pessoa, registro_federacao) VALUES
    (15,'CBF-0001'), (16,'CBF-0002');

INSERT INTO atleta_posicao (id_atleta, id_posicao) VALUES
    (1,1),(2,5),(3,2),(4,5),(5,4),(6,5),
    (7,2),(8,4),(9,3),(10,2),(11,1),(12,5);

INSERT INTO contrato (id_atleta, id_equipe, id_temporada, salario, data_inicio, data_fim) VALUES
    (1,1,1, 50000,'2026-01-01',NULL),
    (2,1,1, 60000,'2026-01-01',NULL),
    (3,1,1, 45000,'2026-01-01',NULL),
    (4,2,1, 55000,'2026-01-01',NULL),
    (5,2,1, 70000,'2026-01-01',NULL),
    (6,2,1, 40000,'2026-01-01',NULL),
    (7,3,1, 48000,'2026-01-01',NULL),
    (8,3,1, 52000,'2026-01-01',NULL),
    (9,3,1, 39000,'2026-01-01',NULL),
    (10,4,1, 61000,'2026-01-01',NULL),
    (11,4,1, 35000,'2026-01-01',NULL),
    (12,4,1, 58000,'2026-01-01',NULL);

INSERT INTO partida (data_hora, status, gols_mandante, gols_visitante,
                     id_temporada, id_mandante, id_visitante, id_estadio) VALUES
    ('2026-03-08 16:00','ENCERRADA',2,1, 1,1,2,1),
    ('2026-03-08 18:00','ENCERRADA',1,1, 1,3,4,3),
    ('2026-03-15 16:00','ENCERRADA',3,0, 1,1,3,1),
    ('2026-03-15 18:00','ENCERRADA',0,2, 1,4,2,4),
    ('2026-03-22 16:00','ENCERRADA',1,1, 1,2,1,2),
    ('2026-03-22 18:00','ENCERRADA',2,2, 1,4,3,4),
    ('2026-03-29 16:00','AGENDADA',  0,0, 1,1,4,1);

INSERT INTO partida_arbitro (id_partida, id_arbitro, papel) VALUES
    (1,13,'PRINCIPAL'),(1,14,'ASSISTENTE'),
    (2,13,'PRINCIPAL'),
    (3,14,'PRINCIPAL'),
    (4,13,'PRINCIPAL'),
    (5,14,'PRINCIPAL'),
    (6,13,'PRINCIPAL');

INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('GOL',            15, 1, 2, 'Gol de cabeça'),
    ('GOL',            55, 1, 2, 'Contra-ataque'),
    ('GOL',            78, 1, 4, 'Falta cobrada'),
    ('CARTAO_AMARELO', 30, 1, 5, 'Falta dura'),
    ('CARTAO_AMARELO', 64, 1, 3, 'Reclamação');

INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('GOL',            22, 2, 8,  'Chute de fora'),
    ('GOL',            70, 2, 10, 'Pênalti'),
    ('CARTAO_VERMELHO',45, 2, 9,  'Falta como último homem');

INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('GOL',            10, 3, 1, 'Gol de pênalti'),
    ('GOL',            33, 3, 2, 'Finalização'),
    ('GOL',            88, 3, 3, 'Escanteio');

INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('GOL',            40, 4, 4, 'Contra-ataque'),
    ('GOL',            82, 4, 5, 'Falta');

INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('GOL',            25, 5, 5, 'Bola parada'),
    ('GOL',            60, 5, 1, 'Rebote');

INSERT INTO evento (tipo, minuto, id_partida, id_atleta, id_atleta2, descricao) VALUES
    ('GOL',            12, 6, 10, NULL, 'Cabeçada'),
    ('GOL',            28, 6, 7,  NULL, 'Arrancada'),
    ('GOL',            50, 6, 12, NULL, 'Finalização'),
    ('GOL',            75, 6, 8,  NULL, 'Rebote'),
    ('SUBSTITUICAO',   65, 6, 9,  11,   'Atleta 9 sai; atleta 11 entra');
