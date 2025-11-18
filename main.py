"""
Autores: Corina García, Erick García, David Heredia
Fecha: 17/11/2025
Descripción: Programa principal que permite al usuario consultar datos de la API de Studio Ghibli
"""
from Módulos.modulo_estadisticas import estadisticas
import Módulos.manejo_datos as md
import Módulos.api_ghibli as ghibli
import time
from Módulos.json_Graficas import ejecutar, eliminar_archivos
import pandas as pd 
import matplotlib.pyplot as plt 
import re

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

# Funcion que recibe una sola pelicula y la devuelve con la lista de personajes formateada
def formatear_pelicula(pelicula, personajes):
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
    return pelicula_formateada

# Funcion que recibe la lista de diccionarios de personajes y la devuelve formateada
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

# Funcion que recibe un solo personaje y lo devuelve con la lista de peliculas formateada
def formatear_personaje(personaje, peliculas):
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
    return personaje_formateado

# Funcion que maneja las consultas web desde el menú principal
def consultas_web(opcion, api):
    if opcion == '1':
        nom = input("Ingrese el nombre de la película a consultar\n(Sugerencias: Castle in the Sky, Grave of the Fireflies): ")
        # Consultar la película por nombre usando la API
        pelicula = api.pelicula_por_nom(nom)
        if pelicula is None:
            print("Error al conectar con la API.")
        elif pelicula == {}:
            print("No se encontró ninguna película con ese nombre.")
        else:
            # Dar formato a lista de personajes
            pelicula_f = formatear_pelicula(pelicula, api.lista_personajes())
            # Imprimir la película con formato legible
            print("| INFORMACIÓN ENCONTRADA |")
            md.imprimir_pelicula(pelicula_f)
            # Agregar película al registro de consultas 
            while True:
                resp = input("¿Desea agregar esta consulta al registro de películas? (si/no): ")
                if resp.lower() == 'si':
                    md.agregar_pel_registro(pelicula_f)
                    print("Consulta agregada al registro.")
                    break
                elif resp.lower() == 'no':
                    break
                else: 
                    print("Respuesta inválida. Por favor ingrese 'si' o 'no'.")
    elif opcion == '2':
        # Buscar personaje por nombre
        nom = input("Ingrese el nombre del personaje a consultar\n(Sugerencias: Ashitaka, San, Totoro): ")
        personaje = api.personaje_por_nom(nom)
        if personaje is None:
            print("Error al conectar con la API.")
        elif personaje == {}:
            print("No se encontró ningún personaje con ese nombre.")
        else:
            # Dar formato a lista de películas
            personaje_f = formatear_personaje(personaje, api.lista_peliculas())
            # Imprimir el personaje con formato legible
            print("| INFORMACIÓN ENCONTRADA |")
            md.imprimir_personaje(personaje_f)
            # Agregar personaje al registro de consultas 
            while True:
                resp = input("¿Desea agregar esta consulta al registro de personajes? (si/no): ")
                if resp.lower() == 'si':
                    md.agregar_per_registro(personaje_f)
                    print("Consulta agregada al registro.")
                    break
                elif resp.lower() == 'no':
                    break
                else: 
                    print("Respuesta inválida. Por favor ingrese 'si' o 'no'.")
    elif opcion == '3':
        # Mostrar consultas de películas
        print("| REGISTRO DE CONSULTAS DE PELÍCULAS |")
        md.mostrar_registro_peliculas()
    elif opcion == '4':
        print("| REGISTRO DE CONSULTAS DE PERSONAJES |")
        md.mostrar_registro_personajes()
    elif opcion == '5':
        print("| REGISTRO DE CONSULTAS DE PELÍCULAS |")
        md.mostrar_registro_peliculas()
        print("| REGISTRO DE CONSULTAS DE PERSONAJES |")
        md.mostrar_registro_personajes()
    else:
        print("Opción inválida, intente de nuevo.")

# Funcion que maneja las consultas de registros desde el menú principal
def consultas_registros(opcion, peliculas, personajes):
    if opcion == '1':
        while True:
            print("="*50) 
            print("""MENU - CONSULTAS DE PELÍCULAS
            1. Buscar por nombre
            2. Buscar por director
            3. Buscar por año de lanzamiento
            4. Buscar por rango de duración
            5. Buscar por calificación mínima
            6. Regresar al menú de consultas de registros""")
            print("="*50)
            subop = input("Seleccione una opción: ")
            if subop == '6':
                break
            else:
                consultas_peliculas(subop, peliculas)
    elif opcion == '2':
        while True:
            print("="*50)
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
            while True:
                nom = input("Ingrese el nombre de la película a buscar (Sugerencias: My Neighbor Totoro): ")
                encontrados = [p for p in peliculas if p['title'].lower() == nom.lower()]
                if encontrados:
                    for pelicula in encontrados:
                        md.imprimir_pelicula(pelicula)
                else:
                    print("No se encontró ninguna película con ese nombre.")
                resp = input("¿Desea buscar otra película por nombre? (s para sí, cualquier otro caracter para regresar): ")
                if resp.lower() != 's':
                    break
        # Buscar por director
        elif opcion == '2':
            while True:
                director = input("Ingrese el nombre del director a buscar (Sugerencias: Hayao Miyazaki): ")
                encontrados = [p for p in peliculas if p['director'].lower() == director.lower()]
                if encontrados:
                    print(f"| PELÍCULAS ENCONTRADAS DEL DIRECTOR {director.upper()} |")
                    for pelicula in encontrados:
                        md.imprimir_pelicula(pelicula)
                else:
                    print("No se encontró ninguna película de ese director.")
                resp = input("¿Desea buscar otro director? (s para sí, cualquier otro caracter para regresar): ")
                if resp.lower() != 's':
                    break
        # Buscar por año de lanzamiento
        elif opcion == '3':
            while True:
                try:
                    # Usar regex para validar que la entrada es un año de 4 dígitos
                    exp_anio = re.compile(r'^\d{4}$')
                    fecha = input("Ingrese el año de lanzamiento a buscar (Sugerencias: 1988, 1991): ")
                    mo = exp_anio.search(fecha)
                    if mo:
                        break
                    else:
                        print("Entrada inválida, ingrese un año de 4 dígitos.")
                except ValueError:
                    print("Entrada inválida, ingrese un valor numérico.")
            f_encontradas = [p for p in peliculas if int(p['release_date']) == int(fecha)]
            if f_encontradas:
                print(f"| PELÍCULAS LANZADAS EN {fecha} |")
                for pelicula in f_encontradas:
                    md.imprimir_pelicula(pelicula)
            else:
                print("No se encontró ninguna película de ese año.")
        # Buscar por rango de duración
        elif opcion == '4':
            while True:
                try:
                    min_duracion = int(input("Ingrese la duración mínima (en minutos): "))
                    max_duracion = int(input("Ingrese la duración máxima (en minutos): "))
                    break
                except ValueError:
                    print("Entrada inválida, ingrese valores numéricos.")
            d_encontradas = [p for p in peliculas if min_duracion <= int(p['running_time']) <= max_duracion]
            if d_encontradas:
                print(f"| PELÍCULAS CON DURACIÓN ENTRE {min_duracion} Y {max_duracion} MINUTOS |")
                for pelicula in d_encontradas:
                    md.imprimir_pelicula(pelicula)
            else:
                print("No se encontró ninguna película en ese rango de duración.")
        # Buscar por calificación mínima
        elif opcion == '5':
            while True:
                try:
                    calificacion = int(input("Ingrese la calificación mínima (entre 0 y 100): "))
                    if 0 <= calificacion <= 100:
                        break
                except ValueError:
                    print("Entrada inválida, ingrese un valor numérico entre 0 y 100.")
            c_encontradas = [p for p in peliculas if int(p['rt_score']) >= calificacion]
            if c_encontradas:
                print(f"| PELÍCULAS CON CALIFICACIÓN MAYOR O IGUAL A {calificacion} |")
                for pelicula in c_encontradas:
                    md.imprimir_pelicula(pelicula)
            else:
                print("No se encontró ninguna película con esa calificación mínima.")
        else: 
            print('Opción inválida. Intente de nuevo')
        respuesta = input("¿Desea hacer otra consulta de películas? (s para sí, cualquier otra tecla para regresar): ")
        if respuesta.lower() != 's':
            break

def consultas_personajes(opcion, personajes):
    # Buscar por nombre
    if opcion == '1':
        while True:
            nom = input("Ingrese el nombre del personaje a buscar (Sugerencias: Totoro, Ashitaka): ")
            encontrados = [p for p in personajes if p['name'].lower() == nom.lower()]
            if encontrados:
                for personaje in encontrados:
                    md.imprimir_personaje(personaje)
            else:
                print("No se encontró ningún personaje con ese nombre.")
            resp = input("¿Desea buscar otro personaje? (s para sí, cualquier otro caracter para regresar): ")
            if resp.lower() != 's':
                break
    # Buscar por género
    elif opcion == '2':
        while True:
            genero = input("Ingrese el género a buscar (H - hombre, M - mujer, N - no especificado): ").upper()
            if genero == "H":
                print("| PERSONAJES DE GÉNERO MASCULINO |")
                for personaje in personajes:
                    if personaje['gender'].lower() == 'male':
                        md.imprimir_personaje(personaje)
            elif genero == "M":
                print("| PERSONAJES DE GÉNERO FEMENINO |")
                for personaje in personajes:
                    if personaje['gender'].lower() == 'female':
                        md.imprimir_personaje(personaje)
            elif genero == "N":
                print("| PERSONAJES DE GÉNERO NO ESPECIFICADO |")
                for personaje in personajes:
                    if personaje['gender'].lower() == "na":
                        md.imprimir_personaje(personaje)
            else:
                print("Género inválido. Intente de nuevo.")
            resp = input("¿Desea buscar otro género? (s para sí, cualquier otro caracter para regresar): ")
            if resp.lower() != 's':
                break
    # Buscar por color de ojos
    elif opcion == '3':
        while True:
            print("""MENU - COLORES DE OJOS
            1. Café
            2. Azul
            3. Negro
            4. Rojo
            5. Verde
            6. Amarillo
            7. Blanco""")
            try: 
                color = int(input("Ingrese el número correspondiente al color de ojos a buscar: "))
            except ValueError:
                print("Entrada inválida. Por favor ingrese un número.")
                return
            color_dicc = {
                '1': 'Brown',
                '2': 'Blue',
                '3': 'Black',
                '4': 'Red',
                '5': 'Green',
                '6': 'Yellow',
                '7': 'White'
            }
            if str(color) in color_dicc:
                print(f"| PERSONAJES CON OJOS DE COLOR {color_dicc[str(color)].upper()} |")
                for personaje in personajes:
                    if personaje['eye_color'].lower() == color_dicc[str(color)].lower():
                        md.imprimir_personaje(personaje)
            else:
                print("Color inválido. Intente de nuevo.")
            resp = input("¿Desea buscar otro color de ojos? (s para sí, cualquier otro caracter para regresar): ")
            if resp.lower() != 's':
                break
    # Buscar por color de cabello
    elif opcion == '4':
        while True:
            print("""MENU - COLORES DE CABELLO
            1. Café
            2. Negro
            3. Rubio
            4. Azul
            5. Verde
            6. Rojo
            7. Blanco
            8. Gris""")
            try:
                color = int(input("Ingrese el número correspondiente al color de cabello a buscar: "))
            except ValueError:
                print("Entrada inválida. Por favor ingrese un número.")
                return
            color_dicc = {
                '1': 'Brown',
                '2': 'Black',
                '3': 'Blonde',
                '4': 'Blue',
                '5': 'Green',
                '6': 'Red',
                '7': 'White',
                '8': 'Grey'
            }
            if str(color) in color_dicc:
                print(f"| PERSONAJES CON CABELLO DE COLOR {color_dicc[str(color)].upper()} |")
                for personaje in personajes:
                    if personaje['hair_color'].lower() == color_dicc[str(color)].lower():
                        md.imprimir_personaje(personaje)
            else:
                print("Color inválido. Intente de nuevo.")
            resp = input("¿Desea buscar otro color de cabello? (s para sí, cualquier otro caracter para regresar): ")
            if resp.lower() != 's':
                break
    else:
        print('Opción inválida. Intente de nuevo')
    
def graficas(opcion):
    # Leer Excel
    try:
        datos = pd.read_excel("ghibli.xlsx", engine="openpyxl")
    except FileNotFoundError:
        print("No existe 'ghibli.xlsx'. Primero genere los datos.")
        time.sleep(2)
        return

    # Convertir números
    for col in ["rt_score", "release_date", "running_time"]:
        if col in datos.columns:
            datos[col] = pd.to_numeric(datos[col], errors="coerce")

    # 1) Duraciones (barras)
    if opcion == 1:
        datos_dur = datos.dropna(subset=["running_time", "title"])
        datos_dur = datos_dur.sort_values("running_time", ascending=False)

        plt.figure(figsize=(12, 6))
        plt.bar(datos_dur["title"], datos_dur["running_time"], color="skyblue")
        plt.title("Duración de películas")
        plt.xlabel("Película")
        plt.ylabel("Minutos")
        plt.xticks(rotation=75, ha="right", fontsize=8)
        plt.grid(True, axis="y", alpha=0.5)
        plt.tight_layout()
        print('CERRAR VENTANA EMERGENTE/GRAFICA PARA CONTINUAR.')
        plt.show()

    # 2) Películas por director (pie)
    elif opcion == 2:
        conteo = datos.groupby("director")["title"].count().reset_index(name="cantidad")

        plt.figure(figsize=(8, 8))
        plt.pie(
            conteo["cantidad"],
            labels=conteo["director"],
            autopct="%1.1f%%",
            startangle=90
        )
        plt.title("Películas por director")
        plt.tight_layout()
        print('CERRAR VENTANA EMERGENTE/GRAFICA PARA CONTINUAR.')
        plt.show()

    # 3) Evolución de calificaciones
    elif opcion == 3:
        datos_anio = datos.dropna(subset=["release_date", "rt_score"])
        datos_anio = datos_anio.groupby("release_date", as_index=False)["rt_score"].mean()

        plt.figure(figsize=(10, 6))
        plt.plot(datos_anio["release_date"], datos_anio["rt_score"], marker="o")
        plt.title("Calificaciones por año")
        plt.xlabel("Año")
        plt.ylabel("Score promedio")
        plt.grid(True)
        plt.tight_layout()
        print('CERRAR VENTANA EMERGENTE/GRAFICA PARA CONTINUAR.')
        plt.show()

    else:
        print("Opción inválida.")
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
        # Consultas web
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
                    consultas_web(subop, api)
        # Consultas de registros
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
        # Estadísticas
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
        # Gráficas
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
                input('\nVolver al menu de graficas, precione cualquier tecla.')
        # Eliminar todo y salir
        elif op == '5':
            # Elimina el archivo xlsx   
            eliminar_archivos()
            # Eliminar archivos de consultas
            md.eliminar_registros()
            print('Eliminando archivos...')
            time.sleep(2)
            print('Eliminados, gracias.')
            # aqui falta el codigo para borrar los registros
            break
        else:
            print("Opción inválida, intente de nuevo.")
# Ejecutar main
main()