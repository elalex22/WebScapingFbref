import pandas as pd
import matplotlib.pyplot as plt
import re

archivo_csv = 'C:/Users/anava/Documents/CIENCIA DE DATOS/2do año/1er cuatri/ATD/TRABAJO ATD/bd_atd_en.csv'

df = pd.read_csv(archivo_csv, delimiter=';',encoding='latin-1')
df_gk=transformacion_pd(df_gk,lista_puerta2)
df_ord=df_gk.sort_values(by='1-Performance:Save%', ascending=False)
delfin=df_ord.loc[:,['Goalkeeper','Squad','Season','1-Performance:GA90','1-Performance:Save%','1-Performance:CS%','1-Penalty Kicks:PKatt','1-Penalty Kicks:Save%']].head(25)

delfin #segunda foto de la diapositiva

# Extraer las columnas de interés
data={'Portero':delfin['Goalkeeper'],
'Porcentaje de Paradas':delfin['1-Performance:Save%'],
'Porcentaje de Porteria a 0':delfin['1-Performance:CS%']}

# Crear el gráfico de barras
td = pd.DataFrame(data)
td.plot(kind='bar', width=ancho_barras)

# Agregar etiquetas y título
plt.xlabel('Portero')

plt.title('Porcentaje de Paradas de cada Portero ')
plt.legend(loc='upper left', bbox_to_anchor=(1,1))
# Rotar las etiquetas del eje x para mejorar la legibilidad
plt.xticks(rotation=45, ha='right')

# Mostrar el gráfico
plt.show()
#gráfico de barras de la diapositiva