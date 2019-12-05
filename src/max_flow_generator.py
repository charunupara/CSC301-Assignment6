import random
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import read_dot
from collections import deque
from tryalgo.graph import add_reverse_arcs

graph = read_dot(
    r"C:\Users\Charun\Desktop\CSC301-Assignment6\input_graphs\input_1.dot")


def augment(graph, flow, source, target):
    n = len(graph)
    A = [0] * n
    augm_path = [None] * n
    Q = deque()
    Q.append(source)
    augm_path[source] = source
    A[source] = float('inf')
    while Q:
        u = Q.popleft()
        for v in graph.neighbors(str(u)):
           cuv = graph[str(u)][str(v)][0]['capacity']
           residual = cuv - graph[str(u)][str(v)][0]['flow']
           if residual > 0 and augm_path[v] is None:
                augm_path[v] = u
                A[v] = min(A[u], residual)
                if v == target:
                   break
                else:
                    Q.append(v)

    return (augm_path, A[target])          

def edmonds_karp(graph, capacity, source, target):
    """Maxmum flow by Edmonds-Karp

    :param graph: directed graph in listlist or listdict format
    :param capacity: in matrix format or same listdict graph
    :param int source: vertex
    :param int target: vertex
    :returns: flow matrix, flow value
    :complexity: :math:`O(|V|*|E|^2)`
    """
    add_reverse_arcs(graph, capacity)
    V = range(len(list((graph.nodes()))))
    flow = [[0 for v in V] for u in V]
    while True:
        augm_path, delta = augment(graph, capacity, flow, source, target)
        if delta == 0:
            break
        v = target                    # remonter vers la source
        while v != source:
            u = augm_path[v]          # et augmenter le flot
            flow[u][v] += delta
            flow[v][u] -= delta
            v = u
    return (flow, sum(flow[source]))  # flot, valeur du flot
# snip}



# augment(graph, 1, 1,2)
print(edmonds_karp(graph, )
