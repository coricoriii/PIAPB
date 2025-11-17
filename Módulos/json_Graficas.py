from .api_ghibli import GhibliAPI
import json
import openpyxl
import os

# Campos que guardaremos
CAMPOS = ['rt_score', 'title', 'director', 'release_date', 'running_time']

def depurar(lista_peliculas):
    #Quita datos que no usamos y convierte números.
    peliculas_limpias = []

    for peli in (lista_peliculas or []):
        nueva = {campo: peli.get(campo, None) for campo in CAMPOS}

        # Convertir valores numéricos
        for campo in ('rt_score', 'release_date', 'running_time'):
            try:
                if nueva[campo] is not None:
                    nueva[campo] = int(nueva[campo])
            except:
                nueva[campo] = None

        peliculas_limpias.append(nueva)

    return peliculas_limpias


def guardar_datos(peliculas_limpias):
    # Guardar JSON
    with open("ghibli_depurado.json", "w", encoding="utf-8") as archivo_json:
        json.dump(peliculas_limpias, archivo_json, indent=4, ensure_ascii=False)

    # Guardar Excel
    libro = openpyxl.Workbook()
    hoja = libro.active
    hoja.title = "Películas"

    hoja.append(CAMPOS)

    for peli in peliculas_limpias:
        fila = [peli.get(campo, None) for campo in CAMPOS]
        hoja.append(fila)

    libro.save("ghibli.xlsx")


def ejecutar():
    #Consulta API, depura y guarda.
    api = GhibliAPI()
    peliculas_api = api.lista_peliculas()

    if peliculas_api:
        peliculas_limpias = depurar(peliculas_api)
        guardar_datos(peliculas_limpias)
    else:
        print("No se pudieron obtener las películas")


def eliminar_archivos():
    #Borra los archivos generados, solo de este modulo. 
    for archivo in ["ghibli_depurado.json", "ghibli.xlsx"]:
        if os.path.exists(archivo):
            os.remove(archivo)


if __name__ == "__main__":
    ejecutar()
