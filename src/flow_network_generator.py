# Generate a graph and save to .dot file
import random
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import write_dot

# maximum capacity of the flow network
max_capacity = 20

def create_flow(id):

    # random number of nodes
    order = random.randint(4,6)


    G = nx.DiGraph()

    for i in range(1, order+1):
        G.add_node(i)


    source = 1
    sink = order + 1
    # G.add_edge(source, sink)


    outgoing_source_edges = random.randint(2, order - 1)
    

    node_dict = {}
    nodeList = list(G.nodes)
   
    # create outgoing edges from source to random vertices
    for i in range(1, outgoing_source_edges):
        G.add_edge(nodeList[0], nodeList[i], capacity=random.randint(1, max_capacity), flow=0)
        node_dict[(nodeList[0], nodeList[i])] = 0

    for i in range(1, len(nodeList)-1):
        for j in range(i, len(nodeList)):
            curr_node = nodeList[i]
            noti = random.randint(1, len(nodeList)-1)
            while noti == i:
                noti = random.randint(1, len(nodeList)-1)
            random_node = nodeList[noti]
            valid_edge = (curr_node, random_node)
            while valid_edge in node_dict.keys() or valid_edge[::-1] in node_dict.keys():
                noti = random.randint(1, len(nodeList)-1)
                while noti == i:
                    noti = random.randint(1, len(nodeList)-1)
                random_node = nodeList[noti]
                valid_edge = (curr_node, random_node)
                break
                
            # Remove self-loop and antiparallel edges
            rev_tuple = (random_node, curr_node)
            if rev_tuple not in node_dict and rev_tuple[0] != rev_tuple[1] :
                G.add_edge(curr_node, random_node, capacity=random.randint(1, max_capacity), flow=0)
                node_dict[valid_edge] = 0
            
                    


    pos = nx.random_layout(G)

    labels = nx.get_edge_attributes(G,'capacity')
    nx.draw(G, pos=pos, with_labels=True, font_weight='bold')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

    plt.savefig(r"C:\Users\Charun\Desktop\CSC301-Assignment6\input_graphs\input_" + str(id) + r".png")
    write_dot(G, r"C:\Users\Charun\Desktop\CSC301-Assignment6\input_graphs\input_" + str(id) + r".dot")
    plt.close()
    G.clear()




for i in range(1, 11):
    create_flow(i)
