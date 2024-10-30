# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 19:40:19 2024

@author: Dea
"""
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para generar y mostrar la tabla de verdad en la interfaz
def procesar():
    texto1 = caja1.get()
    texto2 = caja2.get()
    operacion = combo.get()

    # Limpiar el contenido anterior del cuadro de texto
    resultado_texto.delete(1.0, tk.END)

    # Imprimir información inicial
    resultado_texto.insert(tk.END, f"Preposición 1 (p): {texto1}\n")
    resultado_texto.insert(tk.END, f"Preposición 2 (q): {texto2}\n")
    # Imprimir información inicial con la operación en formato lógico
    if operacion == "y":  # Conjunción (∧)
        resultado_texto.insert(tk.END, f"Operación seleccionada: Conjunción (p ∧ q)\n\n")
    else:  # Disyunción (∨)
        resultado_texto.insert(tk.END, f"Operación seleccionada: Disyunción (p ∨ q)\n\n")

    # Definir las variables de la tabla de verdad
    p = [True, True, False, False]
    q = [True, False, True, False]

    # Generar la tabl de verdad según la operación seleccionada
    if operacion == "y":  # Conjunción (∧)
        resultado = [a and b for a, b in zip(p, q)]
        resultado_texto.insert(tk.END, "Tabla de verdad Conjunción (p ∧ q):\n")
        resultado_texto.insert(tk.END, "p\tq\tp ∧ q\n")
    else:  # Disyunción (p ∨ q)
        resultado = [a or b for a, b in zip(p, q)]
        resultado_texto.insert(tk.END, "Tabla de verdad Disyunción (p ∨ q):\n")
        resultado_texto.insert(tk.END, "p\tq\tp ∨ q\n")

    # Imprimir la tabla de verdad en el cuadro de texto
    for a, b, res in zip(p, q, resultado):
        resultado_texto.insert(tk.END, f"{a}\t{b}\t{res}\n")

    # Generar el árbol de estados
    generar_arbol(operacion)

# Función para generar el árbol de estados
def generar_arbol(operacion):
    fig, ax = plt.subplots()
    
    # Crear el árbol de estados básico con matplotlib
    if operacion == "y":  # Conjunción (∧)
        ax.text(0.5, 0.9, "p ∧ q", fontsize=14, ha='center')
        ax.text(0.3, 0.7, "p", fontsize=12, ha='center')
        ax.text(0.7, 0.7, "q", fontsize=12, ha='center')
        ax.text(0.2, 0.5, "True", fontsize=12, ha='center')
        ax.text(0.4, 0.5, "False", fontsize=12, ha='center')
        ax.text(0.6, 0.5, "True", fontsize=12, ha='center')
        ax.text(0.8, 0.5, "False", fontsize=12, ha='center')

        ax.plot([0.5, 0.3], [0.85, 0.7], 'k-')  # Rama p
        ax.plot([0.5, 0.7], [0.85, 0.7], 'k-')  # Rama q
        ax.plot([0.3, 0.2], [0.65, 0.5], 'k-')  # Rama True p
        ax.plot([0.3, 0.4], [0.65, 0.5], 'k-')  # Rama False p
        ax.plot([0.7, 0.6], [0.65, 0.5], 'k-')  # Rama True q
        ax.plot([0.7, 0.8], [0.65, 0.5], 'k-')  # Rama False q

    else:  # Disyunción (∨)
        ax.text(0.5, 0.9, "p ∨ q", fontsize=14, ha='center')
        ax.text(0.3, 0.7, "p", fontsize=12, ha='center')
        ax.text(0.7, 0.7, "q", fontsize=12, ha='center')
        ax.text(0.2, 0.5, "True", fontsize=12, ha='center')
        ax.text(0.4, 0.5, "False", fontsize=12, ha='center')
        ax.text(0.6, 0.5, "True", fontsize=12, ha='center')
        ax.text(0.8, 0.5, "False", fontsize=12, ha='center')

        ax.plot([0.5, 0.3], [0.85, 0.7], 'k-')  # Rama p
        ax.plot([0.5, 0.7], [0.85, 0.7], 'k-')  # Rama q
        ax.plot([0.3, 0.2], [0.65, 0.5], 'k-')  # Rama True p
        ax.plot([0.3, 0.4], [0.65, 0.5], 'k-')  # Rama False p
        ax.plot([0.7, 0.6], [0.65, 0.5], 'k-')  # Rama True q
        ax.plot([0.7, 0.8], [0.65, 0.5], 'k-')  # Rama False q

    ax.set_axis_off()  # Ocultar los ejes

    # Mostrar el gráfico en la interfaz
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=0, columnspan=3)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Preposiciones Logicas")
ventana.configure(bg='white') 
ventana.minsize(300, 100)
# Crear las cajas de texto
caja1 = tk.Entry(ventana, width=20, bd=2,highlightbackground='blue', highlightcolor='blue')
caja1.grid(row=0, column=0, padx=10, pady=10)

caja2 = tk.Entry(ventana, width=20, bd=2,highlightbackground='blue', highlightcolor='blue')
caja2.grid(row=0, column=2, padx=10, pady=10)

# Crear el menú desplegable
combo = ttk.Combobox(ventana, values=["y", "ó"], width=5)
combo.grid(row=0, column=1, padx=10, pady=10)
combo.current(0)  # Selecciona "Y" por defecto

# Crear el botón "Procesar"
boton = tk.Button(ventana, text="Procesar", command=procesar, font=("Arial", 12), bg='#021D40', fg='white' )
boton.grid(row=1, column=1, pady=10)

# Crear un cuadro de texto para mostrar el resultado
resultado_texto = tk.Text(ventana, height=10, width=45, bd=2,highlightbackground='blue', highlightcolor='blue')
resultado_texto.grid(row=2, column=0, columnspan=3, padx=10, pady=10)



def generar_arbol(operacion):
    fig, ax = plt.subplots()
    
    # Posiciones para las ramas y nodos
    posiciones = {
        'p': (0.5, 0.9),
        'p_true': (0.3, 0.7),
        'p_false': (0.7, 0.7),
        'q_ptrue': (0.2, 0.5),
        'q_pfalse': (0.8, 0.5),
        'q_true_true': (0.15, 0.3),
        'q_true_false': (0.25, 0.3),
        'q_false_true': (0.75, 0.3),
        'q_false_false': (0.85, 0.3),
    }
    
    # Título del árbol dependiendo de la operación
    if operacion == "y":  # Conjunción (∧)
        ax.text(posiciones['p'][0], posiciones['p'][1]+0.05, "p ∧ q", fontsize=14, ha='center')
    else:  # Disyunción (∨)
        ax.text(posiciones['p'][0], posiciones['p'][1]+0.05, "p ∨ q", fontsize=14, ha='center')
    
    # Nodos de p
    ax.text(posiciones['p_true'][0], posiciones['p_true'][1]+0.08, "p = True", fontsize=12, ha='center')
    ax.text(posiciones['p_false'][0], posiciones['p_false'][1]+0.08, "p = False", fontsize=12, ha='center')

    # Nodos de q cuando p es True
    ax.text(posiciones['q_ptrue'][0], posiciones['q_ptrue'][1]+0.04, "q", fontsize=12, ha='center')
    ax.text(posiciones['q_true_true'][0], posiciones['q_true_true'][1]+0.08, "q = True", fontsize=12, ha='right')
    ax.text(posiciones['q_true_false'][0], posiciones['q_true_false'][1]+0.08, "q = False", fontsize=12, ha='left')

    # Nodos de q cuando p es False
    ax.text(posiciones['q_pfalse'][0], posiciones['q_pfalse'][1]+0.04, "q", fontsize=12, ha='center')
    ax.text(posiciones['q_false_true'][0], posiciones['q_false_true'][1]+0.08, "q = True", fontsize=12, ha='right')
    ax.text(posiciones['q_false_false'][0], posiciones['q_false_false'][1]+0.08, "q = False", fontsize=12, ha='left')

    # Generar ramas desde p
    ax.plot([posiciones['p'][0], posiciones['p_true'][0]], [posiciones['p'][1], posiciones['p_true'][1]], 'k-')  # Rama p = True
    ax.plot([posiciones['p'][0], posiciones['p_false'][0]], [posiciones['p'][1], posiciones['p_false'][1]], 'k-')  # Rama p = False

    # Ramas desde q cuando p = True
    ax.plot([posiciones['p_true'][0], posiciones['q_ptrue'][0]], [posiciones['p_true'][1], posiciones['q_ptrue'][1]], 'k-')  # Rama a q
    ax.plot([posiciones['q_ptrue'][0], posiciones['q_true_true'][0]], [posiciones['q_ptrue'][1], posiciones['q_true_true'][1]], 'k-')  # Rama q = True
    ax.plot([posiciones['q_ptrue'][0], posiciones['q_true_false'][0]], [posiciones['q_ptrue'][1], posiciones['q_true_false'][1]], 'k-')  # Rama q = False

    # Ramas desde q cuando p = False
    ax.plot([posiciones['p_false'][0], posiciones['q_pfalse'][0]], [posiciones['p_false'][1], posiciones['q_pfalse'][1]], 'k-')  # Rama a q
    ax.plot([posiciones['q_pfalse'][0], posiciones['q_false_true'][0]], [posiciones['q_pfalse'][1], posiciones['q_false_true'][1]], 'k-')  # Rama q = True
    ax.plot([posiciones['q_pfalse'][0], posiciones['q_false_false'][0]], [posiciones['q_pfalse'][1], posiciones['q_false_false'][1]], 'k-')  # Rama q = False

    # Añadir el resultado final en las hojas
    if operacion == "y":  # Conjunción
        ax.text(posiciones['q_true_true'][0], posiciones['q_true_true'][1] - 0.1, "True", fontsize=12, ha='center')  # p=True, q=True
        ax.text(posiciones['q_true_false'][0], posiciones['q_true_false'][1] - 0.1, "False", fontsize=12, ha='center')  # p=True, q=False
        ax.text(posiciones['q_false_true'][0], posiciones['q_false_true'][1] - 0.1, "False", fontsize=12, ha='center')  # p=False, q=True
        ax.text(posiciones['q_false_false'][0], posiciones['q_false_false'][1] - 0.1, "False", fontsize=12, ha='center')  # p=False, q=False
    else:  # Disyunción
        ax.text(posiciones['q_true_true'][0], posiciones['q_true_true'][1] - 0.1, "True", fontsize=12, ha='center')  # p=True, q=True
        ax.text(posiciones['q_true_false'][0], posiciones['q_true_false'][1] - 0.1, "True", fontsize=12, ha='center')  # p=True, q=False
        ax.text(posiciones['q_false_true'][0], posiciones['q_false_true'][1] - 0.1, "True", fontsize=12, ha='center')  # p=False, q=True
        ax.text(posiciones['q_false_false'][0], posiciones['q_false_false'][1] - 0.1, "False", fontsize=12, ha='center')  # p=False, q=False

    ax.set_axis_off()  # Ocultar los ejes

    # Mostrar el gráfico en la interfaz
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.draw()
    #canvas.get_tk_widget().grid(row=3, column=0, columnspan=3)
    canvas.get_tk_widget().grid(row=1, column=3, rowspan=2)

# Iniciar el bucle principal de la ventana
ventana.mainloop()

