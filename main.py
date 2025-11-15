# main.py

from routing import calcular_rutas
from visualize import visualizar_rutas

def imprimir_camino(nombre, camino, tiempo):
    print(f"\nTrayectoria de {nombre}:")
    for i, (calle, carrera) in enumerate(camino):
        print(f"  Paso {i}: Calle {calle} con Carrera {carrera}")
    print(f"Tiempo total de caminata de {nombre}: {tiempo} minutos")


def elegir_destino():
    print("Establecimientos disponibles:")
    print("  1. Discoteca The Darkness")
    print("  2. Bar La Pasión")
    print("  3. Cervecería Mi Rolita")
    op = input("Elija destino (1/2/3): ").strip()

    if op == "1":
        return "darkness"
    elif op == "2":
        return "pasion"
    elif op == "3":
        return "rolita"
    else:
        print("Opción inválida.")
        return None


def main():
    clave_destino = elegir_destino()
    if clave_destino is None:
        return

    resultados = calcular_rutas(clave_destino)

    print(f"\nDestino elegido: {resultados['destino_nombre']} "
          f"en Calle {resultados['destino_pos'][0]}, "
          f"Carrera {resultados['destino_pos'][1]}")

    # Mostrar caminos en consola
    imprimir_camino("Javier",
                    resultados["javier"]["camino"],
                    resultados["javier"]["tiempo"])
    imprimir_camino("Andreína",
                    resultados["andreina"]["camino"],
                    resultados["andreina"]["tiempo"])

    print("\n--- Sincronización de salida ---")
    print(resultados["sincronizacion"]["mensaje"])

    # Preguntar si quiere ver el grafo
    ver = input("\n¿Desea ver el grafo con los caminos resaltados? (s/n): ").strip().lower()
    if ver == "s":
        visualizar_rutas(resultados)


if __name__ == "__main__":
    main()
