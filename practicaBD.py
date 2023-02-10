import sqlite3
con = sqlite3.connect("prueba.db")
cursor = con.cursor()
res = cursor.execute("CREATE TABLE AbcSevilla(nombre,link,fecha)")

res.fetchone() #para ver lo que se ha creado

'''data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]'''
#cur.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
#con.commit()  # Remember to commit the transaction after executing INSERT
con.close()