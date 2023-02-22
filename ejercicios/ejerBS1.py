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
    list_una_pag = abrir_urls()
    for vino in list_una_pag:
        detalles=vino.find("div",class_="details")
        nombre=detalles.find("a")["title"]
        bodega=detalles.find("div",class_="cellar-name").string
        region=detalles.find("div",class_="region").string
        lista_tipos_uva=list(detalles.find("div",class_="tags").stripped_strings)
        tipos_uva = "".join(lista_tipos_uva)
        

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