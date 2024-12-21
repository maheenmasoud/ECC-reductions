from copy import deepcopy
import random
import cProfile

# lifted simplicial reduction algorithm

def is_clique(common_uncovered_vertices, common_uncovered_edges):
    len_common_vertices = len(common_uncovered_vertices)
    len_common_edges = len(common_uncovered_edges)
    return len_common_edges == len_common_vertices * (len_common_vertices - 1) // 2

def lifted_simplicial_reduction(graph, uncovered_edges, clique_cover):
    # iterate over all uncovered edges in the graph
    for edge in uncovered_edges:
        random_vertex, random_connected_vertex = edge
        print("Current edge:", edge)

        # find the common neighbors of the random edge in the graph
        common_neighbors = set(graph[random_vertex]).intersection(set(graph[random_connected_vertex]))
        common_neighbors.add(random_vertex)
        common_neighbors.add(random_connected_vertex)

        print("common neighbors", common_neighbors)

        # collect uncovered edges in the common neighbors
        uncovered_edges_common_neighbors = set()
        uncovered_vertices_commmon_neighbors = set()
            
        # collect uncovered edges in the common neighbors
        for u in common_neighbors:
            for v in graph[u]:
                if (v in common_neighbors) and ((u, v) in uncovered_edges or (v, u) in uncovered_edges) and (v, u) not in uncovered_edges_common_neighbors:
                    uncovered_edges_common_neighbors.add((u, v))
                    uncovered_vertices_commmon_neighbors.add(u)
                    uncovered_vertices_commmon_neighbors.add(v)

        # if the common neighbors have no uncovered edges, remove the edge from the productive edges
        if  len(uncovered_edges_common_neighbors) == 1:
            print(f"No uncovered edges in common neighbors or no common neighbors for edge {edge}")
            continue

        print("Uncovered edges in common neighbors:", uncovered_edges_common_neighbors)
        print("Uncovered vertices in common neighbors:", uncovered_vertices_commmon_neighbors)

        # check if the common uncovered edges form a clique
        if is_clique(uncovered_vertices_commmon_neighbors, uncovered_edges_common_neighbors):
            print("Clique found")

            # append all common edges (not only the covered ones) to the clique cover
            clique = set()
            for u in common_neighbors:
                for v in common_neighbors:
                    if u != v and (v, u) not in clique:
                        clique.add((u, v))
                       
            print("Clique:", clique)
            clique_cover.append(clique)

            # remove the covered edges from the uncovered edges
            # equivalent to covering uncovered edges
            for edge in uncovered_edges_common_neighbors:
                if edge in uncovered_edges:
                    uncovered_edges.remove(edge)
                elif (edge[1], edge[0]) in uncovered_edges:
                    uncovered_edges.remove((edge[1], edge[0]))
                    
        else:
            print("No clique found")
            continue

def make_uncovered_edges(graph):
    uncovered_edges = set()
    for u in graph:
        for v in graph[u]:
            if (u, v) not in uncovered_edges and (v, u) not in uncovered_edges:
                uncovered_edges.add((u, v))
    return uncovered_edges

def find_cliques(graph):
    clique_cover = []
    uncovered_edges = make_uncovered_edges(graph)
    lifted_simplicial_reduction(graph, uncovered_edges, clique_cover)

    return clique_cover, uncovered_edges

def edges_to_adjacency_list(file_path):
    adjacency_list = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            vertex1, vertex2 = line.strip().split()
            
            if vertex1 not in adjacency_list:
                adjacency_list[vertex1] = []
            adjacency_list[vertex1].append(vertex2)
            
            if vertex2 not in adjacency_list:
                adjacency_list[vertex2] = []
            adjacency_list[vertex2].append(vertex1)
    
    return adjacency_list

def main(graph):
    print("Length of graph:", len(graph))
    clique_cover, uncovered_edges = find_cliques(graph)
    #print("Uncovered edges:", uncovered_edges)
    #print("Clique cover:", clique_cover)
    print("Number of uncovered edges:", len(uncovered_edges))
    print("Number of cliques:", len(clique_cover))

def profile_main(graph):
    cProfile.run('main(graph5)')


if __name__ == "__main__":
    graph = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'C', 'D'],
        'C': ['A', 'B', 'D'],
        'D': ['B', 'A', 'C'],
    }
    graph1 = {
        'A': ['B', 'C', 'D', 'E'],
        'B': ['A', 'C', 'D'],
        'C': ['A', 'B', 'D'],
        'D': ['A', 'B', 'C', 'E'],
        'E': ['A', 'D']
    }

    #main(graph1)
    #main(edges_to_adjacency_list('g5.txt'))
    graph5 = edges_to_adjacency_list('g7.txt')
    #profile_main(graph5)
    main(graph5)

    