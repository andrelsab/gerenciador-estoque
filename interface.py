import tkinter as tk
from tkinter import messagebox, ttk
from estoque import Produto, GerenciadorEstoque

class GerenciadorEstoqueApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Gerenciador de Estoque")
        self.master.geometry("700x500")
        
        self.estoque = GerenciadorEstoque()
        
        # Criação do Notebook (abas)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both')
        
        # Abas
        self.tab_adicionar = tk.Frame(self.notebook)
        self.tab_listar = tk.Frame(self.notebook)
        
        self.notebook.add(self.tab_adicionar, text="Adicionar Produto")
        self.notebook.add(self.tab_listar, text="Listar Produtos")
        
        # Aba Adicionar Produto
        form_frame = ttk.Frame(self.tab_adicionar, padding=20)
        form_frame.pack(fill='both', expand=True)
        
        # Campos de entrada para Adicionar Produto
        ttk.Label(form_frame, text="Código:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.codigo_entry = ttk.Entry(form_frame, width=30)
        self.codigo_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(form_frame, text="Nome:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.nome_entry = ttk.Entry(form_frame, width=30)
        self.nome_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(form_frame, text="Categoria:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.categoria_entry = ttk.Entry(form_frame, width=30)
        self.categoria_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(form_frame, text="Quantidade:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.quantidade_entry = ttk.Entry(form_frame, width=30)
        self.quantidade_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(form_frame, text="Preço:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.preco_entry = ttk.Entry(form_frame, width=30)
        self.preco_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Label(form_frame, text="Localização:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.localizacao_entry = ttk.Entry(form_frame, width=30)
        self.localizacao_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Separator(form_frame, orient="horizontal").grid(row=6, columnspan=2, sticky="ew", pady=10)
        ttk.Button(form_frame, text="Adicionar Produto", command=self.adicionar_produto).grid(row=7, columnspan=2, pady=10)
        
        # Aba Listar Produtos com Treeview e botão de remoção
        ttk.Button(self.tab_listar, text="Atualizar Lista", command=self.listar_produtos).pack(pady=10)
        self.btn_remover_selecionado = ttk.Button(self.tab_listar, text="Remover Produto", command=self.remover_produto_selecionado)
        self.btn_remover_selecionado.pack(pady=5)

        # Configuração da tabela Treeview
        self.tree = ttk.Treeview(self.tab_listar, columns=("Código", "Nome", "Categoria", "Quantidade", "Preço", "Localização"), show="headings")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Categoria", text="Categoria")
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.heading("Preço", text="Preço")
        self.tree.heading("Localização", text="Localização")
        
        # Ajuste de colunas
        self.tree.column("Código", width=50, anchor="center")
        self.tree.column("Nome", width=200, anchor="w")
        self.tree.column("Categoria", width=70, anchor="center")
        self.tree.column("Quantidade", width=60, anchor="center")
        self.tree.column("Preço", width=70, anchor="center")
        self.tree.column("Localização", width=60, anchor="center")
        
        # Barras de rolagem e exibição do Treeview
        self.tree_scroll = ttk.Scrollbar(self.tab_listar, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree_scroll.pack(side="right", fill="y")

    def adicionar_produto(self):
        try:
            codigo = self.codigo_entry.get()
            nome = self.nome_entry.get()
            categoria = self.categoria_entry.get()
            quantidade = int(self.quantidade_entry.get())
            preco = float(self.preco_entry.get())
            localizacao = self.localizacao_entry.get()
            produto = Produto(codigo, nome, categoria, quantidade, preco, localizacao)
            self.estoque.adicionar_produto(produto)
            messagebox.showinfo("Sucesso", f"Produto {nome} adicionado com sucesso.")
            self.limpar_campos()
            self.listar_produtos()
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def listar_produtos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        produtos = self.estoque.listar_produtos()
        for produto in produtos:
            self.tree.insert("", "end", values=produto)

    def remover_produto_selecionado(self):
        selected_item = self.tree.selection()
        if selected_item:
            produto = self.tree.item(selected_item)["values"]
            codigo = produto[0]  # Código do produto é o primeiro valor na linha selecionada
            self.estoque.remover_produto(codigo)
            messagebox.showinfo("Sucesso", f"Produto com código {codigo} removido com sucesso.")
            self.listar_produtos()
        else:
            messagebox.showwarning("Atenção", "Selecione um produto para remover.")
    
    def limpar_campos(self):
        self.codigo_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.categoria_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.localizacao_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = GerenciadorEstoqueApp(root)
    root.mainloop()
