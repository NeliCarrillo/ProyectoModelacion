# city_grid.py
"""
Definición de la ciudad en forma de cuadrícula y reglas de tiempo por cuadra.

Zona considerada:
- Calles: 50 a 55 (crecen hacia el norte)
- Carreras: 10 a 15 (crecen hacia el oeste)

Reglas de tiempo:
- Cuadra normal: 5 minutos
- Carreras 11, 12 y 13: 7 minutos por cuadra (movimiento norte-sur)
- Calle 51: 10 minutos por cuadra (movimiento este-oeste)

Puntos importantes:
- Javier:   Calle 54 con Carrera 14
- Andreína: Calle 52 con Carrera 13

Establecimientos:
- Discoteca The Darkness: Calle 50 con Carrera 14
- Bar La Pasión:         Calle 54 con Carrera 11
- Cervecería Mi Rolita:  Calle 50 con Carrera 12
"""


class CityGrid:
    def __init__(self):
        # Límites de la cuadrícula
        self.min_calle = 50
        self.max_calle = 55
        self.min_carrera = 10
        self.max_carrera = 15

        # Puntos de origen (domicilios)
        self.javier_home = (54, 14)     # (calle, carrera)
        self.andreina_home = (52, 13)

        # Establecimientos de destino
        self.establecimientos = [
            ("Discoteca The Darkness", (50, 14)),  # Calle 50 con Carrera 14
            ("Bar La Pasión", (54, 11)),           # Calle 54 con Carrera 11
            ("Cervecería Mi Rolita", (50, 12)),    # Calle 50 con Carrera 12
        ]

    # ------------------------------
    # Utilidades de la cuadrícula
    # ------------------------------

    def es_interseccion_valida(self, calle, carrera):
        """Verifica si (calle, carrera) está dentro de la zona considerada."""
        return (
            self.min_calle <= calle <= self.max_calle and
            self.min_carrera <= carrera <= self.max_carrera
        )

    def costo_vertical(self, carrera):
        """
        Costo (en minutos) de recorrer una cuadra en sentido norte-sur
        a lo largo de una carrera dada.
        """
        if carrera in (11, 12, 13):
            return 7
        return 5

    def costo_horizontal(self, calle):
        """
        Costo (en minutos) de recorrer una cuadra en sentido este-oeste
        a lo largo de una calle dada.
        """
        if calle == 51:
            return 10
        return 5

    def obtener_vecinos_con_costo(self, nodo):
        """
        Dado un nodo (calle, carrera), devuelve una lista de vecinos
        junto con el costo de caminar hasta ellos.

        nodo: (calle, carrera)
        return: lista de tuplas (nodo_vecino, costo)
        """
        calle, carrera = nodo
        resultados = []

        # Movimiento hacia el norte: (calle + 1, carrera)
        nueva_calle = calle + 1
        if self.es_interseccion_valida(nueva_calle, carrera):
            costo = self.costo_vertical(carrera)
            resultados.append(((nueva_calle, carrera), costo))

        # Movimiento hacia el sur: (calle - 1, carrera)
        nueva_calle = calle - 1
        if self.es_interseccion_valida(nueva_calle, carrera):
            costo = self.costo_vertical(carrera)
            resultados.append(((nueva_calle, carrera), costo))

        # Movimiento hacia el este: (calle, carrera + 1)
        nueva_carrera = carrera + 1
        if self.es_interseccion_valida(calle, nueva_carrera):
            costo = self.costo_horizontal(calle)
            resultados.append(((calle, nueva_carrera), costo))

        # Movimiento hacia el oeste: (calle, carrera - 1)
        nueva_carrera = carrera - 1
        if self.es_interseccion_valida(calle, nueva_carrera):
            costo = self.costo_horizontal(calle)
            resultados.append(((calle, nueva_carrera), costo))

        return resultados

    # ------------------------------
    # Puntos especiales
    # ------------------------------

    def obtener_hogar_javier(self):
        return self.javier_home

    def obtener_hogar_andreina(self):
        return self.andreina_home

    def obtener_establecimientos(self):
        """
        Devuelve la lista de establecimientos:
        [ (nombre, (calle, carrera)), ... ]
        """
        return self.establecimientos

    # ------------------------------
    # Formato de texto
    # ------------------------------

    @staticmethod
    def formatear_interseccion(nodo):
        """
        Convierte (calle, carrera) en un texto legible:
        (54, 14) -> "Calle 54 con Carrera 14"
        """
        calle, carrera = nodo
        return f"Calle {calle} con Carrera {carrera}"
