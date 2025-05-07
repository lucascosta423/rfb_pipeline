import os
from database import get_connection
from downloader import *
from parser import process_csv_and_insert
from concurrent.futures import ThreadPoolExecutor

# Mapeia as extensões para seus respectivos arquivos SQL e número de colunas
EXTENSION_CONFIG = {
    ".ESTABELE": {
        "sql_path": "sql/insertDataEstabelecimentos.sql",
        "columns": 18,
        "fixed_column_indices": [0, 1, 2, 4, 5, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 27]
    },
    ".EMPRECSV": {
        "sql_path": "sql/insertDataEmpresas.sql",
        "columns": 2,
        "fixed_column_indices": [0, 1]
    },
    ".MUNICCSV": {
        "sql_path": "sql/insertDataMunicipios.sql",
        "columns": 2,
        "fixed_column_indices": [0, 1]
    },
    ".SOCIOCSV": {
        "sql_path": "sql/insertDataSocios.sql",
        "columns": 6,
        "fixed_column_indices": [0, 1, 2, 3, 7, 8]
    }
}

nameFile = ["Empresas","Estabelecimentos","Municipios","Socios"]

def run():
    conn = get_connection()
    if not conn:
        print("❌ Conexão com o banco falhou.")
        return

    create_tables(conn)
    truncate_tables(conn)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for name in nameFile:
            futures.append(executor.submit(process_data_type, conn, name, EXTENSION_CONFIG))

        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"⚠️ Erro em uma thread: {e}")

    conn.close()
    print("🔒 Conexão com banco encerrada.")


def process_data_type(conn, name, ext_config):
    pasta_url = get_current_month_folder_url()
    if not pasta_url:
        print(f"❌ URL da pasta do mês não encontrada para {name}")
        return

    zip_links = get_zip_links(pasta_url, name)
    if not zip_links:
        print(f"❌ Nenhum arquivo encontrado para: {name}")
        return

    output_dir = os.path.join("dados_cnpj", name.lower())
    os.makedirs(output_dir, exist_ok=True)

    for zip_url in zip_links:
        try:
            download_zip(zip_url, output_dir)
        except Exception as e:
            print(f"⚠️ Falha ao baixar {zip_url}: {e}")

    for root, _, files in os.walk(output_dir):
        for file in files:
            file_path = os.path.join(root, file)
            for ext, config in ext_config.items():
                if file.endswith(ext):
                    try:
                        print(f"📂 Processando: {file}")
                        process_csv_and_insert(
                            conn=conn,
                            file_path=file_path,
                            sql_file_path=config["sql_path"],
                            expected_columns=config["columns"],
                            fixed_column_indices=config.get("fixed_column_indices"),
                            commit_each_row=True
                        )
                    except Exception as e:
                        print(f"⚠️ Erro ao processar {file}: {e}")
                    finally:
                        os.remove(file_path)
                    break


def truncate_tables(conn):
    try:
        conn.cursor().execute('truncate table empresas,estabelecimentos,municipio,socios')
        conn.commit()
        print(f"✅ Tabelas limpas com sucesso")
    except Exception as e:
        print(f"⚠️ Erro ao trunca tabelas: {e}")

import os

def create_tables(conn, sql_file_path="sql/create_tables.sql"):
    # Garante caminho absoluto com base na localização do script atual
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, sql_file_path)

    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Arquivo SQL não encontrado: {full_path}")

    with open(full_path, "r") as f:
        sql_script = f.read()

    cursor = conn.cursor()

    # Executa múltiplos comandos SQL de uma vez (separados por ";")
    for statement in sql_script.strip().split(";"):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)

    conn.commit()
    print("📐 Tabelas criadas ou já existiam.")
