import networkx as nx
import matplotlib.pyplot as plt


# Structure of the Weighted Bipartite Graph
class Bipartite_graph:

    # Let B=(V,E) an instance of a bipartite graph such that V=L∪R and |L|=n and |R|<=n
    # Let M=(V,E) a matching of B
    # vertices in L are defined
    def __init__(self,n):
        self.B = nx.Graph()
        self.M = nx.Graph()
        self.n=n
        self.L=[]
        self.R=[]
        for c in range(n):
            self.B.add_node(c,bipartite=0)
            self.M.add_node(c,bipartite=0)
            self.L.append(c)

    # This function returns a list of all the edges of a Bipartite graph
    def get_edges(self):
        return list(self.B.edges(data='weight'))
    
    def get_edges_matching(self):
        return list(self.M.edges(data='weight'))
    
    def perfect(self):
        for u in self.L:
            if self.M.degree[u] != 1:
                return False
        return True
    
    def control(self):
        for l in self.L:
            w = sum(self.M[l][r]["weight"] for r in self.M.neighbors(l))
            if(w>1):
                print("ERROR: constraint L not respected") 
        for r in self.R:
            w = sum(self.M[l][r]["weight"] for l in self.M.neighbors(r))
            if(w>1):
                print("ERROR: constraint R not respected")

    # Function called at time t in the online setting (and initialization of offline setting)
    # The remaining informations about G is revealed over t=1,2,...,|R|.
    # When a vertex v in R is revealed then all edges from v to the vertices in L are revealed.
    def revealed(self,t,edges): 
        self.B.add_node(t,bipartite=1)
        self.M.add_node(t,bipartite=1)
        self.R.append(t)
        for e in edges:
            e,w=e.split(':')
            self.B.add_edge(t,int(e),weight=int(w))
    
    # Display functions

    # Display the Bipartite graph
    def display(self):
        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(self.L) ) # put nodes from L at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(self.R) ) # put nodes from R at x=2
        # # nodes
        nx.draw_networkx_nodes(self.B, pos, node_size=700)
        # edges
        nx.draw_networkx_edges(self.B, pos, width=6)
        # node labels
        nx.draw_networkx_labels(self.B, pos, font_size=20, font_family="sans-serif") 
        # edge weight labels
        edge_labels = nx.get_edge_attributes(self.B, "weight")
        nx.draw_networkx_edge_labels(self.B, pos, edge_labels)
        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

    # Display the matching of the Bipartite graph
    def display_matching(self):
        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(self.L) ) # put nodes from L at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(self.R) ) # put nodes from R at x=2
        # # nodes
        nx.draw_networkx_nodes(self.M, pos, node_size=700)
        # edges
        nx.draw_networkx_edges(self.M, pos, width=6)
        # node labels
        nx.draw_networkx_labels(self.M, pos, font_size=20, font_family="sans-serif") 
        # edge weight labels
        edge_labels = nx.get_edge_attributes(self.M, "weight")
        nx.draw_networkx_edge_labels(self.M, pos, edge_labels)
        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()


# Initialization of the Bipartite graph in the Offline setting
# At initialization time, all vertices and edges are known, getting the informations from a file
def offline_init(filename):
    f = open(filename, "r")
    n = f.readline()
    B = Bipartite_graph(int(n))
    t = B.n
    for x in f:
        new=[]
        for e in x.split():
            new.append(e)
        B.revealed(t,new)
        t=t+1
    f.close()
    return B