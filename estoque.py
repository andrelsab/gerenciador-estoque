import sqlite3

class Produto:
    def __init__(self, codigo, nome, categoria, quantidade, preco, localizacao):
        self.codigo = codigo
        self.nome = nome
        self.categoria = categoria
        self.quantidade = quantidade
        self.preco = preco
        self.localizacao = localizacao

class GerenciadorEstoque:
    def __init__(self):
        self.conn = sqlite3.connect('estoque.db', check_same_thread=False)
        self.criar_tabela()

    def criar_tabela(self):
        query = '''
        CREATE TABLE IF NOT EXISTS produtos (
            codigo TEXT PRIMARY KEY,
            nome TEXT,
            categoria TEXT,
            quantidade INTEGER,
            preco REAL,
            localizacao TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def adicionar_produto(self, produto):
        query = '''
        INSERT INTO produtos (codigo, nome, categoria, quantidade, preco, localizacao)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        self.conn.execute(query, (produto.codigo, produto.nome, produto.categoria, 
                                  produto.quantidade, produto.preco, produto.localizacao))
        self.conn.commit()

    def listar_produtos(self):
        query = 'SELECT * FROM produtos'
        cursor = self.conn.execute(query)
        return cursor.fetchall()

    def remover_produto(self, codigo):
        query = 'DELETE FROM produtos WHERE codigo = ?'
        self.conn.execute(query, (codigo,))
        self.conn.commit()
