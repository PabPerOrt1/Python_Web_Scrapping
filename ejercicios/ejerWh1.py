import os
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, KEYWORD, DATETIME, ID, STORED
from whoosh.qparser import QueryParser
from whoosh import query
from tkinter import *
from tkinter import messagebox

agenda={}
dirdocs="extra_dato\Docs\Correos"
dirindex="Index"
dirage="extra_dato\Docs\Agenda"

#Crea un indice desde los documentos contenidos en dirdocs
#El indice lo crea en el directorio dirindex 
def crea_index():
    def carga():
        sch = Schema(remitente=ID(stored=True), destinatarios=KEYWORD(stored=True), fecha=DATETIME(stored=True), asunto=TEXT(stored=True,phrase=False), contenido=TEXT(stored=True,phrase=False), nombrefichero=STORED)
        ix = create_in(dirindex, schema=sch)
        writer = ix.writer()
        for docname in os.listdir(dirdocs):
            if not os.path.isdir(dirdocs+docname):
                add_doc(writer, dirdocs, docname)                  
        writer.commit()
        messagebox.showinfo("INDICE CREADO", "Se han cargado " + str(ix.reader().doc_count()) + " documentos")
    
    if not os.path.exists(dirdocs):
        messagebox.showerror("ERROR", "No existe el directorio de documentos " + dirdocs)
    else:
        if not os.path.exists(dirindex):
            os.mkdir(dirindex)
    if not len(os.listdir(dirindex))==0:
        respuesta = messagebox.askyesno("Confirmar","Indice no vacío. Desea reindexar?") 
        if respuesta:
            carga()           
    else:
        carga()

       
def crea_agenda():
    try:
        fileobj=open(dirage+'\\'+"agenda.txt", "r")
        email=fileobj.readline()
        while email:
            nombre=fileobj.readline()
            agenda[email.strip()]=nombre.strip()
            email=fileobj.readline()
    except:
        messagebox.showerror("ERROR", "No se ha podido crear la agenda. Compruebe que existe el fichero "+dirage+'\\'+"agenda.txt")
           
        
def cuerpo():
    def listar_cuerpo(event):
            ix=open_dir(dirindex)   
            with ix.searcher() as searcher:
                myquery = QueryParser("contenido", ix.schema).parse(str(entry.get()))
                results = searcher.search(myquery)
                listar(results)
            
    v = Toplevel()
    label = Label(v, text="Introduzca consulta sobre el cuerpo: ")
    label.pack(side=LEFT)
    entry = Entry(v)
    entry.bind("<Return>", listar_cuerpo)
    entry.pack(side=LEFT)
    
        
def spam():
    def listar_spam(event):
        ix=open_dir(dirindex)   
        with ix.searcher() as searcher:
            query = QueryParser("asunto", ix.schema).parse(str(entry.get()))
            results = searcher.search(query)
            
            v1 = Toplevel()
            sc = Scrollbar(v1)
            sc.pack(side=RIGHT, fill=Y)
            lb = Listbox(v1, width=100, yscrollcommand=sc.set)
            for row in results:
                s = 'FICHERO: ' + row['nombrefichero']
                lb.insert(END, s)
                s = 'REMITENTE: ' + agenda[row['remitente']]
                lb.insert(END, s)
                lb.insert(END, "-------------------------------")       
            lb.pack(side=LEFT, fill=BOTH)
            sc.config(command=lb.yview)        
    v = Toplevel()
    label = Label(v, text="Introduzca palabra spam: ")
    label.pack(side=LEFT)
    entry = Entry(v)
    entry.bind("<Return>", listar_spam)
    entry.pack(side=LEFT)           


def add_doc(writer, path, docname):
    try:
        fileobj=open(path+'\\'+docname, "r")
        rte=fileobj.readline().strip()
        dtos=fileobj.readline().strip()
        f=fileobj.readline().strip()
        dat=datetime.strptime(f,'%Y%m%d')
        ast=fileobj.readline().strip()
        ctdo=fileobj.read()
        fileobj.close()           
        
        writer.add_document(remitente=rte, destinatarios=dtos, fecha=dat, asunto=ast, contenido=ctdo, nombrefichero=docname)
    
    except:
        messagebox.showerror("ERROR", "Error: No se ha podido añadir el documento "+path+'\\'+docname)


def cargar():
    crea_index()
    crea_agenda()
 
    
def listar(results):      
    v = Toplevel()
    sc = Scrollbar(v)
    sc.pack(side=RIGHT, fill=Y)
    lb = Listbox(v, width=150, yscrollcommand=sc.set)
    for row in results:
        s = 'REMITENTE: ' + row['remitente']
        lb.insert(END, s)       
        s = "DESTINATARIOS: " + row['destinatarios']
        lb.insert(END, s)
        s = "FECHA: " + row['fecha'].strftime('%d-%m-%Y')
        lb.insert(END, s)
        s = "ASUNTO: " + row['asunto']
        lb.insert(END, s)
        s = "CUERPO: " + row['contenido']
        lb.insert(END, s)
        lb.insert(END,"------------------------------------------------------------------------\n")
    lb.pack(side=LEFT, fill=BOTH)
    sc.config(command=lb.yview)


def ventana_principal():
    def listar_todo():
        ix=open_dir(dirindex)
        with ix.searcher() as searcher:
            results = searcher.search(query.Every())
            listar(results) 
    
    raiz = Tk()

    menu = Menu(raiz)

    #DATOS
    menudatos = Menu(menu, tearoff=0)
    menudatos.add_command(label="Cargar", command=cargar)
    menudatos.add_command(label="Listar", command=listar_todo)
    menudatos.add_command(label="Salir", command=raiz.quit)
    menu.add_cascade(label="Datos", menu=menudatos)

    #BUSCAR
    menubuscar = Menu(menu, tearoff=0)
    menubuscar.add_command(label="Cuerpo", command=cuerpo)
    menubuscar.add_command(label="Spam", command=spam)
    menu.add_cascade(label="Buscar", menu=menubuscar)

    raiz.config(menu=menu)

    raiz.mainloop()


if __name__ == "__main__":
    ventana_principal()