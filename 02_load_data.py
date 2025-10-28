# -*- coding: utf-8 -*-
# O encoding magic comment está no lugar correto!

# --- IMPORTS E CONFIGURACAO ---
import psycopg2
import pandas as pd
import numpy as np

# ATENCAO: SUBSTITUA ESSES VALORES PELOS SEUS DADOS REAIS
DB_HOST = "localhost"
DB_NAME = "biblioteca"
DB_USER = 'Daniel'
DB_PASSWORD = "familia4676"
DB_PORT = "5432"


def connect_db():
    """Tenta estabelecer a conexao com o banco de dados."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST, dbname=DB_NAME, user=DB_USER,
            password=DB_PASSWORD, port=DB_PORT,
            client_encoding='utf8'
        )
        return conn
    except Exception as e:
        print(f"ERRO: Nao foi possivel conectar ao banco de dados: {e}")
        return None


def load_dim_tables(conn):
    """Insere dados para gerar os IDs das tabelas Autor e Status."""

    status_data = [('Pendente',), ('Em Andamento',),
                   ('Lido',), ('Abandonado',)]

    autores_data = [
        ('Cressida Cowell', 'Britanica'),
        ('George R. R. Martin', 'Estadunidense'),
        ('Homero', 'Grega'),
        ('Luiz Fernando Verissimo', 'Brasileira'),
        ('Rupert Matthews', 'Britanica'),
        ('Amy Cuddy', 'Estadunidense'),
        ('Neil Gaiman', 'Britanica'),
        ('Daniel Defoe', 'Inglesa'),
    ]

    cursor = conn.cursor()
    print("--- 1. INSERINDO AUTORES E STATUS PARA GERAR CHAVES ---")

    try:
        # Garante que os status e autores base existam antes de carregar Livros.
        # ON CONFLICT DO NOTHING evita duplicacao no caso de rodar o load_dim_tables mais de uma vez.
        cursor.executemany(
            "INSERT INTO Status_leitores (Nome_do_status) VALUES (%s) ON CONFLICT DO NOTHING;", status_data)
        cursor.executemany(
            "INSERT INTO Autores (Nome_do_autor, Nacionalidade) VALUES (%s, %s) ON CONFLICT DO NOTHING;", autores_data)
        conn.commit()
        print("✅ Insercao/Verificacao de IDs concluida.")
    except Exception as e:
        conn.rollback()
        print(f"ERRO ao inserir/verificar IDs: {e}")
    finally:
        cursor.close()


def preprocess_livros_data(file_path):
    """Lê o CSV, aplica a limpeza (Transformação) e retorna os dados prontos."""
    print("\n--- 2. INICIANDO LIMPEZA (TRANSFORMACAO) DOS DADOS ---")

    try:
        df = pd.read_csv(file_path, sep=',', skipinitialspace=True)

        # TRANSFORMAÇÃO 1: Corrige a capitalização do gênero
        df['genero'] = df['genero'].astype(str).str.strip().str.capitalize()

        # TRANSFORMAÇÃO 2: Renomeia as colunas para o padrão do SQL
        df.rename(columns={
            'autor_id': 'ID_autor',
            'status_id': 'ID_status'
        }, inplace=True)
        
        # LIMPEZA: Converte valores nulos do Pandas (NaN) para None do Python/SQL
        df = df.replace({np.nan: None})

        # SELEÇÃO: Garante a ordem e apenas as colunas necessárias para o INSERT
        df_cleaned = df[[
            'ID_autor', 'ID_status', 'titulo', 'ISBN', 'genero',
            'data_de_publicacao', 'data_aquisicao', 'numero_de_paginas',
            'data_inicio_leitura', 'data_fim_leitura'
        ]]

        print("Transformacao concluida. Dados prontos para a carga.")
        return df_cleaned.values.tolist()

    except Exception as e:
        print(f"ERRO durante a transformacao de dados: {e}")
        return None


def load_data_to_db(conn, data_list):
    """Realiza a Carga (Load) dos dados limpos na tabela Livros."""

    insert_query = """
    INSERT INTO Livros (
        ID_autor, ID_status, titulo, ISBN, genero, data_de_publicacao, data_aquisicao, 
        numero_de_paginas, data_inicio_leitura, data_fim_leitura
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor = conn.cursor()
    print("\n--- 3. CARGA DA TABELA LIVROS ---")

    # A logica de TRUNCATE foi movida para o bloco principal para garantir 
    # que os IDs dos Autores existam no momento da insercao.

    try:
        cursor.executemany(insert_query, data_list)
        conn.commit()
        print(
            f"  ✅ Carga concluida! {len(data_list)} registros inseridos na tabela Livros.")
    except Exception as e:
        conn.rollback()
        print(f"  ❌ ERRO durante a insercao de dados. ROLLBACK executado: {e}")
        print(f"  Detalhe do Erro: {e}")
    finally:
        cursor.close()


# --- BLOCO DE EXECUCAO PRINCIPAL (ETL ORDENADO) ---
if __name__ == "__main__":

    # 1. FAZER A CONEXAO
    connection = connect_db()

    if connection:
        
        # --- ETAPA 1: LIMPEZA PARA EVITAR DUPLICAÇÃO ---
        cursor = connection.cursor()
        print("\n--- INICIANDO LIMPEZA GERAL DE TABELAS ---")
        try:
            # Limpar a tabela Livros (deve ser a primeira por ser dependente)
            cursor.execute("TRUNCATE TABLE Livros RESTART IDENTITY CASCADE;")
            
            # Limpar tabelas dimensionais
            cursor.execute("TRUNCATE TABLE Autores RESTART IDENTITY CASCADE;")
            cursor.execute("TRUNCATE TABLE Status_leitores RESTART IDENTITY CASCADE;")
            
            connection.commit()
            print("✅ Limpeza geral concluída (TRUNCATE).")
        except Exception as e:
            connection.rollback()
            print(f"❌ ERRO ao limpar tabelas: {e}")
            connection.close()
            # Interrompe o script se a limpeza falhar
            exit() 
        finally:
            cursor.close()


        # --- ETAPA 2: CARREGAR DIMENSÕES (CRIAÇÃO DE CHAVES ESTRANGEIRAS) ---
        # Recria os IDs de Autores e Status que acabamos de apagar.
        load_dim_tables(connection) 

        # --- ETAPA 3: CARREGAR FATO (LIVROS) ---
        CSV_FILE_PATH = 'acervo_bruto.csv'

        livros_prontos = preprocess_livros_data(CSV_FILE_PATH)

        if livros_prontos:
            # A carga agora encontra os IDs que foram inseridos na etapa 2.
            load_data_to_db(connection, livros_prontos)

        # 4. FECHAR A CONEXAO
        connection.close()
        print("\nProcesso de ETL finalizado. Conexao com o banco de dados encerrada.")
        