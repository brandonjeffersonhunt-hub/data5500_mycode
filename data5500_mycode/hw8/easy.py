#Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph.

import networkx as nx
def count_nodes(graph: nx.Graph):
    return Graph.number_of_nodes()



Graph = nx.Graph()
Graph.add_nodes_from([1,2,3,4])                             #code wasnt working so i put it in chat and asked what was wrong. I didnt have the G in graph captitalized lol
Graph.add_edges_from([(1,2), (2,4), (4,3), (4,1)])


print(count_nodes(Graph))