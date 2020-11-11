from simulator.node import Node
from sim_graph import SimulatorGraph
import copy
import json

################ TODO: Change link_seq_num and link_largest_message_recvd to be undirected (entry for both nodes)

class Link_State_Node(Node):
    def __init__(self, id):
        super().__init__(id)
        self.logging.debug('new node %d' % self.id)
        self.link_seq_nums = {}
        self.link_largest_message_recv = {}
        self.graph = SimulatorGraph(0)

    def check_exists(self, node1, node2):
        return (node1 in self.graph.adj_list and node2 in self.graph.adj_list[node1])
    
    def increment_seq_num(self, src, dst):
        # check if src and dst are in link_seq_num
        if src not in self.link_seq_nums:
            self.link_seq_nums[src] = {}
        if dst not in self.link_seq_nums:
            self.link_seq_nums[dst] = {}
        
        # actually do the incrementing
        if dst not in self.link_seq_nums[src]:
            self.link_seq_nums[src][dst] = 1 
        else:
            self.link_seq_nums[src][dst] += 1
        if src not in self.link_seq_nums[dst]:
            self.link_seq_nums[dst][src] = 1 
        else:
            self.link_seq_nums[dst][src] += 1

    def update_seq_num(self, src, dst, new_seq_num):
        if src not in self.link_seq_nums:
            self.link_seq_nums[src] = {}
        if dst not in self.link_seq_nums:
            self.link_seq_nums[dst] = {}
        self.link_seq_nums[src][dst] = new_seq_num
        self.link_seq_nums[dst][src] = new_seq_num   
        
    def update_lmr(self, src, dst, msg):
        #msg = json.loads(msg_json)
        #if self.id==20:
            #print('Updating node {}'s lmr to {}-{}-{}'.format(self.id, src, dst, msg))
        if src not in self.link_largest_message_recv:
            #self.link_largest_message_recv.update({src: {dst: msg}})
            self.link_largest_message_recv[src] = {}
        if dst not in self.link_largest_message_recv:
            #self.link_largest_message_recv.update({dst: {src: msg}})
            self.link_largest_message_recv[dst] = {}
        self.link_largest_message_recv[dst][src] = msg
        self.link_largest_message_recv[src][dst] = msg
        
        #if self.id==20:
         #   print("Updated node {}'s lmr to: {}".format(self.id, msg))
            
    
    def process_message(self, msg):
        #print(type(msg))
        #msg_dict = json.loads(msg)
        msg_dict = msg
        #print(type(msg_dict))
        #print(msg_dict)
        
        #if isinstance(msg_dict, str):
         #   msg_dict = json.loads(msg_dict)
        src = msg_dict['src']
        src = int(src)
        dst = msg_dict['dst']
        dst = int(dst)
        latency = msg_dict['cost']
        latency = int(latency)
        seq = msg_dict['seq']
        seq = int(seq)
        
        if latency == -1:
            if self.check_exists(src, dst) and seq > self.link_seq_nums[src][dst]:
                self.graph.remove_edge(src, dst) # remove edge checks if it exists
                self.update_seq_num(src, dst, seq)
                if src == self.id:
                    self.neighbors.remove(dst)
                if dst == self.id:
                    self.neighbors.remove(src)
                self.update_lmr(src, dst, msg)
                return True
            else:
                print(self.id, msg, self.link_largest_message_recv)
                return self.link_largest_message_recv[src][dst] 
        # do this if latency is non-negative
        if not self.check_exists(src, dst):
            if src in self.link_largest_message_recv:
                if dst in self.link_largest_message_recv[src] and self.link_largest_message_recv[src][dst]["cost"] == -1:
                    return self.link_largest_message_recv[src][dst]
            if dst == self.id:
                self.neighbors.append(src)
            if src == self.id:
                self.neighbors.append(dst)
            self.graph.add_edge(src, dst, latency)
            self.update_seq_num(src, dst, seq)
            self.update_lmr(src, dst, msg)
            return True
        elif seq > self.link_seq_nums[src][dst]: # and latency < self.graph.adj_list[src][1]:
            self.graph.add_edge(src, dst, latency)
            self.update_seq_num(src, dst, seq)
            self.update_lmr(src, dst, msg)
            return True
        #print(self.id, src, dst, self.link_largest_message_recv)
        #print(self.link_largest_message_recv[src][dst])
        return self.link_largest_message_recv[src][dst]

    # Return a string
    def __str__(self):
        neighbor_str = self.graph.get_neighbors(self.id)
        return ''

    # Fill in this function
    def link_has_been_updated(self, neighbor, latency):
        new_neighbor = False
        if latency == -1 and neighbor in self.neighbors:
            self.neighbors.remove(neighbor)
            self.graph.remove_edge(self.id, neighbor)
        else:
            new_neighbor = neighbor not in self.graph.adj_list
            if neighbor not in self.neighbors:
                self.neighbors.append(neighbor)
            self.graph.add_edge(self.id, neighbor, latency)
        
        # might have to update largest message receive idk
        
        self.increment_seq_num(self.id, neighbor)
        
        #print(self.id, neighbor, self.link_seq_nums)
        message = {'src': self.id, 'dst': neighbor, 'cost': latency, 'seq': self.link_seq_nums[self.id][neighbor]}
        json_message = json.dumps(message)
        self.update_lmr(self.id, neighbor, message)

        #Pack into JSON
        if new_neighbor and self.link_largest_message_recv != {}:
            message = {'src': self.id, 'dst': neighbor, 'cost': latency, 'seq': self.link_seq_nums[self.id][neighbor], 'largest_messages': self.link_largest_message_recv}
            json_message = json.dumps(message)
            self.send_to_neighbor(neighbor, json_message)
        # send new link data to all neighbors
        
        for n in self.neighbors:
            if n != neighbor:
                self.send_to_neighbor(n, json_message)

    # Fill in this function
    def process_incoming_routing_message(self, m):
        
        message = json.loads(m)
        # figure out which largest messages are relevant to us
        #print(self.id, message)
        src = int(message['src']) # who we received this message from
        dst = int(message['dst']) # the node the sender is connected to
        latency = int(message['cost'])
        seq = int(message['seq'])
        updated_response = {}
        forward_response = {}
        first_update = self.process_message(message)
        if 'largest_messages' in message:
            node_dict = message['largest_messages']
            for node1 in node_dict:
                for node2 in node_dict[node1]:
                    #msg_json = json.dumps(node_dict[node1][node2])
                    #print("msg json: ", msg_json)
                    #is_new = self.process_message(json.dumps(node_dict[node1][node2]))
                    is_new = self.process_message(node_dict[node1][node2])
                    if is_new != True:
                        #print(self.id, message, updated_response)
                        #self.graph.print_graph()
                        if int(node1) not in updated_response:
                            updated_response[int(node1)] = {}
                        updated_response[int(node1)][int(node2)] = is_new
                    else:
                        if int(node1) not in forward_response:
                            forward_response[int(node1)] = {}
                        forward_response[int(node1)][int(node2)] = node_dict[node1][node2]
        if first_update != True or updated_response != {}: # have to resend something
            #print(updated_response)
            if first_update != True:
                first_update_obj = first_update #json.loads(first_update)
                msg = {'src': src, 'dst': dst, 'cost': first_update_obj['cost'], 'seq': first_update_obj['seq']}
                json_msg = json.dumps(msg)
            if first_update == True: # just resend data we received, must have to send other data
                msg = {'src': src, 'dst': dst, 'cost': latency, 'seq': seq, 'largest_messages': updated_response}
                json_msg = json.dumps(msg)
                # if first_update == True:
                #     for neighbor in self.neighbors:
                #         if neighbor != src: 
                #             self.send_to_neighbor(neighbor, m)
            elif updated_response != {}:
                first_update_obj = first_update # json.loads(first_update)
                msg = {'src': src, 'dst': dst, 'cost': first_update_obj['cost'], 'seq': first_update_obj['seq'], 'largest_messages': updated_response}
                json_msg = json.dumps(msg)
            self.send_to_neighbor(src, json_msg) # send some variant of the above messages
        
        if first_update == True or forward_response != {}: 
            if forward_response != {}:
                msg = {'src': src, 'dst': dst, 'cost': latency, 'seq': seq, 'largest_messages': forward_response}
                json_msg = json.dumps(msg)
                for neighbor in self.neighbors:
                    if neighbor != src: 
                        self.send_to_neighbor(neighbor, json_msg)
            else:
                msg = {'src': src, 'dst': dst, 'cost': latency, 'seq': seq}
                json_msg = json.dumps(msg)
                for neighbor in self.neighbors:
                    if neighbor != src: 
                        self.send_to_neighbor(neighbor, json_msg)
        
        
        #if self.id == 2:
         #   print(self.id, self.neighbors)
        #if first_update == True:
            # some information is new, send the original message
            # for neighbor in self.neighbors:
            #     if neighbor != src: 
            #         self.send_to_neighbor(neighbor, m)


    # Return a neighbor, -1 if no path to destination
    def get_next_hop(self, destination):
        return self.graph.get_best_neighbor(self.id, destination)