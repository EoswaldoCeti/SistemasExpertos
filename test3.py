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
    root.left.left = Node("B=0")  # A=0, B=0
    root.left.right = Node("B=1")  # A=0, B=1
    root.right.left = Node("B=0")  # A=1, B=0
    root.right.right = Node("B=1")  # A=1, B=1

    # Nodos para C en ambos casos de B
    root.left.left.left = Node("C=0 (Salida=0)")  # A=0, B=0, C=0
    root.left.left.right = Node("C=1 (Salida=0)")  # A=0, B=0, C=1
    root.left.right.left = Node("C=0 (Salida=0)")  # A=0, B=1, C=0
    root.left.right.right = Node("C=1 (Salida=0)")  # A=0, B=1, C=1
    root.right.left.left = Node("C=0 (Salida=0)")  # A=1, B=0, C=0
    root.right.left.right = Node("C=1 (Salida=0)")  # A=1, B=0, C=1
    root.right.right.left = Node("C=0 (Salida=0)")  # A=1, B=1, C=0
    root.right.right.right = Node("C=1 (Salida=1)")  # A=1, B=1, C=1

    return root

def add_edges(graph, node):
    if node is not None:
        if node.left is not None:
            graph.edge(node.name, node.left.name)
            add_edges(graph, node.left)
        if node.right is not None:
            graph.edge(node.name, node.right.name)
            add_edges(graph, node.right)

# Crear el árbol y graficarlo
tree_root = build_tree()
dot = Digraph()

# Añadir nodos al grafo
dot.node(tree_root.name)
add_edges(dot, tree_root)

# Renderizar el gráfico
dot.render('arbol_de_estados', format='png', cleanup=True)
dot.view()
