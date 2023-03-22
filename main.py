import sqlite3
import json

con = sqlite3.connect('p1.db')

with open('devices.json') as f:
    datos = json.load(f)


cursor = con.cursor()

cursor.execute("DROP TABLE puerto")
cursor.execute("DROP TABLE analisis")
cursor.execute("DROP TABLE dispositivo")
cursor.execute("DROP TABLE responsable")

cursor.execute('PRAGMA foreign_keys = ON')

con.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS puerto (id integer primary key AUTOINCREMENT, nombre text not null, analisis_id integer, "
               "FOREIGN KEY (analisis_id) REFERENCES analisis(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS analisis (id integer primary key AUTOINCREMENT, puertos_abiertos int, servicios integer not null, servicios_inseguros integer not null, vulnerabilidades_detectadas integer not null, "
               "FOREIGN KEY (puertos_abiertos) REFERENCES puerto(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS responsable (nombre text primary key, tlf integer, rol text not null)")
cursor.execute("CREATE TABLE IF NOT EXISTS dispositivo (id text primary key, ip text not null, localizacion text, responsable text, analisis integer, FOREIGN KEY(responsable) REFERENCES responsable(nombre), FOREIGN KEY(analisis) REFERENCES analisis(id))")

con.commit()



i = 1
for objeto in datos:
    print(objeto['responsable'])
    nombre_responsable = objeto['responsable']['nombre']
    tlf_responsable = objeto['responsable']['telefono']
    rol_responsable = objeto['responsable']['rol']
    cursor.execute("INSERT INTO responsable VALUES (?, ?, ?)", (nombre_responsable, tlf_responsable, rol_responsable))
    cursor.execute("SELECT * FROM responsable")

con.commit()