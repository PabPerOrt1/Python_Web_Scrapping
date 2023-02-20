from bs4 import BeautifulSoup
import urllib.request 
from tkinter import *
from tkinter import messagebox
import sqlite3

#Buscar Goles no hacerlo


def read_url():
    url = "http://resultados.as.com/resultados/futbol/primera/2021_2022/calendario/"
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f,"lxml")
    return s
#goles = re.compile('(\d+).*(\d+)').search(resultado_enlace.string....)

def load_data():

    con = sqlite3.connect("LaLigaSantanderDB.sqlite")
    con.execute("DROP TABLE IF EXISTS LIGA")
    con.execute('''CREATE TABLE LIGA (JORNADA INTEGER NOT NULL, EQUIPO_LOCAL TEXT NOT NULL, GOLES_LOCAL INTEGER NOT NULL,
     EQUIPO_VISITANTE TEXT NOT NULL, GOLES_VISITANTE INTEGER NOT NULL);''')

    s = read_url()
    lista_jornadas=s.find("div",class_="container content").find("div", class_="col-md-12 col-sm-12 col-xs-12")
    jornadas=lista_jornadas.find_all("div", class_="col-md-6 col-sm-6 col-xs-12")
    numero_jornada=0
    for j in jornadas:
        numero_jornada+=1
        tabla_partidos=j.find("table", class_="tabla-datos").find("tbody").find_all("tr")
        for partido in tabla_partidos:
            local = partido.find("td",class_="col-equipo-local").find("span",class_="nombre-equipo").string
            visitante = partido.find("td",class_="col-equipo-visitante").find("span",class_="nombre-equipo").string
            resultado = list(partido.find("td",class_="col-resultado").find("a",class_="resultado").stripped_strings)[0].split("-")
            goles_local = int(resultado[0])
            goles_visitante = int(resultado[1])
            con.execute('''INSERT INTO LIGA(JORNADA,EQUIPO_LOCAL,GOLES_LOCAL,EQUIPO_VISITANTE,GOLES_VISITANTE) VALUES (?,?,?,?,?)''', (numero_jornada,local,goles_local,visitante,goles_visitante))
    con.commit()
    cursor = con.execute("SELECT COUNT(*) FROM LIGA")
    messagebox.showinfo("Base Datos", "Base de Datos creada correctamente \nHay " + str(cursor.fetchone()[0])+ " registros")
    con.close()  

def list_data():
    room = Toplevel()
    room.title("Listar")
    scrollbar = Scrollbar(room)
    scrollbar.pack(side = RIGHT, fill =Y )
    con = sqlite3.connect("LaLigaSantanderDB.sqlite")
    cursor = con.cursor()
    name = cursor.execute("SELECT JORNADA,EQUIPO_LOCAL,GOLES_LOCAL,EQUIPO_VISITANTE,GOLES_VISITANTE FROM LIGA")
    do=name.fetchall()
    cursor.close()
    lb = Listbox(room, width=150, yscrollcommand=scrollbar.set)
    for row in do:
        lb.insert(END,"JORNADA "+str(row[0]))
        lb.insert(END,"-------------------------")
        lb.insert(END,row[1]+" "+str(row[2])+"-"+str(row[4])+" "+row[3])
        lb.insert(END,"")
    lb.pack(side=LEFT,fill=BOTH)
    scrollbar.config(command=lb.yview)

def first_window():
    top = Tk()
    Almacenar = Button(top,command=load_data, text="Almacenar Resultados")
    Almacenar.pack(side=LEFT)
    Listar = Button(top,command=list_data, text="Listar Jornadas")
    Listar.pack(side=LEFT)
    Buscar =Button(top, text="Buscar Jornada")
    Buscar.pack(side=LEFT)
    top.mainloop()

if __name__ == "__main__":
    first_window()