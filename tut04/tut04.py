
from datetime import datetime
start_time = datetime.now()

import threading
import time
import queue
import sys
        
adj_matrix = {}
all_tables = {}
all_queues = {}

def new_node(node1, node2, w):
    
    if node1 not in adj_matrix:
        adj_matrix[node1] = {}
    adj_matrix[node1][node2] = int(w)

    if node2 not in adj_matrix:
        adj_matrix[node2] = {}
    adj_matrix[node2][node1] = int(w)


def read_txt_file(path):
    
    file = open(path, 'r')
    lines = file.readlines()
    file.close()
    n = int(lines[0].strip())
    nodes = lines[1].split()
    for l in lines[2:]:
        l = l.split()
        if l=='EOF' : break
        if len(l)>=3:
            new_node(l[0], l[1], int(l[2])) 
        else: print('wrong topology')              
        
    return n, nodes   

n_nodes = read_txt_file('/Users/salon/Downloads/2001CS75_CS359/tut04/topology.txt')
n = n_nodes[0]
nodes = n_nodes[1]

print('Total routers:', n)
print('Routers:', nodes)
print('\nAdjacency Matrix:')
print(adj_matrix)

for node in nodes:
    all_queues[node] = queue.Queue()
    all_tables[node] = {}
lock = threading.Lock()
print(all_tables)


class router_thread(threading.Thread):
    
    def __init__(self, node_router):
        
        threading.Thread.__init__(self)
        self.node_router = node_router
        self.iteration = 1
        
    def run(self):
        
        self.init_routing_table()
        lock.acquire()
        print('\nInitial')
        print('Routing Table for:', self.node_router)
        print('\ndest\tcost\tnext_hop')
        for dest, [distance, next_hop] in all_tables[self.node_router].items():
            print(dest, distance, next_hop, sep='\t')
        print(all_tables[self.node_router])
        lock.release()
        
        for i in range(40):
            
            self.update_routing_table()
            lock.acquire()
            print('Iteration:', self.iteration)
            print('\nRouting Table for:', self.node_router)
            print('\ndest\tcost\tnext_hop')
            for dest, [distance, next_hop] in all_tables[self.node_router].items():
                print(dest, distance, next_hop, sep='\t')
            self.iteration += 1
            lock.release()
            time.sleep(2)
            
    def init_routing_table(self):
        
        for adj_node, distance in adj_matrix[self.node_router].items():
            all_tables[self.node_router][adj_node] = [distance, adj_node]
                        
        for node in nodes:
            if node != self.node_router and node not in adj_matrix[self.node_router]:
                all_tables[self.node_router][node] = [float('inf'), None]
        
    def send_routing_table(self):
    
        for adj_node in adj_matrix[self.node_router]:
            all_queues[adj_node].put((self.node_router, all_tables[self.node_router]))

    def receive_routing_table(self):
        
        while all_queues[self.node_router].qsize() < len(adj_matrix[self.node_router]):
            time.sleep(1)
        
        while not all_queues[self.node_router].empty():
            
            (adj_node, received_table) = all_queues[self.node_router].get()
            
            for dest, [distance, next_hop] in received_table.items():
                
                if dest != self.node_router:
                                
                    new_distance = adj_matrix[self.node_router][adj_node] + distance
                    if new_distance < all_tables[self.node_router][dest][0]:
                        all_tables[self.node_router][dest][0] = new_distance
                        all_tables[self.node_router][dest][1] = adj_node
        
    def update_routing_table(self):
    
        self.send_routing_table()
        self.receive_routing_table()
        
    
threads = []
for node in nodes:
    new_router_thread = router_thread(node)
    new_router_thread.start()
    
for thread in threads:
    thread.join()
        
        
        
#This shall be the last lines of the code.
end_time = datetime.now()
print('Duration of Program Execution: {}'.format(end_time - start_time))
