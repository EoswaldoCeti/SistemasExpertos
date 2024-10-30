import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para generar el árbol de estados
def generar_arbol(operacion, ventana, a, b, c, resultado):
    fig, ax = plt.subplots()

    # Colores para las letras
    color_a0 = 'green' if not a else 'black'
    color_a1 = 'green' if a else 'black'

    color_b0 = 'green' if not b else 'black'
    color_b1 = 'green' if b else 'black'

    color_c0 = 'green' if not c else 'black'
    color_c1 = 'green' if c else 'black'

    # Crear el árbol de decisiones
    ax.text(0.5, 0.9, "A", fontsize=14, ha='center', color='black')
    ax.text(0.3, 0.75, "A0", fontsize=12, ha='center', color=color_a0)
    ax.text(0.7, 0.75, "A1", fontsize=12, ha='center', color=color_a1)

    # Ramas de A
    ax.plot([0.5, 0.3], [0.85, 0.75], 'k-')
    ax.plot([0.5, 0.7], [0.85, 0.75], 'k-')

    # Nivel B
    ax.text(0.2, 0.65, "B", fontsize=14, ha='center', color='black')
    ax.text(0.1, 0.55, "B0", fontsize=12, ha='center', color=color_b0)
    ax.text(0.3, 0.55, "B1", fontsize=12, ha='center', color=color_b1)
    ax.plot([0.3, 0.2], [0.75, 0.65], 'k-')
    ax.plot([0.3, 0.3], [0.75, 0.65], 'k-')
    ax.plot([0.7, 0.6], [0.75, 0.65], 'k-')
    ax.plot([0.7, 0.7], [0.75, 0.65], 'k-')

    # Nivel C bajo B0
    ax.text(0.1, 0.45, "C", fontsize=14, ha='center', color='black')
    ax.text(0.05, 0.35, "C0", fontsize=12, ha='center', color=color_c0)
    ax.text(0.15, 0.35, "C1", fontsize=12, ha='center', color=color_c1)
    ax.plot([0.2, 0.1], [0.55, 0.45], 'k-')
    ax.plot([0.2, 0.2], [0.55, 0.45], 'k-')

    # Nivel C bajo B1
    ax.text(0.3, 0.45, "C", fontsize=14, ha='center', color='black')
    ax.text(0.25, 0.35, "C0", fontsize=12, ha='center', color=color_c0)
    ax.text(0.35, 0.35, "C1", fontsize=12, ha='center', color=color_c1)
    ax.plot([0.3, 0.25], [0.55, 0.45], 'k-')
    ax.plot([0.3, 0.3], [0.55, 0.45], 'k-')

    # Ramas finales (Resultado)
    resultado_final = "True" if resultado else "False"
    ax.text(0.05, 0.25, f"R: {resultado_final}", fontsize=12, ha='center', color='red')
    ax.text(0.15, 0.25, f"R: {resultado_final}", fontsize=12, ha='center', color='red')
    ax.text(0.25, 0.25, f"R: {resultado_final}", fontsize=12, ha='center', color='red')
    ax.text(0.35, 0.25, f"R: {resultado_final}", fontsize=12, ha='center', color='red')

    # Etiqueta de operación y resultado
    ax.text(0.5, 0.95, f"Operación: {operacion}", fontsize=14, ha='center', color='blue')

    ax.set_axis_off()  # Ocultar los ejes

    # Mostrar el gráfico en la interfaz
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=3)

def graficar_tabla_verdad(a, b, c, operacion, ventana):
    # Crear un DataFrame para la tabla de verdad
    data = {
        'A': [],
        'B': [],
        'C': [],
        'Resultado': []
    }

    for val_a in [True, False]:
        for val_b in [True, False]:
            for val_c in [True, False]:
                data['A'].append(val_a)
                data['B'].append(val_b)
                data['C'].append(val_c)
                
                # Determinar el resultado basado en la operación seleccionada
                if operacion == "AND":
                    resultado = val_a and val_b and val_c
                else:
                    resultado = val_a or val_b or val_c
                
                data['Resultado'].append(resultado)

    df = pd.DataFrame(data)

    # Graficar la tabla de verdad
    plt.figure(figsize=(10, 5))
    plt.title(f"Tabla de Verdad - Compuerta {operacion}")
    plt.axis('tight')
    plt.axis('off')

    # Crear la tabla con resaltado
    table = plt.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)

    # Resaltar solo la combinación actual
    for i, (val_a, val_b, val_c) in enumerate(zip(df['A'], df['B'], df['C'])):
        if val_a == a and val_b == b and val_c == c:
            table[i + 1, 0].set_facecolor('lightblue')  # Resaltar A
            table[i + 1, 1].set_facecolor('lightblue')  # Resaltar B
            table[i + 1, 2].set_facecolor('lightblue')  # Resaltar C
            table[i + 1, 3].set_facecolor('lightgreen')   # Resaltar Resultado

    plt.show()

def calcular_tabla_verdad():
    try:
        # Obtener los valores de entrada desde los checkbuttons
        a = var_a.get()
        b = var_b.get()
        c = var_c.get()
        operacion = var_operacion.get()  # Obtener la operación seleccionada

        # Calcular el resultado
        if operacion == "AND":
            resultado = a and b and c
        else:
            resultado = a or b or c

        # Mostrar resultados en la etiqueta
        resultado_text.set(f"A: {a}, B: {b}, C: {c}, {operacion} Result: {resultado}")

        # Graficar la tabla de verdad
        graficar_tabla_verdad(a, b, c, operacion, root)

        # Generar el árbol de estados
        generar_arbol(operacion, root, a, b, c, resultado)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Crear ventana principal
root = tk.Tk()
root.title("Tabla de Verdad con Diagrama")

# Variables para los checkbuttons
var_a = tk.BooleanVar()
var_b = tk.BooleanVar()
var_c = tk.BooleanVar()

# Crear widgets para A, B y C usando grid
label_a = tk.Label(root, text="A:")
label_a.grid(row=0, column=0)
check_a = tk.Checkbutton(root, text="On", variable=var_a)
check_a.grid(row=0, column=1)

label_b = tk.Label(root, text="B:")
label_b.grid(row=1, column=0)
check_b = tk.Checkbutton(root, text="On", variable=var_b)
check_b.grid(row=1, column=1)

label_c = tk.Label(root, text="C:")
label_c.grid(row=2, column=0)
check_c = tk.Checkbutton(root, text="On", variable=var_c)
check_c.grid(row=2, column=1)

# Opción para seleccionar la operación
var_operacion = tk.StringVar(value="AND")  # Valor predeterminado
radio_and = tk.Radiobutton(root, text="Compuerta AND", variable=var_operacion, value="AND")
radio_and.grid(row=3, column=0)

radio_or = tk.Radiobutton(root, text="Compuerta OR", variable=var_operacion, value="OR")
radio_or.grid(row=3, column=1)

button_calcular = tk.Button(root, text="Calcular", command=calcular_tabla_verdad)
button_calcular.grid(row=4, column=0, columnspan=2)

resultado_text = tk.StringVar()
label_resultado = tk.Label(root, textvariable=resultado_text)
label_resultado.grid(row=5, column=0, columnspan=2)

# Iniciar el bucle de la aplicación
root.mainloop()
