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
    Button(frame, text="Listar contatos", font=("Arial", 12), width=20, command=menuListar).grid(row=4, column=0, pady=10)
    Button(frame, text="Exportar contatos", font=("Arial", 12), width=20, command=Exportar).grid(row=5, column=0, pady=10)
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


    """Função para exibir a janela de listagem dos contatos."""
    # Criar a janela de listagem
    janela_listar = Tk()
    janela_listar.title("Lista de contatos")
    
    # Conectar ao banco de dados
    conexao = conectarBanco()
    if conexao is None:
        return

    # Executar a consulta SQL
    comando = "SELECT id, nome, telefone, celular FROM contatos ORDER BY id ASC"
    cursor = conexao.cursor()
    try:
        cursor.execute(comando)
        contatos = cursor.fetchall()
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro de Consulta", f"Erro ao buscar dados: {erro}")
        return
    finally:
        cursor.close()
        conexao.close()

    # Variáveis para controlar a navegação
    current_index = [0]

    # Função para atualizar os campos com os dados do contato atual
    def atualizar_campos(index):
        if 0 <= index < len(contatos):
            id, nome, telefone, celular = contatos[index]
            label_nome_valor.config(text=nome)
            label_telefone_valor.config(text=telefone)
            label_celular_valor.config(text=celular)

    # Função para ir para o próximo contato
    def proximo_contato():
        if current_index[0] < len(contatos) - 1:
            current_index[0] += 1
            atualizar_campos(current_index[0])

    # Função para ir para o contato anterior
    def contato_anterior():
        if current_index[0] > 0:
            current_index[0] -= 1
            atualizar_campos(current_index[0])

    # Labels para os dados dos contatos
    Label(janela_listar, text="ID:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
    label_id_valor = Label(janela_listar, width=30, anchor='w', relief="sunken")
    label_id_valor.grid(row=0, column=1, padx=10, pady=5)

    Label(janela_listar, text="Nome:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
    label_nome_valor = Label(janela_listar, width=30, anchor='w', relief="sunken")
    label_nome_valor.grid(row=1, column=1, padx=10, pady=5)

    Label(janela_listar, text="Telefone:").grid(row=2, column=0, padx=10, pady=5, sticky=W)
    label_telefone_valor = Label(janela_listar, width=30, anchor='w', relief="sunken")
    label_telefone_valor.grid(row=2, column=1, padx=10, pady=5)

    Label(janela_listar, text="Celular:").grid(row=3, column=0, padx=10, pady=5, sticky=W)
    label_celular_valor = Label(janela_listar, width=30, anchor='w', relief="sunken")
    label_celular_valor.grid(row=3, column=1, padx=10, pady=5)

    # Botões de navegação
    Button(janela_listar, text="Anterior", command=contato_anterior).grid(row=3, column=0, padx=10, pady=10, sticky=E)
    Button(janela_listar, text="Próximo", command=proximo_contato).grid(row=3, column=1, padx=10, pady=10, sticky=W)

    # Inicializar os campos com o primeiro contato, se houver
    if contatos:
        atualizar_campos(current_index[0])

    # Iniciar o loop da interface gráfica
    janela_listar.mainloop()
   
def menuListar():
    janela_listar = Tk()
    janela_listar.title("Lista de contatos")
    janela_listar.iconbitmap(r"C:\\Python\\Estudo\\Agenda com interface grafica\\images\\newpy.ico")
    
    # Conectar ao banco de dados
    conexao = conectarBanco()
    if conexao is None:
        return

    # Executar a consulta SQL
    comando = "SELECT id, nome, telefone, celular FROM contatos ORDER BY id ASC"
    cursor = conexao.cursor()
    try:
        cursor.execute(comando)
        contatos = cursor.fetchall()
    except mysql.connector.Error as erro:
        messagebox.showerror("Erro de Consulta", f"Erro ao buscar dados: {erro}")
        return
    finally:
        cursor.close()
        conexao.close()

    # Variáveis para controlar a navegação
    current_index = [0]

    # Função para atualizar os campos com os dados do contato atual
    def atualizar_campos(index):
        if 0 <= index < len(contatos):
            id, nome, telefone, celular = contatos[index]
            label_id_valor.config(text=id)
            label_nome_valor.config(text=nome)
            label_telefone_valor.config(text=telefone)
            label_celular_valor.config(text=celular)

    # Função para ir para o próximo contato
    def proximo_contato():
        if current_index[0] < len(contatos) - 1:
            current_index[0] += 1
            atualizar_campos(current_index[0])

    # Função para ir para o contato anterior
    def contato_anterior():
        if current_index[0] > 0:
            current_index[0] -= 1
            atualizar_campos(current_index[0])

    # Labels para os dados dos contatos
    Label(janela_listar, text="ID:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
    label_id_valor = Label(janela_listar, width=30, anchor='w', relief="sunken")
    label_id_valor.grid(row=0, column=1, padx=10, pady=5)

    Label(janela_listar, text="Nome:").grid(row=1, column=0, padx=10, pady=5, sticky=W)
    label_nome_valor = Label(janela_listar, width=30, anchor='w', relief="sunken")
    label_nome_valor.grid(row=1, column=1, padx=10, pady=5)

    Label(janela_listar, text="Telefone:").grid(row=2, column=0, padx=10, pady=5, sticky=W)
    label_telefone_valor = Label(janela_listar, width=30, anchor='w', relief="sunken")
    label_telefone_valor.grid(row=2, column=1, padx=10, pady=5)

    Label(janela_listar, text="Celular:").grid(row=3, column=0, padx=10, pady=5, sticky=W)
    label_celular_valor = Label(janela_listar, width=30, anchor='w', relief="sunken")
    label_celular_valor.grid(row=3, column=1, padx=10, pady=5)

    # Botões de navegação
    Button(janela_listar, text="Anterior", command=contato_anterior).grid(row=4, column=0, padx=10, pady=10, sticky=E)
    Button(janela_listar, text="Próximo", command=proximo_contato).grid(row=4, column=1, padx=10, pady=10, sticky=W)

    # Inicializar os campos com o primeiro contato, se houver
    if contatos:
        atualizar_campos(current_index[0])

    # Iniciar o loop da interface gráfica
    janela_listar.mainloop()
    
def exportarContatos(nome_arquivo):
    """Função para exportar os contatos para um arquivo."""
    try:
        # Conectar ao banco de dados
        conexao = conectarBanco()
        if conexao is None:
            raise Exception("Erro ao conectar ao banco de dados.")

        comando = "SELECT id, nome, telefone, celular FROM contatos ORDER BY id ASC"
        contatos = []

        # Executar a consulta
        cursor = conexao.cursor()
        cursor.execute(comando)

        # Armazenar os resultados na lista de contatos
        for id, nome, telefone, celular in cursor:
            contatos.append({'id': id, 'nome': nome, 'telefone': telefone, 'celular': celular})

        # Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

        # Gravar os resultados em um arquivo
        with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
            for i, contato in enumerate(contatos, start=1):
                registro = (
                    f"Contato {i}\n"
                    f"Nome: {contato['nome']}\n"
                    f"Telefone: {contato['telefone']}\n"
                    f"Celular: {contato['celular']}\n"
                    f"{'-'*30}\n"  # Separador visual entre contatos
                )
                arquivo.write(registro)

        # Mostrar mensagem de sucesso
        messagebox.showinfo("Sucesso", "Exportação realizada com sucesso")

    except Exception as err:
        messagebox.showerror("Erro", f'Impossível exportar: {err}')

def Exportar():
    """Função para abrir a janela onde o usuário informará o nome do arquivo."""
    janela_exportar = Tk()
    janela_exportar.title("Exportar Contatos")
    janela_exportar.iconbitmap(r"C:\\Python\\Estudo\\Agenda com interface grafica\\images\\newpy.ico")
    

    # Label e Entry para nome do arquivo
    Label(janela_exportar, text="Nome do Arquivo:").grid(row=0, column=0, padx=10, pady=10)
    entry_nome_arquivo = Entry(janela_exportar, width=30)
    entry_nome_arquivo.grid(row=0, column=1, padx=10, pady=10)

    # Função para capturar o nome do arquivo e chamar a função de exportação
    def executar_exportacao():
        nome_arquivo = entry_nome_arquivo.get()
        if nome_arquivo.strip() == "":
            messagebox.showerror("Erro", "Por favor, informe um nome de arquivo válido.")
        else:
            if not nome_arquivo.endswith(".txt"):
                nome_arquivo += ".txt"  # Adiciona a extensão se não estiver presente
            exportarContatos(nome_arquivo)
            janela_exportar.destroy()  # Fecha a janela após a exportação

    # Botão para exportar
    Button(janela_exportar, text="Exportar", command=executar_exportacao).grid(row=1, column=1, padx=10, pady=10)

    
menuIniciar()
