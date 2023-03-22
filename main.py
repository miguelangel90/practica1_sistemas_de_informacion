import sqlite3

con = sqlite3.connect('p1.db')

cursor = con.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS dispositivo (id text primary key, ip text, localizacion text, responsable integer, analisis integer)")
cursor.execute("CREATE TABLE IF NOT EXISTS analisis (id integer primary key AUTOINCREMENT, puertos_abiertos text, servicios integer, servicios_inseguros integer, vulnerabilidades_detectadas integer)")
cursor.execute("CREATE TABLE IF NOT EXISTS responsable (nombre text primary key, tlf integer, rol text)")
cursor.execute("CREATE TABLE IF NOT EXISTS puerto (id integer primary key AUTOINCREMENT, nombre text, analisis_id integer)")
con.commit()