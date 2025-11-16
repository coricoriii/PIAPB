from .api_ghibli import GhibliAPI
import json
import pandas as pd
import os

#lista con datos que se conservaran
CAMPOS = ['rt_score', 'title', 'director', 'release_date', 'running_time']

#depuracion de datos e implementacion numerica 
def depurar(peliculas):
    peliculas_depuradas = []

    for p in (peliculas or []):
        nueva_pelicula = {}
        #depuracion de datos innecesarios
        for campo in CAMPOS:
            nueva_pelicula[campo] = p.get(campo, None)
        #convertor a valores numericos 
        for k in ('rt_score', 'release_date', 'running_time'):
            try:
                if nueva_pelicula[k] is not None:
                    nueva_pelicula[k] = int(nueva_pelicula[k])
            except (ValueError, TypeError, KeyError):
                nueva_pelicula[k] = None

        peliculas_depuradas.append(nueva_pelicula)

    return peliculas_depuradas

def guardar_datos(peliculas):
    #guarda datos del json
    with open("ghibli_depurado.json", "w", encoding="utf-8") as f:
        json.dump(peliculas, f, indent=4, ensure_ascii=False)
    #guarda los archivos con pandas
    df = pd.DataFrame(peliculas)
    df.to_csv("ghibli.csv", index=False, encoding="utf-8-sig")

#consulta API, depura los datos y genera los archivos
def ejecutar():
    api = GhibliAPI()
    peliculas = api.lista_peliculas()

    if peliculas:
        depuradas = depurar(peliculas)
        guardar_datos(depuradas)
    else:
        print("Error: no se pudieron obtener las películas")

#funcion para elimnar especificamente los archivos creados en este modulo
def eliminar_archivos():
    for archivo in ['ghibli_depurado.json', 'ghibli.csv']:
        if os.path.exists(archivo):
            os.remove(archivo)

if __name__ == "__main__":
    ejecutar()




