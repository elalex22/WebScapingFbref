import xlsxwriter
import requests
import pandas as pd 
from bs4 import BeautifulSoup
import re
import time
import os
from func_ws import *

ligas = ["La Liga", "Serie A", "Bundesliga", "Premier League",
         "Ligue 1"]  # Ligas a considerar

años = list(range(2023, 2017, -1))  # Temporadas a considerar

tipos_tablas = [
    "standard", "keeper", "defense", "passing", "possession", "shooting"
]  # Tipos de tablas a considerar

tipos_tablas_cod = {tipo_t: i for i, tipo_t in enumerate(tipos_tablas)} # Tipos de tablas con una id asociada
tipo_dato = ["for"]  # Tipos de datos a considerar (for (local) o/y against (visitante))

carpeta = ["Descargas", "Downloads"] # Carpeta donde se van a guardar los archivos

archivos = [("ruta_archivo_total", "trabajoatd_bd_en.xlsx"),
            ("ruta_archivo_liga_año", "trabajoatd_la_en.xlsx"),
            ("ruta_archivo_csv", "bdtotal_en.csv")] # [(nombre_ruta, nombre_archivo), ...]

rutas = {} # Diccionario para almacenar las rutas de los archivos
for ruta, nom_arch in archivos:
  rutas[ruta] = crear_ruta(carpeta[0], carpeta[1], nom_arch)

df_final = pd.DataFrame()  # Crear dataframe común a todas las ligas y años
url_ini = "https://fbref.com/en/comps" # URL base 

with pd.ExcelWriter(rutas["ruta_archivo_liga_año"],
                    engine='xlsxwriter') as writer:

  for liga in ligas:
    
    n_id_liga, n_comp = extraeridliga(liga) #Manejo de ids 
    liga = liga.replace(" ", "-")  # Formato para URL

    for año in años:
      url = f"{url_ini}/{n_comp}/{año-1}-{año}/{año-1}-{año}-{liga}" #URL a scrapear
      resp = requests.get(url)
      sopa = BeautifulSoup(resp.text, "html.parser")

      df_combinado = pd.DataFrame()  # Crear dataframe común a una liga y un año
      ids_tablas_rs = [f"results{año-1}-{año}{n_id_liga}_overall"
                       ]  # Ids de las tablas de la Regular Season

      for id_rs in ids_tablas_rs:
        df_tabla = extraer_datos(sopa, id_rs)
        df_tabla = ordenar_df(df_tabla, "Squad")
        df_combinado = pd.concat([df_combinado, df_tabla], axis=1)

      for tipo_t, cod_t in tipos_tablas_cod.items():
        id_t = f"stats_squads_{tipo_t}_{tipo_dato[0]}" # ID de la tabla
        df_tabla = extraer_datos(sopa, id_t)
        if df_tabla is not None: #Postprocesado
          df_tabla = ordenar_df(df_tabla, "Squad")
          df_tabla.columns = renombrar_col(df_tabla.columns, cod_t)
          eliminar_col(df_tabla, "Squad")
          eliminar_col(df_tabla, "Playing Time")
        df_combinado = pd.concat([df_combinado, df_tabla], axis=1) 

      df_combinado.to_excel(writer, sheet_name=f"{liga}_{año}"
                            )  # Guardar la hoja de liga y año en el excel dividido por liga y año

      df_combinado["League"] = liga  # Actualizar el valor de la columna Liga
      df_combinado["Season"] = f"{año-1}-{año}"  # Actualizar el valor de la columna Año

      df_final = pd.concat([df_final, df_combinado],ignore_index=True)

    time.sleep(1)  #Esperar para que no salte la alerta antiwebscraping

df_final.to_excel(rutas["ruta_archivo_total"], engine="xlsxwriter", sheet_name="Hoja1")  # Guardar el dataframe_total en un excel
df_final.to_csv(rutas["ruta_archivo_csv"])  #Guardar el dataframe_total en un csv