import os
from dotenv import load_dotenv

load_dotenv()


try:
    BASE_URL = os.getenv("BASE_URL")
    PARAMS = {
        "user": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT"),
    }
except Exception as e:
    print(f"❌ Erro ao carregar as variaveis de ambiente: {e}")
