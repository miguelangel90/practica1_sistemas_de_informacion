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

i = 0
## INSERTAMOS LOS DATOS
for objeto in datos:

    ## TABLA RESPONSABLE
    nombre_responsable = objeto['responsable']['nombre']
    tlf_responsable = objeto['responsable']['telefono']
    rol_responsable = objeto['responsable']['rol']
    cursor.execute("INSERT OR IGNORE INTO responsable VALUES (?, ?, ?)", (nombre_responsable, tlf_responsable, rol_responsable))

    ## TABLA DISPOSITIVO
    id_dispositivo = objeto['id']
    ip_dispositivo = objeto['ip']
    localizacion_dispositivo = objeto['localizacion']
    cursor.execute("INSERT INTO dispositivo VALUES (?, ?, ?, ?)", (id_dispositivo, ip_dispositivo, localizacion_dispositivo, nombre_responsable))

    ## TABLA ANALISIS
    id_analisis= i
    ## id_dispositivo=
    puerto_abierto=objeto["analisis"]["puertos_abiertos"]
    servicio_normal=objeto["analisis"]["servicios"]
    servicio_inseguro= objeto["analisis"]["servicios_inseguros"]
    vulnerabilidad_detectada=objeto["analisis"]["vulnerabilidades_detectadas"]
    cursor.execute("INSERT INTO analisis VALUES (?, ?, ?, ?,?,?)",(id_analisis, ip_dispositivo, puerto_abierto, servicio_normal, servicio_inseguro, vulnerabilidad_detectada))


    ## TABLA PUERTOS
    id_puerto= 0
    ## id_analisis= i
    for puerto_nuevo in objeto["analisis"]["puertos_abiertos"]:
        cursor.execute("INSERT INTO puerto VALUES (?, ?, ?)",(id_puerto, puerto_nuevo, id_analisis))
        id_puerto= id_puerto+1


    #print(objeto['analisis']['puertos_abiertos'], i)
    #for puerto in objeto['analisis']['puertos_abiertos']:
     #   cursor.execute("INSERT INTO puerto VALUES (nombre, analisis_id)", (puerto, i))

    i = i + 1
    con.commit()