#inicio
# main.py
"""
Programa principal para el proyecto de modelación de sistemas de redes.

Permite seleccionar un establecimiento de destino en Bogotá y calcula
las trayectorias óptimas para Javier y Andreína, indicando quién debe
salir antes y cuánto tiempo antes para llegar simultáneamente.
"""

from city_grid import CityGrid
from routing import calcular_rutas_para_pareja


def mostrar_encabezado():
    print("=" * 70)
    print("  PROYECTO: MODELACIÓN DE REDES EN BOGOTÁ - JAVIER Y ANDREÍNA")
    print("=" * 70)
    print()


def mostrar_menu_establecimientos(city):
    """
    Muestra el menú de establecimientos y devuelve
    (nombre, (calle, carrera)) del elegido.
    """
    establecimientos = city.obtener_establecimientos()

    print("Seleccione el establecimiento de destino:")
    for i, (nombre, coord) in enumerate(establecimientos, start=1):
        calle, carrera = coord
        print(f"  {i}. {nombre}  ({CityGrid.formatear_interseccion(coord)})")

    print()

    while True:
        opcion = input("Opción (1 - {}): ".format(len(establecimientos))).strip()
        if not opcion.isdigit():
            print("  -> Por favor ingrese un número válido.")
            continue

        opcion = int(opcion)
        if 1 <= opcion <= len(establecimientos):
            nombre, coord = establecimientos[opcion - 1]
            print()
            print(f"Has seleccionado: {nombre}")
            print()
            return nombre, coord
        else:
            print("  -> Opción fuera de rango, intente nuevamente.")


def mostrar_ruta_persona(nombre_persona, info_persona):
    """
    Imprime de forma elegante la información de ruta para una persona.
    info_persona es un diccionario con claves:
      - origen
      - destino
      - camino
      - tiempo
    """
    origen = info_persona["origen"]
    destino = info_persona["destino"]
    camino = info_persona["camino"]
    tiempo = info_persona["tiempo"]

    print("-" * 70)
    print(f"{nombre_persona}:")
    print(f"  Sale de: {CityGrid.formatear_interseccion(origen)}")
    print(f"  Llega a: {CityGrid.formatear_interseccion(destino)}")
    print(f"  Tiempo total de caminata: {tiempo} minutos")
    print("  Trayectoria:")

    for i, nodo in enumerate(camino, start=1):
        print(f"    {i:2d}. {CityGrid.formatear_interseccion(nodo)}")

    print("-" * 70)
    print()


def mostrar_sincronizacion(info_sinc):
    sale_antes = info_sinc["sale_antes"]
    diferencia = info_sinc["diferencia"]

    print("=" * 70)
    print("SINCRONIZACIÓN DE LA PAREJA")
    print("=" * 70)

    if diferencia == 0:
        print("Ambos deben salir al mismo tiempo para llegar juntos al destino.")
    else:
        print(f"{sale_antes} debe salir {diferencia} minutos antes que el/la otro/a")
        print("para que lleguen simultáneamente al establecimiento.")

    print("=" * 70)
    print()


def main():
    city = CityGrid()
    mostrar_encabezado()

    # Seleccionar destino
    nombre_destino, coord_destino = mostrar_menu_establecimientos(city)

    # Calcular rutas
    resultado = calcular_rutas_para_pareja(city, coord_destino)

    # Mostrar resultados
    print(f"Destino seleccionado: {nombre_destino}")
    print(f"Ubicación: {CityGrid.formatear_interseccion(coord_destino)}")
    print()

    mostrar_ruta_persona("Javier", resultado["javier"])
    mostrar_ruta_persona("Andreína", resultado["andreina"])
    mostrar_sincronizacion(resultado["sincronizacion"])

    print("Fin del programa. ¡Que disfruten su cita (en secreto)! 😉")


if __name__ == "__main__":
    main()
