import networkx as nx
import matplotlib.pyplot as plt
import Matching.Online.waterfilling as w


# Online Minimum Weight Perfect Matching

# Let G=(V,E) an instance of a bipartite graph such that V=L∪R and at t=0, only the vertices in L are known.
# The remaining informations about G is revealed over t=1,2,...,|R|.
# When a vertex v in R is revealed then all edges from v to the vertices in L are revealed.
class Bipartite_graph:
    # initializing G at t=0 : only L is known
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

    def display(self):
        pos = dict()
        pos.update( (n, (1, i)) for i, n in enumerate(self.L) ) # put nodes from L at x=1
        pos.update( (n, (2, i)) for i, n in enumerate(self.R) ) # put nodes from R at x=2
        # # nodes
        nx.draw_networkx_nodes(self.B, pos, node_size=700)
        # edges
        nx.draw_networkx_edges(self.B, pos, width=6)
        ax = plt.gca()
        ax.margins(0.08)
        plt.axis("off")
        plt.tight_layout()
        plt.show()

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


    def revealed(self,t,edges): 
        self.B.add_node(t,bipartite=1)
        self.M.add_node(t,bipartite=1)
        self.R.append(t)
        for e in edges:
            self.B.add_edge(t,e)



def wat(filename,display=False,steps=False):
    f = open(filename, "r")
    n = f.readline()
    B=Bipartite_graph(int(n))
    t=B.n
    d={}
    for x in f:
        new_revealed=[]
        for e in x.split():
            new_revealed.append(int(e))
        B.revealed(t,new_revealed)
        w.waterfilling(B, t, new_revealed,d)
        if(steps):
            B.display_matching()
        t=t+1
    if(display):
        B.display_matching()
    f.close()