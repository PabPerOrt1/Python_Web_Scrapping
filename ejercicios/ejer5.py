"""cuando solo es un string pongo .string si hay varias cosas con varios strings poner stripe_string"""
"""como no tengo garantía de si algun campo falta en vez de coger ej: buscar el 6 campo que es director=. Si algun campo de antes falta
ya no sería el sexto, asi que lo mejor es buscar el campo 

find.netsibling para los dd para evitar salto de linea"""

from bs4 import BeautifulSoup
import urllib.request 
from tkinter import *
from tkinter import messagebox


def abrir_url():
    url = "https://www.elseptimoarte.net/estrenos"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f,"lxml")
    return s

def lista_url():
    url_especial="https://www.elseptimoarte.net"
    lista=[]
    text = abrir_url()
    lista_pelis = text.find("ul", class_="elements")
    todas_pelis = lista_pelis.find_all("li")
    for peli in todas_pelis:
        enlaces = peli.find("h3").find("a")["href"]
        lista.append(url_especial+enlaces)
    return lista

def extraer_campos():
    urls=lista_url()
    
def ventana_principal():
    raiz = Tk()
    menu = Menu(raiz)
    #DATOS
    menudatos = Menu(menu, tearoff=0)
    menudatos.add_command(label="Cargar" )
    menudatos.add_command(label="Listar" )
    menudatos.add_command(label="Salir" )
    menu.add_cascade(label="Datos", menu=menudatos)
    #BUSCAR
    menubuscar = Menu(menu, tearoff=0)
    menubuscar.add_command(label="Título" )
    menubuscar.add_command(label="Fecha" )
    menubuscar.add_command(label="Géneros")
    menu.add_cascade(label="Buscar", menu=menubuscar)
    raiz.config(menu=menu)
    raiz.mainloop()
if __name__ == "__main__":
    cargar()