from tkinter import *
from tkinter import messagebox
import csv
import sqlite3

def load_data():
    con = sqlite3.connect("BooksDataDB.sqlite")
    con.text_factory = str
    con.execute("DROP TABLE IF EXISTS BOOKS")
    con.execute('''CREATE TABLE BOOKS (ISBN CHAR(9) PRIMARY KEY,TITLE TEXT NOT NULL, AUTHOR TEXT NOT NULL, YEAR INTEGER NOT NULL, PUBLISHER TEXT NOT NULL);''')      
    with open('extra_dato/books.csv') as books:  
        reader = csv.reader(books,delimiter=";")
        next(reader)
        for isbn,title,author,year,publisher in reader:
            if year == "Unknown":
                year = 0
            con.execute('''INSERT INTO BOOKS(ISBN,TITLE,AUTHOR,YEAR,PUBLISHER) VALUES (?,?,?,?,?)''',(isbn,title,author,year,publisher))
    con.commit()
    cursor = con.execute("SELECT COUNT(*) FROM BOOKS")
    messagebox.showinfo("Base Datos", "Base de Dats creada correctamente \nHay " + str(cursor.fetchone()[0])+ " registros")
    con.close()    

def first_window():
    app = Tk()
    app.title("Book app")
    menu = Menu(app)
    
    datamenu = Menu(menu, tearoff = 0)
    menu.add_cascade(label="Datos", menu= datamenu) 
    datamenu.add_command(label = "Cargar",command=load_data)
    datamenu.add_command(label = "Salir",command=app.quit)
    
    listmenu= Menu(menu,tearoff=0)
    menu.add_cascade(label="Listar",menu=listmenu)
    listmenu.add_command(label = "Completo")
    listmenu.add_command(label = "Ordenado")

    searchmenu = Menu(menu, tearoff = 0)
    menu.add_cascade(label="Datos", menu= searchmenu) 
    searchmenu.add_command(label = "Titulo")
    searchmenu.add_command(label = "Editorial")

    app.config(menu=menu)
    app.mainloop()



if __name__ == "__main__":
    first_window()