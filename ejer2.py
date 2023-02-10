from tkinter import *
import sqlite3
from ejer1 import *

'''scrollbar = Scrollbar(top)
scrollbar.pack( side = RIGHT, fill = Y )
'''
'''Listar es listbox con scrollbar
busca mes es label con entryframe
'''
url="https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml"


def store_data():
    con = sqlite3.connect("SevillaNewsDB.db")
    con.text_factory = str
    con.execute("DROP TABLE IF EXISTS DATA")
    con.execute("""CREATE TABLE NEWS (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TITLE TEXT NOT NULL, LINK TEXT NOT NULL, PUBDATE DATE NOT NULL);""")
    text = read_url(url)
    for t in text:
        con.execute("""INSERT INTO NEWS (TITLE, LINK, PUBDATE) VALUES (?,?,?)""",(t[0],t[1],t[2]))
    con.commit()
    
    return None


def list_data():
    room = Toplevel()
    room.title("Listar")
    scrollbar = Scrollbar(room)
    scrollbar.pack( side = RIGHT, fill = Y )
    return None


def first_window():
    top = Tk()
    Almacenar = Button(top,command=store_data,text="Almacenar")
    Almacenar.pack(side=LEFT)
    Listar = Button(top,command=list_data, text="Listar")
    Listar.pack(side=LEFT)
    Busca_Mes =Button(top, text="Busca Mes")
    Busca_Mes.pack(side=LEFT)
    Busca_Día =Button(top, text="Busca Día")
    Busca_Día.pack(side=LEFT)
    top.mainloop()
if __name__ == "__main__":
    first_window()