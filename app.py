from tkinter import *
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from tkinter import Tk, Label, Entry, Button



connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="passwordmanager"
)

def adicionar_senha():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()


    if not site or not username or not password:
        messagebox.showerror("Error", "Please, fill in all fields.")
        return


    cursor = connection.cursor()
    query = "INSERT INTO manager (site, username, password) VALUES (%s, %s, %s)"
    values = (site, username, password)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()

    messagebox.showinfo("Success", "Password successfully added!")

def limpar_campos():
    site_entry.delete(0, END)
    username_entry.delete(0, END)
    password_entry.delete(0, END)

def exibir_senhas():
 
    cursor = connection.cursor()
    query = "SELECT site, username, password FROM manager"
    cursor.execute(query)
    senhas = cursor.fetchall()
    cursor.close()


    root.withdraw()


    senha_window = Tk()
    senha_window.title("Saved Passwords")

    def fechar_janela_senhas():
        senha_window.destroy()
        root.deiconify()

    senha_window.protocol("WM_DELETE_WINDOW", fechar_janela_senhas)


    senha_table = ttk.Treeview(senha_window, columns=("Site", "Usuário", "Senha"), show="headings")
    senha_table.heading("Site", text="Site")
    senha_table.column("Site", width=150)
    senha_table.heading("Usuário", text="User")
    senha_table.column("Usuário", width=150)
    senha_table.heading("Senha", text="Password")
    senha_table.column("Senha", width=150)


    for senha in senhas:
        senha_table.insert("", END, values=(senha[0], senha[1], senha[2]))

    senha_table.pack()


    menu = Menu(senha_window, tearoff=0)
    menu.add_command(label="Remove", command=lambda: confirmar_remover_senha(senha_table))
    senha_table.bind("<Button-3>", lambda e: menu.post(e.x_root, e.y_root))


    def editar_celula(event):
        item = senha_table.selection()[0]
        coluna = senha_table.identify_column(event.x)


        valor_atual = senha_table.item(item)["values"][int(coluna[1:]) - 1]


        entry = Entry(senha_table, width=20)
        entry.insert(0, valor_atual)

        def salvar_edicao():
            novo_valor = entry.get()


            campo = coluna[1:]
            if campo == "1":
                campo = "site"
            elif campo == "2":
                campo = "username"
            elif campo == "3":
                campo = "password"

            cursor = connection.cursor()
            query = f"UPDATE manager SET {campo} = %s WHERE site = %s AND username = %s AND password = %s"
            cursor.execute(query, (novo_valor, senha_table.item(item)["values"][0], senha_table.item(item)["values"][1], senha_table.item(item)["values"][2]))
            connection.commit()
            cursor.close()

     
            senha_table.set(item, coluna, novo_valor)
            entry.destroy()

        def cancelar_edicao():
            entry.destroy()


        bbox = senha_table.bbox(item, column=coluna)
        x = bbox[0] + senha_table.winfo_x() + 2
        y = bbox[1] + senha_table.winfo_y() + 2
        entry.place(x=x, y=y, anchor="nw")
        entry.focus_set()
        entry.bind("<Return>", lambda event: salvar_edicao())
        entry.bind("<Escape>", lambda event: cancelar_edicao())

    senha_table.bind("<Double-Button-1>", editar_celula)


    fechar_button = Button(senha_window, text="Close", command=fechar_janela_senhas)
    fechar_button.pack()

def confirmar_remover_senha(senha_table):

    selection = senha_table.selection()
    if selection:

        values = senha_table.item(selection)["values"]


        resposta = messagebox.askyesno("Confirmation", "You are sure you want remove that line?")

        if resposta:

            cursor = connection.cursor()
            query = "DELETE FROM manager WHERE site = %s AND username = %s AND password = %s"
            cursor.execute(query, values)
            connection.commit()
            cursor.close()


            senha_table.delete(selection)

            messagebox.showinfo("Success", "Password successfully removed!")
    else:
        messagebox.showwarning("Aviso", "No lines selected.")


root = Tk()
root.title("Password Manager")


style = ttk.Style()
style.theme_use("clam")


style.configure(
    "Custom.TButton",
    relief="flat",
    borderwidth=0,
    foreground="#ffffff",
    background="#808080",
    font=("Arial", 12),
    width=15,
)
style.map(
    "Custom.TButton",
    foreground=[("active", "#ffffff")],
    background=[("active", "#5a5a5a")],
)


site_label = ttk.Label(root, text="Site:")
site_label.grid(row=0, column=0, padx=10, pady=10)
username_label = ttk.Label(root, text="User:")
username_label.grid(row=1, column=0, padx=10, pady=10)
password_label = ttk.Label(root, text="Password:")
password_label.grid(row=2, column=0, padx=10, pady=10)


site_label.configure(background=root.cget("background"))
username_label.configure(background=root.cget("background"))
password_label.configure(background=root.cget("background"))


site_entry = ttk.Entry(root, width=30)
site_entry.grid(row=0, column=1, padx=10, pady=10)
username_entry = ttk.Entry(root, width=30)
username_entry.grid(row=1, column=1, padx=10, pady=10)
password_entry = ttk.Entry(root, width=30, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=10)


add_button = ttk.Button(root, text="Add Password", style="Custom.TButton", command=adicionar_senha)
add_button.grid(row=3, column=0, padx=10, pady=10)
clear_button = ttk.Button(root, text="Clear fields", style="Custom.TButton", command=limpar_campos)
clear_button.grid(row=3, column=1, padx=10, pady=10)
view_button = ttk.Button(root, text="Saved passwords", style="Custom.TButton", command=exibir_senhas)
view_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)


root.mainloop()

connection.close()