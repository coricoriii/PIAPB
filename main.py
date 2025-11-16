import Módulos.api_ghibli as ghibli
import time
from Módulos.json_Graficas import ejecutar, eliminar_archivos
import pandas as pd 
import matplotlib.pyplot as plt 


# Funcion que recibe la lista de diccionarios de peliculas y la devuelve
# sin datos innecesarios y con la lista de personajes formateada
def formatear_peliculas(peliculas, personajes):
    peliculas_formateadas = []
    for pelicula in peliculas:
        pelicula_formateada = {
            "id": pelicula["id"],
            "title": pelicula["title"],
            "description": pelicula["description"],
            "director": pelicula["director"],
            "producer": pelicula["producer"],
            "release_date": pelicula["release_date"],
            "running_time": pelicula["running_time"],
            "rt_score": pelicula["rt_score"],
            "people": []
        }
        # Recorremos la lista de URLs de personajes asociadas a los personajes
        for personaje_url in pelicula["people"]:
            # Ignorar la URL genérica que apunta a todos los personajes
            if personaje_url == "https://ghibliapi.vercel.app/people/":
                continue
            # Buscar el personaje correspondiente
            personaje = None
            for p in personajes:
                if p["url"] == personaje_url:
                    personaje = p
                    break
            # Si se encontró el personaje, agregar el nombre
            if personaje:
                pelicula_formateada["people"].append({
                    "name": personaje.get("name")
                })
        peliculas_formateadas.append(pelicula_formateada)
    return peliculas_formateadas

def formatear_personajes(personajes, peliculas):
    personajes_formateados = []
    for personaje in personajes:
        personaje_formateado = {
            "id": personaje["id"],
            "name": personaje["name"],
            "gender": personaje["gender"],
            "age": personaje["age"],
            "eye_color": personaje["eye_color"],
            "hair_color": personaje["hair_color"],
            "films": []
        }
        # Recorremos la lista de URLs de películas asociadas a los personajes
        for pelicula_url in personaje["films"]:
            # Buscar la película correspondiente
            pelicula = None
            for p in peliculas:
                if p["url"] == pelicula_url:
                    pelicula = p
                    break
            # Si se encontró la película, agregar el título
            if pelicula:
                personaje_formateado["films"].append({
                    "title": pelicula.get("title")
                })
        personajes_formateados.append(personaje_formateado)
    return personajes_formateados

def consultas_web(opcion):
    if opcion == '1':
        nom = input("Ingrese el nombre de la película a consultar\n(Sugerencias: Castle in the Sky, Grave of the Fireflies): ")
        # pendiente
    elif opcion == '2':
        pass
    elif opcion == '3':
        pass
    elif opcion == '4':
        pass
    elif opcion == '5':
        pass
    else:
        print("Opción inválida, intente de nuevo.")

def consultas_registros(opcion, peliculas, personajes):
    if opcion == '1':
        while True: 
            print("""MENU - CONSULTAS DE PELÍCULAS
            1. Buscar por nombre
            2. Buscar por director
            3. Buscar por año de lanzamiento
            4. Buscar por rango de duración
            5. Buscar por calificación mínima
            6. Regresar al menú de consultas de registros""")
            subop = input("Seleccione una opción: ")
            if subop == '6':
                break
            else:
                consultas_peliculas(subop, peliculas)
    elif opcion == '2':
        while True:
            print("""MENU - CONSULTAS DE PERSONAJES
        1. Buscar por nombre
        2. Buscar por género
        3. Buscar por color de ojos
        4. Buscar por color de cabello
        5. Regresar al menú de consultas de registros""")
            subop = input("Seleccione una opción: ")
            if subop == '5':
                break
            else:
                consultas_personajes(subop, personajes)
    else:
        print("Opción inválida, intente de nuevo.")    

def consultas_peliculas(opcion, peliculas):
    while True:
        # Buscar por nombre
        if opcion == '1':
            nom = input("Ingrese el nombre de la película a buscar: ")
        # Buscar por director
        elif opcion == '2':
            pass
        # Buscar por año de lanzamiento
        elif opcion == '3':
            pass
        # Buscar por rango de duración
        elif opcion == '4':
            pass
        # Buscar por calificación mínima
        elif opcion == '5':
            pass
        else: 
            print('Opción inválida. Intente de nuevo')
        respuesta = input("¿Desea hacer otra consulta de películas? (s para sí, cualquier otra tecla para regresar): ")
        if respuesta.lower() != 's':
            break

def consultas_personajes(opcion, personajes):
    # Buscar por nombre
    if opcion == '1':
        pass
    # Buscar por género
    elif opcion == '2':
        pass
    # Buscar por color de ojos
    elif opcion == '3':
        pass
    # Buscar por color de cabello
    elif opcion == '4':
        pass
    else:
        print('Opción inválida. Intente de nuevo')

def estadisticas(opcion, peliculas, personajes):
    # Promedios generales (duración y calificación)
    if opcion == '1':
        pass
    # Top 5 películas mejor calificadas
    elif opcion == '2':
        pass
    # Porcentaje de personajes por género
    elif opcion == '3':
        pass
    # Características físicas más comunes
    elif opcion == '4':
        pass
    # Colores de cabello más comunes
    elif opcion == '5':
        pass
    else:
        print("Opción inválida, intente de nuevo.")
    
def graficas(opcion):
    # Intentar leer el CSV 
    try:
        df = pd.read_csv("ghibli.csv", encoding="utf-8-sig")
    except FileNotFoundError:
        print("No se encontró 'ghibli.csv'. Primero genera los datos desde el menú de Gráficas.")
        time.sleep(2)
        return

    # Convertir columnas numéricas
    for col in ["rt_score", "release_date", "running_time"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 1) Duración por película (barras)
    if opcion == 1:
        df_dur = df.dropna(subset=["running_time", "title"])
        df_dur = df_dur.sort_values("running_time", ascending=False)

        plt.figure(figsize=(12, 6))
        plt.bar(df_dur["title"], df_dur["running_time"], color="skyblue")
        plt.title("Duración de películas (minutos)")
        plt.xlabel("Película")
        plt.ylabel("Duración (min)")
        plt.xticks(rotation=75, ha="right", fontsize=8)
        plt.grid(True, axis="y", alpha=0.5)
        plt.tight_layout()
        print('cierre la grafica/pantalla emergente para poder continuar')
        plt.show()
        

    # 2) Películas por director (grafica pie)
    elif opcion == 2:
        conteo = (
            df.groupby("director")["title"]
              .count()
              .reset_index(name="num_peliculas")
        )

        plt.figure(figsize=(8, 8))
        plt.pie(
            conteo["num_peliculas"],
            labels=conteo["director"],
            autopct="%1.1f%%",
            startangle=90
        )
        plt.title("Distribución de películas por director")
        plt.tight_layout()
        print('cierre la grafica/pantalla emergente para poder continuar')
        plt.show()

    # 3) Evolución de calificaciones (grafica lineal)
    elif opcion == 3:
        df_year = df.dropna(subset=["release_date", "rt_score"])
        df_year = (
            df_year.groupby("release_date", as_index=False)["rt_score"]
                   .mean()
                   .sort_values("release_date")
        )

        plt.figure(figsize=(10, 6))
        plt.plot(df_year["release_date"], df_year["rt_score"], marker="o")
        plt.title("Evolución de calificaciones (promedio por año)")
        plt.xlabel("Año de lanzamiento")
        plt.ylabel("Puntuación promedio (rt_score)")
        plt.grid(True)
        plt.tight_layout()
        print('cierre la grafica/pantalla emergente para poder continuar')
        plt.show()

    else:
        print("Opción inválida en el menú de gráficas.")
        time.sleep(1)
 
def main():
    # Inicializando
    api = ghibli.GhibliAPI()
    # Consultar datos completos de API
    pel = api.lista_peliculas()
    per = api.lista_personajes()
    # Listas finales formateadas
    peliculas = formatear_peliculas(pel, per)
    personajes = formatear_personajes(per, pel)
    # Menu principal 
    print('='*100)
    print("""\t\t\t\t\tSTUDIO GHIBLI API
          Consulta datos y estadísticas acerca de las películas y personajes del Studio Ghibli.""")
    while True:
        print('='*100)
        print("""MENÚ PRINCIPAL
            1. Consultas web
            2. Consultas de registros
            3. Estadísticas
            4. Gráficas
            5. Borrar todo y finalizar""")
        op = input("Seleccione una opción: ")
        if op == '1':
            while True:
                print("""MENU - CONSULTAS WEB
            1. Consultar películas
            2. Consultar personajes
            3. Mostrar consultas de películas
            4. Mostrar consultas de personajes
            5. Mostrar todas las consultas
            6. Regresar al menú principal""")
                subop = input("Seleccione una opción: ")
                if subop == '6':
                    break
                else:
                    consultas_web(subop)
        elif op == '2':
            while True:
                print("""MENU - CONSULTAS DE REGISTROS
                    1. Consultar películas
                    2. Consultar personajes
                    3. Regresar al menú principal""")
                subop = input("Seleccione una opción: ")
                if subop == '3':
                    break
                else:
                    consultas_registros(subop,peliculas,personajes)
        elif op == '3':
            while True:
                print("""MENU - ESTADÍSTICAS
                    1. Promedios generales (duración y calificación)
                    2. Top 5 películas mejor calificadas
                    3. Porcentaje de personajes por género
                    4. Características físicas más comunes
                    5. Colores de cabello más comunes
                    6. Regresar al menú principal""")
                subop = input("Seleccione una opción: ")
                if subop == '6':
                    break
                else:
                    estadisticas(subop, peliculas, personajes)
        elif op == '4':
            #llama a la funcion de ejecutar de modulo creado 
            ejecutar()
            while True:
                print('='*100)
                print("""MENU - GRÁFICAS
                    1. Duracion de peliculas (barras)
                    2. Peliculas por Director (barra pie)
                    3. Evolución de calificaciones (lineal)
                    4. Regresar al menú principal""")
                subop = input("Seleccione una opción: ")
                #validaciones
                if not subop.isdigit(): 
                    print('Solo se aceptan digitios, porfavor ingrese una opcion valida.\n')
                    time.sleep(2)
                    continue
                subop=int(subop)
                if subop <= 0 or subop > 4: 
                    print('Opcion invalida, ingrese un numero valido de submenu.\n')
                    time.sleep(2)
                    continue
                if subop == 4:
                    break
                #llama a la funcion gracias
                graficas(subop)
                #Volver al menu de graficas
                input('\n Volver al menu de graficas, precione cualquier tecla.')
        elif op == '5':
            eliminar_archivos()
            print('eliminando archivos...')
            time.sleep(2)
            print('eliminados, gracias.')
            # aqui falta el codigo para borrar los registros
            break
        else:
            print("Opción inválida, intente de nuevo.")

main()