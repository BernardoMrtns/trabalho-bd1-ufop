# SportsLeagueDB — Projeto Prático de Banco de Dados (CSI440 / CSI602)



Este repositório contém o sistema desktop para gestão de ligas esportivas, desenvolvido como trabalho final da disciplina. O sistema gerencia equipes, atletas, árbitros, técnicos, temporadas, partidas, contratos e eventos de jogo (gols, cartões, substituições). Além disso, gera relatórios automáticos consolidados, como classificação, artilharia e histórico de confrontos.

## 📌 Atendimento aos Requisitos do Enunciado

O projeto foi estruturado com foco em demonstrar o domínio sobre o SGBD, atendendo a todos os critérios exigidos:

* **Acesso ao Banco de Dados (Sem ORM):** O sistema utiliza **SQL puro** através do driver `psycopg2` para Python, sem o uso de ORMs ou APIs que ocultem ou substituam a escrita de comandos SQL.


* **Interface Gráfica:** A interação do usuário ocorre integralmente por meio de uma interface desktop nativa construída com a biblioteca `tkinter`, não dependendo de linhas de comando para sua operação.


* **Entrada e Consulta de Dados:** Todas as operações de CRUD (inserção, edição, exclusão) e visualização de relatórios são realizadas pelas abas da interface desenvolvida.


* **Modelagem (Etapas 1, 2 e 3):** O documento de definição do problema, o Diagrama ER (notação Peter Chen + Mermaid) e o Modelo Lógico estão detalhados na pasta `docs/`.


* **Scripts SQL (Etapa 4):** Toda a definição de DDL (tabelas e restrições), índices, gatilhos, visões e a carga inicial de dados estão sequenciados na pasta `sql/` (`01_schema.sql` a `04_seed.sql`).



## ⚙️ Tecnologias Utilizadas

* **SGBD:** PostgreSQL 15+.


* **Linguagem:** Python 3.11.


* **Interface:** tkinter (GUI nativa).



## 🧠 Destaques da Modelagem de Dados

O banco de dados apresenta construções complexas visando a aplicação prática dos conceitos da disciplina:

* **Herança (Generalização/Especialização):** Implementada na entidade genérica `pessoa`, que se divide em `atleta`, `arbitro` e `tecnico`. A modelagem utiliza uma tabela para cada subclasse, onde a chave primária atua simultaneamente como chave estrangeira para a tabela principal.


* **Entidade Associativa Ternária:** O relacionamento `contrato` envolve `atleta`, `equipe` e `temporada`, armazenando atributos próprios como o salário e o período de vigência.


* **Auto-relacionamento:** A entidade `partida` utiliza um auto-relacionamento com atribuição de papéis para definir a equipe mandante e a equipe visitante.


* **Restrições (CHECK):** Garantem regras de negócio na camada do banco, como placares que não podem ser negativos, equipes mandantes e visitantes que devem ser distintas e minutos de jogo limitados entre 0 e 130.


* **Gatilhos (Triggers):**
* `chk_contrato_atleta_unico`: Regra que impede que um atleta possua contratos simultâneos em equipes diferentes durante a mesma temporada.


* `chk_partida_inscricoes`: Regra que valida se ambas as equipes de uma partida estão devidamente inscritas na temporada correspondente.


* `sync_placar_partida`: Automatiza a atualização do placar final da partida sempre que um novo evento de gol é registrado.




* **Visões (Views):** Responsáveis por consolidar os dados operacionais em relatórios práticos exibidos na interface, como classificação do campeonato, lista de artilheiros, incidência de cartões e elencos.



## 🚀 Como Executar o Sistema (Para Avaliação)

A execução e configuração inicial foram automatizadas para facilitar a correção:

1. **Pré-requisitos:** Certifique-se de ter o **Python 3.10+** e o **PostgreSQL 15+** instalados e em execução.


2. **Configuração de Acesso:** Na raiz do projeto, renomeie o arquivo `.env.example` para `.env` e ajuste as credenciais do PostgreSQL (o usuário configurado deve possuir permissão para executar `CREATE DATABASE`).


3. **Iniciando a Aplicação:**
* **No Windows:** Dê um duplo-clique no arquivo `run.bat`. Este script instalará a dependência do psycopg2 e iniciará o sistema.


* **Manual:** Alternativamente, execute `pip install -r requirements.txt`, navegue até a pasta `src/` e execute `python app.py`.




4. **Criação Automática do Banco:** Ao abrir o sistema pela primeira vez, a barra inferior indicará ausência de conexão. Acesse o menu superior **Banco → (Re)criar banco e popular com dados de exemplo** e confirme.


* Nesta etapa, o sistema criará o banco `sportsleague` automaticamente, executará todos os scripts SQL (tabelas, triggers, views e dados de exemplo) na ordem correta e atualizará a interface.





## 🗂️ Estrutura e Navegação da Interface

As funcionalidades do aplicativo estão separadas em abas lógicas:

* **Cadastros Base e Pessoas:** Inserção e edição de Modalidades, Estádios, Equipes, Atletas, Árbitros e Técnicos.


* **Operações:** Criação de Temporadas, formalização de Inscrições de equipes e gerenciamento de Contratos de atletas.


* **Partidas:** Área dedicada ao registro de jogos e inclusão de eventos ocorridos durante a partida (Gols, Cartões, Substituições).


* **Consultas (Relatórios):** Sub-abas dedicadas à exibição das consultas via Views, incluindo Resumo da temporada, Classificação, Artilharia, Cartões, Confrontos e formação de Elenco.