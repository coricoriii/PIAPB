import requests
import json

class GhibliAPI:
    def __init__(self):
        self.url = "https://ghibliapi.vercel.app"

    # Método para realizar una solicitud GET a la API
    def consulta_api(self, endpoint):
        try:
            response = requests.get(f"{self.url}/{endpoint}")
            response.raise_for_status()  # Verifica si la respuesta fue exitosa
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al consultar la API: {e}")
            return None
    
    def pelicula_por_nom(self, nombre):
        peliculas = self.consulta_api("films")
        # Si la consulta fue exitosa
        if peliculas:
            # Buscar coincidencia exacta
            for pelicula in peliculas:
                if pelicula['title'].lower() == nombre.lower():
                    return pelicula # Tipo de dato: dict
            return {}  # Retorna dict vacío si no encuentra coincidencias
        return None  # Retorna None si hay error de conexión
    
    def personaje_por_nom(self, nombre):
        personajes = self.consulta_api("people")
        # Si la consulta fue exitosa
        if personajes:
            # Buscar coincidencia exacta
            for personaje in personajes:
                if personaje['name'].lower() == nombre.lower():
                    return personaje # Tipo de dato: dict
            return {}  # Retorna dict vacío si no encuentra coincidencias
        return None  # Retorna None si hay error de conexión
    
    def lista_peliculas(self):
        peliculas = self.consulta_api("films")
        return peliculas  # Tipo de dato: lista de diccionarios
    
    def lista_personajes(self):
        personajes = self.consulta_api("people")
        return personajes  # Tipo de dato: lista de diccionarios
