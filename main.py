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

def main():
    api = ghibli.GhibliAPI()
    # Consultar datos completos de API
    pel = api.lista_peliculas()
    per = api.lista_personajes()
    # Listas finales formateadas
    peliculas = formatear_peliculas(pel, per)
    personajes = formatear_personajes(per, pel)
main()