import random

class Node:
    def __init__(self, id, connections = [], data = None):
        self.id = id                        #Node Id
        self.connections = connections     #Nodes connected to this Node
        self.data = data                    #Data stored in this node (may or may not be used)

class PathGenerator:
    def __init__(self, node_count, average_connections):
        self.node_count = node_count
        self.connection_found = False
        self.node = []                     #List of Nodes 
        self.average_connections = average_connections

#region generation functions
    
    def generate_start(self):
        self.initialize_nodes()

        for node_id in range(0,self.node_count): #go through each node in node count
            average = 0
            totalconnections = random.binomialvariate(self.node_count,0.25)
            print("total connections " + str(totalconnections))
            for possible_node in range(0,totalconnections):
                print("Finding " + str(possible_node) + " connection for " + str(node_id))
                self.connection_found = False
                while not self.connection_found:
                    try_id = random.randint(0,self.node_count-1)
                    print("trying to pair " + str(try_id) + " with " + str(node_id))
                    print(self.node[try_id].connections)
                    if try_id is not node_id:
                        if try_id not in self.node[try_id].connections:
                            print("not found in connections, now adding")
                            self.node[try_id].connections.append(node_id)
                            self.node[node_id].connections.append(try_id)
                            self.connection_found = True
                    else:    
                        print(str(try_id) + " is self")         
            print("connections in " + str(node_id) + " = " + str(self.node[node_id].connections))            
                    

                    

    def initialize_nodes(self):
        for i in range(0,self.node_count):
            self.node.append(Node(i))               
                    
                
            #print("average " + str(average))
                    

#end region




if __name__ == "__main__":
    Map = PathGenerator(node_count = 10, average_connections = 3).generate_start()
    



        