# practica1_sistemas_de_informacion
2 Conjunto de datos
Para esta practica, utilizaremos el archivo de material adicional, el cual contiene diferentes archivos. ´
• alerts.csv contiene los registros del detector de intrusos en un sistema en produccion (logs de ´
Suricata).
• devices.json contiene informacion sobre los dispositivos internos de la empresa, as ´ ´ı como un
analisis de puertos y vulnerabilidades. ´
3 Ejercicio 1 [3 puntos]
En este primer ejercicio, el grupo debera desarrollar el modelado del proceso de negocio descrito ´
anteriormente usado las dos notaciones vistas en teor´ıa: Business Process Modeling Notation (1.5
punto) y Unified Modeling Language (1.5 punto)
4 Ejercicio 2 [2 puntos]
El objetivo de este ejercicio sera el de desarrollar un sencillo sistema ETL. No es necesario desarrollar ´
las fases de extraccion ya que disponemos de los archivos correspondientes. Debemos dise ´ nar las ˜
tablas en la base de datos y desarrollar los codigos necesarios para leer los datos de los ficheros y ´
almacenarlos en la base de datos. Despu´es, sera necesario leer los datos desde la BBDD (usando ´
diferentes consultas) y se almacenaran los resultados en uno o varios DataFrames para poder ´
manipularlos. En este ejercicio, para el correcto desarrollo del sistema, sera necesario calcular los ´
siguientes valores:
• Numero de dispositivos (y campos missing o None). 
• Numero de alertas. ´
• Media y desviacion est ´ andar del total de puertos abiertos. ´
• Media y desviacion est ´ andar del n ´ umero de servicios inseguros detectados. ´
• Media y desviacion est ´ andar del n ´ umero de vulnerabilidades detectadas. ´
• Valor m´ınimo y valor maximo del total de puertos abiertos. ´
• Valor m´ınimo y valor maximo del n ´ umero de vulnerabilidades detectadas. ´
5 Ejercicio 3 [2.5 puntos]
Hay datos que nos interesa analizar en las alertas basandonos en agrupaciones, para darle un sentido ´
a nuestro analisis en base a esa agrupaci ´ on. De una manera m ´ as espec ´ ´ıfica, vamos a trabajar con las
siguientes agrupaciones:
• Por prioridad de alerta (1 son alertas graves, 2 alertas medias y 3 alertas bajas).
• Fecha. Estableceremos dos rangos: El mes de julio y el mes de agosto.
En este caso deberemos calcular la siguiente informacion para la variable de vulnerabilidades ´
detectadas en los dispositivos (Nota: en la alerta, el dispositivo puede ser el origen o el destino):
• Numero de observaciones ´
• Numero de valores ausentes (campos missing o None) ´
• Mediana
• Media
• Varianza
• Valores maximo y m ´ ´ınimo
6 Ejercicio 4 [2.5 puntos]
Por ultimo, se programar ´ an las diferentes funciones del MIS. En concreto, se deben generar gr ´ aficos ´
sencillos para obtener los siguientes datos:
• Mostrar las 10 IP de origen mas problem ´ aticas, representadas en un gr ´ afico de barras (las IPs ´
de origen mas problem ´ aticas son las que m ´ as alertas han generado con prioridad 1). ´
• Numero de alertas en el tiempo, representadas en una serie temporal. ´
• Numero de alertas por categor ´ ´ıa, representadas en un grafico de barras. ´
• Dispositivos mas vulnerables (Suma de servicios vulnerables y vulnerabilidades detectadas). ´
• Media de puertos abiertos frente a servicios inseguros y frente al total de servicios detectados.
