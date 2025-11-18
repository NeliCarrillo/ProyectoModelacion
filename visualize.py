# visualize.py

import matplotlib.pyplot as plt
import networkx as nx

from config import CALLES, CARRERAS
from graph_model import construir_lista_aristas


def construir_grafo_networkx():
    G = nx.Graph()
    aristas = construir_lista_aristas()
    for u, v, w in aristas:
        G.add_edge(u, v, weight=w)
    return G


def posiciones_nodos():
    """
    Asigna posiciones (x,y) a cada nodo para dibujarlo como cuadrícula.
    Eje X: carreras (10 a 15), pero con 10 a la DERECHA y 15 a la IZQUIERDA.
    Eje Y: calles (50 a 55), de abajo hacia arriba.
    """
    pos = {}
    min_calle = min(CALLES)
    max_carrera = max(CARRERAS)

    for c in CALLES:
        for k in CARRERAS:
            # x: invertimos las carreras para que 10 quede a la derecha
            x = max_carrera - k      # carrera: 10 → x grande (derecha), 15 → x pequeño (izquierda)
            y = c - min_calle        # calle: 50 abajo, 55 arriba
            pos[(c, k)] = (x, y)
    return pos

def camino_a_aristas(camino):
    """
    Convierte una lista de nodos [n0, n1, n2,...]
    en una lista de aristas [(n0, n1), (n1, n2), ...]
    """
    aristas = []
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i + 1]
        # Como el grafo es no dirigido, normalizamos el orden
        if u < v:
            aristas.append((u, v))
        else:
            aristas.append((v, u))
    return aristas


def visualizar_rutas(resultados):
    """
    resultados: diccionario devuelto por routing.calcular_rutas
    Dibuja el grafo y resalta las rutas de Javier y Andreína.
    """
    G = construir_grafo_networkx()
    pos = posiciones_nodos()

    camino_j = resultados["javier"]["camino"]
    camino_a = resultados["andreina"]["camino"]

    # Aristas en cada camino
    aristas_j = set(camino_a_aristas(camino_j))
    aristas_a = set(camino_a_aristas(camino_a))

    # Clasificamos aristas:
    #  - comunes a ambos
    #  - solo Javier
    #  - solo Andreína
    aristas_comunes = aristas_j & aristas_a
    aristas_solo_j = aristas_j - aristas_comunes
    aristas_solo_a = aristas_a - aristas_comunes

    plt.figure(figsize=(8, 8))

    # Dibujar todas las aristas en gris claro
    nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=1)

    # Resaltar aristas de Javier (azul)
    if aristas_solo_j:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=list(aristas_solo_j),
            edge_color="blue",
            width=3,
            label="Camino Javier",
        )

    # Resaltar aristas de Andreína (rojo)
    if aristas_solo_a:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=list(aristas_solo_a),
            edge_color="red",
            width=3,
            label="Camino Andreína",
        )

    # Aristas que usan ambos (morado)
    if aristas_comunes:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=list(aristas_comunes),
            edge_color="purple",
            width=4,
            style="dashed",
            label="Tramo compartido",
        )

    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="white", edgecolors="black")

    # Etiquetas de nodos como (Cxx,Kyy)
    labels = {n: f"C{n[0]}\nK{n[1]}" for n in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7)

    # Marcar origen/destino con textos adicionales
    destino_pos = resultados["destino_pos"]
    plt.scatter(
        pos[destino_pos][0],
        pos[destino_pos][1],
        s=200,
        c="gold",
        edgecolors="black",
        zorder=5,
        label="Destino",
    )

    # Título (incluye mensaje de sincronización)
    mensaje_sync = resultados["sincronizacion"]["mensaje"]

    titulo = (
        f"Rutas hacia {resultados['destino_nombre']}\n"
        f"Tiempo Javier: {resultados['javier']['tiempo']} min, "
        f"Tiempo Andreína: {resultados['andreina']['tiempo']} min\n"
        f"{mensaje_sync}"
    )
    plt.title(titulo)


    plt.axis("off")
    plt.legend()
    plt.tight_layout()
    plt.show()
