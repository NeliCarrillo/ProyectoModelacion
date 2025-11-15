# graph_model.py

import heapq
from config import CALLES, CARRERAS

def dentro_del_mapa(calle, carrera):
    return calle in CALLES and carrera in CARRERAS


def peso_arista(origen, destino):
    """
    origen y destino son tuplas (calle, carrera) adyacentes.
    """
    c1, k1 = origen
    c2, k2 = destino

    # Movimiento vertical (misma carrera)
    if k1 == k2 and abs(c1 - c2) == 1:
        # Carreras 11,12,13 tardan 7 min por cuadra
        if k1 in (11, 12, 13):
            return 7
        else:
            return 5

    # Movimiento horizontal (misma calle)
    if c1 == c2 and abs(k1 - k2) == 1:
        # Calle 51 tarda 10 min por cuadra
        if c1 == 51:
            return 10
        else:
            return 5

    # No debería pasar si solo usamos vecinos válidos
    return float("inf")


def vecinos(calle, carrera):
    movimientos = [
        (1, 0),   # subir una calle
        (-1, 0),  # bajar una calle
        (0, 1),   # carrera +1
        (0, -1),  # carrera -1
    ]
    for dc, dk in movimientos:
        nc, nk = calle + dc, carrera + dk
        if dentro_del_mapa(nc, nk):
            yield (nc, nk)


def dijkstra(origen):
    """
    Devuelve:
    - dist: dict nodo -> distancia mínima
    - padre: dict nodo -> nodo anterior en el camino mínimo
    """
    dist = {}
    padre = {}
    heap = []

    dist[origen] = 0
    padre[origen] = None
    heapq.heappush(heap, (0, origen))

    while heap:
        d_actual, nodo = heapq.heappop(heap)
        if d_actual > dist[nodo]:
            continue

        calle, carrera = nodo
        for nb in vecinos(calle, carrera):
            w = peso_arista(nodo, nb)
            nd = d_actual + w
            if nb not in dist or nd < dist[nb]:
                dist[nb] = nd
                padre[nb] = nodo
                heapq.heappush(heap, (nd, nb))

    return dist, padre


def reconstruir_camino(padre, destino):
    camino = []
    actual = destino
    while actual is not None:
        camino.append(actual)
        actual = padre[actual]
    camino.reverse()
    return camino


# --- (Opcional) Construir grafo para networkx en visualize.py ---

def construir_lista_aristas():
    """
    Devuelve una lista de aristas (u, v, peso)
    para usar en la visualización con networkx.
    """
    aristas = []
    for c in CALLES:
        for k in CARRERAS:
            origen = (c, k)
            # Solo mirar derecha y arriba para no repetir
            posibles_vecinos = [
                (c + 1, k),   # arriba
                (c, k + 1),   # derecha
            ]
            for destino in posibles_vecinos:
                if dentro_del_mapa(*destino):
                    w = peso_arista(origen, destino)
                    aristas.append((origen, destino, w))
    return aristas
