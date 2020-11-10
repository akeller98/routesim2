import sys

class SimulatorGraph:
    def __init__(self, num_vertices):
        self.num_vertices = num_vertices
        self.adj_list = {}
        #{0: {1: 6, 2: 6}}
        for i in range(self.num_vertices):
            self.adj_list[i] = {}

    def add_edge(self, src, dst, cost):
        #print("adding edge ({}, {})".format(src, dst))
        if src in self.adj_list:
            self.adj_list[src][dst] = cost
        else:
            self.num_vertices += 1
            self.adj_list[src] = {dst: cost}
        if dst in self.adj_list:
            self.adj_list[dst][src] = cost
        else:
            self.num_vertices += 1
            self.adj_list[dst] = {src: cost}

    def remove_edge(self, src, dst):
        #print("removing edge ({}, {})".format(src, dst))
        if src in self.adj_list:
            if dst in self.adj_list[src]:
                del self.adj_list[src][dst]
                del self.adj_list[dst][src]
    
    def remove_node(self, node):
        #print("removing node {}".format(node))
        self.num_vertices -= 1
        if node in self.adj_list:
            del self.adj_list[node]
            for adj_node in self.adj_list:
                if node in self.adj_list[adj_node]:
                    del self.adj_list[adj_node][node]
                    
    def print_graph(self):
        print(self.adj_list)

    def get_neighbors(self, node):
        if node in self.adj_list:
            return self.adj_list[node]
        else:
            return {}

    def get_min_edge(self, dist, path):
        min_edge = sys.maxsize
        min_vertex = -1
        for vertex in self.adj_list.keys():
            if vertex not in path and dist[vertex] < min_edge:
                min_edge = dist[vertex]
                min_vertex = vertex
        return min_vertex

    def dijkstra(self, start_node):
        dist = {}
        for node in self.adj_list.keys():
            dist[node] = sys.maxsize
        dist[start_node] = 0
        prev = {}
        prev[start_node] = -1

        min_path = {}
        for node in self.adj_list.keys():
            next_node = self.get_min_edge(dist, min_path)
            if next_node == -1:
                continue
            min_path[next_node] = node
            
            #print(self.get_neighbors(next_node))
            for neighbor, latency in self.get_neighbors(next_node).items():
                if neighbor not in min_path and dist[neighbor] > dist[next_node] + latency:
                    dist[neighbor] = dist[next_node] + latency
                    prev[neighbor] = next_node
        return prev

    def get_best_neighbor(self, src, dest):
        print("About to run dijkstra's on {} to {}".format(src, dest))
        shortest_paths = self.dijkstra(dest)
        self.print_graph()
        if src in shortest_paths:
            return shortest_paths[src]
        else:
            return -1
        
def main():
    graph4 = SimulatorGraph(8)
    graph4.add_edge(0,4,7)
    graph4.add_edge(4,7,3)
    graph4.add_edge(7,3,7)
    graph4.add_edge(7,6,6)
    graph4.add_edge(6,5,4)
    graph4.add_edge(5,1,4)
    graph4.add_edge(5,2,5)
    graph4.add_edge(2,4,6)
    graph4.dijkstra(2)

    graph = SimulatorGraph(5)
    graph.add_edge(0,1,10)
    graph.add_edge(1,2,12)
    graph.add_edge(2,3,23)
    graph.add_edge(0,2,122)
    graph.add_edge(1,3,333)
    graph.remove_edge(1,2)
    graph.print_graph()
    graph.dijkstra(0)

    print("\n\n")

    graph2 = SimulatorGraph(5)
    graph2.add_edge(0,1,10)
    graph2.add_edge(1,2,12)
    graph2.add_edge(2,3,23)
    graph2.remove_node(2)
    graph2.print_graph()

    print("\n\n")

    graph3 = SimulatorGraph(0)
    graph3.add_edge(0,1,3)
    graph3.print_graph()
    
if __name__ == '__main__':
    print("Poo Poo Pee Pee")
    main()
