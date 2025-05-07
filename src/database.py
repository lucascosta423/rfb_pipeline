import psycopg2
from rfb_config import PARAMS

def get_connection():
    try:
        conn = psycopg2.connect(**PARAMS)
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None