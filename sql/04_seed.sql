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
    ('Estadio Azteca', 'Cidade do México', 83264),
    ('MetLife Stadium', 'Nova York/Nova Jersey', 82500),
    ('SoFi Stadium', 'Los Angeles', 70240),
    ('BMO Field', 'Toronto', 30000),
    ('AT&T Stadium', 'Dallas', 80000),
    ('Hard Rock Stadium', 'Miami', 64767),
    ('Estadio Akron', 'Guadalajara', 49850),
    ('BC Place', 'Vancouver', 54500);

INSERT INTO equipe (nome, sigla, cidade, id_estadio_sede) VALUES
    ('Brasil', 'BRA', 'Rio de Janeiro', 1), 
    ('França', 'FRA', 'Paris', 2),
    ('Argentina', 'ARG', 'Buenos Aires', 3),
    ('Estados Unidos', 'USA', 'Washington', 4),
    ('Inglaterra', 'ING', 'Londres', 5),
    ('Espanha', 'ESP', 'Madri', 6),
    ('Portugal', 'POR', 'Lisboa', 7),
    ('Alemanha', 'ALE', 'Berlim', 8);

INSERT INTO temporada (nome, ano, data_inicio, data_fim, id_modalidade) VALUES
    ('Copa do Mundo FIFA', 2026, '2026-06-11', '2026-07-19', 1);

INSERT INTO inscricao_temporada (id_temporada, id_equipe) VALUES
    (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8);

INSERT INTO pessoa (nome, cpf, data_nasc, nacionalidade, tipo) VALUES
    -- Atletas: Brasil (1-3)
    ('Alisson Becker',   '11111111111', '1992-10-02', 'Brasileira', 'ATLETA'),
    ('Marquinhos',       '22222222222', '1994-05-14', 'Brasileira', 'ATLETA'),
    ('Vinícius Júnior',  '33333333333', '2000-07-12', 'Brasileira', 'ATLETA'),
    -- Atletas: França (4-6)
    ('Mike Maignan',     '44444444444', '1995-07-03', 'Francesa', 'ATLETA'),
    ('Dayot Upamecano',  '55555555555', '1998-10-27', 'Francesa', 'ATLETA'),
    ('Kylian Mbappé',    '66666666666', '1998-12-20', 'Francesa', 'ATLETA'),
    -- Atletas: Argentina (7-9)
    ('Emiliano Martínez','77777777777', '1992-09-02', 'Argentina', 'ATLETA'),
    ('Cristian Romero',  '88888888888', '1998-04-27', 'Argentina', 'ATLETA'),
    ('Lionel Messi',     '99999999999', '1987-06-24', 'Argentina', 'ATLETA'),
    -- Atletas: Estados Unidos (10-12)
    ('Matt Turner',      '10101010101', '1994-06-24', 'Norte-americana', 'ATLETA'),
    ('Tim Ream',         '12121212121', '1987-10-05', 'Norte-americana', 'ATLETA'),
    ('Christian Pulisic','13131313131', '1998-09-18', 'Norte-americana', 'ATLETA'),
    -- Atletas: Inglaterra (13-15)
    ('Jordan Pickford',  '18181818181', '1994-03-07', 'Inglesa', 'ATLETA'),
    ('John Stones',      '19191919191', '1994-05-28', 'Inglesa', 'ATLETA'),
    ('Jude Bellingham',  '20202020202', '2003-06-29', 'Inglesa', 'ATLETA'),
    -- Atletas: Espanha (16-18)
    ('Unai Simón',       '21212121212', '1997-06-11', 'Espanhola', 'ATLETA'),
    ('Rodri',            '23232323232', '1996-06-22', 'Espanhola', 'ATLETA'),
    ('Lamine Yamal',     '24242424242', '2007-07-13', 'Espanhola', 'ATLETA'),
    -- Atletas: Portugal (19-21)
    ('Diogo Costa',      '25252525252', '1999-09-19', 'Portuguesa', 'ATLETA'),
    ('Rúben Dias',       '26262626262', '1997-05-14', 'Portuguesa', 'ATLETA'),
    ('Cristiano Ronaldo','27272727272', '1985-02-05', 'Portuguesa', 'ATLETA'),
    -- Atletas: Alemanha (22-24)
    ('Manuel Neuer',     '28282828282', '1986-03-27', 'Alemã', 'ATLETA'),
    ('Antonio Rüdiger',  '29292929292', '1993-03-03', 'Alemã', 'ATLETA'),
    ('Jamal Musiala',    '30303030303', '2003-02-26', 'Alemã', 'ATLETA'),
    
    -- Árbitros (25-27)
    ('Szymon Marciniak', '31313131313', '1981-01-07', 'Polonesa', 'ARBITRO'),
    ('Wilton S. Sampaio','32323232323', '1981-12-28', 'Brasileira', 'ARBITRO'),
    ('Anthony Taylor',   '34343434343', '1978-10-20', 'Inglesa', 'ARBITRO'),

    -- Técnicos (28-35)
    ('Dorival Júnior',   '35353535353', '1962-04-25', 'Brasileira', 'TECNICO'),
    ('Didier Deschamps', '36363636363', '1968-10-15', 'Francesa', 'TECNICO'),
    ('Lionel Scaloni',   '37373737373', '1978-05-16', 'Argentina', 'TECNICO'),
    ('Gregg Berhalter',  '38383838383', '1973-08-01', 'Norte-americana', 'TECNICO'),
    ('Gareth Southgate', '39393939393', '1970-09-03', 'Inglesa', 'TECNICO'),
    ('Luis de la Fuente','40404040404', '1961-06-21', 'Espanhola', 'TECNICO'),
    ('Roberto Martínez', '41414141414', '1973-07-13', 'Espanhola', 'TECNICO'),
    ('Julian Nagelsmann','42424242424', '1987-07-23', 'Alemã', 'TECNICO');

INSERT INTO atleta (id_pessoa, altura, peso, num_camisa) VALUES
    (1,1.93,91,1),(2,1.83,75,4),(3,1.76,73,7),
    (4,1.91,89,1),(5,1.86,83,4),(6,1.78,75,10),
    (7,1.95,88,1),(8,1.85,79,13),(9,1.70,72,10),
    (10,1.91,79,1),(11,1.86,82,13),(12,1.77,73,10),
    (13,1.85,77,1),(14,1.88,72,5),(15,1.86,75,10),
    (16,1.90,80,1),(17,1.91,82,16),(18,1.80,68,19),
    (19,1.86,82,1),(20,1.87,83,4),(21,1.87,83,7),
    (22,1.93,93,1),(23,1.90,85,2),(24,1.84,72,10);

INSERT INTO arbitro (id_pessoa, categoria) VALUES
    (25,'FIFA'), (26,'FIFA'), (27,'FIFA');

INSERT INTO tecnico (id_pessoa, registro_federacao) VALUES
    (28,'CBF-01'), (29,'FFF-01'), (30,'AFA-01'), (31,'USSF-01'),
    (32,'FA-01'), (33,'RFEF-01'), (34,'FPF-01'), (35,'DFB-01');

INSERT INTO atleta_posicao (id_atleta, id_posicao) VALUES
    (1,1),(2,2),(3,5), 
    (4,1),(5,2),(6,5), 
    (7,1),(8,2),(9,5), 
    (10,1),(11,2),(12,5),
    (13,1),(14,2),(15,4),
    (16,1),(17,4),(18,5),
    (19,1),(20,2),(21,5),
    (22,1),(23,2),(24,4);

INSERT INTO contrato (id_atleta, id_equipe, id_temporada, salario, data_inicio, data_fim) VALUES
    (1,1,1, 100000,'2026-06-01','2026-07-20'),
    (2,1,1, 100000,'2026-06-01','2026-07-20'),
    (3,1,1, 150000,'2026-06-01','2026-07-20'),
    (4,2,1, 90000, '2026-06-01','2026-07-20'),
    (5,2,1, 95000, '2026-06-01','2026-07-20'),
    (6,2,1, 200000,'2026-06-01','2026-07-20'),
    (7,3,1, 95000, '2026-06-01','2026-07-20'),
    (8,3,1, 85000, '2026-06-01','2026-07-20'),
    (9,3,1, 250000,'2026-06-01','2026-07-20'),
    (10,4,1, 60000, '2026-06-01','2026-07-20'),
    (11,4,1, 55000, '2026-06-01','2026-07-20'),
    (12,4,1, 120000,'2026-06-01','2026-07-20'),
    (13,5,1, 80000, '2026-06-01','2026-07-20'),
    (14,5,1, 90000, '2026-06-01','2026-07-20'),
    (15,5,1, 180000,'2026-06-01','2026-07-20'),
    (16,6,1, 70000, '2026-06-01','2026-07-20'),
    (17,6,1, 140000,'2026-06-01','2026-07-20'),
    (18,6,1, 110000,'2026-06-01','2026-07-20'),
    (19,7,1, 75000, '2026-06-01','2026-07-20'),
    (20,7,1, 100000,'2026-06-01','2026-07-20'),
    (21,7,1, 220000,'2026-06-01','2026-07-20'),
    (22,8,1, 90000, '2026-06-01','2026-07-20'),
    (23,8,1, 110000,'2026-06-01','2026-07-20'),
    (24,8,1, 160000,'2026-06-01','2026-07-20');

-- Simulando as Quartas de Final, Semifinais e Final
INSERT INTO partida (data_hora, status, gols_mandante, gols_visitante,
                     id_temporada, id_mandante, id_visitante, id_estadio) VALUES
    ('2026-07-04 16:00','ENCERRADA',2,1, 1,1,2,5), -- Quartas 1: BRA x FRA
    ('2026-07-04 20:00','ENCERRADA',3,1, 1,3,4,6), -- Quartas 2: ARG x USA
    ('2026-07-05 16:00','ENCERRADA',1,2, 1,5,6,7), -- Quartas 3: ING x ESP
    ('2026-07-05 20:00','ENCERRADA',0,1, 1,8,7,8), -- Quartas 4: ALE x POR
    ('2026-07-10 20:00','ENCERRADA',3,2, 1,1,6,3), -- Semi 1: BRA x ESP
    ('2026-07-11 20:00','ENCERRADA',1,1, 1,3,7,4), -- Semi 2: ARG x POR (Simulando empate que foi para penaltis)
    ('2026-07-19 16:00','AGENDADA', 0,0, 1,1,3,2); -- Final: BRA x ARG (Agendada)

INSERT INTO partida_arbitro (id_partida, id_arbitro, papel) VALUES
    (1,25,'PRINCIPAL'),(1,26,'QUARTO'),
    (2,27,'PRINCIPAL'),
    (3,25,'PRINCIPAL'),
    (4,26,'PRINCIPAL'),
    (5,27,'PRINCIPAL'),
    (6,25,'PRINCIPAL'),
    (7,26,'PRINCIPAL');

-- Eventos: BRA x FRA
INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('GOL',            20, 1, 3, 'Vinícius Júnior dribla o goleiro'),
    ('GOL',            65, 1, 6, 'Mbappé empata de fora da área'),
    ('GOL',            88, 1, 2, 'Marquinhos de cabeça no escanteio'),
    ('CARTAO_AMARELO', 40, 1, 5, 'Falta tática de Upamecano');

-- Eventos: ARG x USA
INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('GOL',            12, 2, 9,  'Messi de falta, no ângulo'),
    ('GOL',            44, 2, 8,  'Romero de cabeça'),
    ('GOL',            60, 2, 12, 'Pulisic diminui para os EUA'),
    ('GOL',            89, 2, 9,  'Messi em jogada individual');

-- Eventos: ING x ESP
INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('GOL',            30, 3, 15, 'Bellingham abre o placar para a Inglaterra'),
    ('GOL',            55, 3, 18, 'Lamine Yamal empata com golaço'),
    ('GOL',            82, 3, 17, 'Rodri vira o jogo para a Espanha');

-- Eventos: ALE x POR
INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('CARTAO_VERMELHO',35, 4, 23, 'Rüdiger expulso por falta dura'),
    ('GOL',            75, 4, 21, 'Cristiano Ronaldo de pênalti');

-- Eventos: BRA x ESP
INSERT INTO evento (tipo, minuto, id_partida, id_atleta, descricao) VALUES
    ('GOL',            10, 5, 18, 'Yamal surpreende no início'),
    ('GOL',            33, 5, 3,  'Vinícius Júnior empata no contra-ataque'),
    ('GOL',            60, 5, 17, 'Rodri acerta chute de longe'),
    ('GOL',            75, 5, 3,  'Vinícius Júnior empata novamente'),
    ('GOL',            92, 5, 2,  'Marquinhos vira nos acréscimos');

-- Eventos: ARG x POR
INSERT INTO evento (tipo, minuto, id_partida, id_atleta, id_atleta2, descricao) VALUES
    ('GOL',            45, 6, 21, NULL, 'Cristiano Ronaldo de cabeça'),
    ('GOL',            88, 6, 9,  NULL, 'Messi empata no fim do jogo'),
    ('CARTAO_AMARELO', 115, 6, 7, NULL, 'Goleiro Martinez faz cera no final do jogo e toma amarelo');