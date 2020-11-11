[1mdiff --git a/link_state_node_copy.py b/link_state_node_copy.py[m
[1mindex 3a14fac..0d70369 100644[m
[1m--- a/link_state_node_copy.py[m
[1m+++ b/link_state_node_copy.py[m
[36m@@ -59,7 +59,7 @@[m [mclass Link_State_Node(Node):[m
             [m
     [m
     def process_message(self, msg):[m
[31m-        print(type(msg))[m
[32m+[m[32m        #print(type(msg))[m
         #msg_dict = json.loads(msg)[m
         msg_dict = msg[m
         #print(type(msg_dict))[m
[36m@@ -79,6 +79,7 @@[m [mclass Link_State_Node(Node):[m
         if latency == -1:[m
             if self.check_exists(src, dst) and seq > self.link_seq_nums[src][dst]:[m
                 self.graph.remove_edge(src, dst) # remove edge checks if it exists[m
[32m+[m[32m                self.update_seq_num(src, dst, seq)[m
                 if src == self.id:[m
                     self.neighbors.remove(dst)[m
                 if dst == self.id:[m
[36m@@ -120,15 +121,7 @@[m [mclass Link_State_Node(Node):[m
             new_neighbor = neighbor not in self.graph.adj_list[m
             if neighbor not in self.neighbors:[m
                 self.neighbors.append(neighbor)[m
[31m-            #print(self.id, neighbor)[m
[31m-            #print('link_has_been_updated: adding edge ({}, {})'.format(self.id, neighbor))[m
             self.graph.add_edge(self.id, neighbor, latency)[m
[31m-            #print(self.graph.print_graph())[m
[31m-            # new_node_message = {'graph': self.graph.adj_list, 'seq_nums': self.link_seq_nums}[m
[31m-            # new_node_message_json = json.dumps(new_node_message)[m
[31m-            # longest_message_recv_json = json.dumps(self.link_largest_message_recv)[m
[31m-            #self.send_to_neighbor(neighbor, new_node_message_json)[m
[31m-            # {src, dst, cost, seq/time}[m
         [m
         # might have to update largest message receive idk[m
         [m
[36m@@ -150,6 +143,8 @@[m [mclass Link_State_Node(Node):[m
 [m
     # Fill in this function[m
     def process_incoming_routing_message(self, m):[m
[32m+[m[32m        if self.id==1:[m
[32m+[m[32m            print(m)[m
         message = json.loads(m)[m
         # figure out which largest messages are relevant to us[m
         #print(self.id, message)[m
[36m@@ -161,17 +156,6 @@[m [mclass Link_State_Node(Node):[m
         first_update = self.process_message(message)[m
         if 'largest_messages' in message:[m
             node_dict = message['largest_messages'][m
[31m-            # for node1, msg_dict in node_dict.items():[m
[31m-            #     for node2, msg in msg_dict.items():[m
[31m-            #         msg_json = json.dumps(node_dict[node1][node2])[m
[31m-            #         print("msg json: ", msg_json)[m
[31m-            #         is_new = self.process_message(msg_json)[m
[31m-            #         if is_new != True:[m
[31m-            #             #print(self.id, message, updated_response)[m
[31m-            #             #self.graph.print_graph()[m
[31m-            #             if int(node1) not in updated_response:[m
[31m-            #                 updated_response[int(node1)] = {}[m
[31m-            #             updated_response[int(node1)][int(node2)] = is_new[m
             for node1 in node_dict:[m
                 for node2 in node_dict[node1]:[m
                     #msg_json = json.dumps(node_dict[node1][node2])[m
[36m@@ -186,14 +170,13 @@[m [mclass Link_State_Node(Node):[m
                         updated_response[int(node1)][int(node2)] = is_new[m
         [m
         if first_update != True or updated_response != {}: # have to resend something[m
[31m-            print(updated_response)[m
[32m+[m[32m            #print(updated_response)[m
             first_update_obj = first_update #json.loads(first_update)[m
             msg = {'src': src, 'dst': dst, 'cost': first_update_obj['cost'], 'seq': first_update_obj['seq']}[m
             json_msg = json.dumps(msg)[m
             if first_update == True: # just resend data we received, must have to send other data[m
                 msg = {'src': src, 'dst': dst, 'cost': latency, 'seq': seq, 'largest_messages': updated_response}[m
                 json_msg = json.dumps(msg)[m
[31m-                # some information is new, send the original message[m
                 for neighbor in self.neighbors:[m
                     if neighbor != src: [m
                         self.send_to_neighbor(neighbor, m)[m
[36m@@ -201,8 +184,12 @@[m [mclass Link_State_Node(Node):[m
                 first_update_obj = first_update # json.loads(first_update)[m
                 msg = {'src': src, 'dst': dst, 'cost': first_update_obj['cost'], 'seq': first_update_obj['seq'], 'largest_messages': updated_response}[m
                 json_msg = json.dumps(msg)[m
[31m-            [m
             self.send_to_neighbor(src, json_msg) # send some variant of the above messages[m
[32m+[m[32m        #if first_update == True:[m
[32m+[m[32m            # some information is new, send the original message[m
[32m+[m[32m            # for neighbor in self.neighbors:[m
[32m+[m[32m            #     if neighbor != src:[m[41m [m
[32m+[m[32m            #         self.send_to_neighbor(neighbor, m)[m
 [m
 [m
     # Return a neighbor, -1 if no path to destination[m
[1mdiff --git a/simulator/config.py b/simulator/config.py[m
[1mindex 330a56f..3409c0d 100644[m
[1m--- a/simulator/config.py[m
[1m+++ b/simulator/config.py[m
[36m@@ -1,6 +1,6 @@[m
 from generic_node import Generic_Node[m
 from distance_vector_node import Distance_Vector_Node[m
[31m-from link_state_node import Link_State_Node[m
[32m+[m[32mfrom link_state_node_copy import Link_State_Node[m
 [m
 ROUTE_ALGORITHM = [[m
     "GENERIC",[m
