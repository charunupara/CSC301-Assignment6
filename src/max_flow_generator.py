import random
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.algorithms.flow.utils import *
from networkx.algorithms.flow import edmonds_karp
from networkx.drawing.nx_pydot import read_dot, write_dot
from collections import deque
from tryalgo.graph import add_reverse_arcs

def max_flow(id):

    G = read_dot(r"C:\Users\Charun\Desktop\CSC301-Assignment6\input_graphs\input_" + str(id) + r".dot")
    my_source = list(G.nodes)[0]
    my_sink = list(G.nodes)[-1]

    def my_build_residual_network(G, capacity):

        R = nx.DiGraph()
        R.add_nodes_from(G)

        inf = float('inf')
        # Extract edges with positive capacities. Self loops excluded.
        edge_list = [(u, v, attr) for u, v, attr in G.edges(data=True)
                    if u != v and float(attr.get(capacity, inf).replace('"','')) > 0]
        
        inf = 3 * sum(float(attr[capacity].replace('"','')) for u, v, attr in edge_list
                    if capacity.replace('"','') in attr and attr[capacity] != inf) or 1
        if G.is_directed():
            for u, v, attr in edge_list:
                r = min(float(attr.get(capacity, inf).replace('"','')), inf)
                if not R.has_edge(u, v):
                    # Both (u, v) and (v, u) must be present in the residual
                    # network.
                    R.add_edge(u, v, capacity=r)
                    R.add_edge(v, u, capacity=0)
                else:
                    # The edge (u, v) was added when (v, u) was visited.
                    R[u][v]['capacity'] = r
        else:
            for u, v, attr in edge_list:
                # Add a pair of edges with equal residual capacities.
                r = min(attr.get(capacity, inf), inf)
                R.add_edge(u, v, capacity=r)
                R.add_edge(v, u, capacity=r)

        # Record the value simulating infinity.
        R.graph['inf'] = inf

        return R



    def my_edmonds_karp(G, s, t, capacity='capacity', residual=None, value_only=False, cutoff=None):
        R = my_edmonds_karp_impl(G, s, t, capacity, residual, cutoff)
        return R

    def my_edmonds_karp_impl(G, s, t, capacity, residual, cutoff):
        if s not in G:
            raise Exception('source not in graph')
        if t not in G:
            raise Exception('sink not in graph')
        if s == t:
            raise Exception('source and sink need to be different nodes')

        if residual is None:
            R = my_build_residual_network(G, capacity)
        else:
            R = residual
        
        for u in R:
            for edge in R[u].values():
                edge['flow'] = 0
            
        if cutoff is None:
            cutoff = float('inf')
            
        R.graph['flow_value'] = my_edmonds_karp_core(R, s, t, cutoff)
        
        return R
        
    def my_edmonds_karp_core(R, s, t, cutoff):
        residual_nodes = R.nodes
        residual_pred = R.pred
        residual_succ = R.succ

        inf = R.graph['inf']

        def augment(path):
            flow = inf
            my_iter = iter(path)
            u = next(my_iter)
            for v in my_iter:
                attribute = residual_succ[u][v]
                flow = min(flow, attribute['capacity'] - attribute['flow'])
                u = v

            my_iter = iter(path)
            u = next(my_iter)
            for v in my_iter:
                residual_succ[u][v]['flow'] += flow
                residual_succ[v][u]['flow'] -= flow
                u = v
            return flow

        def bfs():
            predecessor = {s: None}
            queue_s = [s]
            successor = {t: None}
            queue_t = [t]
            while True:
                queue = []
                if len(queue_s) <= len(queue_t):
                    for u in queue_s:
                        for v, attribute in residual_succ[u].items():
                            if v not in predecessor and attribute['flow'] < attribute['capacity']:
                                predecessor[v] = u
                                if v in successor:
                                    return v, predecessor, successor
                                queue.append(v)
                    if not queue:
                        return None, None, None
                    queue_s = queue
                else:
                    for u in queue_t:
                        for v, attribute in residual_pred[u].items():
                            if v not in successor and attribute['flow'] < attribute['capacity']:
                                successor[v] = u
                                if v in predecessor:
                                    return v, predecessor, successor
                                queue.append(v)
                    if not queue:
                        return None, None, None
                    queue_t = queue

        
        flow_value = 0
        while flow_value < cutoff:
            v, predecessor, successor = bfs()
            if predecessor is None:
                break
            path = [v]
            u = v
            while u != s:
                u = predecessor[u]
                path.append(u)

            path.reverse()
            u = v
            while u != t:
                u = successor[u]
                path.append(u)
            flow_value += augment(path)

        return flow_value




    R = my_edmonds_karp(G, my_source, my_sink)
    print(R.graph['flow_value'])


    flow_attr = nx.get_edge_attributes(R,'flow')


    # remove non-participating edges
    for k, v in flow_attr.items():
        if float(v) <= 0:
            R.remove_edge(k[0], k[1])

    flow_attr = nx.get_edge_attributes(R,'flow')

    cap_attr = nx.get_edge_attributes(R,'capacity')

    labels = {}

    for (k1, v1), (k2, v2) in zip(flow_attr.items(), cap_attr.items()):
        labels[k1] = str(v1) + "/" + str(v2)
    
    # Remove non participating nodes
    for final_node in list(R.nodes):
        if R.degree[final_node] == 0:
            R.remove_node(final_node)

    write_dot(R, r"C:\Users\Charun\Desktop\CSC301-Assignment6\output_graphs\output_" + str(id) + r".dot")

    pos=nx.spring_layout(R)

    nx.draw(R,pos,with_labels=True)
    nx.draw_networkx_edge_labels(R,pos,edge_labels=labels)
    plt.savefig(r"C:\Users\Charun\Desktop\CSC301-Assignment6\output_graphs\output_" + str(id) + r".png")

    plt.close()
    G.clear()
    R.clear()







