from bs4 import BeautifulSoup
import urllib.request 

# import os, ssl
# if (not os.environ.get("PYTHON"))
"""almacenar de cada vino: nombre, precio,origen,bodega,tipo_uva"""
def abrir_url():
    url = "https://www.vinissimus.com/es/vinos/tinto/?cursor=0"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f,"lxml")
    return s

def cargar():
    s = abrir_url()
    list_una_pag = s.find_all("div",class_="product-list-item")
    
    for vino in list_una_pag:
        detalles=vino.find("div",class_="details")
        nombre=detalles.find("a")["title"]
        bodega=detalles.find("div",class_="cellar-name").string
        region=detalles.find("div",class_="region").string
        tipo_uva=list(detalles.find("div",class_="tags").stripped_strings)
        print("".join(tipo_uva))
        
if __name__ == "__main__":
    cargar()