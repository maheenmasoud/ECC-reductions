import networkx as nx
import matplotlib.pyplot as plt

def visualize_graph(file_path):
    edges =[]

    with open(file_path, 'r') as file:
        for line in file:
            vertex1, vertex2 = line.strip().split()
            edges.append((vertex1, vertex2))

        G = nx.Graph()
        G.add_edges_from(edges)

        nx.draw(G, with_labels=True)
        plt.show()

if __name__ == "__main__":
    visualize_graph('g8.txt')
