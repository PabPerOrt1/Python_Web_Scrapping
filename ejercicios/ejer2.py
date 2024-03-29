from tkinter import *
from tkinter import messagebox
import sqlite3
from ejer1 import *

'''scrollbar = Scrollbar(top)
scrollbar.pack( side = RIGHT, fill = Y )
'''
'''Listar es listbox con scrollbar
busca mes es label con entryframe
'''
url="https://sevilla.abc.es/rss/feeds/Sevilla_Sevilla.xml"
meses = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
                    'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

global texto

def store_data():
    con = sqlite3.connect("SevillaNewsDB.sqlite")
    con.text_factory = str
    con.execute("DROP TABLE IF EXISTS NEWS")
    con.execute("""CREATE TABLE NEWS (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    TITLE TEXT NOT NULL, LINK TEXT NOT NULL, PUBDATE DATE NOT NULL);""")
    text = read_url(url)
    for t in text:
        con.execute("""INSERT INTO NEWS (TITLE, LINK, PUBDATE) VALUES (?,?,?)""",(t[0],t[1],t[2]))
    con.commit()
    
    cursor = con.execute("SELECT COUNT(*) FROM NEWS")
    messagebox.showinfo("Base Datos","Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " registros")
    con.close()

def list_data():
    room = Toplevel()
    room.title("Listar")
    scrollbar = Scrollbar(room)
    scrollbar.pack(side = RIGHT, fill =Y )
    

    con = sqlite3.connect("SevillaNewsDB.sqlite")
    cursor = con.cursor()
    name = cursor.execute("SELECT title,link,pubdate FROM news")
    do=name.fetchall()
    cursor.close()

    lb = Listbox(room, width=150, yscrollcommand=scrollbar.set)
    for row in do:
        lb.insert(END,row[0])
        lb.insert(END,row[1])
        lb.insert(END,row[2])
        lb.insert(END,"")
    lb.pack(side=LEFT,fill=BOTH)
    scrollbar.config(command=lb.yview)




def new_window_month():
    def search_month(event):
        month=entry.get()
        window= Toplevel()
        window.title("Results")
        scrollbar = Scrollbar(window)
        scrollbar.pack(side = RIGHT, fill =Y )
        con = sqlite3.connect("SevillaNewsDB.sqlite")
        con.text_factory = str
        cursor = con.cursor()
        expresion = "%"+ str(meses[month]) +"%"
        seleq = cursor.execute(""" SELECT * FROM NEWS WHERE pubdate LIKE ?""", (expresion,))
        list_month_data = seleq.fetchall()
        cursor.close()
        con.close()
        lb = Listbox(window, width=150, yscrollcommand=scrollbar.set)
        for row in list_month_data:
            lb.insert(END,row[0])
            lb.insert(END,row[1])
            lb.insert(END,row[2])
            lb.insert(END,"")
        lb.pack(side=LEFT,fill=BOTH)
        scrollbar.config(command=lb.yview)
        
    tkmonth = Toplevel()
    tkmonth.title("Filter by month")
    label = Label(tkmonth,text="Introduzca el mes: (Xxx)")
    label.pack(side=LEFT)
    entry = Entry(tkmonth,bd=5)
    entry.bind("<Return>", search_month)
    entry.pack(side = RIGHT)


def new_window_day():
    def search_day(event):
        day=entry.get()
        window= Toplevel()
        window.title("Results")
        scrollbar = Scrollbar(window)
        scrollbar.pack(side = RIGHT, fill =Y )
        con = sqlite3.connect("SevillaNewsDB.sqlite")
        con.text_factory = str
        cursor = con.cursor()
        seleq = cursor.execute(""" SELECT * FROM NEWS WHERE pubdate LIKE ?""", (day,))
        list_month_data = seleq.fetchall()
        cursor.close()
        con.close()
        lb = Listbox(window, width=150, yscrollcommand=scrollbar.set)
        for row in list_month_data:
            lb.insert(END,row[0])
            lb.insert(END,row[1])
            lb.insert(END,row[2])
            lb.insert(END,"")
        lb.pack(side=LEFT,fill=BOTH)
        scrollbar.config(command=lb.yview)
        
    tkmonth = Toplevel()
    tkmonth.title("Filter by day")
    label = Label(tkmonth,text="Introduzca el dia: (dd/mm/aaaa)")
    label.pack(side=LEFT)
    entry = Entry(tkmonth,bd=5)
    entry.bind("<Return>", search_day)
    entry.pack(side = RIGHT)



def first_window():
    top = Tk()
    Almacenar = Button(top,command=store_data,text="Almacenar")
    Almacenar.pack(side=LEFT)
    Listar = Button(top,command=list_data, text="Listar")
    Listar.pack(side=LEFT)
    Busca_Mes =Button(top,command=new_window_month, text="Busca Mes")
    Busca_Mes.pack(side=LEFT)
    Busca_Día =Button(top,command=new_window_day, text="Busca Día")
    Busca_Día.pack(side=LEFT)
    top.mainloop()
if __name__ == "__main__":
    first_window()