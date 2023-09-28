import csv
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

# URL da página da web
base_url = 'https://ge.globo.com/futebol/times/sao-paulo/noticia/2023/07/29/sao-paulo-anuncia-a-contratacao-do-meia-james-rodriguez.ghtml'

response = requests.get(base_url)
html_content = response.content

soup = BeautifulSoup(html_content, 'html.parser')

# Encontrar todos os elementos <p> e filtrar aqueles que contêm o texto "futebol"
futebol_paragraphs = [p.get_text().strip() for p in soup.find_all('p') if "futebol" in p.get_text().lower()]

# Salvar dados em um arquivo CSV
csv_filename = "dados.csv"

with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ["texto"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()

    for paragraph in futebol_paragraphs:
        writer.writerow({"texto": paragraph})

# Conexão com o MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['WebScraping']
collection = db['textofutebol']

# Ler dados do arquivo CSV e inserir no MongoDB
with open(csv_filename, 'r', newline='', encoding='utf-8') as csv_file:
     # Criar um leitor de CSV que interpreta cada linha como um dicionário
    csv_reader = csv.DictReader(csv_file)
     # Iterar pelas linhas do arquivo CSV
    for idx, row in enumerate(csv_reader, start=1):
         # Criar um dicionário contendo os dados da linha atual
        data = {
            "id": idx,  # Atribuir um ID único baseado no índice
            "texto": row['texto']  # Extrair o texto da coluna 'texto'
        }
        collection.insert_one(data)
        print(f'Dados {idx} inseridos com sucesso no MongoDB.')

# Fechar a conexão com o MongoDB
client.close()
