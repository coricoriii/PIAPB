from modulo_estadisticas import estadisticas
import Módulos.api_ghibli as ghibli
import json

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

def graficas(opcion, peliculas, personajes):
    # Películas por director
    if opcion == '1':
        pass
    # Personajes por género
    elif opcion == '2':
        pass
    # Evolución de calificaciones
    elif opcion == '3':
        pass
    else:
        print("Opción inválida, intente de nuevo.")

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
    print("""STUDIO GHIBLI API
          Consulta datos y estadísticas acerca de las películas y personajes del Studio Ghibli.""")
    while True:
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
            while True:
                print("""MENU - GRÁFICAS
                    1. Películas por director
                    2. Personajes por género
                    3. Evolución de calificaciones
                    4. Regresar al menú principal""")
                subop = input("Seleccione una opción: ")
                if subop == '4':
                    break
                else:
                    graficas(subop, peliculas, personajes)
        elif op == '5':
            # aqui falta el codigo para borrar los registros
            break
        else:
            print("Opción inválida, intente de nuevo.")

main()