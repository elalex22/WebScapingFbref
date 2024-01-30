#PARA REALIZAR LA TRANSFORMACIÓN DE CADA LIGA
def transformacion_Pts(df_final):
    if df_final is not None and 'Pts' in df_final and 'MP' in df_final:
        df_final['Pts-Partido'] = (df_final['Pts'] / df_final['MP'])*38 # SACAMOS PUNTOS DE CADA EQUIPO, DIVIDIMOS POR Nº PARTIDOS Y MULTIPLICAMOS POR 38 PARA REALIZAR LA APROXIMACIÓN
    else:
        print("El DataFrame no es válido o no contiene las columnas necesarias.")
    return df_final

df_final = transformacion_Pts(df_final)

#PARA ELIMINAR DUPLICADOS
def unico(df_final,columna):
    lista=[]
    for i in df_final[columna].drop_duplicates():
        lista.append(i)
    return lista

#MEDIA DE PUNTOS CON LOS QUE TE SALVAS, EL PRIMERO QUE NO DESCIENDE
def ultimo(df_final):
    years=unico(df_final,'Season')
    leagues=unico(df_final,'League')

    dic={}
    for league in leagues:
        ligas=df_final.loc[df_final['League']==league]
        lista=[]
        for year in years:
            ligas_año=ligas.loc[ligas['Season']==year]
            descendidos=ligas_año.loc[ligas_año['Notes']=='Relegated']
            minimo=min(descendidos['Rk'])-1
            pts=ligas_año.loc[ligas_año['Rk']==minimo]
            lista.append(int(pts['Pts-Partido']))
        dic[league]=round(sum(lista)/len(lista),3)

    return dic

#MEDIA DE PUNTOS DE EQUIPOS DESCENDIDOS EN CADA LIGA
def descenso(df_final):
    #PREPROCESAMOS LOS DATOS PARA DESCENDIDOS
    section=df_final.loc[df_final['Notes']=='Relegated']

    lista=[]
    for i in section['League'].drop_duplicates():
        lista.append(i)
    dic={}

    for liga in lista:
        #DONDE REALIZAMOS COMPROBACIÓN LIGA Y SUMA PUNTOS
        liga_Pts=section.loc[section['League']==liga]
        puntos=sum(int(pts) for pts in liga_Pts['Pts-Partido'])
        dic[liga]=round(puntos/len(liga_Pts),3)

    return dic

#MEDIA DE PUNTOS DE EQUIPOS CAMPEONES EN CADA LIGA

def campeon(df_final):
    years=unico(df_final,'Season')
    leagues=unico(df_final,'League')

    dic={}
    for league in leagues:
        ligas=df_final.loc[df_final['League']==league]
        lista=[]
        for year in years:
            ligas_año=ligas.loc[ligas['Season']==year]
            campeones = ligas_año.loc[ligas_año['Rk']==1]
            lista.append(int(campeones['Pts-Partido']))
        print(lista)
        dic[league]=round(sum(lista)/len(lista),3)

    return dic
#MEDIA DE PUNTOS EQUIPOS ENTRAN EN CHAMPIONS   
def champions(df_final):

    section=df_final.loc[df_final['Notes']=='→ Champions League via league finish']

    lista=[]
    for i in section['League'].drop_duplicates():
        lista.append(i)
    avg_leagues=round((sum(int(pts) for pts in section['Pts-Partido'])/len(section)),2)
    #ligas individual
    dic={}
    for liga in lista:

        liga_Pts=section.loc[section['League']==liga]
        puntos=sum(int(pts) for pts in liga_Pts['Pts-Partido'])
        dic[liga]=round(puntos/len(liga_Pts),3)

    return dic
#MÍNIMO PARA ENTRAR EN CHAMPIONS, ES DECIR, EL ÚLTIMO EQUIPO QUE HA ENTRADO
def minimo_champions(df_final):    
    years=unico(df_final,'Season')
    leagues=unico(df_final,'League')

    dic={}
    for league in leagues:
        ligas=df_final.loc[df_final['League']==league]
        lista=[]
        for year in years:
            ligas_año=ligas.loc[ligas['Season']==year]
            entrar=ligas_año.loc[ligas_año['Notes']=='→ Champions League via league finish']
            maximo=max(entrar['Rk'])
            pts=ligas_año.loc[ligas_año['Rk']==maximo]
            lista.append(int(pts['Pts-Partido']))
        dic[league]=round(sum(lista)/len(lista),3)

    return dic

#PROGRAMA PARA REALIZAR LAS GRÁFICAS
import matplotlib.pyplot as plt
import numpy as np

diccionario_salvacion = descenso(df_final)
diccionario_descenso = ultimo(df_final)
diccionario_campeon = campeon(df_final)
diccionario_med_champions = champions(df_final)
diccionario_min_champions = minimo_champions(df_final)

# Suponiendo que x contiene las ligas
x = list(diccionario_descenso.keys())

y_camp = list(diccionario_campeon.values())
y_med_champ = list(diccionario_med_champions.values())
y_min_champ = list(diccionario_min_champions.values())
y_salv = list(diccionario_salvacion.values())
y_desc = list(diccionario_descenso.values())
bar_width = 0.15  # Ancho de cada barra

fig, ax = plt.subplots()

# Grafica las barras
bar_camp = ax.bar(np.arange(len(x)), y_camp, width=bar_width, label="MEDIA PTS CAMPEÓN")
bar_med_champ = ax.bar(np.arange(len(x)) + bar_width, y_med_champ, width=bar_width, label="MEDIA PTS CHAMPIONS")
bar_min_champ = ax.bar(np.arange(len(x)) + 2*bar_width, y_min_champ, width=bar_width, label="MEDIA PTS MÍNIMA CHAMPIONS")
bar_salv = ax.bar(np.arange(len(x)) - bar_width, y_salv, width=bar_width, label="MEDIA PTS DESCENSO")
bar_desc = ax.bar(np.arange(len(x)) - 2*bar_width, y_desc, width=bar_width, label="MEDIA PTS SALVACIÓN")

# Configura las etiquetas en el eje x
ax.set_xticks(np.arange(len(x)))
ax.set_xticklabels(x)

ax.set_title('Puntos descenso, salvación, campeonato, media y mínima Champions por liga')
ax.set_xlabel('LIGA')
ax.set_ylabel('MEDIA PUNTOS')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')  # Ajusta la posición de la leyenda
ax.grid(which = "both")
ax.minorticks_on()
ax.tick_params(which = "minor", bottom = False, left = False)
plt.show()




#DESVIACIONES

#calculo desviaciones
import numpy as np
import matplotlib.pyplot as plt

def calculo_dic_desv(liga):
    # Filtrar el DataFrame para obtener solo la liga especificada
    liga_data = df_final[df_final['League'] == liga]
    # Obtener una lista de años únicos para la liga
    years = liga_data['Season'].unique()
    # Crear un diccionario para almacenar las desviaciones estándar por año
    dic = {}
    # Calcular la desviación estándar por temporada para la liga especificada
    for year in years:
        liga_temporada = liga_data[liga_data['Season'] == year]
        desv = np.std(liga_temporada['Pts'])
        dic[year] = desv
    return dic

def calcular_promedio(diccionarios):
    count = 0
    suma = 0
    for dic in diccionarios.values():
        for value in dic.values():
            count += 1
            suma += value
    return suma / count if count > 0 else 0

def graficar_desviaciones(dic_Total, promedio_fin):
    for liga, desviaciones in dic_Total.items():
        years = list(desviaciones.keys())
        deviation_values = list(desviaciones.values())

        # Crear el gráfico para cada liga
        plt.figure(figsize=(8, 5))
        plt.bar(years, deviation_values, color='skyblue')

        # Agregar una línea horizontal para el valor promedio
        plt.axhline(y=promedio_fin, color='red', linestyle='--', label=f'Promedio: {promedio_fin:.2f}')

        plt.xlabel('Año')
        plt.ylabel('Desviación Estándar')
        plt.title(f'Desviación Estándar por Año - Liga {liga}')
        plt.xticks(rotation=45)
        plt.legend()  # Mostrar la leyenda con el valor promedio
        plt.tight_layout()
        plt.show()
descendidos=df_final.loc[df_final['Notes']=='Relegated']

# Calcular las desviaciones estándar y el promedio
dic_Total = {}
for liga in descendidos['League'].drop_duplicates():
    dic_Total[liga] = calculo_dic_desv(liga)

promedio_fin = calcular_promedio(dic_Total)

# Graficar las desviaciones estándar con la línea del promedio
graficar_desviaciones(dic_Total, promedio_fin)