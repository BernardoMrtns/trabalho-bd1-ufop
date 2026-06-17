# SportsLeagueDB — Sistema de Gestão de Liga Esportiva

Projeto Prático das disciplinas **CSI440 / CSI602** (Banco de Dados).

Sistema desktop para gerenciar uma liga esportiva: equipes, atletas, árbitros,
técnicos, temporadas, partidas, contratos e eventos (gols, cartões,
substituições) — com geração de classificação, artilharia, cartões e confrontos.

- **SGBD:** PostgreSQL 15+
- **Linguagem:** Python 3.11
- **Interface:** tkinter (GUI desktop nativa)
- **Acesso ao BD:** **SQL puro** via driver `psycopg2` — **sem ORM**, conforme exigido pelo enunciado.

---

## 📐 Conformidade com o enunciado

| Exigência do enunciado | Como é atendida |
|------------------------|-----------------|
| Acesso via interface (não por linha de comando) | GUI tkinter (`src/gui/`). |
| Sem ORM / APIs que substituam SQL | Só o driver `psycopg2`; todo SQL é escrito à mão em `src/db.py` e `src/repositories.py`. |
| Entrada/inserção de dados pela interface | Abas de cadastro (CRUD completo). |
| Consulta aos dados pela interface | Aba **Consultas** (classificação, artilharia, cartões, confrontos, elenco). |
| Modelo conceitual (ER) | `docs/02_diagrama_er.md` (Peter Chen + Mermaid). |
| Modelo lógico | `docs/03_modelo_logico.md`. |
| Scripts SQL de criação e povoamento | `sql/01_schema.sql`, `02_indexes_triggers.sql`, `03_views.sql`, `04_seed.sql`. |

---

## 🗂️ Estrutura do projeto

```
SportsLeagueDB/
├── README.md                  ← este arquivo
├── requirements.txt           ← dependências (só psycopg2-binary)
├── .env.example               ← modelo de configuração de conexão
├── .gitignore
├── run.bat                    ← inicializador para Windows
├── docs/
│   ├── 01_definicao_do_problema.md   ← Etapa 1
│   ├── 02_diagrama_er.md             ← Etapa 2
│   └── 03_modelo_logico.md           ← Etapa 3
├── sql/
│   ├── 01_schema.sql          ← DDL: tabelas + constraints (Etapa 4)
│   ├── 02_indexes_triggers.sql← índices + triggers de regras de negócio
│   ├── 03_views.sql           ← views de classificação/artilharia/etc.
│   └── 04_seed.sql            ← dados de exemplo
└── src/
    ├── app.py                 ← ponto de entrada (python app.py)
    ├── config.py              ← leitura de .env / variáveis de ambiente
    ├── db.py                  ← camada de conexão (SQL puro)
    ├── repositories.py        ← funções SQL por entidade/consulta
    └── gui/
        ├── __init__.py
        ├── main.py            ← janela principal + menu
        ├── widgets.py         ← Tabela, Formulario, diálogos
        ├── crud.py            ← CrudFrame reutilizável
        ├── util.py            ← conversões de tipo
        ├── abas_cadastros.py  ← Modalidade, Posição, Estádio, Equipe
        ├── abas_operacionais.py← Temporada, Atletas, Árbitros, Técnicos, Inscrição, Contrato
        ├── aba_partidas.py    ← Partidas + Eventos
        └── aba_consultas.py   ← Relatórios (classificação, artilharia, ...)
```

---

## 🚀 Como executar

### 1. Pré-requisitos
- **PostgreSQL 15+** instalado e em execução.
- **Python 3.10+** (testado no 3.11.9).

### 2. Configurar a conexão
Copie `.env.example` para `.env` (na raiz do projeto) e ajuste:

```env
PGHOST=localhost
PGPORT=5432
PGUSER=postgres
PGPASSWORD=sua_senha
PGDATABASE=sportsleague
```

> O usuário precisa ter permissão para `CREATE DATABASE`. O superusuário
> `postgres` tem por padrão.

### 3. Instalar dependências e rodar

**Windows (recomendado):** dê duplo-clique em `run.bat`, ou no Prompt:

```cmd
cd SportsLeagueDB
run.bat
```

**Manual (qualquer SO):**

```bash
pip install -r requirements.txt
cd src
python app.py
```

### 4. Criar o banco e popular com dados de exemplo
Ao abrir o sistema pela primeira vez, a barra de status mostrará "Sem conexão".
No menu **Banco → (Re)criar banco e popular com dados de exemplo**, confirme.
O sistema:
1. Cria (ou recria) o banco `sportsleague`;
2. Executa os scripts `01..04` em ordem;
3. Recarrega todas as abas.

> Alternativa por linha de comando (apenas para setup — não para uso do sistema):
> ```bash
> psql -U postgres -f sql/01_schema.sql -d sportsleague
> psql -U postgres -f sql/02_indexes_triggers.sql -d sportsleague
> psql -U postgres -f sql/03_views.sql -d sportsleague
> psql -U postgres -f sql/04_seed.sql -d sportsleague
> ```

---

## 🧩 Modelagem — destaques

O esquema foi desenhado para **não ser "muito simples"**, exibindo várias
construções ricas:

- **Generalização/especialização (herança):** `pessoa` → `atleta` / `arbitro` / `tecnico`,
  mapeada como *uma tabela por subclasse* (PK da subclasse = FK para a mãe).
- **Relacionamento N:N com atributo:** `partida_arbitro` (papel do árbitro),
  `atleta_posicao`.
- **Entidade associativa ternária:** `contrato` (atleta × equipe × temporada),
  com atributos próprios (salário, datas).
- **Auto-relacionamento com papel:** `partida` (mandante × visitante).
- **Regras de negócio via CHECK constraints:** placar ≥ 0, mandante ≠ visitante,
  data_fim > data_inicio, minuto entre 0 e 130, substituição exige 2º atleta, etc.
- **Triggers:**
  - `chk_contrato_atleta_unico` — atleta não pode ter dois contratos ativos com
    equipes diferentes na mesma temporada (R3).
  - `chk_partida_inscricoes` — as equipes da partida devem estar inscritas na
    temporada (R4).
  - `sync_placar_partida` — recalcula o placar da partida a partir dos eventos
    de GOL.
- **Views:** classificação, artilharia, cartões, confrontos, elenco, partidas
  detalhadas, resumo da temporada.

---

## 🖥️ Usando o sistema

A interface é organizada em grupos de abas:

1. **Cadastros** — Modalidades, Posições, Estádios, Equipes.
2. **Pessoas** — Atletas, Árbitros, Técnicos.
3. **Operações** — Temporadas, Inscrições (equipe × temporada), Contratos.
4. **Partidas** — cadastro de partidas e registro de eventos; ao selecionar uma
   partida, os eventos aparecem abaixo.
5. **Consultas** — relatórios em sub-abas:
   - **Resumo** geral das temporadas;
   - **Classificação** do campeonato;
   - **Artilharia**;
   - **Cartões**;
   - **Confrontos** entre duas equipes;
   - **Elenco** de uma equipe numa temporada.

Cada CRUD tem botões **Novo / Editar / Excluir / Atualizar**. As tabelas
permitem ordenar clicando no cabeçalho e editar com duplo-clique.

---

## 🎥 Roteiro para a apresentação/vídeo (≤ 15 min)

1. **Problema (1–2 min):** o que é o SportsLeagueDB e por que é útil
   (ver `docs/01_definicao_do_problema.md`).
2. **Modelagem (4–5 min):**
   - Mostre o diagrama ER (`docs/02_diagrama_er.md`) — destaque a generalização
     `pessoa`, o contrato ternário e o auto-relacionamento partida.
   - Mostre o modelo lógico (`docs/03_modelo_logico.md`) e explique as
     decisões (tabela por subclasse, desnormalizações).
3. **Decisões de projeto (2 min):** regras de negócio via CHECK e triggers,
   views de relatório, por que SQL puro (conforme enunciado).
4. **Demonstração (5–6 min):**
   - Bootstrap do banco pelo menu.
   - Cadastre uma equipe/atleta/contrato (mostre a trigger R3 rejeitando um
     contrato duplicado do mesmo atleta com outra equipe).
   - Tente cadastrar uma partida com equipes não inscritas (mostre a trigger R4).
   - Registre gols e veja o placar ser atualizado e a classificação mudar.
   - Mostre Artilharia, Cartões e Confrontos.
5. **Conclusão (1 min):** conformidade com o enunciado e possíveis extensões.

---

## ⚠️ Observações

- O bootstrap **apaga e recria** o banco. Em uso real, faça backup antes.
- A extensão `pg_trgm` (busca aproximada) é opcional; se o usuário não tiver
  privilégio, o sistema continua funcionando (consultas usam `ILIKE`/igualdade).
- O `cpf` é `CHAR(11)` sem formatação — digite somente números.
