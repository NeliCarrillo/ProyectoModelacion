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
    pos = {}
    min_calle = min(CALLES)
    max_carrera = max(CARRERAS)

    for c in CALLES:
        for k in CARRERAS:
            x = max_carrera - k      
            y = c - min_calle        
            pos[(c, k)] = (x, y)
    return pos

def camino_a_aristas(camino):
    aristas = []
    for i in range(len(camino) - 1):
        u = camino[i]
        v = camino[i + 1]
        if u < v:
            aristas.append((u, v))
        else:
            aristas.append((v, u))
    return aristas


def visualizar_rutas(resultados):
    G = construir_grafo_networkx()
    pos = posiciones_nodos()

    camino_j = resultados["javier"]["camino"]
    camino_a = resultados["andreina"]["camino"]
    aristas_j = set(camino_a_aristas(camino_j))
    aristas_a = set(camino_a_aristas(camino_a))
    aristas_comunes = aristas_j & aristas_a
    aristas_solo_j = aristas_j - aristas_comunes
    aristas_solo_a = aristas_a - aristas_comunes

    plt.figure(figsize=(8, 8))

    nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=1)

    edge_labels = nx.get_edge_attributes(G, "weight")
    edge_labels = {e: f"{w} min" for e, w in edge_labels.items()}
    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=7,
        label_pos=0.5,   # posición a la mitad de la arista
    )

    if aristas_solo_j:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=list(aristas_solo_j),
            edge_color="blue",
            width=3,
            label="Camino Javier",
        )

    if aristas_solo_a:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=list(aristas_solo_a),
            edge_color="red",
            width=3,
            label="Camino Andreína",
        )

    if aristas_comunes:
        nx.draw_networkx_edges(
            G, pos,
            edgelist=list(aristas_comunes),
            edge_color="purple",
            width=4,
            style="dashed",
            label="Tramo compartido",
        )

    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="white", edgecolors="black")

    labels = {n: f"C{n[0]}\nK{n[1]}" for n in G.nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7)

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

    mensaje_sync = resultados["sincronizacion"]["mensaje"]
    titulo = (
        f"Rutas hacia {resultados['destino_nombre']}\n"
        f"Tiempo Javier: {resultados['javier']['tiempo']} min, "
        f"Tiempo Andreína: {resultados['andreina']['tiempo']} min\n"
        f"{mensaje_sync}"
    )
    plt.title(titulo)

    plt.axis("off")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
