from bs4 import BeautifulSoup
import urllib.request 
from tkinter import *
from tkinter import messagebox
import sqlite3
import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context



def extraer_elementos():

    conn = sqlite3.connect('juegosMesa.sqlite')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS JUEGOS")
    conn.execute('''CREATE TABLE JUEGOS (TITULO TEXT, PORCENTAJE INTEGER, PRECIO REAL NOT NULL,
     TEMATICA TEXT NOT NULL, COMPLEJIDAD TEXT NOT NULL);''')

    url =  "https://zacatrus.es/juegos-de-mesa.html"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    lista_juegos=s.find("div", class_="columns").find("div", class_="products")
    juegos=lista_juegos.find_all("div", class_="product-item-info")
    for j in juegos:
        titulo = j.find("a",class_="product-item-link").string.strip()
        porcentaje = j.find("div",class_="product-reviews-summary")
        if porcentaje:
            porc = list(porcentaje.find("div",class_="rating-result").find("span").stripped_strings)[0].split("%")[0]
        else:
            porc = -1
        precio = list(j.find("div",class_="price-box").find("span", class_="price").stripped_strings)[0].split("€")[0]
        dentro = j.find("a",class_="product-item-link")["href"]
        f2 = urllib.request.urlopen(dentro)
        s2 = BeautifulSoup(f2, "lxml")
        descripcion_juego = s2.find("div", class_="trs")
        descripciones=descripcion_juego.find_all("div", class_="tr")
        for dj in descripciones:
            if (dj.find("div", class_="col label").string) == "Temática":
                tematica = dj.find("div", class_="col data").string.strip()
            if (dj.find("div", class_="col label").string) == "Complejidad":
                complejidad = dj.find("div", class_="col data").string.strip()

        conn.execute('''INSERT INTO JUEGOS (TITULO,PORCENTAJE,PRECIO,TEMATICA,COMPLEJIDAD) VALUES (?,?,?,?,?)''',(titulo,porc,precio,tematica,complejidad))
        conn.commit()
    num_juegos = conn.execute("SELECT COUNT(*) FROM JUEGOS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(num_juegos.fetchone()[0])+ " número de juegos de mesa")
    conn.close()

def listar_mejores_juegos():
    conn = sqlite3.connect('juegosMesa.sqlite')
    conn.text_factory = str
    cursor = conn.execute("SELECT * FROM JUEGOS WHERE PORCENTAJE >= 90 ORDER BY PORCENTAJE DESC ")

    v = Toplevel()
    v.title("Listar Mejores Juegos")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    juegos = cursor.fetchall()
    for row in juegos:
        s = 'JUEGO: ' + row[0]
        lb.insert(END, s)
        lb.insert(END, "------------------------------------------------------------------------")
        s = "     PORCENTAJE: " + str(row[1]) + ' | PRECIO: ' + row[2]+ ' | TEMATICA: ' + row[3] + ' | COMPLEJIDAD: ' + row[4]
        lb.insert(END, s)
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)

def listar_juegos():
    conn = sqlite3.connect('juegosMesa.sqlite')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO, PORCENTAJE, PRECIO, TEMATICA, COMPLEJIDAD FROM JUEGOS")   

    v = Toplevel()
    v.title("Listar Juegos")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    juegos = cursor.fetchall()
    for row in juegos:
        s = 'JUEGO: ' + row[0]
        lb.insert(END, s)
        lb.insert(END, "------------------------------------------------------------------------")
        s = "     PORCENTAJE: " + str(row[1]) + ' | PRECIO: ' + row[2]+ ' | TEMATICA: ' + row[3] + ' | COMPLEJIDAD: ' + row[4]
        lb.insert(END, s)
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)  

def juegos_tematica():
    def listar(event):
            room = Toplevel()
            room.title("Buscar por Temática")
            scrollbar = Scrollbar(room)
            scrollbar.pack(side = RIGHT, fill =Y )
            conn = sqlite3.connect('juegosMesa.sqlite')
            conn.text_factory = str
            cursor = conn.execute("SELECT TITULO, TEMATICA, COMPLEJIDAD FROM JUEGOS WHERE TEMATICA LIKE '%" + str(entry.get()) + "%'")
            do = cursor.fetchall()
            lb = Listbox(room, width=150, yscrollcommand=scrollbar.set)
            for row in do:
                lb.insert(END,"")
                lb.insert(END,row[0])
                lb.insert(END,row[1])
                lb.insert(END,row[2])
                lb.insert(END,"")
            lb.pack(side=LEFT,fill=BOTH)
            scrollbar.config(command=lb.yview)   
            conn.close()

    conn = sqlite3.connect('juegosMesa.sqlite')
    conn.text_factory = str
    cursor = conn.execute("SELECT DISTINCT TEMATICA FROM JUEGOS")
    #####################3
    tematica = [d[0] for d in cursor]
    
    ventana = Toplevel()
    label = Label(ventana,text="Seleccione una tematica: ")
    label.pack(side=LEFT)
    entry = Spinbox(ventana, width= 30, values=tematica)
    entry.bind("<Return>", listar)
    entry.pack(side=LEFT)
    
    conn.close()

def juegos_por_complejidad():
    def listar(event):
            room = Toplevel()
            room.title("Buscar por Complejidad")
            scrollbar = Scrollbar(room)
            scrollbar.pack(side = RIGHT, fill =Y )
            conn = sqlite3.connect('juegosMesa.sqlite')
            conn.text_factory = str
            cursor = conn.execute("SELECT TITULO, TEMATICA, COMPLEJIDAD FROM JUEGOS WHERE COMPLEJIDAD LIKE '%" + str(entry.get()) + "%'")
            do = cursor.fetchall()
            lb = Listbox(room, width=150, yscrollcommand=scrollbar.set)
            for row in do:
                lb.insert(END,row[0])
                lb.insert(END,row[1])
                lb.insert(END,row[2])
                lb.insert(END,"")
            lb.pack(side=LEFT,fill=BOTH)
            scrollbar.config(command=lb.yview)   
            conn.close()

    conn = sqlite3.connect('juegosMesa.sqlite')
    conn.text_factory = str
    cursor = conn.execute("SELECT DISTINCT COMPLEJIDAD FROM JUEGOS")
    #####################3
    complejidades = [d[0] for d in cursor]
    
    ventana = Toplevel()
    label = Label(ventana,text="Seleccione una Complejidad: ")
    label.pack(side=LEFT)
    entry = Spinbox(ventana, width= 30, values=complejidades)
    entry.bind("<Return>", listar)
    entry.pack(side=LEFT)
    
    conn.close()

def first_window():
    top = Tk()
    top.title("App juego de mesa")
    menu = Menu(top)
    datamenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Datos", menu=datamenu)
    datamenu.add_command(label="Cargar",command= extraer_elementos)
    datamenu.add_command(label="Salir",command=top.quit)

    listmenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Listar", menu=listmenu)
    listmenu.add_command(label="Juegos",command=listar_juegos)
    listmenu.add_command(label="Mejores juegos",command=listar_mejores_juegos)

    searchmenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Buscar", menu=searchmenu)
    searchmenu.add_command(label="Juegos por temática",command=juegos_tematica)
    searchmenu.add_command(label="Juegos por complejidad",command=juegos_por_complejidad)
    top.config(menu=menu)
    top.mainloop()

if __name__  == "__main__":
    first_window()