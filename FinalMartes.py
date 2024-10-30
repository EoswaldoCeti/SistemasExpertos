import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from graphviz import Digraph

class Node:
    def __init__(self, name):
        self.name = name
        self.left = None
        self.right = None

def build_tree():
    root = Node("A")
    
    root.left = Node("A=0")
    root.right = Node("A=1")

    root.left.left = Node("B0 = 0")
    root.left.right = Node("B0 = 1")
    root.right.left = Node("B1 = 0")
    root.right.right = Node("B1 = 1")

    root.left.left.left = Node("C0 = 0 (Salida=0)")
    root.left.left.right = Node("C0 = 1 (Salida=0)")
    root.left.right.left = Node("C1 = 0 (Salida=0)")
    root.left.right.right = Node("C1 = 1 (Salida=0)")
    root.right.left.left = Node("C2 = 0 (Salida=0)")
    root.right.left.right = Node("C2 = 1 (Salida=0)")
    root.right.right.left = Node("C3 = 0 (Salida=0)")
    root.right.right.right = Node("C3 = 1 (Salida=1)")

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
    tree_root = build_tree()
    dot = Digraph()

    def determine_colors(a, b, c):
        colors = {}
        path = []

        def visit(node):
            if node is not None:
                colors[node.name] = "black"
                visit(node.left)
                visit(node.right)

        visit(tree_root)

        if a:
            colors["A"] = "green"
            path.append("A")
            if b:
                colors["B1 = 1"] = "green"
                path.append("B1 = 1")
                colors["C3 = 1 (Salida=1)"] = "green" if c else "red"
                path.append("C3 = 1 (Salida=1)")
                colors["C2 = 0 (Salida=0)"] = "green" if not c else "red"
                path.append("C2 = 0 (Salida=0)")
            else:
                colors["B0 = 0"] = "green"
                path.append("B0 = 0")
                colors["C0 = 0 (Salida=0)"] = "green" if not c else "red"
                path.append("C0 = 0 (Salida=0)")
                colors["C1 = 0 (Salida=0)"] = "green" if c else "red"
                path.append("C1 = 0 (Salida=0)")
        else:
            colors["A"] = "green"
            colors["A=0"] = "green"
            path.append("A=0")
            if b:
                colors["B0 = 1"] = "green"
                path.append("B0 = 1")
                colors["C1 = 0 (Salida=0)"] = "green" if not c else "red"
                path.append("C1 = 0 (Salida=0)")
            else:
                colors["B0 = 0"] = "green"
                path.append("B0 = 0")
                colors["C2 = 1 (Salida=0)"] = "green" if c else "red"
                path.append("C2 = 1 (Salida=0)")
                colors["C2 = 0 (Salida=0)"] = "green" if not c else "red"
                path.append("C2 = 0 (Salida=0)")

        return colors

    colors = determine_colors(a, b, c)

    def add_colored_nodes(graph, node):
        if node is not None:
            color = colors.get(node.name, "black")
            graph.node(node.name, color=color)
            add_colored_nodes(graph, node.left)
            add_colored_nodes(graph, node.right)

    add_colored_nodes(dot, tree_root)
    add_edges(dot, tree_root)

    dot.render('arbol_de_estados', format='png', cleanup=True)
    dot.view()

def graficar_tabla_verdad(a, b, c, operacion, ventana, header_a, header_b, header_c):
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
                
                if operacion == "AND":
                    resultado = val_a and val_b and val_c
                else:
                    resultado = val_a or val_b or val_c
                
                data['Resultado'].append(resultado)

    df = pd.DataFrame(data)

    plt.figure(figsize=(10, 5))
    plt.title(f"Tabla de Verdad - Compuerta {operacion}")
    plt.axis('tight')
    plt.axis('off')

    table = plt.table(cellText=df.values, colLabels=[header_a, header_b, header_c, 'Resultado'], cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.2)

    for i, (val_a, val_b, val_c) in enumerate(zip(df['A'], df['B'], df['C'])):
        if val_a == a and val_b == b and val_c == c:
            table[i + 1, 0].set_facecolor('lightblue')
            table[i + 1, 1].set_facecolor('lightblue')
            table[i + 1, 2].set_facecolor('lightblue')
            table[i + 1, 3].set_facecolor('lightgreen')

    plt.show()

def calcular_tabla_verdad():
    try:
        a = var_a.get()
        b = var_b.get()
        c = var_c.get()
        operacion = var_operacion.get()

        if operacion == "AND":
            resultado = a and b and c
        else:
            resultado = a or b or c

        resultado_text.set(f"A: {a}, B: {b}, C: {c}, {operacion} Result: {resultado}")

        # Obtener encabezados de los Entry
        header_a = entry_header_a.get() or 'A'
        header_b = entry_header_b.get() or 'B'
        header_c = entry_header_c.get() or 'C'

        graficar_tabla_verdad(a, b, c, operacion, root, header_a, header_b, header_c)
        generar_arbol(root, a, b, c, resultado)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

# Crear ventana principal
root = tk.Tk()
root.title("Tabla de Verdad con Diagrama")

var_a = tk.BooleanVar()
var_b = tk.BooleanVar()
var_c = tk.BooleanVar()

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

var_operacion = tk.StringVar(value="AND")
radio_and = tk.Radiobutton(root, text="Compuerta AND", variable=var_operacion, value="AND")
radio_and.grid(row=3, column=0)

radio_or = tk.Radiobutton(root, text="Compuerta OR", variable=var_operacion, value="OR")
radio_or.grid(row=3, column=1)

# Campos de entrada para encabezados
tk.Label(root, text="Encabezado A:").grid(row=4, column=0)
entry_header_a = tk.Entry(root)
entry_header_a.grid(row=4, column=1)

tk.Label(root, text="Encabezado B:").grid(row=5, column=0)
entry_header_b = tk.Entry(root)
entry_header_b.grid(row=5, column=1)

tk.Label(root, text="Encabezado C:").grid(row=6, column=0)
entry_header_c = tk.Entry(root)
entry_header_c.grid(row=6, column=1)

button_calcular = tk.Button(root, text="Calcular", command=calcular_tabla_verdad)
button_calcular.grid(row=7, column=0, columnspan=2)

resultado_text = tk.StringVar()
label_resultado = tk.Label(root, textvariable=resultado_text)
label_resultado.grid(row=8, column=0, columnspan=2)

# Iniciar el bucle de la aplicación
root.mainloop()
