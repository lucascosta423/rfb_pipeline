import os
import zipfile
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from rfb_config import BASE_URL

def get_current_month_folder_url():
    hoje = datetime.now()
    #pasta_ano_mes = hoje.strftime("%Y-%m") + "/"
    pasta_ano_mes = "2025-04/"

    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    for a in soup.find_all('a', href=True):
        if a['href'] == pasta_ano_mes:
            return BASE_URL + a['href']
    return None

def get_zip_links(pasta_url, nameFile):

    response = requests.get(pasta_url)
    soup = BeautifulSoup(response.text, "html.parser")

    return [
        pasta_url + a['href']
        for a in soup.find_all('a', href=True)
        if a['href'].endswith(".zip") and f"{nameFile.capitalize()}" in a['href']
    ]

def download_zip(zip_url, destination_folder):
    filename = os.path.basename(zip_url)
    zip_path = os.path.join(destination_folder, filename)

    print(f"🔽 Baixando: {filename}")
    response = requests.get(zip_url)
    with open(zip_path, "wb") as f:
        f.write(response.content)

    print(f"📦 Extraindo: {filename}")
    extract_zip(zip_path, destination_folder)
    os.remove(zip_path)

def extract_zip(zip_path, destination_folder):
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(destination_folder)

