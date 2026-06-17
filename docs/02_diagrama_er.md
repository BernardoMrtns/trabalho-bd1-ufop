# Etapa 2 — Diagrama Conceitual (ER)

> **Ferramenta utilizada:** Mermaid (renderizado pelo GitHub, VS Code e outros editores Markdown).
> **Notação adotada:** ER simplificada — caixas são **entidades**, losangos são **relacionamentos** (representados como bordas rotuladas no Mermaid), linhas com cardinalidade `(min, max)` usando a notação `(1,1)`, `(0,n)`, `(1,n)`.

---

## 2.1 Descrição em notação Peter Chen (texto)

Entidades (retângulos) e Atributos (elipses; **chave** sublinhada, *derivado* em itálico):

- **MODALIDADE** (<u>id_modalidade</u>, nome, n_jogadores_por_time)
- **POSICAO** (<u>id_posicao</u>, nome, id_modalidade)
- **TEMPORADA** (<u>id_temporada</u>, nome, ano, data_inicio, data_fim, id_modalidade)
- **ESTADIO** (<u>id_estadio</u>, nome, cidade, capacidade)
- **EQUIPE** (<u>id_equipe</u>, nome, sigla, cidade, id_estadio_sede)
- **PESSOA** (<u>id_pessoa</u>, nome, cpf, data_nasc, nacionalidade)  — *superclasse (generalização)*
  - **ATLETA** (<u>id_pessoa</u>, altura, peso, num_camisa)  — especialização
  - **ARBITRO** (<u>id_pessoa</u>, categoria)  — especialização
  - **TECNICO** (<u>id_pessoa</u>, registro_federacao)  — especialização
- **PARTIDA** (<u>id_partida</u>, data_hora, status, gols_mandante, gols_visitante, id_temporada, id_mandante, id_visitante, id_estadio)
- **EVENTO** (<u>id_evento</u>, tipo, minuto, id_partida, id_atleta, id_atleta2, descricao)  — `id_atleta2` usado em substituição (entra/sai)
- **CONTRATO** (<u>id_contrato</u>, salario, data_inicio, data_fim, id_atleta, id_equipe, id_temporada)
- **INSCRICAO** (<u>id_temporada, id_equipe</u>)  — associativa (N:N)
- **ATLETA_POSICAO** (<u>id_atleta, id_posicao</u>)  — associativa (N:N)

### Relacionamentos (losangos) com cardinalidade

| Relacionamento | Entidades | Cardinalidade |
|----------------|-----------|----------------|
| R-tem-modalidade | TEMPORADA → MODALIDADE | (n,1) : (1,n) |
| R-agrupa-posicao | POSICAO → MODALIDADE | (n,1) : (1,n) |
| R-sede | EQUIPE → ESTADIO | (n,1) : (0,n) |
| R-ocorre-em-estadio | PARTIDA → ESTADIO | (n,1) : (0,n) |
| R-pertence-temporada | PARTIDA → TEMPORADA | (n,1) : (1,n) |
| R-mandante | PARTIDA → EQUIPE (mandante) | (n,1) : (0,n) |
| R-visitante | PARTIDA → EQUIPE (visitante) | (n,1) : (0,n) |
| R-arbitra | PARTIDA ↔ ARBITRO | (n,m) com atributo `papel` |
| R-tem-evento | PARTIDA → EVENTO | (1,n) : (1,1) |
| R-autor | EVENTO → ATLETA | (0,n) : (0,n) |
| R-contrata | CONTRATO liga ATLETA, EQUIPE, TEMPORADA | (0,n) p/ cada — entidade associativa |
| R-inscricao | EQUIPE ↔ TEMPORADA | (n,m) — entidade associativa INSCRICAO |
| R-joga-posicao | ATLETA ↔ POSICAO | (n,m) |
| R-generalizacao | PESSOA → {ATLETA, ARBITRO, TECNICO} | total/exclusiva |

---

## 2.2 Diagrama em Mermaid

```mermaid
erDiagram
    MODALIDADE ||--o{ TEMPORADA : "tem"
    MODALIDADE ||--o{ POSICAO   : "define"
    TEMPORADA  ||--o{ PARTIDA   : "realiza"
    ESTADIO    ||--o{ EQUIPE    : "sede"
    ESTADIO    ||--o{ PARTIDA   : "sedia"
    EQUIPE     ||--o{ PARTIDA   : "mandante"
    EQUIPE     ||--o{ PARTIDA   : "visitante"

    EQUIPE     }o--o{ TEMPORADA : "inscricao"
    ATLETA     }o--o{ POSICAO   : "joga"
    ARBITRO    }o--o{ PARTIDA   : "arbitra"

    PESSOA ||--o| ATLETA  : "eh"
    PESSOA ||--o| ARBITRO : "eh"
    PESSOA ||--o| TECNICO : "eh"

    PARTIDA ||--o{ EVENTO  : "tem"
    ATLETA  ||--o{ EVENTO  : "autor"
    ATLETA  ||--o{ EVENTO  : "relacionado"

    CONTRATO }o--|| ATLETA    : "liga"
    CONTRATO }o--|| EQUIPE    : "liga"
    CONTRATO }o--|| TEMPORADA : "liga"

    MODALIDADE {
        int    id_modalidade PK
        string nome
        int    n_jogadores
    }
    POSICAO {
        int    id_posicao PK
        string nome
        int    id_modalidade FK
    }
    TEMPORADA {
        int    id_temporada PK
        string nome
        int    ano
        date   data_inicio
        date   data_fim
        int    id_modalidade FK
    }
    ESTADIO {
        int    id_estadio PK
        string nome
        string cidade
        int    capacidade
    }
    EQUIPE {
        int    id_equipe PK
        string nome
        string sigla
        string cidade
        int    id_estadio_sede FK
    }
    PESSOA {
        int    id_pessoa PK
        string nome
        string cpf UK
        date   data_nasc
        string nacionalidade
    }
    ATLETA {
        int    id_pessoa PK_FK
        float  altura
        float  peso
        int    num_camisa
    }
    ARBITRO {
        int    id_pessoa PK_FK
        string categoria
    }
    TECNICO {
        int    id_pessoa PK_FK
        string registro_federacao
    }
    PARTIDA {
        int    id_partida PK
        datetime data_hora
        string status
        int    gols_mandante
        int    gols_visitante
        int    id_temporada FK
        int    id_mandante FK
        int    id_visitante FK
        int    id_estadio FK
    }
    EVENTO {
        int    id_evento PK
        string tipo
        int    minuto
        int    id_partida FK
        int    id_atleta FK
        int    id_atleta2 FK
        string descricao
    }
    CONTRATO {
        int    id_contrato PK
        numeric salario
        date   data_inicio
        date   data_fim
        int    id_atleta FK
        int    id_equipe FK
        int    id_temporada FK
    }
```

### Observações de modelagem
- A generalização `PESSOA → {ATLETA, ARBITRO, TECNICO}` foi modelada como **tabela-mãe + tabelas-filhas com PK herdada** (mapeamento "uma tabela por subclasse"); é a abordagem que melhor preserva a integridade e evita duplicação de CPF.
- `CONTRATO` é uma entidade associativa que conecta três entidades (atleta, equipe, temporada), pois tem atributos próprios (salário, datas) e é referenciada por regras de negócio (R3).
- `ARBITRO × PARTIDA` é N:N com atributo `papel` (árbitro principal, bandeirinha, etc.).
