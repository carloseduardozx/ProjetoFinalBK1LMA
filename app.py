from flask import Flask, render_template

app = Flask(__name__)

def load_produtos():
    try:
        with open('data/produtos.txt', 'r') as f:
            produtos = [linha.strip() for linha in f.readlines()]
    except FileNotFoundError:
        produtos = ["Produto 1", "Produto 2", "Produto 3"]  # Dados de exemplo
    return produtos

@app.route('/')
def index():
    produtos = load_produtos()
    return render_template('index.html', produtos=produtos)

# Nova rota para a página de menu
@app.route('/menu')
def menu():
    return render_template('menu.html')

if __name__ == '__main__':
    app.run(debug=True)
