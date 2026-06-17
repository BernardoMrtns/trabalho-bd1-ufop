# Etapa 1 — Definição do Problema

> Projeto Prático das disciplinas CSI440 / CSI602 — Banco de Dados.

---

## Tabela 1 — Referência para execução da Etapa 1

| Campo | Conteúdo |
|-------|----------|
| **Nome do SBD** | **SportsLeagueDB** — Sistema de Gestão de Liga Esportiva |
| **Desenvolvimento** | (preencher nomes completos e matrícula dos componentes) |
| **Sobre o Projeto** | Sistema desktop para gerenciar uma liga esportiva amadora/profissional: cadastro de equipes, atletas, técnicos, árbitros e estádios; organização de temporadas e campeonatos por modalidade; registro de partidas e dos eventos que ocorrem nelas (gols, cartões, substituições); controle de contratos dos atletas com as equipes por temporada; e geração de consultas como classificação do campeonato, artilharia e histórico de confrontos. |
| **Finalidade** | Centralizar em um único banco relacional todos os dados operacionais da liga, garantindo integridade (regras de negócio via constraints e triggers) e permitindo consulta e relatórios por meio de uma interface gráfica — sem uso de linha de comando. |

---

## Requisitos (Regras de Negócio)

O sistema deve armazenar e respeitar as seguintes regras:

### Entidades principais
1. **Modalidade** (ex.: Futebol, Basquete, Vôlei) — cada modalidade define o número de integrantes e a dinâmica das partidas.
2. **Temporada** — pertence a uma modalidade (ex.: "Futebol 2026"), tem ano, data de início e fim.
3. **Posição** — posições válidas da modalidade (ex.: Goleiro, Zagueiro; Armador; Levantador). Um atleta pode atuar em múltiplas posições.
4. **Equipe** — representa um time (ex.: "Tubarões FC"), tem sigla, cidade e um estádio sede.
5. **Estádio** — local onde ocorrem partidas; tem nome, cidade e capacidade.
6. **Pessoa** (superclasse) — dados comuns (nome, data de nascimento, CPF, nacionalidade). Especializa-se em:
   - **Atleta** — altura, peso, número da camisa opcional.
   - **Árbitro** — categoria (ex.: FIFA, estadual).
   - **Técnico** — registro da federação.
7. **Partida** — ocorre em uma temporada, entre duas equipes (mandante e visitante), em um estádio, em data/hora definidas, com placares de cada lado. Tem status (agendada, em andamento, encerrada, cancelada).
8. **Contrato** — vincula um **atleta** a uma **equipe** durante uma **temporada** específica (entidade associativa com valor de salário e datas). **Um atleta não pode ter dois contratos ativos com equipes diferentes na mesma temporada** (regra via trigger).
9. **Evento de Partida** — registro de algo que ocorre durante a partida, ligado a uma partida e (geralmente) a um atleta e minuto do jogo. Tipos: gol, cartão amarelo, cartão vermelho, substituição (entra/sai).
10. **Inscrição de Temporada** — registra quais equipes participam de uma temporada (relacionamento N:N entre equipe e temporada). **Uma partida só pode envolver equipes inscritas em sua temporada** (regra via trigger).

### Regras de integridade (a serem garantidas no BD)
- R1: O mandante e o visitante de uma partida devem ser equipes **diferentes**.
- R2: Placar (gols) **não pode ser negativo**.
- R3: Um **atleta** não pode ter mais de um contrato **ativo** (data_fim nula ou ≥ hoje) com equipes diferentes na **mesma temporada**.
- R4: As equipes de uma **partida** devem estar **inscritas na temporada** da partida.
- R5: O **estádio** de uma partida deve ser sediado na mesma cidade do mandante **ou** ser o estádio sede de uma das duas equipes (regra flexível da liga).
- R6: **CPF único** entre pessoas (constraint UNIQUE).
- R7: Minuto do evento entre **0 e 130**.
- R8: Nenhum jogador pode registrar dois cartões vermelhos na mesma partida (exemplo de regra de consistência básica).
- R9: Data de início da temporada **anterior** à data de fim.
- R10: Data de nascimento **não superior** à data atual.

### Funcionalidades obrigatórias da interface
- Cadastro (inserção), alteração e remoção de: modalidades, temporadas, posições, estádios, equipes, pessoas (atletas/árbitros/técnicos), contratos, inscrições, partidas e eventos.
- Consultas pré-definidas:
  - **Classificação** do campeonato de uma temporada (pontos, vitórias, empates, derrotas, gols pró/contra, saldo).
  - **Artilharia** (atletas com mais gols em uma temporada).
  - **Cartões** por atleta/equipe.
  - **Histórico de confrontos** entre duas equipes.
  - **Escalação** de uma equipe em uma partida (atletas contratados que têm contrato ativo na temporada).
- Acesso **exclusivamente** pela interface gráfica (sem linha de comando nem pgAdmin para operações do dia a dia).
