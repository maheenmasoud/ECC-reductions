from copy import deepcopy
import random
import cProfile

# lifted simplicial reduction algorithm

# set the random seed
random.seed(0)

def rule_one(graph, uncovered_edges, removed_vertices):
    for vertex in graph:
        if vertex in removed_vertices:
            continue
        all_edges_covered = True
        for neighbor in graph[vertex]:
            if neighbor in removed_vertices:
                continue
            if (vertex, neighbor) not in uncovered_edges and (neighbor, vertex) not in uncovered_edges:
                all_edges_covered = False
                break
        
        if all_edges_covered:
            removed_vertices.add(vertex)
            
            for neighbor in graph[vertex]:
                if (vertex, neighbor) in uncovered_edges:
                    uncovered_edges.remove((vertex, neighbor))
                elif (neighbor, vertex) in uncovered_edges:
                    uncovered_edges.remove((neighbor, vertex))


def is_clique(common_uncovered_vertices, common_uncovered_edges):
    '''Function to check if the common uncovered edges form a clique'''
    len_common_vertices = len(common_uncovered_vertices)
    len_common_edges = len(common_uncovered_edges)
    # print("len_common_vertices", len_common_vertices)
    # print("len_common_edges", len_common_edges)
    return len_common_edges == len_common_vertices * (len_common_vertices - 1) // 2

def get_uncovered_edges_and_vertices(common_neighbors, uncovered_edges, graph):
    uncovered_edges_common_neighbors = set()
    uncovered_vertices_commmon_neighbors = set()
        
    # collect uncovered edges in the common neighbors
    for u in common_neighbors:
        for v in graph[u]:
            if (v in common_neighbors) and ((u, v) in uncovered_edges or (v, u) in uncovered_edges) and (v, u) not in uncovered_edges_common_neighbors:
                uncovered_edges_common_neighbors.add((u, v))
                uncovered_vertices_commmon_neighbors.add(u)
                uncovered_vertices_commmon_neighbors.add(v)
    return uncovered_edges_common_neighbors, uncovered_vertices_commmon_neighbors

def lifted_simplicial_reduction_new(graph, uncovered_edges, clique_cover, removed_vertices):
    for vertex in graph:
        if vertex in removed_vertices:
            continue
        
        for neighbor in graph[vertex]:
            if neighbor in removed_vertices:
                continue

            if (vertex, neighbor) not in uncovered_edges and (neighbor, vertex) not in uncovered_edges:
                continue
            common_neighbors_uncovered_edges = set()
            common_neighbors_uncovered_vertices = set()
            common_neighbors = set(graph[vertex]).intersection(set(graph[neighbor]))
            common_neighbors.add(vertex)
            common_neighbors.add(neighbor)

            #print("common neighbors", common_neighbors)
            common_neighbors_uncovered_edges, common_neighbors_uncovered_vertices = get_uncovered_edges_and_vertices(common_neighbors, uncovered_edges, graph)

            #print("Uncovered edges in common neighbors:", common_neighbors_uncovered_edges)
            #print("Uncovered vertices in common neighbors:", common_neighbors_uncovered_vertices)

            if len(common_neighbors_uncovered_edges) == 1:
                clique_cover.append({(vertex, neighbor)})
                if (vertex, neighbor) in uncovered_edges:
                    uncovered_edges.remove((vertex, neighbor))
                elif (neighbor, vertex) in uncovered_edges:
                    uncovered_edges.remove((neighbor, vertex))
                continue

            if is_clique(common_neighbors_uncovered_vertices, common_neighbors_uncovered_edges):
                clique = set()
                for u in common_neighbors:
                    for v in common_neighbors:
                        if u != v and (u, v) not in clique and (v, u) not in clique:
                            clique.add((u, v))

                #print("Clique:", clique)
                clique_cover.append(clique)

                for edge in common_neighbors_uncovered_edges:
                    if edge in uncovered_edges:
                        uncovered_edges.remove(edge)
                    elif (edge[1], edge[0]) in uncovered_edges:
                        uncovered_edges.remove((edge[1], edge[0]))
            # else:
            #     print("No clique found")

def make_uncovered_edges(graph):
    uncovered_edges = set()
    for u in graph:
        for v in graph[u]:
            if (u, v) not in uncovered_edges and (v, u) not in uncovered_edges:
                uncovered_edges.add((u, v))
    return uncovered_edges

def find_cliques(graph):
    clique_cover = []
    removed_vertices = set()
    uncovered_edges = make_uncovered_edges(graph)
    print("Uncovered edges before reduction:", len(uncovered_edges))
    #lifted_simplicial_reduction(graph, uncovered_edges, clique_cover)
    lifted_simplicial_reduction_new(graph, uncovered_edges, clique_cover, removed_vertices)

    return clique_cover, uncovered_edges

def edges_to_adjacency_list(file_path):
    adjacency_list = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            vertex1, vertex2 = line.strip().split()
            
            if vertex1 not in adjacency_list:
                adjacency_list[vertex1] = set()
            adjacency_list[vertex1].add(vertex2)
            
            if vertex2 not in adjacency_list:
                adjacency_list[vertex2] = set()
            adjacency_list[vertex2].add(vertex1)
    
    return adjacency_list

def main(graph):
    print("Length of graph:", len(graph))
    clique_cover, uncovered_edges = find_cliques(graph)
    #print("Uncovered edges:", uncovered_edges)
    #print("Clique cover:", clique_cover)
    print("Number of uncovered edges:", len(uncovered_edges))
    print("Number of cliques:", len(clique_cover))

def profile_main(graph):
    cProfile.run('main(graph)')

if __name__ == "__main__":
    #main(edges_to_adjacency_list('g5.txt'))
    graph = edges_to_adjacency_list('g1.txt')
    profile_main(graph)
    test_graph = {'1': {'2', '3', '4'}, '2': {'1', '3', '4'}, '3': {'1', '2', '4'}, '4': {'1', '2', '3'}}
    #main(test_graph)

    