import json

def get_produtos():
    with open("data/produtos.json", "r") as file:
        return json.load(file)

def save_contato(dados):
    with open("data/contatos.json", "a") as file:
        json.dump(dados, file)
        file.write("\n")
