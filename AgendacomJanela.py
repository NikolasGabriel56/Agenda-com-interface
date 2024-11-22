import os
import platform
import mysql.connector
from tkinter import Tk, Button, Label, Frame, Toplevel, Entry
from PIL import Image, ImageTk


agenda = {
    "user": "SEU USUARIO",  #informe seu usuário do DATABASE
    "password": "SUA SENHA", #informe sua senha do DATABASE
    "host": "127.0.0.1",
    "database": "SEU DATABASE" #informe seu DATABASE
}

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
    Button(frame, text="Alterar contato", font=("Arial", 12), width=20).grid(row=2, column=0, pady=10)
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
    
    Button(janela_cadastrar, text="Cadastrar", font=("Arial", 12)).grid(row=9, columnspan=3, pady=15)
    Button(janela_cadastrar, text="Voltar ao menu iniciar", font=("Arial", 12)).grid(row=10, column=2, pady=15)
    
    

menuIniciar()
