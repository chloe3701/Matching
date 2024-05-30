import hungarian_classic
from random import choice
import networkx as nx

# find min sum(i in V) d[i]
# s.t d[i]+d[j] >= r[i][j] for (i,j) in E
def approx_dist_feasible(B,r):
    d={v : 0 for v in B.B.nodes()}
    G = B.B.copy()
    L=B.L.copy()
    while (G.edges()):
        i = choice(L)
        while (G.degree(i)>0):
            # j = arg max(r[i][j] for j in neighbors(i))
            if(i<B.n):
                j = max(G.neighbors(i), key=lambda j: r[i][j])
                d[i] =r[i][j]
                L.remove(i)
            else:
                j = max(G.neighbors(i), key=lambda j: r[j][i])
                d[i] =r[j][i]
            G.remove_node(i)
            i=j
    return d

def make_feasible(B,p,q):
    # r[u][v] is the "overflow" of the edge (u,v)
    # meaning by how much p[u]+q[v] break the weight of the edge (u,v)
    r = {u:{} for u in B.L}
    for e in B.B.edges():
        u=min(e[0],e[1])
        v=max(e[0],e[1])
        r[u][v] = max(0, p[u]+q[v] - B.B[u][v]["weight"])
    d = approx_dist_feasible(B,r)
    while(d):
        v,dv=d.popitem()
        if(v<B.n):
            p[v]=p[v]-dv
        else:
            q[v]=q[v]-dv
        
    return p,q

def predict_dual(B,model):
    p = {u: 50 for u in B.L}
    q = {v: -10 for v in B.R}
    return p,q

# Initialisation: M = ∅ p=q= learned duals
# TODO: Learn the duals
def init_dual(B,model):
    p,q = predict_dual(B,model)
    p,q = make_feasible(B,p,q)
    
    return p,q

def hungarian_learned(B,model):
    p,q = init_dual(B,model)
    w = hungarian_classic.hungarian(B,p,q)
    hungarian_classic.verify(B,p,q)
    B.display_matching()
    return w
    