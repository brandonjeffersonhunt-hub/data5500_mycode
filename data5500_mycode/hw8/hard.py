#  2. Write a Python function that takes a NetworkX graph as input and returns the number of nodes in the graph that have a degree greater than 5

#I was confused by the question so I chat gpt'd what it meant if a node has a degree of 5
import networkx as nx
def count_five_degree_nodes(graph: nx.Graph):
    count = 0
    for node, degree in graph.degree():
        if degree > 5:
            count += 1
        else:
            count += 0
    return count



Graph = nx.Graph()
Graph.add_nodes_from([1,2,3,4,5,6,7,8])                           
Graph.add_edges_from([(1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (8,1), (2,4), (5,7), (8,7)])


print("# of nodes with a degree > 5: ", count_five_degree_nodes(Graph))