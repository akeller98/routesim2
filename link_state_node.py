from simulator.node import Node
from sim_graph import SimulatorGraph
import copy
import json


class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.logging.debug("new node %d" % self.id)
        self.link_seq_nums = {}
        self.link_largest_message_recv = {}
        self.graph = SimulatorGraph(0)

    # Return a string
    def __str__(self):
        neighbor_str = self.graph.get_neighbors(self.id)
        return ""

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        if latency == -1 and neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
            self.graph.remove_edge(self.id, neighbor)
        else:
            self.neighbors.append(neighbor)
            #print("link_has_been_updated: adding edge ({}, {})".format(self.id, neighbor))
            self.graph.add_edge(self.id, neighbor, latency)
            new_node_message = {"graph": self.graph.adj_list, "seq_nums": self.link_seq_nums}
            new_node_message_json = json.dumps(new_node_message)
            self.send_to_neighbor(neighbor, new_node_message_json)
            # {src, dst, cost, seq/time}
        
        if neighbor not in self.link_seq_nums:
            self.link_seq_nums[neighbor] = 1
        else:
            self.link_seq_nums[neighbor] += 1
        
        #Pack into JSON
        message = {"src": self.id, "dst": neighbor, "cost": latency, "seq": self.link_seq_nums[neighbor]}
        json_message = json.dumps(message)
        self.send_to_neighbors(json_message)

    # Fill in this function
    def process_incoming_routing_message(self, m):
        message = json.loads(m)
        if "graph" in message and "seq_nums" in message:
            temp_adj_list = message["graph"]
            for node1, val in temp_adj_list.items():
                for node2, cost in val.items():
                    self.graph.add_edge(int(node1), int(node2), int(cost))
            self.link_seq_nums = message["seq_nums"]
            return
        src = message["src"]
        dst = message["dst"]
        latency = message["cost"]
        seq = message["seq"]
        #print('id', self.id, "src", src, "dst", dst, "seq", seq, self.link_seq_nums)
        
        if src not in self.link_seq_nums or seq > self.link_seq_nums[src] or src not in self.link_largest_message_recv:
            self.link_seq_nums[src] = seq
            self.link_largest_message_recv[src] = m
            if latency == -1 and src in self.neighbors:
                self.neighbors.remove(src)
                self.graph.remove_edge(src, dst)
            else:
                #check is new node added and new node is adjacent 
                if self.id == dst and src not in self.neighbors:
                    self.neighbors.append(src)
                #print("process_incoming_routing_message: adding edge ({}, {})".format(src, dst))
                self.graph.add_edge(src, dst, latency)
            #send to all neighbors except original sender
            for n in self.neighbors:
                if n != src:
                    self.send_to_neighbor(n, m)
        else:
            #send largest message received back to sender
            self.send_to_neighbor(src, self.link_largest_message_recv[src])

    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        return self.graph.get_best_neighbor(self.id, destination)