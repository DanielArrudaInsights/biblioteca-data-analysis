# 📚 Pipeline ETL e Análise de Acervo Pessoal (Portfólio de Dados)

## 🎯 Objetivo do Projeto

Este projeto demonstra a criação de um **Pipeline de ETL (Extract, Transform, Load)** de ponta a ponta, partindo de dados brutos de um CSV e transformando-os em uma base relacional (PostgreSQL) para geração de KPIs (Key Performance Indicators) sobre hábitos de leitura.

O foco é comprovar o domínio nas etapas de: **Limpeza, Modelagem de Dados, Consulta SQL Avançada e Geração de Insights Acionáveis.**

## 🛠️ Stack Tecnológica

| Componente | Tecnologia | Função no Projeto |
| :--- | :--- | :--- |
| **Extração e Transformação** | Python (Pandas) | Leitura do CSV, limpeza de dados (Datas, Strings) e normalização. |
| **Modelagem e Carga (ETL)** | PostgreSQL (psycopg2) | Criação do esquema relacional (DDL) e inserção dos dados limpos (DML). |
| **Análise de Dados** | SQL | Geração de KPIs e métricas de performance para o acervo. |
| **Controle de Versão** | Git / GitHub | Versionamento e documentação do projeto. |

---

## 📊 Principais Insights de Dados (KPIs)

Os resultados das análises SQL oferecem uma visão clara sobre o volume e a eficiência do acervo:

### 1. KPI: Taxa de Conclusão do Acervo

* **O que informa:** Percentual de sucesso na conclusão dos livros iniciados.
* **Ação/Valor:** Ajuda a medir a eficácia da seleção de leitura.

| total_livros | livros_concluidos | percentual_conclusao |
| :--- | :--- | :--- |
| 10 | 3 | 30.0% |

### 2. Análise de Performance: Tempo Médio de Leitura por Gênero

* **O que informa:** A média de dias gastos para concluir livros de cada gênero.
* **Ação/Valor:** Permite identificar a demanda de tempo para diferentes tipos de conteúdo, auxiliando no planejamento.

| genero | tempo_medio_leitura_dias_arredondado |
| :--- | :--- |
| Classico juvenil | 102 dias |
| Cronica brasileira | 110 dias |
| Literatura infantojuvenil | 131 dias |
| Literatura brasileira | 138 dias |
| Literatura americana | 195 dias |
| Historia em quadrinhos | 285 dias |

---

### 3. Análise de Prioridade: Top 5 Autores com Livros Pendentes

* **O que informa:** Autores com o maior volume de livros no acervo e quantos deles ainda estão com o status 'Pendente' (na lista de espera).
* **Ação/Valor:** Permite priorizar compras ou iniciar leituras de autores favoritos.

| Nome_do_autor | total_livros_no_acervo | livros_pendentes |
| :--- | :--- | :--- |
| Luiz Fernando Verissimo | 2 | 1 |
| Cressida Cowell | 2 | 1 |
| Amy Cuddy | 1 | 0 |
| Daniel Defoe | 1 | 0 |
| George R. R. Martin | 1 | 0 |

---

## 📂 Arquivos do Projeto

- `01_create_biblioteca.sql`: Criação das tabelas (DDL).
- `02_load_data.py`: Script do pipeline ETL (Python/Pandas).
- `03_analysis.sql`: Scripts SQL com as 3 análises.