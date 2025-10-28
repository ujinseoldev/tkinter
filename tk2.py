import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

con = sqlite3.connect("pessoas.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS pessoas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    endereco TEXT
)
""")
con.commit()

def salvar_pessoa():
    nome = entrada_nome.get().strip()
    endereco = entrada_endereco.get().strip()

    if nome == "":
        messagebox.showwarning("Atenção", "Digite um nome antes de salvar!")
        return

    if endereco == "":
        messagebox.showwarning("Atenção", "Digite um endereço antes de salvar!")
        return

    cur.execute("INSERT INTO pessoas (nome, endereco) VALUES (?, ?)", (nome, endereco))
    con.commit()

    entrada_nome.delete(0, tk.END)
    entrada_endereco.delete(0, tk.END)

    messagebox.showinfo("Sucesso", f"Pessoa '{nome}' salva com sucesso!")
    atualizar_grade()

def atualizar_grade():
    for item in tabela.get_children():
        tabela.delete(item)

    cur.execute("SELECT id, nome, endereco FROM pessoas ORDER BY id DESC")
    for row in cur.fetchall():
        tabela.insert("", tk.END, values=row)

janela = tk.Tk()
janela.title("Cadastro de Pessoas")
janela.geometry("500x350")

rotulo_nome = tk.Label(janela, text="Digite o nome:")
rotulo_nome.pack(pady=5)

entrada_nome = tk.Entry(janela, width=40)
entrada_nome.pack(pady=5)

rotulo_endereco = tk.Label(janela, text="Digite o endereço:")
rotulo_endereco.pack(pady=5)

entrada_endereco = tk.Entry(janela, width=40)
entrada_endereco.pack(pady=5)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=5)

botao_salvar = tk.Button(frame_botoes, text="Salvar", command=salvar_pessoa)
botao_salvar.grid(row=0, column=0, padx=5)

botao_sair = tk.Button(frame_botoes, text="Fechar", command=janela.destroy)
botao_sair.grid(row=0, column=1, padx=5)

tabela = ttk.Treeview(janela, columns=("id", "nome", "endereco"), show="headings", height=8)
tabela.heading("id", text="ID")
tabela.heading("nome", text="Nome")
tabela.heading("endereco", text="Endereço")

tabela.column("id", width=50, anchor="center")
tabela.column("nome", width=150)
tabela.column("endereco", width=250)

tabela.pack(pady=10, fill="x", padx=10)

atualizar_grade()

janela.mainloop()

con.close()
