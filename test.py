import json

# Caminho do arquivo JSON
arquivo_json = "C:\\Users\\herci\\Documents\\Projetos Python\\cred.json"

# Abrir o arquivo JSON e converter para string
with open(arquivo_json, 'r') as f:
    dados_json = f.read()

# Agora a variável 'dados_json' é uma string contendo o conteúdo do JSON
print(dados_json)
