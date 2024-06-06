import hungarian_classic
from random import choice
import networkx as nx
import learning

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
    #print(B.B.edges())
    for e in B.B.edges():
        u=min(e[0],e[1])
        v=max(e[0],e[1])
        p[u]=int(p[u])
        q[v]=int(q[v])
        r[u][v] = max(0, p[u]+q[v] - B.B[u][v]["weight"])
    d = approx_dist_feasible(B,r)
    while(d):
        v,dv=d.popitem()
        if(v<B.n):
            p[v]=p[v]-dv
        else:
            q[v]=q[v]-dv
        
    return p,q

# TODO: Learn the duals
def predict_dual(B,model_p,model_q):
    features_df = learning.extract_features(B.B)
    X = features_df.drop(columns=['node']).values
    
    p_pred = model_p.predict(X)
    q_pred = model_q.predict(X)
    
    p = {node: p_pred[i] for i, node in enumerate(B.B.nodes()) if node in B.L}
    q = {node: q_pred[i] for i, node in enumerate(B.B.nodes()) if node in B.R}
    return p,q

# Initialisation: M = ∅ p=q= learned duals

def init_dual(B,model_p,model_q):
    p,q = predict_dual(B,model_p,model_q)
    p,q = make_feasible(B,p,q)
    
    return p,q

def hungarian_learned(B,model_p,model_q,display=False):
    p,q = init_dual(B,model_p,model_q)
    w,i = hungarian_classic.hungarian(B,p,q)
    if(display):
        hungarian_classic.verify(B,p,q)
        B.display_matching()
    return w,i
    