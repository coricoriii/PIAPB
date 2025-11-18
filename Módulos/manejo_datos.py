"""
Módulo para manejo de datos de películas y personajes.
Contiene funciones para imprimir información en formato legible,
agregar registros de consultas a archivos de texto y mostrar dichos registros.

"""
import os 

# Funcion que recibe un diccionario de pelicula y lo imprime con formato legible
def imprimir_pelicula(pelicula):
    print(f"Título: {pelicula['title']}")
    print(f"Descripción: {pelicula['description']}")
    print(f"Director: {pelicula['director']}")
    print(f"Productor: {pelicula['producer']}")
    print(f"Año de lanzamiento: {pelicula['release_date']}")
    print(f"Duración: {pelicula['running_time']} minutos")
    print(f"Calificación {pelicula['rt_score']}")
    print("Personajes:")
    for personaje in pelicula['people']:
        print(f" - {personaje['name']}")

# Funcion que recibe un diccionario de personaje y lo imprime con formato legible
def imprimir_personaje(personaje):
    print(f"Nombre: {personaje['name']}")
    print(f"Género: {personaje['gender']}")
    print(f"Edad: {personaje['age']}")
    print(f"Color de ojos: {personaje['eye_color']}")
    print(f"Color de cabello: {personaje['hair_color']}")
    print(f"Películas:")
    for pelicula in personaje['films']:
        print(f" - {pelicula['title']}")

# Funcion que agrega una pelicula al registro de consultas en formato txt
def agregar_pel_registro(pelicula):
    with open("Reportes de consultas/consultas_peli.txt", "a") as archivo:
        archivo.write(f"Titulo: {pelicula['title']}\n")
        archivo.write(f"Descripcion: {pelicula['description']}\n")
        archivo.write(f"Director: {pelicula['director']}\n")
        archivo.write(f"Productor: {pelicula['producer']}\n")
        archivo.write(f"Fecha de lanzamiento: {pelicula['release_date']}\n")
        archivo.write(f"Duracion: {pelicula['running_time']} minutos\n")
        archivo.write(f"Calificacion {pelicula['rt_score']}\n")
        archivo.write("Personajes:\n")
        for personaje in pelicula['people']:
            archivo.write(f" - {personaje['name']}\n")
        archivo.write("\n")

# Funcion que agrega un personaje al registro de consultas en formato txt
def agregar_per_registro(personaje):
    with open("Reportes de consultas/consultas_pers.txt", "a") as archivo:
        archivo.write(f"Nombre: {personaje['name']}\n")
        archivo.write(f"Genero: {personaje['gender']}\n")
        archivo.write(f"Edad: {personaje['age']}\n")
        archivo.write(f"Color de ojos: {personaje['eye_color']}\n")
        archivo.write(f"Color de cabello: {personaje['hair_color']}\n")
        archivo.write("Peliculas:\n")
        for pelicula in personaje['films']:
            archivo.write(f" - {pelicula['title']}\n")
        archivo.write("\n")

# Funcion que muestra el contenido del archivo de registro de peliculas
def mostrar_registro_peliculas():
    try:
        with open("Reportes de consultas/consultas_peli.txt", "r") as archivo:
            contenido = archivo.read()
            print(contenido)
    except FileNotFoundError:
        print("No hay registros de consultas de películas.")

# Funcion que muestra el contenido del archivo de registro de personajes
def mostrar_registro_personajes():
    try:
        with open("Reportes de consultas/consultas_pers.txt", "r") as archivo:
            contenido = archivo.read()
            print(contenido)
    except FileNotFoundError:
        print("No hay registros de consultas de personajes.")

# Funcion que elimina los archivos de registros de consultas
def eliminar_registros():
    archivos = ["Reportes de consultas/consultas_peli.txt", "Reportes de consultas/consultas_pers.txt"]
    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)