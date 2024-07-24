import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

# Configuração do tema escuro
root = tk.Tk()
root.title('Kalk Sports')

# Definição de cores para o tema escuro
cor_bg = '#0D7259'  # Cor de fundo
cor_fg = 'white'    # Cor do texto
cor_entry_bg = '#3a3a3a'  # Cor de fundo das entradas
cor_entry_fg = 'white'     # Cor do texto nas entradas
cor_button_bg = '#4a4a4a'  # Cor de fundo dos botões
cor_button_fg = 'white'     # Cor do texto nos botões
cor_listbox_bg = '#3a3a3a'  # Cor de fundo da lista
cor_listbox_fg = 'white'    # Cor do texto na lista

# Aplicando o estilo
root.configure(bg=cor_bg)

# Criação do notebook para abas
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

# Criando as duas abas
frame_cadastro = tk.Frame(notebook, bg=cor_bg)
frame_lista = tk.Frame(notebook, bg=cor_bg)

notebook.add(frame_cadastro, text="Cadastro de Alunos")
notebook.add(frame_lista, text="Lista de Alunos")

# Função para salvar dados no banco de dados SQLite
def salvar_dados():
    # Conectar ao banco de dados (se não existir, será criado automaticamente)
    conn = sqlite3.connect('alunos.db')
    cursor = conn.cursor()

    # Obter dados do formulário
    nome = entry_nome.get()
    data_nascimento = entry_data_nascimento.get()
    cpf = entry_cpf.get()
    cep = entry_cep.get()
    bolsa = combo_bolsa.get()
    esporte = combo_esporte.get()

    # Validar campos
    if len(cpf) != 14:
        messagebox.showerror('Erro', 'CPF deve ter o formato: 123.456.789-12')
        return
    if len(cep) != 9:
        messagebox.showerror('Erro', 'CEP deve ter o formato: 12345-678')
        return

    try:
        # Tenta converter a data para o formato correto
        data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y').strftime('%d/%m/%Y')
    except ValueError:
        messagebox.showerror('Erro', 'Data de nascimento deve ter o formato: dd/mm/aaaa')
        return

    # Inserir dados na tabela
    cursor.execute('INSERT INTO alunos (nome, data_nascimento, cpf, cep, bolsa, esporte) VALUES (?, ?, ?, ?, ?, ?)',
                   (nome, data_nascimento, cpf, cep, bolsa, esporte))
    conn.commit()

    # Fechar conexão
    conn.close()

    # Limpar campos do formulário
    entry_nome.delete(0, tk.END)
    entry_data_nascimento.delete(0, tk.END)
    entry_cpf.delete(0, tk.END)
    entry_cep.delete(0, tk.END)
    combo_bolsa.set('')
    combo_esporte.set('')

    messagebox.showinfo('Sucesso', 'Cadastro realizado com sucesso!')

    # Atualizar lista de cadastros
    listar_cadastros()

# Função para formatar CPF enquanto o usuário digita
def formatar_cpf(event):
    # Obtém o conteúdo atual do campo
    valor = event.widget.get()

    # Remove qualquer caractere que não seja dígito
    valor = ''.join(digito for digito in valor if digito.isdigit())

    # Aplica a formatação do CPF (123.456.789-12)
    if len(valor) >= 11:
        valor_formatado = f'{valor[:3]}.{valor[3:6]}.{valor[6:9]}-{valor[9:]}'
        event.widget.delete(0, tk.END)
        event.widget.insert(0, valor_formatado)

# Função para formatar CEP enquanto o usuário digita
def formatar_cep(event):
    # Obtém o conteúdo atual do campo
    valor = event.widget.get()

    # Remove qualquer caractere que não seja dígito
    valor = ''.join(digito for digito in valor if digito.isdigit())

    # Aplica a formatação do CEP (12345-678)
    if len(valor) >= 5:
        valor_formatado = f'{valor[:5]}-{valor[5:]}'
        event.widget.delete(0, tk.END)
        event.widget.insert(0, valor_formatado)

# Função para formatar a data de nascimento enquanto o usuário digita
def formatar_data(event):
    # Obtém o conteúdo atual do campo
    valor = event.widget.get()

    # Remove qualquer caractere que não seja dígito
    valor = ''.join(digito for digito in valor if digito.isdigit())

    # Adiciona barras conforme o usuário digita (DD/MM/AAAA)
    if len(valor) >= 2:
        valor_formatado = f'{valor[:2]}/{valor[2:4]}/{valor[4:]}'
        event.widget.delete(0, tk.END)
        event.widget.insert(0, valor_formatado[:10])  # Limita ao formato DD/MM/AAAA

# Função para listar todos os cadastros na interface
def listar_cadastros():
    # Conectar ao banco de dados
    conn = sqlite3.connect('alunos.db')
    cursor = conn.cursor()

    # Limpar lista de cadastros anterior (se existir)
    for row in tree.get_children():
        tree.delete(row)

    # Selecionar todos os cadastros
    cursor.execute('SELECT nome, data_nascimento, cpf, cep, bolsa, esporte FROM alunos')
    cadastros = cursor.fetchall()

    # Adicionar cada cadastro à tabela
    for cadastro in cadastros:
        tree.insert("", "end", values=cadastro)

    # Fechar conexão
    conn.close()

# Função para excluir cadastro selecionado
def excluir_cadastro():
    # Obter o item selecionado na tabela
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Erro', 'Selecione um cadastro para excluir.')
        return

    # Obter os valores do cadastro selecionado
    cadastro_valores = tree.item(selected_item)['values']

    # Conectar ao banco de dados
    conn = sqlite3.connect('alunos.db')
    cursor = conn.cursor()

    # Excluir cadastro do banco de dados com base nos valores
    cursor.execute('DELETE FROM alunos WHERE nome = ? AND data_nascimento = ? AND cpf = ? AND cep = ? AND bolsa = ? AND esporte = ?',
                   (cadastro_valores[0], cadastro_valores[1], cadastro_valores[2], cadastro_valores[3], cadastro_valores[4], cadastro_valores[5]))
    conn.commit()

    # Fechar conexão
    conn.close()

    messagebox.showinfo('Sucesso', 'Cadastro excluído com sucesso.')

    # Atualizar lista de cadastros
    listar_cadastros()

# Criação da tabela (apenas se não existir)
conn = sqlite3.connect('alunos.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS alunos (
        nome TEXT,
        data_nascimento TEXT,
        cpf TEXT,
        cep TEXT,
        bolsa TEXT,
        esporte TEXT
    )
''')
conn.commit()
conn.close()

# Definindo a largura mínima das colunas
frame_cadastro.grid_columnconfigure(0, minsize=150)
frame_cadastro.grid_columnconfigure(1, minsize=250)

label_nome = tk.Label(frame_cadastro, text='Nome:', bg=cor_bg, fg=cor_fg)
label_nome.grid(row=0, column=0, padx=10, pady=5, sticky='w')
entry_nome = tk.Entry(frame_cadastro, width=30, bg=cor_entry_bg, fg=cor_entry_fg)
entry_nome.grid(row=0, column=1, padx=10, pady=5, sticky='we')

label_data_nascimento = tk.Label(frame_cadastro, text='Data de Nascimento:', bg=cor_bg, fg=cor_fg)
label_data_nascimento.grid(row=1, column=0, padx=10, pady=5, sticky='w')
entry_data_nascimento = tk.Entry(frame_cadastro, width=30, bg=cor_entry_bg, fg=cor_entry_fg)
entry_data_nascimento.grid(row=1, column=1, padx=10, pady=5, sticky='we')
entry_data_nascimento.bind('<KeyRelease>', formatar_data)

label_cpf = tk.Label(frame_cadastro, text='CPF:', bg=cor_bg, fg=cor_fg)
label_cpf.grid(row=2, column=0, padx=10, pady=5, sticky='w')
entry_cpf = tk.Entry(frame_cadastro, width=30, bg=cor_entry_bg, fg=cor_entry_fg)
entry_cpf.grid(row=2, column=1, padx=10, pady=5, sticky='we')
entry_cpf.bind('<KeyRelease>', formatar_cpf)

label_cep = tk.Label(frame_cadastro, text='CEP:', bg=cor_bg, fg=cor_fg)
label_cep.grid(row=3, column=0, padx=10, pady=5, sticky='w')
entry_cep = tk.Entry(frame_cadastro, width=30, bg=cor_entry_bg, fg=cor_entry_fg)
entry_cep.grid(row=3, column=1, padx=10, pady=5, sticky='we')
entry_cep.bind('<KeyRelease>', formatar_cep)

label_bolsa = tk.Label(frame_cadastro, text='Bolsa:', bg=cor_bg, fg=cor_fg)
label_bolsa.grid(row=4, column=0, padx=10, pady=5, sticky='w')
combo_bolsa = ttk.Combobox(frame_cadastro, values=["100%", "50%","0%"], state="readonly", width=27)
combo_bolsa.grid(row=4, column=1, padx=10, pady=5, sticky='we')

label_esporte = tk.Label(frame_cadastro, text='Esporte:', bg=cor_bg, fg=cor_fg)
label_esporte.grid(row=5, column=0, padx=10, pady=5, sticky='w')
combo_esporte = ttk.Combobox(frame_cadastro, values=["Futebol", "Futsal", "Basquete", "Vôlei", "Jiu-Jitsu", "Boxe", "Xadrez", "Tênis", "Natação", "Ginástica"], state="readonly", width=27)
combo_esporte.grid(row=5, column=1, padx=10, pady=5, sticky='we')

# Botão de cadastrar na aba de Cadastro
button_salvar = tk.Button(frame_cadastro, text='Cadastrar', command=salvar_dados, bg=cor_button_bg, fg=cor_button_fg)
button_salvar.grid(row=6, column=1, columnspan=5, padx=10, pady=20)

# Lista de cadastros na aba de Lista
label_cadastros = tk.Label(frame_lista, text='Cadastros:', bg=cor_bg, fg=cor_fg)
label_cadastros.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

# Adicionando uma tabela para exibir os cadastros
tree = ttk.Treeview(frame_lista, columns=("Nome", "Data de Nascimento", "CPF", "CEP", "Bolsa", "Esporte"), show='headings', height=15)
tree.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky=tk.EW)

# Definindo os cabeçalhos da tabela
tree.heading("Nome", text="Nome", anchor='center')
tree.heading("Data de Nascimento", text="Data de Nascimento", anchor='center')
tree.heading("CPF", text="CPF", anchor='center')
tree.heading("CEP", text="CEP", anchor='center')
tree.heading("Bolsa", text="Bolsa", anchor='center')
tree.heading("Esporte", text="Esporte", anchor='center')

# Definindo a largura das colunas e centralizando o texto
tree.column("Nome", width=150, anchor='center')
tree.column("Data de Nascimento", width=120, anchor='center')
tree.column("CPF", width=100, anchor='center')
tree.column("CEP", width=80, anchor='center')
tree.column("Bolsa", width=80, anchor='center')
tree.column("Esporte", width=100, anchor='center')

# Botão de excluir na aba de Lista
button_excluir = tk.Button(frame_lista, text='Excluir Selecionado', command=excluir_cadastro, bg=cor_button_bg, fg=cor_button_fg)
button_excluir.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Botão de listar cadastrados na aba de Lista
button_listar = tk.Button(frame_lista, text='Listar Cadastrados', command=listar_cadastros, bg=cor_button_bg, fg=cor_button_fg)
button_listar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Iniciar a interface gráfica
root.mainloop()
