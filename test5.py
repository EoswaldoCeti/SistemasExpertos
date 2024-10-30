import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt  # Asegúrate de importar matplotlib.pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from graphviz import Digraph

class Node:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

def build_tree():
    root = Node("A")
    
    # Nodos para A = 0 y A = 1
    root.left = Node("A=0")  # A=0
    root.right = Node("A=1")  # A=1

    # Nodos para B en ambos casos de A
    root.left.left = Node("B0 = 0")  # A=0, B0=0
    root.left.right = Node("B0 = 1")  # A=0, B1=1
    root.right.left = Node("B1 = 0")  # A=1, B0=0
    root.right.right = Node("B1 = 1")  # A=1, B1=1

    # Nodos para C en ambos casos de B
    root.left.left.left = Node("C0 = 0 (Salida=0)")  # A=0, B0=0, C0=0
    root.left.left.right = Node("C1 = 1 (Salida=0)")  # A=0, B0=0, C1=1
    root.left.right.left = Node("C2 = 0 (Salida=0)")  # A=0, B1=1, C0=0
    root.left.right.right = Node("C3 = 1 (Salida=0)")  # A=0, B1=1, C1=1
    root.right.left.left = Node("C4 = 0 (Salida=0)")  # A=1, B0=0, C0=0
    root.right.left.right = Node("C5 = 1 (Salida=0)")  # A=1, B0=0, C1=1
    root.right.right.left = Node("C6 = 0 (Salida=0)")  # A=1, B1=1, C0=0
    root.right.right.right = Node("C7 = 1 (Salida=1)")  # A=1, B1=1, C1=1

    return root

def add_edges(graph, node):
    if node is not None:
        if node.left is not None:
            graph.edge(node.name, node.left.name)
            add_edges(graph, node.left)
        if node.right is not None:
            graph.edge(node.name, node.right.name)
            add_edges(graph, node.right)

def generar_arbol(ventana, a, b, c, resultado):
    # Crear el árbol y graficarlo
    tree_root = build_tree()
    dot = Digraph()

    # Añadir nodos al grafo
    dot.node(tree_root.name)
    add_edges(dot, tree_root)

    # Renderizar el gráfico
    dot.render('arbol_de_estados', format='png', cleanup=True)
    dot.view()

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
        generar_arbol(root, a, b, c, resultado)

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
