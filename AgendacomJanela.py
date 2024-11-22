import os
import platform
import mysql.connector
from tkinter import Tk, Button, Label, Frame, Toplevel, Entry, messagebox
from PIL import Image, ImageTk

def conectarBanco():
    """Função para conectar ao banco de dados."""
    try:
        dados_conexao = {
        "user": "root",
        "password": "91649041",
        "host": "127.0.0.1",
        "database": "agenda"
        }
        conexao = mysql.connector.connect(**dados_conexao)
        return conexao
    except mysql.connector.Error as erro:
        # Exibe uma mensagem de erro se não conseguir conectar
        messagebox.showerror("Erro de Conexão", f"Erro ao conectar ao banco de dados: {erro}")
        return None


def menuIniciar():
    global iniciar
    iniciar = Tk()
    iniciar.title("Agenda")
    iniciar.geometry("600x400")
    
    
    
    iniciar.grid_rowconfigure(0, weight=1)  
    iniciar.grid_columnconfigure(0, weight=1)  
    
   
    frame = Frame(iniciar)
    frame.grid(row=0, column=0, sticky="nsew")  
    
    
    frame.grid_rowconfigure(0, weight=1)  
    frame.grid_columnconfigure(0, weight=1)  

   
    Label(frame, text="Seja bem vindo à agenda", font=("Arial", 20)).grid(row=0, column=0, pady=20)
    Button(frame, text="Cadastrar contato", font=("Arial", 12), width=20, command=menuCadastrar).grid(row=1, column=0, pady=10)
    Button(frame, text="Alterar contato", font=("Arial", 12), width=20, command=menuAlterar).grid(row=2, column=0, pady=10)
    Button(frame, text="Deletar contato", font=("Arial", 12), width=20).grid(row=3, column=0, pady=10)
    Button(frame, text="Listar contatos", font=("Arial", 12), width=20).grid(row=4, column=0, pady=10)
    Button(frame, text="Exportar contatos", font=("Arial", 12), width=20).grid(row=5, column=0, pady=10)
    Button(frame, text="Sair", font=("Arial", 12), width=20, command=iniciar.destroy).grid(row=6, column=0, pady=10)
    
    
    
    iniciar.mainloop()

def menuCadastrar():
    janela_cadastrar = Toplevel(iniciar)
    janela_cadastrar.title("Cadastrar contato")
    
    Label(janela_cadastrar, text="Insira os dados do contato:", font=("Arial",16)).grid(row=1, columnspan=3, pady=5)
    Label(janela_cadastrar, text="Nome:", font=("Arial",14)).grid(row=2, columnspan=3, pady=5)
    nomeCadastro = Entry(janela_cadastrar, font=("Arial", 10))
    nomeCadastro.grid(row=3, columnspan=3, pady=2)
    
    Label(janela_cadastrar, text="Telefone", font=("Arial",12)).grid(row=4, columnspan=3, pady=5)
    telefoneCadastro = Entry(janela_cadastrar, font=("Arial", 10))
    telefoneCadastro.grid(row=5, columnspan=3, pady=2)
    
    Label(janela_cadastrar, text="Celular:", font=("Arial",12)).grid(row=6, columnspan=3, pady=5)
    celularCadastro = Entry(janela_cadastrar, font=("Arial", 10))
    celularCadastro.grid(row=7, columnspan=3, pady=2)
       
    def verificaCadastro():
        if nomeCadastro.get() and telefoneCadastro.get() and celularCadastro.get():
            confirma = messagebox.askyesno("Confirma?", f"Dados do contato:\n Nome: {nomeCadastro.get()}, Telefone: {telefoneCadastro.get()}, Celular: {celularCadastro.get()}")
            if confirma:
                try:
                    nome = nomeCadastro.get()
                    telefone = telefoneCadastro.get()
                    celular = celularCadastro.get()

                    
                    conexao = conectarBanco()
                    if conexao is not None:
                        cursor = conexao.cursor()
                        comando_sql = "INSERT INTO contatos (nome, telefone, celular) VALUES (%s, %s, %s)"
                        cursor.execute(comando_sql, (nome, telefone, celular))
                        conexao.commit()
                        
                        cursor.close()
                        conexao.close()
                        
                        messagebox.showinfo("Sucesso", "Contato cadastrado com sucesso!")
                except Exception as erro:
                    messagebox.showerror("Erro", f"Erro ao cadastrar contato: {erro}")  
            else:
                messagebox.showinfo("Cancelado", "Cadastro cancelado.") 
        else:
            messagebox.showwarning("Aviso", "Todos os campos precisam ser preenchidos!")
            
    Button(janela_cadastrar, text="Cadastrar", font=("Arial", 12), command=verificaCadastro).grid(row=9, columnspan=3, pady=15)
    Button(janela_cadastrar, text="Voltar ao menu", font=("Arial", 12), command=janela_cadastrar.destroy).grid(row=10, column=2, pady=15)
    
def menuAlterar():
    janela_alterar = Toplevel(iniciar)
    janela_alterar.title("Alterar contato")
    
    Label(janela_alterar, text="Informe como irá achar o contato", font=("Arial",16)).grid(row=1, columnspan=3, pady=5)
    Button(janela_alterar, text="ID:", font=("Arial",12)).grid(row=2, columnspan=3, pady=5)
    Button(janela_alterar, text="Nome:", font=("Arial",12)).grid(row=3, columnspan=3, pady=5)
    Button(janela_alterar, text="Telefone:", font=("Arial",12)).grid(row=4, columnspan=3, pady=5)
    Button(janela_alterar, text="Celular:", font=("Arial",12)).grid(row=5, columnspan=3, pady=5)
    
    Button(janela_alterar, text="Voltar ao menu", font=("Arial", 12), command=janela_alterar.destroy).grid(row=10, column=2, pady=15)

menuIniciar()
