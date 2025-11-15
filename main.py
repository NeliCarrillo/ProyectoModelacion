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

# Intentamos importar Tkinter para la ventana del mapa
try:
    import tkinter as tk
except ImportError:
    tk = None


def mostrar_encabezado():
    print("=" * 70)
    print("  PROYECTO: MODELACIÓN DE REDES EN BOGOTÁ - NELI Y SOFIA")
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


# ---------------------------------------------------------------------
# Ventana gráfica con el mapa de la cuadrícula y las rutas
# ---------------------------------------------------------------------
def mostrar_mapa_ventana(city, info_javier, info_andreina, nombre_destino):
    """
    Abre una ventana Tkinter con un mapa de la cuadrícula y
    las rutas de Javier y Andreína.

    Colores:
      - Azul     : ruta de Javier
      - Rojo     : ruta de Andreína
      - Morado   : tramo compartido
      - Amarillo : destino
      - Celeste  : casa de Javier
      - Rosa     : casa de Andreína
    """
    if tk is None:
        print("No se pudo cargar Tkinter. No es posible mostrar la ventana gráfica.")
        return

    # Datos de las rutas
    camino_j = info_javier["camino"]
    camino_a = info_andreina["camino"]
    origen_j = info_javier["origen"]
    origen_a = info_andreina["origen"]
    destino = info_javier["destino"]  # mismo que el de Andreína

    set_j = set(camino_j)
    set_a = set(camino_a)

    # Parámetros de dibujo
    cell_size = 60       # tamaño de cada cuadro en píxeles
    margin = 50          # margen para etiquetas
    filas = city.max_calle - city.min_calle + 1   # 55 - 50 + 1 = 6
    cols = city.max_carrera - city.min_carrera + 1  # 15 - 10 + 1 = 6

    width = margin + cols * cell_size + 40
    height = margin + filas * cell_size + 80

    root = tk.Tk()
    root.title(f"Mapa de rutas - {nombre_destino}")

    canvas = tk.Canvas(root, width=width, height=height, bg="white")
    canvas.pack()

    # Etiquetas de columnas (carreras)
    for idx, carrera in enumerate(range(city.min_carrera, city.max_carrera + 1)):
        x = margin + idx * cell_size + cell_size / 2
        canvas.create_text(x, margin - 20, text=f"Cr{carrera}",
                           font=("Arial", 10, "bold"))

    # Etiquetas de filas (calles)
    # Las calles van de max_calle (arriba) a min_calle (abajo)
    for idx, calle in enumerate(range(city.max_calle, city.min_calle - 1, -1)):
        y = margin + idx * cell_size + cell_size / 2
        canvas.create_text(margin - 30, y, text=f"Cl{calle}",
                           font=("Arial", 10, "bold"))

    # Dibujar la cuadrícula y colorear según quién pasa
    for fila_idx, calle in enumerate(range(city.max_calle, city.min_calle - 1, -1)):
        for col_idx, carrera in enumerate(range(city.min_carrera, city.max_carrera + 1)):
            x0 = margin + col_idx * cell_size
            y0 = margin + fila_idx * cell_size
            x1 = x0 + cell_size
            y1 = y0 + cell_size

            nodo = (calle, carrera)

            # Determinar color y texto de la celda
            fill = "white"
            text = ""

            if nodo == destino:
                fill = "yellow"
                text = "D"
            elif nodo == origen_j:
                fill = "lightblue"
                text = "J"
            elif nodo == origen_a:
                fill = "pink"
                text = "A"
            elif nodo in set_j and nodo in set_a:
                fill = "violet"
            elif nodo in set_j:
                fill = "blue"
            elif nodo in set_a:
                fill = "red"

            canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline="gray")

            if text:
                canvas.create_text(
                    (x0 + x1) / 2,
                    (y0 + y1) / 2,
                    text=text,
                    font=("Arial", 12, "bold")
                )

    # Leyenda en la parte inferior
    legend_y = margin + filas * cell_size + 10

    def cuadrito_leyenda(x, color, label):
        size = 15
        canvas.create_rectangle(x, legend_y, x + size, legend_y + size,
                                fill=color, outline="black")
        canvas.create_text(x + size + 40, legend_y + size / 2,
                           text=label, anchor="w", font=("Arial", 9))

    x_legend = margin
    cuadrito_leyenda(x_legend, "lightblue", "Casa Javier")
    x_legend += 160
    cuadrito_leyenda(x_legend, "pink", "Casa Andreína")
    x_legend += 180
    cuadrito_leyenda(x_legend, "yellow", "Destino")

    legend_y += 25
    x_legend = margin
    cuadrito_leyenda(x_legend, "blue", "Ruta Javier")
    x_legend += 160
    cuadrito_leyenda(x_legend, "red", "Ruta Andreína")
    x_legend += 180
    cuadrito_leyenda(x_legend, "violet", "Tramo compartido")

    root.mainloop()


def main():
    city = CityGrid()
    mostrar_encabezado()

    # Seleccionar destino
    nombre_destino, coord_destino = mostrar_menu_establecimientos(city)

    # Calcular rutas
    resultado = calcular_rutas_para_pareja(city, coord_destino)

    # Mostrar resultados en consola
    print(f"Destino seleccionado: {nombre_destino}")
    print(f"Ubicación: {CityGrid.formatear_interseccion(coord_destino)}")
    print()

    mostrar_ruta_persona("Javier", resultado["javier"])
    mostrar_ruta_persona("Andreína", resultado["andreina"])
    mostrar_sincronizacion(resultado["sincronizacion"])

    # Ventana gráfica con el mapa de las rutas
    mostrar_mapa_ventana(city, resultado["javier"], resultado["andreina"], nombre_destino)

    print("Fin del programa. ¡Que disfruten su cita (en secreto)! 😉")


if __name__ == "__main__":
    main()
