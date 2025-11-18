# routing.py

from config import JAVIER, ANDREINA, DESTINOS
from graph_model import dijkstra, enumerar_caminos, reconstruir_camino


def caminos_razonables(origen, destino, margen_extra=20):
    """
    Genera caminos desde 'origen' a 'destino' que no sean
    mucho peores que el óptimo.
    """
    dist, _ = dijkstra(origen)
    t_min = dist[destino]
    tiempo_max = t_min + margen_extra

    todos = enumerar_caminos(origen, destino, tiempo_max=tiempo_max)
    # Ordenar por tiempo creciente
    todos.sort(key=lambda ct: ct[1])
    return todos


def elegir_pareja_de_caminos(caminos_j, caminos_a, destino):
    """
    Elige un par (camino_j, camino_a) que:
      - no comparta nodos intermedios,
      - minimice tiempo_j + tiempo_a.

    caminos_j y caminos_a son listas de (camino, tiempo).
    """
    mejor = None
    mejor_costo = float("inf")

    for camino_j, t_j in caminos_j:
        nodos_j = set(camino_j[:-1])  # excluimos el destino
        for camino_a, t_a in caminos_a:
            nodos_a = set(camino_a[:-1])
            # Intersección de nodos intermedios: si hay, se descarta
            if nodos_j & nodos_a:
                continue

            costo = t_j + t_a
            if costo < mejor_costo:
                mejor_costo = costo
                mejor = (camino_j, t_j, camino_a, t_a)

    return mejor


def calcular_rutas(destino):
    """
    destino puede ser:
      - una clave de DESTINOS (str), por ejemplo: "darkness", "pasion", "rolita"
      - una tupla (calle, carrera) para un destino personalizado, por ejemplo: (52, 11)
    """
    # 1. Determinar posición y nombre del destino
    if isinstance(destino, str):
        if destino not in DESTINOS:
            raise ValueError("Destino no válido")

        destino_info = DESTINOS[destino]
        destino_pos = destino_info["pos"]
        destino_nombre = destino_info["nombre"]
    else:
        # asumimos que es una tupla (calle, carrera)
        destino_pos = destino
        destino_nombre = f"Destino personalizado (Calle {destino_pos[0]}, Carrera {destino_pos[1]})"

    # 2. Caminos razonables para cada uno
    caminos_j = caminos_razonables(JAVIER, destino_pos, margen_extra=20)
    caminos_a = caminos_razonables(ANDREINA, destino_pos, margen_extra=20)

    mejor = elegir_pareja_de_caminos(caminos_j, caminos_a, destino_pos)

    # Si no encontramos ninguna pareja que no se cruce,
    # hacemos fallback a los caminos más cortos individuales:
    if mejor is None:
        dist_j, padre_j = dijkstra(JAVIER)
        dist_a, padre_a = dijkstra(ANDREINA)

        camino_j = reconstruir_camino(padre_j, destino_pos)
        camino_a = reconstruir_camino(padre_a, destino_pos)
        t_j = dist_j[destino_pos]
        t_a = dist_a[destino_pos]
    else:
        camino_j, t_j, camino_a, t_a = mejor

    resultado = {
        "destino_nombre": destino_nombre,
        "destino_pos": destino_pos,
        "javier": {
            "origen": JAVIER,
            "camino": camino_j,
            "tiempo": t_j,
        },
        "andreina": {
            "origen": ANDREINA,
            "camino": camino_a,
            "tiempo": t_a,
        },
    }

    # Sincronización de salida
    if t_j == t_a:
        resultado["sincronizacion"] = {
            "tipo": "simultaneo",
            "mensaje": "Ambos pueden salir al mismo tiempo y llegarán juntos.",
        }
    elif t_j > t_a:
        diferencia = t_j - t_a
        resultado["sincronizacion"] = {
            "tipo": "javier_antes",
            "diferencia": diferencia,
            "mensaje": f"Javier debe salir {diferencia} minutos antes que Andreína.",
        }
    else:
        diferencia = t_a - t_j
        resultado["sincronizacion"] = {
            "tipo": "andreina_antes",
            "diferencia": diferencia,
            "mensaje": f"Andreína debe salir {diferencia} minutos antes que Javier.",
        }

    return resultado
