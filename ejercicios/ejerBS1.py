from bs4 import BeautifulSoup
import urllib.request 
from tkinter import *
from tkinter import messagebox
import sqlite3
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

"""almacenar de cada vino: nombre, precio,origen,bodega,tipo_uva"""
def abrir_urls():
    lista = []
    for i in range(0,3):
        multiplicacion = 36*i
        url = f"https://www.vinissimus.com/es/vinos/tinto/?cursor={multiplicacion}"
        f = urllib.request.urlopen(url)
        s = BeautifulSoup(f,"lxml")
        list_una_pag = s.find_all("div",class_="product-list-item")
        lista.extend(list_una_pag)
    return lista

def cargar():
    con = sqlite3.connect("VinosDB.sqlite")
    con.execute("DROP TABLE IF EXISTS VINOS")
    con.execute("""CREATE TABLE VINOS (NAME TEXT, PRICE REAl, ORIGIN TEXT, WINE_CELLAR TEXT,
    GRAPE_TYPE TEXT)""")
    cursor = con.cursor()

    list_una_pag = abrir_urls()
    for vino in list_una_pag:
        detalles=vino.find("div",class_="details")
        precio = list(vino.find("p",class_=["price"]).stripped_strings)[0]
        dto = vino.find("p",class_=["price"]).find_next_sibling("p",class_="dto")
        nombre=detalles.find("a")["title"]
        bodega=detalles.find("div",class_="cellar-name").string
        region=detalles.find("div",class_="region").string
        lista_tipos_uva=list(detalles.find("div",class_="tags").stripped_strings)
        tipos_uva = "".join(lista_tipos_uva)
        if dto:
            precio = list(dto.stripped_strings)[0]
        cursor.execute("INSERT INTO VINOS (NAME,PRICE,ORIGIN,WINE_CELLAR,GRAPE_TYPE) VALUES (?,?,?,?,?)", (nombre,precio,region,bodega,tipos_uva))
        con.commit()
    num_vinos = cursor.execute("SELECT COUNT(*) FROM VINOS")
    messagebox.showinfo("Base Datos", "Base de datos creada correctamente \nHay " + str(num_vinos.fetchone()[0])+ " número de vinos")
    cursor.close()
    con.close()
def first_window():
    app = Tk()
    app.title("Vino app")
    menu = Menu(app)
    
    datamenu = Menu(menu, tearoff = 0)
    menu.add_cascade(label="Datos", menu= datamenu) 
    datamenu.add_command(label = "Cargar",command=cargar)
    datamenu.add_command(label = "Listar")
    datamenu.add_command(label = "Salir",command=app.quit)
    
    # listmenu= Menu(menu,tearoff=0)
    # menu.add_cascade(label="Listar",menu=listmenu)
    # listmenu.add_command(label = "Completo",command=list_data)
    # listmenu.add_command(label = "Ordenado",command=listar_ordenado)

    app.config(menu=menu)
    app.mainloop()

if __name__ == "__main__":
    first_window()