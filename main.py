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
    root = tk.Tk()
    root.title("Proyecto de Modelación de Sistemas de Redes")
    root.configure(bg="#e8eff7")
    root.update_idletasks()
    root.minsize(600, 520)
    titulo = tk.Label(
        root,
        text="Proyecto de Modelación de Sistemas de Redes",
        font=("Helvetica", 20, "bold"),
        bg="#e8eff7",
        fg="#1f3c88",
        wraplength=550,
        justify="center"
    )
    titulo.pack(pady=15)

    subtitulo = tk.Label(
        root,
        text="Integrantes:\nNelson Carrillo • José Francisco • Luis Pérez",
        font=("Helvetica", 20),
        bg="#e8eff7",
        fg="#3a4750",
        justify="center",
    )
    subtitulo.pack(pady=5)

    frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
    frame.pack(pady=30, padx=40, fill="both", expand=True)

    label_opciones = tk.Label(
        frame,
        text="Seleccione el destino:",
        font=("Helvetica", 20, "bold"),
        bg="#ffffff",
        fg="#303841"
    )
    label_opciones.pack(pady=15)

    estilo = ttk.Style()
    estilo.configure(
        "TButton",
        font=("Helvetica", 20),
        padding=10
    )

    def pedir_entero_en_rango(texto, minimo, maximo):
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

    def destino_personalizado():
        calle = pedir_entero_en_rango(
            "Ingrese la CALLE (50 a 55):",
            50,
            55
        )
        if calle is None:
            return  
        carrera = pedir_entero_en_rango(
            "Ingrese la CARRERA (10 a 15):",
            10,
            15
        )
        if carrera is None:
            return  

        ejecutar_calculo((calle, carrera))

    btn_darkness = ttk.Button(
        frame,
        text="Discoteca The Darkness",
        command=lambda: ejecutar_calculo("darkness")
    )
    btn_darkness.pack(pady=8)

    btn_pasion = ttk.Button(
        frame,
        text="Bar La Pasión",
        command=lambda: ejecutar_calculo("pasion")
    )
    btn_pasion.pack(pady=8)

    btn_rolita = ttk.Button(
        frame,
        text="Cervecería Mi Rolita",
        command=lambda: ejecutar_calculo("rolita")
    )
    btn_rolita.pack(pady=8)

    btn_personalizado = ttk.Button(
        frame,
        text="Destino personalizado",
        command=destino_personalizado
    )
    btn_personalizado.pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
