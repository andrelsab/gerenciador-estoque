from flask import Flask, render_template, request, redirect, url_for, jsonify
from estoque import GerenciadorEstoque, Produto

app = Flask(__name__)
estoque = GerenciadorEstoque()

@app.route('/')
def index():
    produtos = estoque.listar_produtos()
    return render_template('listar_produtos.html', produtos=produtos)

@app.route('/adicionar', methods=['POST'])
def adicionar_produto():
    codigo = request.form['codigo']
    nome = request.form['nome']
    categoria = request.form['categoria']
    quantidade = int(request.form['quantidade'])
    preco = float(request.form['preco'])
    localizacao = request.form['localizacao']

    novo_produto = Produto(codigo, nome, categoria, quantidade, preco, localizacao)
    estoque.adicionar_produto(novo_produto)
    return redirect(url_for('index'))

@app.route('/remover/<codigo>', methods=['POST'])
def remover_produto(codigo):
    estoque.remover_produto(codigo)
    return redirect(url_for('index'))

@app.route('/api/produtos', methods=['GET'])
def api_listar_produtos():
    produtos = estoque.listar_produtos()
    produtos_json = [produto.__dict__ for produto in produtos]
    return jsonify(produtos_json)

if __name__ == '__main__':
    app.run(debug=True)
