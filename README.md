# 📚 Pipeline ETL e Análise de Acervo Pessoal (Portfólio de Dados)

## 🎯 Objetivo do Projeto

Este projeto demonstra a criação de um **Pipeline de ETL (Extract, Transform, Load)** de ponta a ponta, partindo de dados brutos de um CSV e transformando-os em uma base relacional (PostgreSQL) para geração de **KPIs (Key Performance Indicators)** sobre hábitos de leitura.

O foco é comprovar o domínio nas etapas de: **Limpeza, Modelagem de Dados, Consulta SQL Avançada, Garantia de Integridade de Dados (TRUNCATE) e Geração de Insights Acionáveis.**

## 🛠️ Stack Tecnológica

| Componente | Tecnologia | Função no Projeto |
| :--- | :--- | :--- |
| **Extração e Transformação** | Python (Pandas) | Leitura do CSV, limpeza de dados (Datas, Strings) e normalização. |
| **Modelagem e Carga (ETL)** | PostgreSQL (psycopg2) | Criação do esquema relacional (DDL) e inserção dos dados limpos (DML) com **regra de não-duplicação (TRUNCATE)**. |
| **Análise de Dados** | SQL | Geração de KPIs e métricas de performance para o acervo. |
| **Controle de Versão** | Git / GitHub | Versionamento e documentação do projeto. |

---

## 📊 Principais Insights de Dados (KPIs)

Os resultados das análises SQL oferecem uma visão clara sobre o volume e a eficiência do acervo, refletindo as **datas corrigidas e otimizadas** no *dataset*.

### 1. KPI: Taxa de Conclusão do Acervo

* **O que informa:** Percentual de livros que atingiram o status 'Lido' em relação ao total do acervo.
* **Ação/Valor:** Mede a eficácia da seleção de leitura.

| total_livros | livros_concluidos | **percentual_conclusao** |
| :--- | :--- | :--- |
| 10 | 3 | **30.0%** |

### 2. Análise de Performance: Tempo Médio de Leitura por Gênero

* **O que informa:** O **Tempo de Ciclo de Leitura**, medindo a média de dias entre a data de início e a data de conclusão de um livro, **incluindo** os períodos de pausa.
* **Ação/Valor:** Permite identificar a demanda de tempo para diferentes tipos de conteúdo.

| genero | **tempo_medio_leitura_dias_arredondado** |
| :--- | :--- |
| Historia em quadrinhos | **40 dias** |
| Classico juvenil | **60 dias** |
| Literatura americana | **71 dias** |
| Cronica brasileira | 86 dias |
| Literatura brasileira | 83 dias |
| Literatura infantojuvenil | 76 dias |
| Roma antiga | 79 dias |
| Relacoes humanas | 85 dias |


### 3. Análise de Prioridade: Top 5 Autores com Livros Pendentes

* **O que informa:** Autores com o maior volume de livros no acervo e quantos deles ainda estão com o status 'Pendente'.
* **Ação/Valor:** Permite priorizar futuras leituras de autores favoritos.

| Nome_do_autor | total_livros_no_acervo | livros_pendentes |
| :--- | :--- | :--- |
| Luiz Fernando Verissimo | **2** | 1 |
| Cressida Cowell | 2 | 1 |
| Amy Cuddy | 1 | 0 |
| Daniel Defoe | 1 | 0 |
| George R. R. Martin | 1 | 0 |

---

## 🤖 Uso de Inteligência Artificial e Resolução de Problemas

O desenvolvimento deste projeto contou com o auxílio de uma **Inteligência Artificial (Gemini, Google)** para acelerar o aprendizado e garantir a qualidade do código através da **resolução de desafios complexos**, como:

* **Integridade de Dados e ETL:** Refatoração do script Python para incluir o comando `TRUNCATE` no fluxo correto, **eliminando a duplicação de dados** e resolvendo o erro de Chave Estrangeira (`FOREIGN KEY`) no PostgreSQL.
* **Data Quality (Outliers):** Identificação e correção de *outliers* na análise de tempo de leitura, garantindo que os KPIs refletissem uma métrica consistente e acionável.
* **Versionamento e Documentação:** Consultoria em Git/GitHub para garantir um *push* e histórico de *commit* limpos e a estruturação do `README.md` com foco em valor (KPIs) para o recrutamento.

---

## 📂 Arquivos do Projeto

- `01_create_biblioteca.sql`: Criação das tabelas (DDL).
- `02_load_data.py`: Script do pipeline ETL (Python/Pandas).
- `03_analysis.sql`: Scripts SQL com as 3 análises.