from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import os
from db_connector import get_produtos

app = Flask(__name__)
app.secret_key = 'supersecretkey'

CONTATOS_FILE = "contatos.json"

def save_contato_to_file(data):
    if os.path.exists(CONTATOS_FILE):
        with open(CONTATOS_FILE, "r") as file:
            contatos = json.load(file)
    else:
        contatos = []

    contatos.append(data)

    with open(CONTATOS_FILE, "w") as file:
        json.dump(contatos, file, indent=4)

@app.route("/")
def home():
    produtos = get_produtos()
    return render_template("index.html", produtos=produtos)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        mensagem = request.form.get("mensagem")

        contato_data = {
            "nome": nome,
            "email": email,
            "mensagem": mensagem
        }

        save_contato_to_file(contato_data)

        return redirect(url_for("contato_sucesso"))

    return render_template("contato.html")

@app.route("/contato/sucesso")
def contato_sucesso():
    return render_template("contato_sucesso.html")

@app.route("/produtos")
def produtos():
    produtos = get_produtos()
    return render_template("produtos.html", produtos=produtos)

@app.route("/adicionar_carrinho/<int:produto_id>")
def adicionar_carrinho(produto_id):
    produtos = get_produtos()
    produto = next((p for p in produtos if p["id"] == produto_id), None)
    if produto:
        if "carrinho" not in session:
            session["carrinho"] = []
        session["carrinho"].append(produto)
        session.modified = True
    return redirect(url_for("carrinho"))

@app.route("/carrinho")
def carrinho():
    carrinho = session.get("carrinho", [])
    total = sum(item['preco'] for item in carrinho)
    return render_template("carrinho.html", carrinho=carrinho, total=total)

@app.route("/remover_carrinho/<int:produto_id>")
def remover_carrinho(produto_id):
    carrinho = session.get("carrinho", [])
    session["carrinho"] = [item for item in carrinho if item["id"] != produto_id]
    session.modified = True
    return redirect(url_for("carrinho"))

@app.route("/finalizar_compra", methods=["POST"])
def finalizar_compra():
    session["carrinho"] = []
    session.modified = True
    return redirect(url_for("compra_sucesso"))

@app.route("/compra_sucesso")
def compra_sucesso():
    return render_template("compra_sucesso.html")

if __name__ == "__main__":
    app.run(debug=True)
