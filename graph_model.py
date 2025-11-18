import heapq
from config import CALLES, CARRERAS

def dentro_del_mapa(calle, carrera):
    return calle in CALLES and carrera in CARRERAS


def peso_arista(origen, destino):
    c1, k1 = origen
    c2, k2 = destino

    # Movimiento vertical (misma carrera)
    if k1 == k2 and abs(c1 - c2) == 1:
        if k1 in (11, 12, 13):  # aceras malas
            return 7
        else:
            return 5

    # Movimiento horizontal (misma calle)
    if c1 == c2 and abs(k1 - k2) == 1:
        if c1 == 51:  # calle comercial
            return 10
        else:
            return 5

    return float("inf")


def vecinos(calle, carrera):
    movimientos = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]
    for dc, dk in movimientos:
        nc, nk = calle + dc, carrera + dk
        if dentro_del_mapa(nc, nk):
            yield (nc, nk)


def dijkstra(origen):
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
            if nb not in dist or nd < dist[nb]: #relajamos un vecino
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


def construir_lista_aristas():
    aristas = []
    for c in CALLES:
        for k in CARRERAS:
            origen = (c, k)
            posibles_vecinos = [
                (c + 1, k),
                (c, k + 1),
            ]
            for destino in posibles_vecinos:
                if dentro_del_mapa(*destino):
                    w = peso_arista(origen, destino)
                    aristas.append((origen, destino, w))
    return aristas

def enumerar_caminos(origen, destino, tiempo_max=None):
    """
    Devuelve una lista de tuplas (camino, tiempo_total),
    donde 'camino' es una lista de nodos desde origen hasta destino.

    Se usa DFS con poda por tiempo máximo y sin ciclos (simple paths).
    """
    caminos = []

    def dfs(actual, tiempo_acum, camino, visitados):
        # Poda por tiempo
        if tiempo_max is not None and tiempo_acum > tiempo_max:
            return

        if actual == destino:
            caminos.append((list(camino), tiempo_acum))
            return

        for nb in vecinos(*actual):
            if nb in visitados:
                continue
            w = peso_arista(actual, nb)
            nuevo_tiempo = tiempo_acum + w
            # Poda de nuevo
            if tiempo_max is not None and nuevo_tiempo > tiempo_max:
                continue

            visitados.add(nb)
            camino.append(nb)
            dfs(nb, nuevo_tiempo, camino, visitados)
            camino.pop()
            visitados.remove(nb)

    visitados = {origen}
    dfs(origen, 0, [origen], visitados)
    return caminos
