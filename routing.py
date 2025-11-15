# routing.py
"""
Algoritmos de búsqueda de rutas y tiempos de caminata
para Javier y Andreína en la cuadrícula de Bogotá.
"""

import heapq
from city_grid import CityGrid


def dijkstra(city, origen, destino):
    """
    Implementación del algoritmo de Dijkstra para encontrar
    el camino de menor tiempo entre dos intersecciones.

    Parámetros:
        city: instancia de CityGrid
        origen: tupla (calle, carrera)
        destino: tupla (calle, carrera)

    Retorna:
        (camino, costo_total)

        camino: lista de nodos [(calle, carrera), ...] desde origen a destino
        costo_total: tiempo total en minutos

        Si no hay camino (no debería pasar en esta cuadrícula),
        devuelve (None, None).
    """
    # Distancia mínima conocida hasta cada nodo
    dist = {}
    # Nodo previo en el camino óptimo
    prev = {}

    # Cola de prioridad: (distancia_acumulada, nodo)
    heap = []

    dist[origen] = 0
    heapq.heappush(heap, (0, origen))

    while heap:
        dist_actual, nodo_actual = heapq.heappop(heap)

        # Si ya encontramos el destino, podemos terminar
        if nodo_actual == destino:
            break

        # Si esta distancia no es la mejor conocida, la descartamos
        if dist_actual > dist.get(nodo_actual, float("inf")):
            continue

        # Recorrer vecinos
        for vecino, costo in city.vecinos(nodo_actual):
            nueva_dist = dist_actual + costo
            if nueva_dist < dist.get(vecino, float("inf")):
                dist[vecino] = nueva_dist
                prev[vecino] = nodo_actual
                heapq.heappush(heap, (nueva_dist, vecino))

    if destino not in dist:
        # No se encontró camino
        return None, None

    # Reconstruir camino desde el destino hacia atrás
    camino = []
    nodo = destino
    while nodo != origen:
        camino.append(nodo)
        nodo = prev[nodo]
    camino.append(origen)
    camino.reverse()

    return camino, dist[destino]


def calcular_rutas_para_pareja(city, destino):
    """
    Calcula las rutas óptimas para Javier y Andreína
    hacia un destino dado.

    Parámetros:
        city: instancia de CityGrid
        destino: tupla (calle, carrera)

    Retorna un diccionario con:
        {
            "javier": {
                "origen": (calle, carrera),
                "destino": (calle, carrera),
                "camino": [...],
                "tiempo": minutos
            },
            "andreina": {
                "origen": ...,
                "destino": ...,
                "camino": [...],
                "tiempo": minutos
            },
            "sincronizacion": {
                "sale_antes": "Javier" o "Andreína" o "Nadie",
                "diferencia": minutos (entero)
            }
        }
    """
    hogar_javier = city.obtener_hogar_javier()
    hogar_andreina = city.obtener_hogar_andreina()

    # Ruta de Javier
    camino_j, tiempo_j = dijkstra(city, hogar_javier, destino)
    # Ruta de Andreína
    camino_a, tiempo_a = dijkstra(city, hogar_andreina, destino)

    if camino_j is None or camino_a is None:
        # En esta cuadrícula no debería ocurrir,
        # pero lo manejamos por seguridad.
        raise RuntimeError("No se pudo encontrar ruta para uno de los dos.")

    # Cálculo de sincronización
    if tiempo_j == tiempo_a:
        sale_antes = "Nadie (salen al mismo tiempo)"
        diferencia = 0
    elif tiempo_j > tiempo_a:
        # Javier tarda más, por lo tanto debe salir antes
        sale_antes = "Javier"
        diferencia = tiempo_j - tiempo_a
    else:
        # Andreína tarda más, por lo tanto debe salir antes
        sale_antes = "Andreína"
        diferencia = tiempo_a - tiempo_j

    resultado = {
        "javier": {
            "origen": hogar_javier,
            "destino": destino,
            "camino": camino_j,
            "tiempo": tiempo_j,
        },
        "andreina": {
            "origen": hogar_andreina,
            "destino": destino,
            "camino": camino_a,
            "tiempo": tiempo_a,
        },
        "sincronizacion": {
            "sale_antes": sale_antes,
            "diferencia": diferencia,
        },
    }

    return resultado
