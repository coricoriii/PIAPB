
"""
    3. Estadísticas
    MENÚ - ESTADÍSTICAS
    1. Promedios generales (duración y calificación)
    2. Top 5 películas mejor calificadas
    3. Porcentaje de personajes por género
    4. Características físicas más comunes
    5. Colores de cabello más comunes
    6. Regresar al menú principal
"""
    
def convetir_entero(valor): 
    """
    Convierte '97', '97.0' o 97 a enteros para poder manipularlos.
    Si no se puede convertir, regresa "None" para que no genere un 
    error y se siga con el proceso.
    """
    try:
        num = str(valor).strip()
        if num.isdigit():
            return int(num)
        else:
         return int(float(num)) #Aqui se genera un error si no es un número y activa el except
    except:
        return None

def prom_duracion(peliculas):
    """Calcula el promedio de duración de las películas."""
    total = 0
    cont = 0 
    for pelicula in peliculas:
        duracion = convetir_entero(pelicula.get("running_time"))
        if duracion is not None:
            total += duracion
            cont += 1
    if cont > 0:
            return total / cont
    else:
        return 0
        
def prom_calificacion(peliculas):
    """Calcula el promedio de calificación de las películas."""
    total = 0
    cont = 0 
    for pelicula in peliculas:
        cal = convetir_entero(pelicula.get("rt_score"))
        if cal is not None:
            total += cal
            cont += 1
    if cont > 0:
        return total / cont
    else:
        return 0
 
def top5_pelis(peliculas):
    """Regresa una lista con las 5 películas mejor calificadas."""
    validas = []
    for peli in peliculas:
        rtscore = convetir_entero(peli.get("rt_score"))
        if rtscore is not None:
            peli["rt_score"] = rtscore  # Guardamos el score ya convertido a número
            validas.append(peli) # Almacenamos en la lista las con calificación válida
    
    #Usamos el "sorted" para ordenar las peliculas por calificación y "lambda" para indicar que se ordene por rt_score
    ordenadas = sorted(validas, key=lambda p: p["rt_score"], reverse=True)
    
    # Regresamos solo las primeras 5 de lista ordenada
    return ordenadas[:5]        

def porcentaje_genero(personajes):
    """Calcula el porcentaje de personajes por género."""
    cont = {}
    for per in personajes:
        # Limpiamos el valor de género
        genero = str(per.get("gender", "")).strip().lower()
        #Aqui nos saltamos los géneros vacíos o "unknown" para no contarlos 
        if genero == "" or genero.lower() in ("unknown", "na", "n/a"):
            continue

        # Contamos la cantidad por género
        if genero in cont:
            cont[genero] += 1 #Si ya existe, le sumamos 1 y se separa entre Male o Female por los valores de la llave
        else:
            cont[genero] = 1 #Si no existe, la inicializamos en 1
    total = sum(cont.values())

    # Si no hay datos válidos, regresamos lista vacía (aunque es poco probable que pase)
    if total == 0:
        return []

    # Generamos la lista de resultados con cantidad y porcentaje
    resultados = []
    for genero, cantidad in cont.items():
        porcentaje = round(cantidad * 100 / total, 2)
        resultados.append((genero,   cantidad, porcentaje))
    return resultados

def colores_ojos(personajes):
    cont = {}
    """Cuenta la frecuencia de colores de ojos entre los personajes"""
    "Nota: se parece mucho a la logica de porcentaje_genero, pero aquí solo contamos"
    for per in personajes:
        color = str(per.get("eye_color", "")).strip().lower()

        # Ignorar datos desconocidos o vacíos
        if color == "" or color.lower() in ("unknown", "na", "n/a"):
            continue

        # Contar y almacenar
        if color in cont:
            cont[color] += 1
        else:
            cont[color] = 1

    # Ordenar por más frecuentes con sorted y lambda
    ordenados = sorted(cont.items(), key=lambda x: x[1], reverse=True)
    return ordenados[:3]  # Regresar solo los 3 más comunes

def colores_cabello(personajes):
    """Cuenta la frecuencia de colores de cabello entre los personajes"""
    """Nota: es casi lo mismo que la funcion colores_ojos, pero aqui es para cabello"""
    cont = {}
    for per in personajes:
        color = str(per.get("hair_color", "")).strip().lower()
        # Ignorar datos desconocidos o vacíos
        if color == "" or color.lower() in ("unknown", "na", "n/a"):
            continue
        # Contar y almacenar
        if color in cont:
            cont[color] += 1
        else:
            cont[color] = 1
    # Ordenar de mayor a menor frecuencia
    ordenados = sorted(cont.items(), key=lambda x: x[1], reverse=True)
    return ordenados[:3]  # Regresar solo los 3 más comunes

def estadisticas(opcion, peliculas, personajes):
    # Promedios generales (duración y calificación)
    if opcion == '1':
        print(f"Peliculas cargadas: {len(peliculas)}")
        duracion = prom_duracion(peliculas)
        calificación = prom_calificacion(peliculas)
        print("\n--- PROMEDIOS ---")
        print(f"Duración promedio: {duracion:.0f} min")
        print(f"Calificación promedio: {calificación:.0f}")
    # Top 5 películas mejor calificadas
    elif opcion == '2':
        print("\n--- TOP 5 PELÍCULAS MEJOR CALIFICADAS ---")
        mejores = top5_pelis(peliculas)
        #Se usa "enumerate" para numerar las peliculas del top 5 en pares con la i y se empieza en 1
        for i, peli in enumerate(mejores, start=1):
            print(f"{i}. {peli['title']} — {peli['rt_score']}")
    # Porcentaje de personajes por género
    elif opcion == '3':
        print("\n--- PORCENTAJE DE PERSONAJES POR GÉNERO ---")
        resultados = porcentaje_genero(personajes)
        if not resultados: #Por si no hay datos válidos
            print("No hay datos de género válidos.")
        else:
            for genero, cantidad, porcentaje in resultados:
                print(f"{genero}: {cantidad} personajes ({porcentaje:.0f}%)")
    # Colores de ojos más comunes
    elif opcion == '4':
        resultado = colores_ojos(personajes)
        print("\n--- COLORES DE OJOS MÁS COMUNES ---")
        for color, cantidad in resultado:
            print(f"{color}: {cantidad} personajes")
    # Colores de cabello más comunes
    elif opcion == '5':
        resultado = colores_cabello(personajes)
        print("\n--- COLORES DE CABELLO MÁS COMUNES ---")
        for color, cantidad in resultado:
            print(f"{color}: {cantidad} personajes")
    else:
        print("Opción inválida, intente de nuevo.")
  