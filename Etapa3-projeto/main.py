import json
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# URL da página da web
base_url = 'https://ge.globo.com/futebol/times/sao-paulo/noticia/2023/07/29/sao-paulo-anuncia-a-contratacao-do-meia-james-rodriguez.ghtml'

response = requests.get(base_url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar todos os elementos <p> e filtrar aqueles que contêm o texto "futebol"
futebol_paragraphs = [p.get_text().strip() for p in soup.find_all('p') if "futebol" in p.get_text().lower()]

# Salvar dados em um arquivo JSON
json_filename = "dados.json"

with open(json_filename, mode='w', encoding='utf-8') as json_file:
    data = {"textos": futebol_paragraphs}
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Conexão com o MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['WebScrapingJSON']
collection = db['textofutebolJSON']

# Ler dados do arquivo JSON e inserir no MongoDB
with open(json_filename, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    textos = data.get("textos", [])

    for idx, texto in enumerate(textos, start=1):
        data = {
            "id": idx,  # Atribuir um ID único baseado no índice
            "texto": texto  # Extrair o texto da coluna 'texto'
        }
        collection.insert_one(data)
        print(f'Dados {idx} inseridos com sucesso no MongoDB.')

# Fechar a conexão com o MongoDB
client.close()
