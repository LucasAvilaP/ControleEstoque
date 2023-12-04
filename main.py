import sys
import tkinter.messagebox
from tkinter import *
import pandas as pd
from login import LoginWindow
import PySimpleGUI as sg

db_path = "C:/Users/lucas.avila/Desktop/ProjetoEstoque/Estoque.db"

login_window = LoginWindow(db_path)
login_window.show()

if  not login_window.is_logged_in:
    tkinter.messagebox.showinfo(title="ATENÇÃO", message="O programa foi encerrado pois o usuário não realizou login")
    sys.exit()



######## funcionalidades do sistema #############
import pyodbc

dados_conexao = ("Driver={SQLite3 ODBC Driver};"
                 "Server=localhost;"
                 "Database=C:/Users/lucas.avila/Desktop/ProjetoEstoque/Estoque.db")

conexao = pyodbc.connect(dados_conexao)
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
""")

conexao.commit()


def adicionar_insumo():
    if len(nome_insumo.get()) < 2 or len(Tipo_insumo.get()) < 1 or len(qtde_insumo.get()) == 0:
        # exibir uma mensagem -> nome do insumo inválido
        # deletar tudo da caixa de texto
        caixa_texto.delete("1.0", END)

        # escrever na caixa de texto
        caixa_texto.insert("1.0", f"nome do insumo ou Tipo inválido!")
        # finalizar função
        return
    cursor.execute(f'''
    SELECT * FROM Estoque WHERE Produto="{nome_insumo.get().capitalize()}" AND Tipo="{Tipo_insumo.get().upper()}"
    ''')
    existing_insumo = cursor.fetchone()

    if existing_insumo:
        new_quantity = existing_insumo[2] + int(qtde_insumo.get())
        cursor.execute(f'''
        UPDATE Estoque
        SET Quantidade={new_quantity}
        WHERE Produto="{nome_insumo.get().capitalize()}" AND Tipo="{Tipo_insumo.get().upper()}"
        ''')
    else:
        cursor.execute(f'''
        INSERT INTO Estoque (Produto, Quantidade, Data, Tipo)
        VALUES 
        ("{nome_insumo.get().capitalize()}", {qtde_insumo.get()}, "{data_insumo.get()}", "{Tipo_insumo.get().upper()}")
        ''')
    conexao.commit()

    # deletar tudo da caixa de texto
    caixa_texto.delete("1.0", END)

    # escrever na caixa de texto
    caixa_texto.insert("1.0", f"{nome_insumo.get()} adicionado com sucesso!")


def deletar_insumo():
    if len(nome_insumo.get()) < 2 or len(Tipo_insumo.get()) < 1:
        # exibir uma mensagem -> nome do insumo inválido
        # deletar tudo da caixa de texto
        caixa_texto.delete("1.0", END)

        # escrever na caixa de texto
        caixa_texto.insert("1.0", f"nome do insumo ou Tipo inválido!")
        # finalizar função
        return
    # deletar insumo
    cursor.execute(f'''
    DELETE FROM Estoque 
    WHERE Produto="{nome_insumo.get().capitalize()}" AND Tipo="{Tipo_insumo.get().upper()}"
    ''')
    cursor.commit()
    # deletar tudo da caixa de texto
    caixa_texto.delete("1.0", END)

    # escrever na caixa de texto
    caixa_texto.insert("1.0", f"{nome_insumo.get()} deletado com sucesso!")


def consumir_insumo():
    if len(nome_insumo.get()) < 2 or len(Tipo_insumo.get()) < 1:
        # exibir uma mensagem -> nome do insumo inválido
        # deletar tudo da caixa de texto
        caixa_texto.delete("1.0", END)

        # escrever na caixa de texto
        caixa_texto.insert("1.0", f"nome e Tipo do insumo inválido!")
        # finalizar função
        return
    # consumir insumo
    cursor.execute(f'''
    UPDATE Estoque 
    SET Quantidade=Quantidade-{qtde_insumo.get()}
    WHERE Produto="{nome_insumo.get().capitalize()}" AND Tipo="{Tipo_insumo.get().upper()}"
    ''')
    cursor.commit()
    # deletar tudo da caixa de texto
    caixa_texto.delete("1.0", END)

    # escrever na caixa de texto
    caixa_texto.insert("1.0", f"{nome_insumo.get()} foi consumido em {qtde_insumo.get()} unidades!")


def visualizar_insumo():
    if len(nome_insumo.get()) < 2 and len(Tipo_insumo.get()) < 2:
        # exibir uma mensagem -> nome do insumo inválido
        # deletar tudo da caixa de texto
        caixa_texto.delete("1.0", END)

        # escrever na caixa de texto
        caixa_texto.insert("1.0", f"nome do insumo inválido!")
        # finalizar função
        return

    # Pesquisar pelo insumo
    query = "SELECT * FROM Estoque"
    conditions = []
    if nome_insumo.get().strip():
        conditions.append(f"Produto='{nome_insumo.get().strip().capitalize()}'")
    if Tipo_insumo.get().strip():
        conditions.append(f"Tipo='{Tipo_insumo.get().strip().upper()}'")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query)
    valores = cursor.fetchall()
    texto = ""
    for id_produto, nome, quantidade, entrada, Tipo in valores:
        texto = texto + f'''
        -----
        Produto: {nome}
        Quantidade: {quantidade}
        Entrada: {entrada}
        Tipo: {Tipo}
        '''
        
    # deletar tudo da caixa de texto
    caixa_texto.delete("1.0", END)

    # escrever na caixa de texto
    caixa_texto.insert("1.0", texto)
    
    
def exportar_excel():
    valores = cursor.execute("""
    SELECT * FROM Estoque 
    """)

    valores = pd.read_sql("SELECT Produto, Quantidade, Data, Tipo FROM Estoque", con=conexao)
    valores.to_csv(r'Itens em estoque.csv', sep=';')


######### criação da Janela ##################

window =Tk()


window.geometry("711x646")
window.configure(bg="#ffffff")
canvas = Canvas(
    window,
    bg="#ffffff",
    height=646,
    width=711,
    bd=0,
    highlightthickness=0,
    relief="ridge")
canvas.place(x=0, y=0)

background_img = PhotoImage(file=f"janela/background.png")
background = canvas.create_image(
    355.5, 323.0,
    image=background_img)

img0 = PhotoImage(file=f"janela/img0.png")
b0 = Button(
    image=img0,
    borderwidth=0,
    highlightthickness=0,
    command=visualizar_insumo,
    relief="flat")

b0.place(
    x=479, y=195,
    width=178,
    height=38)

img1 = PhotoImage(file=f"janela/img1.png")
b1 = Button(
    image=img1,
    borderwidth=0,
    highlightthickness=0,
    command=deletar_insumo,
    relief="flat")

b1.place(
    x=247, y=197,
    width=178,
    height=36)

img2 = PhotoImage(file=f"janela/img2.png")
b2 = Button(
    image=img2,
    borderwidth=0,
    highlightthickness=0,
    command=consumir_insumo,
    relief="flat")

b2.place(
    x=479, y=123,
    width=178,
    height=35)

img3 = PhotoImage(file=f"janela/img3.png")
b3 = Button(
    image=img3,
    borderwidth=0,
    highlightthickness=0,
    command=adicionar_insumo,
    relief="flat")

b3.place(
    x=247, y=125,
    width=178,
    height=34)

img4 = PhotoImage(file=f"janela/img4.png")
b4 = Button(
    image=img4,
    borderwidth=0,
    highlightthickness=0,
    command=exportar_excel,
    relief="flat"
)

b4.place(
    x=511, y=620,
    width=150,
    height=20
)

entry0_img = PhotoImage(file=f"janela/img_textBox0.png")
entry0_bg = canvas.create_image(
    455.0, 560.0,
    image=entry0_img)

caixa_texto = Text(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

caixa_texto.place(
    x=250, y=502,
    width=410,
    height=114)

entry1_img = PhotoImage(file=f"janela/img_textBox1.png")
entry1_bg = canvas.create_image(
    517.0, 294.5,
    image=entry1_img)

nome_insumo = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

nome_insumo.place(
    x=377, y=278,
    width=280,
    height=31)

entry2_img = PhotoImage(file=f"janela/img_textBox2.png")
entry2_bg = canvas.create_image(
    517.0, 340.5,
    image=entry2_img)

data_insumo = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

data_insumo.place(
    x=377, y=324,
    width=280,
    height=31)

entry3_img = PhotoImage(file=f"janela/img_textBox3.png")
entry3_bg = canvas.create_image(
    517.0, 388.5,
    image=entry3_img)

Tipo_insumo = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

Tipo_insumo.place(
    x=377, y=372,
    width=280,
    height=31)

entry4_img = PhotoImage(file=f"janela/img_textBox4.png")
entry4_bg = canvas.create_image(
    517.0, 436.5,
    image=entry4_img)

qtde_insumo = Entry(
    bd=0,
    bg="#ffffff",
    highlightthickness=0)

qtde_insumo.place(
    x=377, y=420,
    width=280,
    height=31)


window.resizable(False, False)
window.mainloop()



cursor.close()
conexao.close()