import re
import itertools
import matplotlib.pyplot as plt
import pandas as pd
import json
import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Variables globales
var_counter = 1
total_results = []
global_state = {}

def draw_tree(node, ax, x, y, dx):
    if node is not None:
        ax.text(x, y, node.value, ha='center', va='center', bbox=dict(boxstyle='round', facecolor='wheat'))

        if node.left:
            ax.plot([x, x - dx], [y - 0.1, y - 0.4], 'k-')
            draw_tree(node.left, ax, x - dx, y - 0.4, dx / 2)

        if node.right:
            ax.plot([x, x + dx], [y - 0.1, y - 0.4], 'k-')
            draw_tree(node.right, ax, x + dx, y - 0.4, dx / 2)

def evaluate_expression(expr, values):
    for var, val in values.items():
        expr = expr.replace(var, str(val))
    try:
        return eval(expr.replace('~', 'not ').replace('∧', ' and ').replace('∨', ' or '))
    except Exception:
        return None

def extract_propositions(statement):
    # Modificar el enunciado para utilizar símbolos lógicos y reemplazar "NO" por "~"
    modified_statement = statement.replace(" y ", "∧").replace(" o ", "∨").replace(" NO ", "~")

    # Extraer proposiciones utilizando un regex
    propositions = re.split(r',|\s+y\s+|\s+o\s+|\s+NO\s+', statement)
    variables = {}
    formula = modified_statement

    for index, prop in enumerate(propositions):
        prop = prop.strip()
        var_name = f"P{var_counter + index}"  # Generar variable P1, P2, P3, ...

        # Si la proposición tiene "NO", se maneja el símbolo "~" en la fórmula
        if "NO" in prop:
            prop_without_no = prop.replace("NO", "").strip()  # Eliminar "NO" para obtener solo la proposición
            variables[var_name] = prop_without_no  # Guardar la proposición sin "NO" en variables
            formula = formula.replace(prop, f"~{var_name}")  # Reemplazar en la fórmula
        else:
            variables[var_name] = prop  # Guardar la proposición en variables sin cambios
            formula = formula.replace(prop, var_name)

    return variables, formula

def truth_table(vars_map, expr):
    var_list = list(vars_map.keys())
    combinations = list(itertools.product([False, True], repeat=len(var_list)))
    results = []

    for combination in combinations:
        values = dict(zip(var_list, combination))
        result = evaluate_expression(expr, values)
        values['Resultado'] = result
        results.append(values)

    return pd.DataFrame(results)

def variable_states(expr):
    states = {}
    for var in set(re.findall(r'P\d+', expr)):
        states[var] = False if f"~{var}" in expr else True
            
    return pd.DataFrame.from_dict(states, orient='index', columns=["Valor"])

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def load_from_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def show_graph(node):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')
    draw_tree(node, ax, 0, 0, 4)
    plt.title("Árbol de Estados")
    plt.show()

def build_tree(vars_map):
    if not vars_map:
        return None
    var_list = list(vars_map.keys())
    root = TreeNode(var_list[0])
    queue = [(root, 0)]

    while queue:
        parent, index = queue.pop(0)

        if index < len(var_list):
            current_var = var_list[index]

            true_node = TreeNode(f"{current_var} = True")
            false_node = TreeNode(f"{current_var} = False")

            parent.right = true_node
            parent.left = false_node

            queue.append((false_node, index + 1))
            queue.append((true_node, index + 1))

    return root

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Proposiciones")

        self.total_results = []
        self.existing_props = set()

        # Configuración de la interfaz
        self.text_area = scrolledtext.ScrolledText(master, width=80, height=20)
        self.text_area.pack(pady=10)

        self.btn_add_statement = tk.Button(master, text="Ingresar Enunciado", command=self.add_statement)
        self.btn_add_statement.pack(pady=5)

        self.btn_load_json = tk.Button(master, text="Cargar JSON", command=self.load_json)
        self.btn_load_json.pack(pady=5)

        self.btn_assign_values = tk.Button(master, text="Asignar Valores a Variables", command=self.assign_values)
        self.btn_assign_values.pack(pady=5)

        self.btn_show_formula = tk.Button(master, text="Mostrar Fórmulas", command=self.show_formulas)
        self.btn_show_formula.pack(pady=5)

        self.btn_show_table = tk.Button(master, text="Mostrar Tablas de Verdad", command=self.show_tables)
        self.btn_show_table.pack(pady=5)

        self.btn_show_graph = tk.Button(master, text="Mostrar Grafo de Estados", command=self.show_graph)
        self.btn_show_graph.pack(pady=5)

        self.btn_save_json = tk.Button(master, text="Guardar como JSON", command=self.save_json)
        self.btn_save_json.pack(pady=5)

        self.btn_exit = tk.Button(master, text="Salir", command=self.exit_app)
        self.btn_exit.pack(pady=5)

    def add_statement(self):
        statement = simpledialog.askstring("Ingresar Enunciado", "Introduce el enunciado:")
        if statement:
            variables, formula = extract_propositions(statement)
            data_to_save = {
                'enunciado': statement,
                'variables': variables,
                'formula': formula,
                'tabla': truth_table(variables, formula).to_dict(orient='records'),
                'tabla_estados': variable_states(formula).to_dict(orient='index')
            }
            self.total_results.append(data_to_save)
            messagebox.showinfo("Éxito", "Enunciado agregado exitosamente.")

    def load_json(self):
        filename = simpledialog.askstring("Cargar JSON", "Introduce el nombre del archivo JSON:")
        if filename:
            try:
                self.total_results = load_from_json(filename)
                self.existing_props = {var for result in self.total_results for var in result['variables'].values()}
                messagebox.showinfo("Éxito", "Datos cargados exitosamente.")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {e}")

    def assign_values(self):
        if not self.total_results:
            messagebox.showwarning("Advertencia", "No hay resultados cargados para asignar valores.")
            return
        
        dialog = tk.Toplevel(self.master)
        dialog.title("Asignar Valores a Variables")

        for result in self.total_results:
            variables = result['variables']
            for var in variables.keys():
                value = simpledialog.askstring("Asignar Valor", f"Asigna 0 (negativo) o 1 (positivo) para {var}:")
                if value is not None:
                    if value in ['0', '1']:
                        variables[var] = int(value)  # Convertir a entero
                    else:
                        messagebox.showerror("Error", "Por favor, ingresa solo 0 o 1.")

        messagebox.showinfo("Éxito", "Valores asignados a las variables exitosamente.")

    def show_formulas(self):
        self.text_area.delete(1.0, tk.END)
        for result in self.total_results:
            self.text_area.insert(tk.END, f"Enunciado: {result['enunciado']}\n")
            self.text_area.insert(tk.END, f"Fórmula: {result['formula']}\n\n")

    def show_tables(self):
        self.text_area.delete(1.0, tk.END)
        for result in self.total_results:
            table = pd.DataFrame(result['tabla'])
            self.text_area.insert(tk.END, f"Tabla de Verdad:\n{table}\n\n")

    def show_graph(self):
        if not self.total_results:
            messagebox.showwarning("Advertencia", "No hay resultados cargados para mostrar grafo.")
            return
        for result in self.total_results:
            variables = result['variables']
            tree = build_tree(variables)
            show_graph(tree)

    def save_json(self):
        filename = simpledialog.askstring("Guardar como JSON", "Introduce el nombre del archivo para guardar:")
        if filename:
            save_to_json(self.total_results, filename)
            messagebox.showinfo("Éxito", "Datos guardados exitosamente.")

    def exit_app(self):
        self.master.quit()

# Ejecución de la interfaz gráfica
if __name__ == "__main__":
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()
