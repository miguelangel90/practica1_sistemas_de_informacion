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
cursor.execute("CREATE TABLE IF NOT EXISTS analisis (id integer primary key AUTOINCREMENT, dispositivo text, puertos_abiertos int, servicios integer not null, servicios_inseguros integer not null, vulnerabilidades_detectadas integer not null, "
               "FOREIGN KEY (dispositivo) REFERENCES dispositivo(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS responsable (nombre text primary key, tlf integer, rol text )")
cursor.execute("CREATE TABLE IF NOT EXISTS dispositivo (id text primary key, ip text not null, localizacion text, responsable text, "
               "FOREIGN KEY(responsable) REFERENCES responsable(nombre))")

con.commit()

i = 1
for objeto in datos:
    nombre_responsable = objeto['responsable']['nombre']
    tlf_responsable = objeto['responsable']['telefono']
    rol_responsable = objeto['responsable']['rol']
    cursor.execute("INSERT OR IGNORE INTO responsable VALUES (?, ?, ?)", (nombre_responsable, tlf_responsable, rol_responsable))
    id_dispositivo = objeto['id']
    ip_dispositivo = objeto['ip']
    localizacion_dispositivo = objeto['localizacion']
    cursor.execute("INSERT INTO dispositivo VALUES (?, ?, ?, ?)", (id_dispositivo, ip_dispositivo, localizacion_dispositivo, nombre_responsable))
    #print(objeto['analisis']['puertos_abiertos'], i)
    #for puerto in objeto['analisis']['puertos_abiertos']:
     #   cursor.execute("INSERT INTO puerto VALUES (nombre, analisis_id)", (puerto, i))
    i = i + 1
    con.commit()