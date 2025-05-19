from os import system
import random
import networkx as nx
import m_arista

system('cls')


#=====================Cargar achivo de Grafo==========
def cargar_grafo(grafo_sin_peso):
    grafo=nx.Graph(nx.nx_pydot.read_dot(grafo_sin_peso))# lectura de grafo
    grafo_pesado = {}
    nodos = list(grafo.nodes)
    for nodo in nodos:
        vecinos = {}
        for vecino, atributos in grafo[nodo].items():
            peso = atributos.get('weight', 1)  # Obtener el peso, default a 1 si no existe
            vecinos[vecino] = peso
        grafo_pesado[nodo] = vecinos
    return grafo_pesado, nodos


#====================Generar archivo.dot con las distancias=======
def generar_grafo_graphviz_distancias(lista_aristas, distancias, nodo_raiz, nombre_grafo):
    archivo = f"{nombre_grafo}.dot"
    try:
        with open(archivo, "x") as archivo_graphviz:
            archivo_graphviz.write("graph {\n")

            # Escribir información de los nodos con etiquetas de distancia
            for nodo, distancia_total in distancias.items():
                etiqueta_nodo = f"{nodo}({distancia_total})" if nodo != nodo_raiz else f"{nodo}(0)"
                archivo_graphviz.write(f'  "{nodo}" [label="{etiqueta_nodo}"];\n')

            # Escribir las aristas con sus pesos
            for arista in lista_aristas:
                archivo_graphviz.write(f'  "{arista.nodo1}" -- "{arista.nodo2}" [weight={arista.peso}];\n')

            archivo_graphviz.write("}\n")
        print(f"Archivo '{nombre_grafo}.dot' generado exitosamente.")
    except Exception as e:
        print(f"Error al generar el archivo .dot: {e}")


#==================Algoritmo de Dijkstra=======================
def dijkstra(grafo, inicio):
    distancia = {nodo: float('inf') for nodo in grafo}
    padre = {nodo: None for nodo in grafo}
    distancia[inicio] = 0
    nodos_no_visitados = set(grafo)
    arbol_expansion = []

    while nodos_no_visitados:
        nodo_actual = None
        dist_minima = float('inf')
        for nodo in nodos_no_visitados:
            if distancia[nodo] < dist_minima:
                dist_minima = distancia[nodo]
                nodo_actual = nodo

        if nodo_actual is None:
            break

        nodos_no_visitados.remove(nodo_actual)

        for vecino, peso in grafo[nodo_actual].items():
            if distancia[vecino] > distancia[nodo_actual] + peso:
                distancia[vecino] = distancia[nodo_actual] + peso
                padre[vecino] = nodo_actual

    # Construir la lista de aristas del árbol de expansión
    for nodo, p in padre.items():
        if p is not None:
            peso_arista = grafo[p][nodo]
            arbol_expansion.append(m_arista.arista(p, nodo, peso_arista))

    return arbol_expansion, distancia  # Devolvemos también el diccionario de distancias

#=============Programa Principal==================

grafo_base='Malla20.dot'
nodo_raiz='10'
# grafo=nx.Graph(nx.nx_pydot.read_dot(grafo_base))
# nodos=list(grafo.nodes())
# nodo_raiz=random.choice(nodos)

grafo_con_pesos, nodos = cargar_grafo(grafo_base)
arbol_resultante, distancias = dijkstra(grafo_con_pesos, nodo_raiz) # Obtenemos las distancias
nombre_arbol_Dijkstra = "Dijkstra_Malla_200"
generar_grafo_graphviz_distancias(arbol_resultante, distancias, nodo_raiz, nombre_arbol_Dijkstra)

