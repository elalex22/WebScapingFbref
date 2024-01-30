import pandas as pd
import os


def crear_ruta(carpeta_es, carpeta_en, nombre_archivo):
  ruta_carpeta_es = os.path.join(os.path.expanduser("~"),
                                 carpeta_es)  #Ruta si tienes el SO en español
  ruta_carpeta_en = os.path.join(os.path.expanduser("~"),
                                 carpeta_en)  #Ruta si tienes el SO en inglés

  if os.path.exists(ruta_carpeta_es):
    ruta_carpeta = ruta_carpeta_es
  elif os.path.exists(ruta_carpeta_en):
    ruta_carpeta = ruta_carpeta_en
  else:
    print("No se encontró ninguna carpeta de descargas.")

  ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

  return ruta_archivo


def extraer_datos(sopa, id_tabla):
  try:
    tabla = sopa.find("table", id=id_tabla)
    if tabla is not None:
      df_tabla = pd.read_html(str(tabla))[0]
      return df_tabla
    else:
      print(f"No se encontró ninguna tabla con el ID '{id_tabla}'.")
      return None
  except pd.errors.EmptyDataError:
    print(f"Error: La tabla con ID '{id_tabla}' está vacía.")
    return None
  except Exception as e:
    print(
        f"Error al intentar extraer datos de la tabla con ID '{id_tabla}': {e}"
    )
    return None


def extraeridliga(liga):
  if "la" in liga.lower():
    return 121, 12
  elif "ligue" in liga.lower():
    return 131, 13
  elif "serie" in liga.lower():
    return 111, 11
  elif "bundesliga" in liga.lower():
    return 201, 20
  elif "premier" in liga.lower():
    return 91, 9


def ordenar_df(df, keyword):
  try:
    # Intentar ordenar el DataFrame por la columna especificada
    df_ordenado = df.sort_values(by=keyword).reset_index(drop=True)
    return df_ordenado
  except Exception as e:
    # Manejar el error si la columna especificada no existe
    if isinstance(e, KeyError):
      print(f'Error: La columna "{keyword}" no existe en el DataFrame.')
      return df
    else:
      print(f"Se produjo un error inesperado tratando de ordenar el DF.")
      return df


def renombrar_col(index, cod_t):
  try:
    nuevo_index = [
        f"{cod_t}-{nivel2}-90" if "90" in nivel1 else f"{cod_t}-{nivel2}"
        if "Unnamed" in nivel1 else f"{cod_t}-{nivel1}:{nivel2}"
        for nivel1, nivel2 in index
    ]
    index = index.droplevel(1)
    return pd.Index(nuevo_index, name=index.name)
  except Exception as e:
    print(f"Error en la función renombrar_col: {e}")


"""def eliminar_col(df, kw):
   for c in df.columns:
      if kw in c:
         df.drop(c, axis=1, inplace=True)"""


def eliminar_col(df, kw):  # Función más eficiente gracias a la vectorización
  cols_eliminar = df.filter(like=kw).columns
  try:
    df.drop(columns=cols_eliminar, inplace=True)
  except KeyError as e:
    print(f"No se encontraron columnas en el DataFrame que contengan {kw}")
  except Exception as e:
    print(f"Se produjo un error inesperado: {e}")

def tiene_numeros(linea):
  # Patrón regular para verificar si hay al menos un dígito en la línea
  patron_numeros = re.compile(r'^\d+$')
  return bool(patron_numeros.search(linea))

def transformacion_pd(df, lista):
for atr in lista:
    first_value = df.loc[:, atr].iloc[0]
    if isinstance(first_value, int):
        df[atr] = df[atr].astype(float)
    elif isinstance(first_value, str):
        try:
            df[atr] = df[atr].str.replace(',', '.').astype(float)
        except AttributeError:
            pass
return df