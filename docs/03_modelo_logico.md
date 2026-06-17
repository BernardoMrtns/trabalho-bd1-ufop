# Etapa 3 — Modelo Lógico

> Mapeamento do modelo conceitual (Etapa 2) para o modelo relacional.
> Notação: `RELACAO (atributo_chave*, atributo, FK→tabela(ref))` — `*` = chave primária, FK indicada com seta.

---

## 3.1 Regras de mapeamento aplicadas

| Construção conceitual | Estratégia relacional adotada |
|-----------------------|-------------------------------|
| Entidade normal | Tabela própria; PK com `SERIAL`. |
| Atributo composto/multivalorado | Não há; todos os atributos são atômicos. |
| Relacionamento 1:N | FK na tabela do lado "N". |
| Relacionamento N:N | Tabela associativa com PK composta. |
| Relacionamento 1:1 | Implementado por especialização (generalização total). |
| Generalização (PESSOA → subclasses) | **Uma tabela por subclasse**; cada subclasse tem PK = FK para PESSOA. |
| Entidade associativa com atributos (CONTRATO) | Tabela própria com PK simples (surrogate) e três FKs. |
| Auto-relacionamento com papel (mandante/visitante) | Duas FKs na mesma tabela (PARTIDA). |

---

## 3.2 Esquema relacional

```
MODALIDADE (id_modalidade*, nome, n_jogadores_por_time)
    PK: id_modalidade

POSICAO (id_posicao*, nome, id_modalidade → MODALIDADE)
    PK: id_posicao
    FK: id_modalidade → MODALIDADE
    UNIQUE: (nome, id_modalidade)

ESTADIO (id_estadio*, nome, cidade, capacidade)
    PK: id_estadio

EQUIPE (id_equipe*, nome, sigla, cidade, id_estadio_sede → ESTADIO)
    PK: id_equipe
    FK: id_estadio_sede → ESTADIO
    UNIQUE: sigla

TEMPORADA (id_temporada*, nome, ano, data_inicio, data_fim, id_modalidade → MODALIDADE)
    PK: id_temporada
    FK: id_modalidade → MODALIDADE
    CHECK: data_fim > data_inicio
    UNIQUE: (nome, ano)

PESSOA (id_pessoa*, nome, cpf, data_nasc, nacionalidade, tipo)
    PK: id_pessoa
    UNIQUE: cpf
    CHECK: data_nasc <= CURRENT_DATE
    tipo ∈ {ATLETA, ARBITRO, TECNICO}

ATLETA (id_pessoa* → PESSOA, altura, peso, num_camisa)
    PK: id_pessoa
    FK: id_pessoa → PESSOA ON DELETE CASCADE
    CHECK: altura > 0 AND peso > 0

ARBITRO (id_pessoa* → PESSOA, categoria)
    PK: id_pessoa
    FK: id_pessoa → PESSOA ON DELETE CASCADE

TECNICO (id_pessoa* → PESSOA, registro_federacao)
    PK: id_pessoa
    FK: id_pessoa → PESSOA ON DELETE CASCADE

ATLETA_POSICAO (id_atleta* → ATLETA, id_posicao* → POSICAO)
    PK: (id_atleta, id_posicao)

INSCRICAO_TEMPORADA (id_temporada* → TEMPORADA, id_equipe* → EQUIPE)
    PK: (id_temporada, id_equipe)

PARTIDA (id_partida*, data_hora, status, gols_mandante, gols_visitante,
         id_temporada → TEMPORADA,
         id_mandante  → EQUIPE,
         id_visitante → EQUIPE,
         id_estadio   → ESTADIO)
    PK: id_partida
    CHECK: gols_mandante >= 0 AND gols_visitante >= 0
    CHECK: id_mandante <> id_visitante
    UNIQUE: (id_estadio, data_hora)   -- duas partidas não no mesmo estádio/hora
    status ∈ {AGENDADA, EM_ANDAMENTO, ENCERRADA, CANCELADA}

PARTIDA_ARBITRO (id_partida* → PARTIDA, id_arbitro* → ARBITRO, papel)
    PK: (id_partida, id_arbitro)
    papel ∈ {PRINCIPAL, ASSISTENTE, QUARTO}

CONTRATO (id_contrato*, salario, data_inicio, data_fim,
          id_atleta    → ATLETA,
          id_equipe    → EQUIPE,
          id_temporada → TEMPORADA)
    PK: id_contrato
    FK: (id_atleta, id_temporada) implícito via trigger (R3)
    UNIQUE: (id_atleta, id_temporada, data_inicio)   -- evita duplicar contrato idêntico
    CHECK: data_fim IS NULL OR data_fim >= data_inicio

EVENTO (id_evento*, tipo, minuto, id_partida → PARTIDA,
        id_atleta → ATLETA, id_atleta2 → ATLETA, descricao)
    PK: id_evento
    FK: id_partida → PARTIDA ON DELETE CASCADE
    CHECK: minuto BETWEEN 0 AND 130
    tipo ∈ {GOL, CARTAO_AMARELO, CARTAO_VERMELHO, SUBSTITUICAO}
    CHECK: (tipo = 'SUBSTITUICAO') = (id_atleta2 IS NOT NULL)
```

---

## 3.3 Desnormalizações e decisões
- `PESSOA.tipo` (coluna discriminadora) foi mantida para acelerar consultas que filtram por categoria de pessoa, embora seja derivável das tabelas-filhas. É uma desnormalização controlada (mantida em sincronia por aplicação/triggers).
- `gols_mandante`/`gols_visitante` em PARTIDA são **redundantes** em relação à soma de eventos GOL, mas evitam agregação a cada consulta de classificação (desnormalização para desempenho, validada pela aplicação).
- Adicionadas `UNIQUE` em (sigla) e (cpf) para reforçar regras de negócio R6 e identidade das equipes.
