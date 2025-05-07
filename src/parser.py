import csv
import os

def read_sql_file(sql_file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, sql_file_path)

    try:
        with open(full_path, 'r', encoding='utf-8') as sql_file:
            return sql_file.read().strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo {full_path} não encontrado. Verifique o caminho.")


def process_csv_and_insert(
    conn,
    file_path,
    sql_file_path,
    expected_columns,
    fixed_column_indices=None,
    commit_each_row=True
):
    """
    Processa um CSV e insere no banco.

    Args:
        conn: conexão com o banco.
        file_path: caminho do CSV.
        sql_file_path: caminho do SQL de inserção.
        expected_columns: número de colunas esperadas.
        fixed_column_indices: lista de índices a extrair da linha (ou None para todas).
        commit_each_row: se True, faz commit linha a linha. Se False, faz ao final.
    """
    insert_sql = read_sql_file(sql_file_path)

    try:
        with conn.cursor() as cur, open(file_path, 'r', encoding='latin1') as f:
            reader = csv.reader((line.replace('\x00', '') for line in f), delimiter=';')

            for i, row in enumerate(reader, 1):
                try:
                    # Seleciona apenas colunas fixas se necessário
                    if fixed_column_indices:
                        row = [row[j] if j < len(row) else '' for j in fixed_column_indices]

                    # Garante o tamanho certo da linha
                    row += [''] * (expected_columns - len(row))
                    row = row[:expected_columns]

                    row = [str(field).replace('\x00', '') for field in row]

                    cur.execute(insert_sql, row)

                    if commit_each_row:
                        conn.commit()

                except Exception as e:
                    print(f"⚠️ Erro na linha {i}: {e} | Dados: {row}")
                    if commit_each_row:
                        conn.rollback()
                    continue

            if not commit_each_row:
                conn.commit()

        print(f"✅ Inserido: {file_path}")

    except Exception as e:
        print(f"❌ Falha no arquivo {file_path}: {e}")
        conn.rollback()
