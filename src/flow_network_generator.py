# Generate a graph and save to .dot file
import random
import networkx as nx
import matplotlib.pyplot as plt

order = random.randint(4,6)

G = nx.DiGraph()

for i in range(1, order+1):
    G.add_node(i)


source = 1
sink = order + 1
# G.add_edge(source, sink)


outgoing_source_edges = random.randint(2, order - 1)
print(outgoing_source_edges)

node_dict = {}
nodeList = list(G.nodes)
print(nodeList[0], nodeList[-1])
# create outgoing edges from source to random vertices
for i in range(0, outgoing_source_edges):
    G.add_edge(nodeList[0], nodeList[i])

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
            print(valid_edge, node_dict)

        G.add_edge(curr_node, random_node)
        node_dict[valid_edge] = 0

# size = random.randint(order - 1, (order * (order - 1)))

# '''
# Start with source
# Pick random number of edges

# '''


# print(nodeList)
# for i in range(0, size + 1):


#     random_source_index = random.randint(1, len(nodeList) - 1)
#     random_dest_index = random.randint(1, len(nodeList) - 1)

#     while random_source_index == random_dest_index:
#         random_dest_index = random.randint(1, len(nodeList) - 1)
    
#     cur = (random_source_index, random_dest_index)


#     if cur not in node_dict:
#         G.add_edge(random_source_index, random_dest_index)
#         node_dict[cur] = 0
#     else:
#         random_source_index = random.randint(1, len(nodeList) - 1)
#         random_dest_index = random.randint(1, len(nodeList) - 1)

#         while random_source_index == random_dest_index:
#             random_dest_index = random.randint(1, len(nodeList) - 1)

#         cur = (random_source_index, random_dest_index)

#         G.add_edge(random_source_index, random_dest_index)
#         node_dict[cur] = 0
        
        


pos = nx.random_layout(G)

nx.draw(G, pos=pos, with_labels=True, font_weight='bold')

print(node_dict)
plt.show()

