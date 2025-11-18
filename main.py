# main.py

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from routing import calcular_rutas
from visualize import visualizar_rutas


def imprimir_camino(nombre, camino, tiempo):
    print(f"\nTrayectoria de {nombre}:")
    for i, (calle, carrera) in enumerate(camino):
        print(f"  Paso {i}: Calle {calle} con Carrera {carrera}")
    print(f"Tiempo total de caminata de {nombre}: {tiempo} minutos")


def ejecutar_calculo(destino):
    """
    'destino' puede ser:
      - str: clave de DESTINOS ("darkness", "pasion", "rolita")
      - tuple: (calle, carrera) para destino personalizado
    """
    resultados = calcular_rutas(destino)

    print(f"\nDestino elegido: {resultados['destino_nombre']} "
          f"en Calle {resultados['destino_pos'][0]}, "
          f"Carrera {resultados['destino_pos'][1]}")

    imprimir_camino("Javier",
                    resultados["javier"]["camino"],
                    resultados["javier"]["tiempo"])

    imprimir_camino("Andreína",
                    resultados["andreina"]["camino"],
                    resultados["andreina"]["tiempo"])

    print("\n--- Sincronización de salida ---")
    print(resultados["sincronizacion"]["mensaje"])

    visualizar_rutas(resultados)


def main():
    # ------- Ventana principal -------
    root = tk.Tk()
    root.title("Proyecto de Modelación de Sistemas de Redes")
    root.geometry("550x460")
    root.configure(bg="#e8eff7")  # Color suave

    # ------- Título -------
    titulo = tk.Label(
        root,
        text="Proyecto de Modelación de Sistemas de Redes",
        font=("Helvetica", 18, "bold"),
        bg="#e8eff7",
        fg="#1f3c88",
        wraplength=500,
        justify="center"
    )
    titulo.pack(pady=15)

    # ------- Subtítulo -------
    subtitulo = tk.Label(
        root,
        text="Integrantes:\nNelson Carrillo • José Francisco • Luis Pérez",
        font=("Helvetica", 12),
        bg="#e8eff7",
        fg="#3a4750",
        justify="center",
    )
    subtitulo.pack(pady=5)

    # ------- Frame para botones -------
    frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
    frame.pack(pady=30, padx=20)

    label_opciones = tk.Label(
        frame,
        text="Seleccione el destino:",
        font=("Helvetica", 14, "bold"),
        bg="#ffffff",
        fg="#303841"
    )
    label_opciones.pack(pady=15)

    # ------- Estilo de los botones -------
    estilo = ttk.Style()
    estilo.configure(
        "TButton",
        font=("Helvetica", 12),
        padding=10
    )

    # -------- Función auxiliar para pedir números con validación --------
    def pedir_entero_en_rango(texto, minimo, maximo):
        """
        Pide un número entero con simpledialog y valida:
        - que sea entero
        - que esté entre [minimo, maximo]
        Devuelve el número o None si el usuario cancela.
        """
        while True:
            valor = simpledialog.askstring(
                "Destino personalizado",
                texto,
                parent=root
            )
            if valor is None:  # Cancelar
                return None

            valor = valor.strip()

            if not valor.isdigit():
                messagebox.showerror("Valor inválido", "Debe ingresar un número entero.")
                continue

            numero = int(valor)
            if numero < minimo or numero > maximo:
                messagebox.showerror(
                    "Fuera de rango",
                    f"El valor debe estar entre {minimo} y {maximo}."
                )
                continue

            return numero

    # -------- Botón para destino personalizado --------
    def destino_personalizado():
        # Pedir CALLE (50–55)
        calle = pedir_entero_en_rango(
            "Ingrese la CALLE (50 a 55):",
            50,
            55
        )
        if calle is None:
            return  # usuario canceló

        # Pedir CARRERA (10–15)
        carrera = pedir_entero_en_rango(
            "Ingrese la CARRERA (10 a 15):",
            10,
            15
        )
        if carrera is None:
            return  # usuario canceló

        # Todo válido: ejecutar cálculo con destino personalizado
        ejecutar_calculo((calle, carrera))

    # ------- Botón 1 -------
    btn_darkness = ttk.Button(
        frame,
        text="Discoteca The Darkness",
        command=lambda: ejecutar_calculo("darkness")
    )
    btn_darkness.pack(pady=10)

    # ------- Botón 2 -------
    btn_pasion = ttk.Button(
        frame,
        text="Bar La Pasión",
        command=lambda: ejecutar_calculo("pasion")
    )
    btn_pasion.pack(pady=10)

    # ------- Botón 3 -------
    btn_rolita = ttk.Button(
        frame,
        text="Cervecería Mi Rolita",
        command=lambda: ejecutar_calculo("rolita")
    )
    btn_rolita.pack(pady=10)

    # ------- Botón 4 - Personalizado -------
    btn_personalizado = ttk.Button(
        frame,
        text="Destino personalizado",
        command=destino_personalizado
    )
    btn_personalizado.pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
