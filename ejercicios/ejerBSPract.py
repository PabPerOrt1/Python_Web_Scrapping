from bs4 import BeautifulSoup
import urllib.request 
from tkinter import *
from tkinter import messagebox
import sqlite3
import os, ssl
from datetime import datetime

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def cambia_fecha(fecha):
    meses = {'enero':'01','febrero':'02','marzo':'03','abril':'04','mayo':'05','junio':'06',
                    'julio':'07','agosto':'08','septiembre':'09','octubre':'10','noviembre':'11','diciembre':'12'}
    f = fecha.split()
    fecha_final = f[0] + "/" + meses[f[1]] + "/" + f[2]
    return datetime.strptime(fecha_final, '%d/%m/%Y').date()

def extraer_elementos():

    conn = sqlite3.connect('recetasDB.sqlite')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS RECETAS")
    conn.execute('''CREATE TABLE RECETAS (TITULO TEXT, DIFICULTAD TEXT, NUM_COMENSALES INTEGER,
     TIEMPO_PREP INTEGER, AUTOR TEXT, FECHA DATE);''')
    
    url =  "https://www.recetasgratis.net/Recetas-de-Aperitivos-tapas-listado_receta-1_1.html"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    lista_recetas = s.find("div", class_="main-content").find("div", class_="clear padding-left-1")
    recetas = lista_recetas.find_all("div", class_="resultado link")
    for r in recetas:
        titulo = r.find("a",class_="titulo").string.strip()
        dificultad = r.find("div",class_="info_snippet").find("span")
        if dificultad != None:
            dif = dificultad.string.strip()
        else:
            dif = "Desconocido"
        propiedades = r.find("div", class_="properties")
        if propiedades != None:
            comensales = int(propiedades.find("span", class_="property comensales").string)
            duracion = propiedades.find("span", class_="property duracion").string.strip()
        else:
            comensales = -1
            duracion = "Desconocido"
        dentro = r.find("a",class_="titulo titulo--resultado")["href"]
        f2 = urllib.request.urlopen(dentro)
        s2 = BeautifulSoup(f2, "lxml")
        dentro_receta = s2.find("div", class_="container").find("div", class_="main-content").find("article", class_="columna-post")
        dr = dentro_receta.find("div", class_="info_articulo").find("div", class_="nombre_autor")
        autor = dr.find("a", class_="ga").string
        fecha = dr.find("span").string
        if fecha[0] == "A":
            date = fecha.split(":")[1].strip()
        else:
            date = fecha.strip()
        fechosa = cambia_fecha(date)

        conn.execute('''INSERT INTO RECETAS (TITULO,DIFICULTAD,NUM_COMENSALES,TIEMPO_PREP,AUTOR,FECHA) VALUES (?,?,?,?,?,?)''',(titulo,dif,comensales,duracion,autor,fechosa))
        conn.commit()
        
    
    num_recetas = conn.execute("SELECT COUNT(*) FROM RECETAS")
    num_autores = conn.execute("SELECT COUNT(DISTINCT AUTOR) FROM RECETAS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(num_recetas.fetchone()[0])+ " número de recetas y " + str(num_autores.fetchone()[0]) + " autores")
    conn.close()



def listar_recetas():
    conn = sqlite3.connect('recetasDB.sqlite')
    conn.text_factory = str
    cursor = conn.execute("SELECT TITULO, DIFICULTAD, NUM_COMENSALES, TIEMPO_PREP FROM RECETAS")   
    
    v = Toplevel()
    v.title("Listar Recetas")
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    juegos = cursor.fetchall()
    for row in juegos:
        s = 'TITULO: ' + row[0]
        lb.insert(END, s)
        lb.insert(END, "------------------------------------------------------------------------")
        s1 = "     DIFICULTAD: " + str(row[1]) 
        lb.insert(END, s1)
        s2 = '     NUM_COMENSALES: ' + str(row[2])
        lb.insert(END, s2)
        s3 = '     TIEMPO_PREP: ' + row[3]
        lb.insert(END, s3)
        lb.insert(END,"\n\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)

def recetas_autor():
    def listar(event):
            room = Toplevel()
            room.title("Buscar por Autor")
            scrollbar = Scrollbar(room)
            scrollbar.pack(side = RIGHT, fill =Y )
            conn = sqlite3.connect('recetasDB.sqlite')
            conn.text_factory = str
            cursor = conn.execute("SELECT TITULO, DIFICULTAD, NUM_COMENSALES, TIEMPO_PREP, AUTOR FROM RECETAS WHERE AUTOR LIKE '%" + str(entry.get()) + "%'")
            do = cursor.fetchall()
            lb = Listbox(room, width=150, yscrollcommand=scrollbar.set)
            for row in do:
                lb.insert(END,'TITULO: ' + row[0])
                lb.insert(END, "------------------------------------------------------------------------")
                lb.insert(END, 'DIFICULTAD: ' + row[1])
                lb.insert(END, 'NUM_COMENSALES: '+ str(row[2]))
                lb.insert(END, 'TIEMPO_PREP: ' + row[3])
                lb.insert(END, 'AUTOR: '+ row[4])
                lb.insert(END,'\n\n')
            lb.pack(side=LEFT,fill=BOTH)
            scrollbar.config(command=lb.yview)   
            conn.close()

    conn = sqlite3.connect('recetasDB.sqlite')
    conn.text_factory = str
    cursor = conn.execute("SELECT DISTINCT AUTOR FROM RECETAS")
    #####################3
    autores = [d[0] for d in cursor]
    
    ventana = Toplevel()
    label = Label(ventana,text="Seleccione un Autor: ")
    label.pack(side=LEFT)
    entry = Spinbox(ventana, width= 30, values=autores)
    entry.bind("<Return>", listar)
    entry.pack(side=LEFT)
    
    conn.close()

def recetas_fecha():
    def listar(event):
            room = Toplevel()
            room.title("Buscar receta por fecha")
            scrollbar = Scrollbar(room)
            scrollbar.pack(side = RIGHT, fill =Y )
            conn = sqlite3.connect('recetasDB.sqlite')
            conn.text_factory = str
            joseda=datetime.strptime(str(entry.get()), '%d/%m/%Y').date()
            fecha_bd = joseda.strftime('%Y-%m-%d')
            cursor = conn.execute(f"SELECT TITULO, DIFICULTAD, NUM_COMENSALES, TIEMPO_PREP, FECHA FROM RECETAS WHERE FECHA < '{fecha_bd}'")
            do = cursor.fetchall()
            lb = Listbox(room, width=150, yscrollcommand=scrollbar.set)
            for row in do:
                lb.insert(END,'TITULO: ' + row[0])
                lb.insert(END, "------------------------------------------------------------------------")
                lb.insert(END, 'DIFICULTAD: ' + row[1])
                lb.insert(END, 'NUM_COMENSALES: '+ str(row[2]))
                lb.insert(END, 'TIEMPO_PREP: ' + row[3])
                lb.insert(END, 'FECHA: '+ str(row[4]))
                lb.insert(END,'\n\n')
            lb.pack(side=LEFT,fill=BOTH)
            scrollbar.config(command=lb.yview)   
            conn.close()
    
    ventana = Toplevel()
    label = Label(ventana,text="Introduzca una fecha en formato (día/mes/año): ")
    label.pack(side=LEFT)
    entry = Entry(ventana, width= 30, bd=5)
    entry.bind("<Return>", listar)
    entry.pack(side=LEFT)

def first_window():
    top = Tk()
    top.title("Recetas")
    menu = Menu(top)
    datamenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Datos", menu=datamenu)
    datamenu.add_command(label="Cargar", command=extraer_elementos)
    datamenu.add_command(label="Salir",command=top.quit)

    listmenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Listar", menu=listmenu)
    listmenu.add_command(label="Recetas", command=listar_recetas)

    searchmenu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Buscar", menu=searchmenu)
    searchmenu.add_command(label="Recetas por autor", command=recetas_autor)
    searchmenu.add_command(label="Recetas por fecha",command=recetas_fecha)
    top.config(menu=menu)
    top.mainloop()

if __name__  == "__main__":
    first_window()