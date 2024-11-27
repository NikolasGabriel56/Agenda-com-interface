import os
import platform
import mysql.connector
from tkinter import *
from tkinter import messagebox

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
    iniciar.iconbitmap(r"C:\\Python\\Estudo\\Agenda com interface grafica\\images\\newpy.ico")
    
    
    
    iniciar.grid_rowconfigure(0, weight=1)  
    iniciar.grid_columnconfigure(0, weight=1)  
    
   
    frame = Frame(iniciar)
    frame.grid(row=0, column=0, sticky="nsew")  
    
    
    frame.grid_rowconfigure(0, weight=1)  
    frame.grid_columnconfigure(0, weight=1)  

   
    Label(frame, text="Seja bem vindo à agenda", font=("Arial", 20)).grid(row=0, column=0, pady=20)
    Button(frame, text="Cadastrar contato", font=("Arial", 12), width=20, command=menuCadastrar).grid(row=1, column=0, pady=10)
    Button(frame, text="Alterar contato", font=("Arial", 12), width=20, command=menuAlterar).grid(row=2, column=0, pady=10)
    Button(frame, text="Deletar contato", font=("Arial", 12), width=20, command=menuDeletar).grid(row=3, column=0, pady=10)
    Button(frame, text="Listar contatos", font=("Arial", 12), width=20).grid(row=4, column=0, pady=10)
    Button(frame, text="Exportar contatos", font=("Arial", 12), width=20).grid(row=5, column=0, pady=10)
    Button(frame, text="Sair", font=("Arial", 12), width=20, command=iniciar.destroy).grid(row=6, column=0, pady=10)
    
    
    
    iniciar.mainloop()

def menuCadastrar():
    janela_cadastrar = Toplevel(iniciar)
    janela_cadastrar.title("Cadastrar contato")
    janela_cadastrar.iconbitmap(r"C:\\Python\\Estudo\\Agenda com interface grafica\\images\\newpy.ico")
    
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
    # Criação da janela principal para alterar contato
    janela_alterar = Toplevel()
    janela_alterar.title("Alterar contato")
    janela_alterar.geometry("500x500")  # Ajuste de tamanho para garantir espaço
    janela_alterar.iconbitmap(r"C:\\Python\\Estudo\\Agenda com interface grafica\\images\\newpy.ico")

    # Mensagem inicial
    Label(janela_alterar, text="Informe como irá achar o contato", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

    # Campo e botão para buscar por ID
    Label(janela_alterar, text="ID:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=E)
    entrada_id = Entry(janela_alterar, font=("Arial", 12))
    entrada_id.grid(row=1, column=1, pady=5)
    Button(janela_alterar, text="Buscar ID", font=("Arial", 12), command=lambda: buscarContato(janela_alterar, 'ID', entrada_id.get())).grid(row=1, column=2, pady=5, padx=5)

    # Campo e botão para buscar por Nome
    Label(janela_alterar, text="Nome:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky=E)
    entrada_nome = Entry(janela_alterar, font=("Arial", 12))
    entrada_nome.grid(row=2, column=1, pady=5)
    Button(janela_alterar, text="Buscar Nome", font=("Arial", 12), command=lambda: buscarContato(janela_alterar, 'Nome', entrada_nome.get())).grid(row=2, column=2, pady=5, padx=5)

    # Campo e botão para buscar por Telefone
    Label(janela_alterar, text="Telefone:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky=E)
    entrada_telefone = Entry(janela_alterar, font=("Arial", 12))
    entrada_telefone.grid(row=3, column=1, pady=5)
    Button(janela_alterar, text="Buscar Telefone", font=("Arial", 12), command=lambda: buscarContato(janela_alterar, 'Telefone', entrada_telefone.get())).grid(row=3, column=2, pady=5, padx=5)

    # Campo e botão para buscar por Celular
    Label(janela_alterar, text="Celular:", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5, sticky=E)
    entrada_celular = Entry(janela_alterar, font=("Arial", 12))
    entrada_celular.grid(row=4, column=1, pady=5)
    Button(janela_alterar, text="Buscar Celular", font=("Arial", 12), command=lambda: buscarContato(janela_alterar, 'Celular', entrada_celular.get())).grid(row=4, column=2, pady=5, padx=5)

    # Botão para voltar ao menu principal
    Button(janela_alterar, text="Voltar ao menu", font=("Arial", 12), command=janela_alterar.destroy).grid(row=5, column=1, pady=20)

def menuDeletar():
    janela_deletar = Tk()
    janela_deletar.title("Deletar contato")
    janela_deletar.geometry("500x300")
    janela_deletar.iconbitmap(r"C:\\Python\\Estudo\\Agenda com interface grafica\\images\\newpy.ico")
    
    # Mensagem inicial
    Label(janela_deletar, text="Informe como irá achar o contato", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

    # Campo e botão para buscar por ID
    Label(janela_deletar, text="ID:", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=E)
    entrada_id = Entry(janela_deletar, font=("Arial", 12))
    entrada_id.grid(row=1, column=1, pady=5)
    Button(janela_deletar, text="Buscar ID", font=("Arial", 12), command=lambda: buscarContatoDel(janela_deletar, 'ID', entrada_id.get())).grid(row=1, column=2, pady=5, padx=5)

    # Campo e botão para buscar por Nome
    Label(janela_deletar, text="Nome:", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky=E)
    entrada_nome = Entry(janela_deletar, font=("Arial", 12))
    entrada_nome.grid(row=2, column=1, pady=5)
    Button(janela_deletar, text="Buscar Nome", font=("Arial", 12), command=lambda: buscarContatoDel(janela_deletar, 'Nome', entrada_nome.get())).grid(row=2, column=2, pady=5, padx=5)

    # Campo e botão para buscar por Telefone
    Label(janela_deletar, text="Telefone:", font=("Arial", 12)).grid(row=3, column=0, padx=5, pady=5, sticky=E)
    entrada_telefone = Entry(janela_deletar, font=("Arial", 12))
    entrada_telefone.grid(row=3, column=1, pady=5)
    Button(janela_deletar, text="Buscar Telefone", font=("Arial", 12), command=lambda: buscarContatoDel(janela_deletar, 'Telefone', entrada_telefone.get())).grid(row=3, column=2, pady=5, padx=5)

    # Campo e botão para buscar por Celular
    Label(janela_deletar, text="Celular:", font=("Arial", 12)).grid(row=4, column=0, padx=5, pady=5, sticky=E)
    entrada_celular = Entry(janela_deletar, font=("Arial", 12))
    entrada_celular.grid(row=4, column=1, pady=5)
    Button(janela_deletar, text="Buscar Celular", font=("Arial", 12), command=lambda: buscarContatoDel(janela_deletar, 'Celular', entrada_celular.get())).grid(row=4, column=2, pady=5, padx=5)

    # Botão para voltar ao menu principal
    Button(janela_deletar, text="Voltar ao menu", font=("Arial", 12), command=janela_deletar.destroy).grid(row=5, column=1, pady=20)

def buscarContato(janela, tipo_busca, valor_busca):
    conexao = conectarBanco()
    if conexao is None:
        return

    cursor = conexao.cursor(dictionary=True)
    try:
        # Montando a consulta SQL com base no tipo de busca
        if tipo_busca == 'ID':
            sql = "SELECT * FROM contatos WHERE id = %s"
        elif tipo_busca == 'Nome':
            sql = "SELECT * FROM contatos WHERE nome LIKE %s"
            valor_busca = f"%{valor_busca}%"  # Para buscar por similaridade
        elif tipo_busca == 'Telefone':
            sql = "SELECT * FROM contatos WHERE telefone = %s"
        elif tipo_busca == 'Celular':
            sql = "SELECT * FROM contatos WHERE celular = %s"

        cursor.execute(sql, (valor_busca,))
        contato = cursor.fetchone()

        if contato:
            # Exibir os campos para editar o contato na mesma janela
            Label(janela, text="Nome:", font=("Arial", 14)).grid(row=6, column=0, pady=5, sticky=E)
            entrada_nome = Entry(janela, font=("Arial", 14))
            entrada_nome.grid(row=6, column=1, pady=5)
            entrada_nome.insert(0, contato['nome'])
            
            Label(janela, text="Telefone:", font=("Arial", 14)).grid(row=7, column=0, pady=5, sticky=E)
            entrada_telefone = Entry(janela, font=("Arial", 14))
            entrada_telefone.grid(row=7, column=1, pady=5)
            entrada_telefone.insert(0, contato['telefone'])
            
            Label(janela, text="Celular:", font=("Arial", 14)).grid(row=8, column=0, pady=5, sticky=E)
            entrada_celular = Entry(janela, font=("Arial", 14))
            entrada_celular.grid(row=8, column=1, pady=5)
            entrada_celular.insert(0, contato['celular'])

            # Botão para salvar as alterações
            Button(janela, text="Salvar Alterações", font=("Arial", 12),
                   command=lambda: salvarAlteracoes(contato['id'], entrada_nome.get(), entrada_telefone.get(), entrada_celular.get(), conexao, janela)).grid(row=9, column=1, pady=10)
        else:
            messagebox.showinfo("Contato não encontrado", "Nenhum contato encontrado com esse valor.")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro ao buscar contato", f"Erro ao buscar contato: {erro}")
    finally:
        cursor.close()

def salvarAlteracoes(id_contato, nome, telefone, celular, conexao, janela):
    cursor = conexao.cursor()
    try:
        sql = "UPDATE contatos SET nome = %s, telefone = %s, celular = %s WHERE id = %s"
        cursor.execute(sql, (nome, telefone, celular, id_contato))
        conexao.commit()

        messagebox.showinfo("Sucesso", "Contato alterado com sucesso!")
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro ao salvar alterações", f"Erro ao salvar alterações: {erro}")
    finally:
        cursor.close()
        conexao.close()

def buscarContatoDel(janela, tipo_busca, valor_busca):
    janela_busca = Toplevel()
    janela_busca.title("Deletar contato")
    janela_busca.geometry("400x200")  # Ajuste de tamanho para garantir espaço
    janela_busca.iconbitmap(r"C:\\Python\\Estudo\\Agenda com interface grafica\\images\\newpy.ico")
    
    conexao = conectarBanco()
    if conexao is None:
        return

    cursor = conexao.cursor(dictionary=True)
    try:
        # Montando a consulta SQL com base no tipo de busca
        if tipo_busca == 'ID':
            sql = "SELECT * FROM contatos WHERE id = %s"
        elif tipo_busca == 'Nome':
            sql = "SELECT * FROM contatos WHERE nome LIKE %s"
            valor_busca = f"%{valor_busca}%"  # Para buscar por similaridade
        elif tipo_busca == 'Telefone':
            sql = "SELECT * FROM contatos WHERE telefone = %s"
        elif tipo_busca == 'Celular':
            sql = "SELECT * FROM contatos WHERE celular = %s"

        cursor.execute(sql, (valor_busca,))
        contato = cursor.fetchone()

        if contato:
            # Exibir os campos para visualizar o contato antes da exclusão
            Label(janela_busca, text="Nome:", font=("Arial", 14)).grid(row=6, column=0, pady=5, sticky=E)
            entrada_nome = Entry(janela_busca, font=("Arial", 14))
            entrada_nome.grid(row=6, column=1, pady=5)
            if contato['nome']:
                entrada_nome.insert(0, contato['nome'])
            entrada_nome.config(state='disabled')
            
            Label(janela_busca, text="Telefone:", font=("Arial", 14)).grid(row=7, column=0, pady=5, sticky=E)
            entrada_telefone = Entry(janela_busca, font=("Arial", 14))
            entrada_telefone.grid(row=7, column=1, pady=5)
            if contato['telefone']:
                entrada_telefone.insert(0, contato['telefone'])
            entrada_telefone.config(state='disabled')
            
            Label(janela_busca, text="Celular:", font=("Arial", 14)).grid(row=8, column=0, pady=5, sticky=E)
            entrada_celular = Entry(janela_busca, font=("Arial", 14))
            entrada_celular.grid(row=8, column=1, pady=5)
            if contato['celular']:
                entrada_celular.insert(0, contato['celular'])
            entrada_celular.config(state='disabled')

            # Botão para confirmar a exclusão do contato
            botao_deletar = Button(janela_busca, text="Deletar", font=("Arial", 12),
                                   command=lambda: deletarContato(janela, tipo_busca, valor_busca))
            botao_deletar.grid(row=9, column=1, pady=10)

        else:
            messagebox.showinfo("Contato não encontrado", "Nenhum contato encontrado com esse valor.")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro ao buscar contato", f"Erro ao buscar contato: {erro}")
    finally:
        cursor.close()
        conexao.close()

def deletarContato(janela, tipo_busca, valor_busca):
    conexao = conectarBanco()
    if conexao is None:
        return

    cursor = conexao.cursor(dictionary=True)
    try:
        # Montando a consulta SQL com base no tipo de busca
        if tipo_busca == 'ID':
            sql = "SELECT * FROM contatos WHERE id = %s"
        elif tipo_busca == 'Nome':
            sql = "SELECT * FROM contatos WHERE nome LIKE %s"
            valor_busca = f"%{valor_busca}%"  # Para buscar por similaridade
        elif tipo_busca == 'Telefone':
            sql = "SELECT * FROM contatos WHERE telefone = %s"
        elif tipo_busca == 'Celular':
            sql = "SELECT * FROM contatos WHERE celular = %s"

        cursor.execute(sql, (valor_busca,))
        contato = cursor.fetchone()

        if contato:
            # Confirmar exclusão do contato
            confirmacao = messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este contato?")
            if confirmacao:
                delete_sql = "DELETE FROM contatos WHERE id = %s"
                cursor.execute(delete_sql, (contato['id'],))
                conexao.commit()
                messagebox.showinfo("Sucesso", "Contato deletado com sucesso!")
                janela.destroy()  # Fecha a janela após a exclusão
        else:
            messagebox.showinfo("Contato não encontrado", "Nenhum contato encontrado com esse valor.")

    except mysql.connector.Error as erro:
        messagebox.showerror("Erro ao deletar contato", f"Erro ao deletar contato: {erro}")
    finally:
        cursor.close()
        conexao.close()

menuIniciar()
