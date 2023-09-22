from tkinter import Tk, Label, Button, Entry, messagebox
from tkinter.messagebox import askyesno
import sqlite3
import PySimpleGUI as sg
import re


class LoginWindow:
    def __init__(self, db_path):
        self.db_path = db_path
        self.root = Tk()
        self.root.title("Faça seu login")
        self.root.geometry('250x200')
        self.is_logged_in = False



        Label(self.root, text="Nome de usuário:").pack()
        self.username_entry = Entry(self.root, width=30)
        self.username_entry.pack()

        Label(self.root, text="Senha:").pack()
        self.password_entry = Entry(self.root, show="*", width=30)
        self.password_entry.pack()

        Button(self.root, text="Login", command=self.login).pack()
        Button(self.root, text="Registrar", command=self.register).pack()

    def show(self):
        self.root.mainloop()

    def is_valid(self, text):
        return  re.match("[A-Za-z0-9_]+$", text)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        conexao = sqlite3.connect(self.db_path)
        cursor = conexao.cursor()

        if len(password) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres")
            return

        if not username or not password:
            messagebox.showerror(title="Erro", message="O nome de usuário e senha são obrigatórios")

        if not self.is_valid(username):
            messagebox.showerror(title="Erro", message="Nome de usuário não deve conter caracteres especiais")
            return

        cursor.execute("INSERT INTO Usuarios (username, password) VALUES (?, ?)", (username, password))
        conexao.commit()

        cursor.close()
        conexao.close()

        messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")

    def login(self):
        username = self.username_entry.get().lower().strip()
        password = self.password_entry.get().lower().strip()

        conexao = sqlite3.connect(self.db_path)
        cursor = conexao.cursor()


        cursor.execute("SELECT * FROM Usuarios WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        cursor.close()
        conexao.close()

        if user:
            self.is_logged_in = True
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.root.destroy()
        else:
            messagebox.showerror("Erro", "Nome de usuário ou senha incorretos")




