import os
import time
import datetime
from runner import run
from downloader import get_current_month_folder_url  # ajuste se o caminho for diferente

LAST_PROCESSED_FILE = "last_processed_month.txt"

def get_current_month_str():
    return datetime.datetime.now().strftime("%Y-%m")

def already_processed_this_month():
    if os.path.exists(LAST_PROCESSED_FILE):
        with open(LAST_PROCESSED_FILE, "r") as f:
            last = f.read().strip()
        return last == get_current_month_str()
    return False

def mark_as_processed():
    with open(LAST_PROCESSED_FILE, "w") as f:
        f.write(get_current_month_str())





def main_loop():
    while True:
        current_month = get_current_month_str()
        print(f"🕒 Verificando dados para o mês: {current_month}")

        if already_processed_this_month():
            print("✅ Dados do mês atual já foram processados. Aguardando próximo mês.")
        else:
            pasta_url = get_current_month_folder_url()
            if pasta_url:
                print(f"📁 Pasta encontrada: {pasta_url}")
                run()
                mark_as_processed()
            else:
                print("❌ Pasta do mês ainda não está disponível. Verificando novamente amanhã.")

        # Dorme por 24h
        time.sleep(60 * 60 * 24)

if __name__ == "__main__":
    main_loop()
