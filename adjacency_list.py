import json

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

def main():
    graph = edges_to_adjacency_list('g3.txt')
    # print(json.dumps(graph, indent=4))
    # print(graph['9'])
    # print(graph['28'])
    # a = ['1', '5', '11', '12', '16', '22', '24', '28', '34', '35', '39', '45']
    # b = ['3', '4', '8', '9', '14', '15', '19', '20', '47']

    # print(set(a).intersection(b))

if __name__ == "__main__":
    main()