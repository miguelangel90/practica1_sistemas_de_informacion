import sqlite3
import json
import csv
import pandas as pd
import numpy as np

con = sqlite3.connect('p1.db')

with open('devices.json') as f:
    datos = json.load(f)



cursor = con.cursor()

cursor.execute("DROP TABLE IF  EXISTS puerto ")
cursor.execute("DROP TABLE IF  EXISTS analisis")
cursor.execute("DROP TABLE IF  EXISTS dispositivo")
cursor.execute("DROP TABLE IF  EXISTS responsable")
cursor.execute("DROP TABLE IF  EXISTS alerta")

cursor.execute('PRAGMA foreign_keys = ON')

con.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS puerto (id integer primary key AUTOINCREMENT, nombre text, analisis_id integer, "
               "FOREIGN KEY (analisis_id) REFERENCES analisis(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS analisis (id integer primary key AUTOINCREMENT, dispositivo text, servicios integer not null, servicios_inseguros integer not null, vulnerabilidades_detectadas integer not null, "
               "FOREIGN KEY (dispositivo) REFERENCES dispositivo(id))")
cursor.execute("CREATE TABLE IF NOT EXISTS responsable (nombre text primary key, tlf integer, rol text )")
cursor.execute("CREATE TABLE IF NOT EXISTS dispositivo (id text primary key, ip text not null, localizacion text, responsable text, "
               "FOREIGN KEY(responsable) REFERENCES responsable(nombre))")
cursor.execute("CREATE TABLE IF NOT EXISTS alerta (id integer primary key AUTOINCREMENT,fecha_hora text not null,sid integer not null,msg text not null,clasificacion text not null,prioridad text not null,protocolo text not null,origen text not null,destino text not null,puerto integer not null)")
con.commit()

i = 1
#id_puerto= 0
## INSERTAMOS LOS DATOS
for objeto in datos:

    ## TABLA RESPONSABLE
    nombre_responsable = objeto['responsable']['nombre']
    tlf_responsable = objeto['responsable']['telefono']
    if tlf_responsable == "None":
        tlf_responsable = None
    rol_responsable = objeto['responsable']['rol']
    cursor.execute("INSERT OR IGNORE INTO responsable VALUES (?, ?, ?)", (nombre_responsable, tlf_responsable, rol_responsable))

    ## TABLA DISPOSITIVO
    id_dispositivo = objeto['id']
    ip_dispositivo = objeto['ip']
    localizacion_dispositivo = objeto['localizacion']
    if localizacion_dispositivo == "None":
        localizacion_dispositivo = None
    cursor.execute("INSERT INTO dispositivo VALUES (?, ?, ?, ?)", (id_dispositivo, ip_dispositivo, localizacion_dispositivo, nombre_responsable))

    ## TABLA ANALISIS
    id_analisis= i
    servicio_normal=objeto["analisis"]["servicios"]
    servicio_inseguro= objeto["analisis"]["servicios_inseguros"]
    vulnerabilidad_detectada=objeto["analisis"]["vulnerabilidades_detectadas"]
    cursor.execute("INSERT INTO analisis(dispositivo, servicios, servicios_inseguros, vulnerabilidades_detectadas) VALUES (?, ?, ?, ?)",(id_dispositivo, servicio_normal, servicio_inseguro, vulnerabilidad_detectada))


    ## TABLA PUERTOS
    if objeto["analisis"]["puertos_abiertos"] != "None":
        for puerto_nuevo in objeto["analisis"]["puertos_abiertos"]:
            cursor.execute("INSERT INTO puerto(nombre, analisis_id) VALUES (?, ?)", (puerto_nuevo, id_analisis))
    i = i + 1
    con.commit()

# IMPORTAMOS EL CSV
with open('alerts.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader, None)
    for row in csvreader:
        cursor.execute('INSERT INTO alerta (fecha_hora, sid, msg, clasificacion, prioridad, protocolo, origen, destino, puerto) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', row)

    con.commit()


##  EJERCICIO 2

df = pd.read_sql_query('SELECT COUNT(id) FROM dispositivo', con)
print("Numero de dispositivos:")
print(df)

df = pd.read_sql_query("SELECT COUNT(*) FROM ALERTA WHERE MSG LIKE '%issing%'", con)
print("Numero de missings:")
print(df)

df = pd.read_sql_query('SELECT COUNT(id) FROM alerta', con)
print("Numero de alertas:")
print(df)

df = pd.read_sql_query('SELECT COUNT(analisis_id) as nPuertos FROM puerto GROUP BY analisis_id', con)
media = df['nPuertos'].dropna().mean()
desviacion = df['nPuertos'].dropna().std()
print('Media del total puertos abiertos:', media)
print('Desviación estándar del total puertos abiertos:', desviacion)


df = pd.read_sql_query('SELECT servicios_inseguros FROM analisis', con)
media = df['servicios_inseguros'].dropna().mean()
desviacion = df['servicios_inseguros'].dropna().std()
print('Media servicios_inseguros:', media)
print('Desviación estándar servicios_inseguros:', desviacion)

df = pd.read_sql_query('SELECT vulnerabilidades_detectadas FROM analisis', con)
media = df['vulnerabilidades_detectadas'].dropna().mean()
desviacion = df['vulnerabilidades_detectadas'].dropna().std()
print('Media vulnerabilidades_detectadas:', media)
print('Desviación estándar vulnerabilidades_detectadas:', desviacion)

df = pd.read_sql_query('SELECT COUNT(analisis_id) as nPuertos FROM puerto GROUP BY analisis_id', con)
print("Valor minimo y valor maximo del total de puertos abiertos:")
#conteo = df['nPuertos'].value_counts()
maximo = df['nPuertos'].max()
minimo = df['nPuertos'].min()
print('El valor máximo es: ', str(maximo))
print('El valor mínimo es: ', str(minimo))

df = pd.read_sql_query('SELECT vulnerabilidades_detectadas FROM analisis', con)
maximo = df['vulnerabilidades_detectadas'].max()
minimo = df['vulnerabilidades_detectadas'].min()
print("VValor minimo y valor maximo del numero de vulnerabilidades detectadas:")
print('El valor máximo es: ', str(maximo))
print('El valor mínimo es: ', str(minimo))


## EJERCICIO 3

## Por prioridad

df = pd.read_sql_query('SELECT prioridad, COUNT(*) as nAlertas, SUM(vulnerabilidades_detectadas) FROM alerta JOIN dispositivo ON dispositivo.ip = alerta.origen OR dispositivo.ip = alerta.destino JOIN analisis a on dispositivo.id = a.dispositivo GROUP BY prioridad', con)
print("Numero de observaciones:")
print(df)

df = pd.read_sql_query("SELECT prioridad, COUNT(*) as nMissings FROM alerta JOIN dispositivo ON dispositivo.ip = alerta.origen OR dispositivo.ip = alerta.destino JOIN analisis a on dispositivo.id = a.dispositivo  WHERE MSG LIKE '%issing%' GROUP BY prioridad", con)
print("Numero de missings:")
print(df)

df = pd.read_sql_query("SELECT vulnerabilidades_detectadas FROM alerta JOIN dispositivo ON dispositivo.ip = alerta.origen OR dispositivo.ip = alerta.destino JOIN analisis a on dispositivo.id = a.dispositivo GROUP BY prioridad", con)
mediana = df['vulnerabilidades_detectadas'].median()

print('La mediana de vulnerabilidades detectadas es: ', mediana)

df = pd.read_sql_query("SELECT prioridad, AVG(vulnerabilidades_detectadas) as Media_de_vulnerabilidades_detectadas FROM alerta JOIN dispositivo ON dispositivo.ip = alerta.origen OR dispositivo.ip = alerta.destino JOIN analisis a on dispositivo.id = a.dispositivo GROUP BY prioridad", con)
print(df)



con.close()
