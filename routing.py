# routing.py

from config import JAVIER, ANDREINA, DESTINOS
from graph_model import dijkstra, reconstruir_camino

def calcular_rutas(clave_destino):
    """
    clave_destino: "darkness", "pasion" o "rolita"
    Devuelve un diccionario con caminos y tiempos para Javier y Andreína.
    """
    if clave_destino not in DESTINOS:
        raise ValueError("Destino no válido")

    destino_info = DESTINOS[clave_destino]
    destino = destino_info["pos"]

    # Javier
    dist_j, padre_j = dijkstra(JAVIER)
    t_j = dist_j[destino]
    camino_j = reconstruir_camino(padre_j, destino)

    # Andreína
    dist_a, padre_a = dijkstra(ANDREINA)
    t_a = dist_a[destino]
    camino_a = reconstruir_camino(padre_a, destino)

    resultado = {
        "destino_nombre": destino_info["nombre"],
        "destino_pos": destino,
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

    # Información de sincronización
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
