import sys
import networkx as nx
sys.path.append('../')
from Utils import graph
import math
import collections



# This finds an augmenting path of the matching composed of tight edges using BFS
# an augmenting path is an alternating path that starts from and ends on (two different) unmatched vertices
# Complexity O(n)
def find_augmenting(B, p, q, start):
    visited = {u:False for u in B.M.nodes()}
    queue = collections.deque([(start,True)])
    visited[start]=True
    parents = {start: None}

    while queue:
        node, alternate = queue.popleft()
        for neighbor in B.B.neighbors(node):
            left = min(node,neighbor)
            right = max(node,neighbor)
            next_alternate = B.M.has_edge(node,neighbor)
            if (not visited[neighbor]) and (B.B[node][neighbor]["weight"] == p[left] + q[right]) and ((alternate == (not next_alternate))):
                visited[neighbor] = True
                parents[neighbor] = node
                if B.M.degree(neighbor) == 0:
                    path = []
                    while parents[neighbor] is not None:
                        path.append((parents[neighbor],neighbor))
                        neighbor = parents[neighbor]
                    return path
                queue.appendleft((neighbor,  next_alternate))
    return None
    


# This augments the matching given an augmenting path found with the previous function
def augment(B,path):
    P = nx.Graph()
    for c in range(B.n * 2):
            P.add_node(c)
    for e in path:
        P.add_edge(e[0],e[1],weight=B.B[e[0]][e[1]]["weight"])
    B.M=nx.symmetric_difference(B.M,P)

   
# This adjust some of the dual vaiables to make additional edges tight
def adjust(B, p, q):
    # is there a vertex u in L that doesn't belong to any tight edges ?
    for u in B.L:
        min_v=[]
        min_t=100000
        augmentable=False
        for v in B.B.neighbors(u):
            value = B.B[u][v]["weight"] - p[u] - q[v]
            if(value==0):
                augmentable=False
                break
            else:
                if(value<=min_t):
                    if(value<min_t):
                        min_v=[v]
                    else:
                        min_v=min_v+[v]
                    min_t=value
                  
                    augmentable=True
        if(augmentable):
            for v in min_v:
                # -> Yes, we raise the value of p[u]
                if(B.M.degree[v]==0):
                    p[u]+=min_t
                    return

    # -> no (every u in L belong to a tight edge)
    # we have a vertex set T U S (Hungarian tree) : if one endpoint of an edge e in M belongs to TUS then both endpoint do
    # initialize T to be the set of free vertices in L
    T = {u for u in B.L if B.M.degree[u] == 0}
    S = set()
    
    while True:
        # compute delta = min{B.B[u][v]["weight"] - p[u] - q[v] | u∈ L∩T, v ∈ R\S}
        delta = math.inf
        for u in T:
            for v in B.B.neighbors(u):
                if v not in S:
                    delta = min(delta, B.B[u][v]["weight"] - p[u] - q[v])
        
        # print(p,q)
        # print(delta)
        # B.display_matching()            
        if(delta > 0):
            # Dual adjustement step
            # -> adjust all p[u] to p[u] + delta and all q[v] to q[v] - delta
            for u in T:
                p[u] += delta
            for v in S:
                q[v] -= delta
        else:  # There is at least one tight edge e = (u, v) from L ∩ T to R \ S
            for u in T:
                for v in B.B.neighbors(u):
                    if v not in S and B.B[u][v]["weight"] == p[u] + q[v]:
                        
                        # v is a free vertex
                        # Augmentation step
                        if B.M.degree[v] == 0:
                            start = [u for u in B.L if B.M.degree(u)== 0]
                            for s in start:
                                path = find_augmenting(B,p,q,s)
                                if path != None:
                                    break
                            # Error handling
                            if(path==None):
                                print("Error path empty")
                                print(p,q)
                                B.display_matching()
                            augment(B,path)
                            # end of the phase
                            return
                        
                        else:
                            # Identify e = (u', v) ∈ M and add v and u' to T
                            # Tree growing step
                            # there should only be one
                            for u in B.M.neighbors(v):
                                if u not in T:
                                    u_prime = u
                                    break
                            T.add(u_prime)
                            S.add(v)
                            break
                else:
                    continue
                break

# This verifies if the computed solution is correct
def verify(B,p,q):
    sum_primal = 0
    sum_dual = 0
    for e in B.M.edges():
        sum_primal += B.B[e[0]][e[1]]["weight"]
    for u in B.L:
        if(B.M.degree(u)!=1):
            print("Error in the matching")
            B.display_matching()
        sum_dual += p[u]
    for v in B.R:
        if(B.M.degree(v)!=1):
            print("Error in the matching")
            B.display_matching()
        sum_dual += q[v]
    if(sum_dual == sum_primal):
        print("The solution of the Primal-Dual Hungarian algorithm is optimal (by strong duality)")
    else:
        print("The solution of the Primal-Dual Hungarian algorithm is not optimal:")
        print("sum_dual=",sum_dual," but sum_primal=",sum_primal)
        B.display_matching()


# Initialisation: M = ∅ p=q=0
def init_dual(B):
    p = {u: 0 for u in B.L}
    q = {v: 0 for v in B.R}
    return p,q

# Hungarian algorithm after initialisation of the dual variables
def hungarian(B,p,q):
    i=0
    # While the matching built is not perfect:
    while(not B.perfect()):
        # B.display_matching()
        # print(p,q)
        i+=1
        path = None
        start = [u for u in B.L if B.M.degree(u)== 0]
        for s in start:
            path = find_augmenting(B,p,q,s)
            if(path != None):
                break
        if (path == None):
            adjust(B,p,q)
        else:
            augment(B,path)
            
    # return the value of the matching
    w = 0
    for e in B.M.edges():
        w = w + B.B[e[0]][e[1]]["weight"]
    
    return w,i

# Classic hungarian algorithm
def hungarian_classic(B,display=False):
    p,q = init_dual(B)
    w, iterations = hungarian(B,p,q)
    if(display):
        verify(B,p,q)
        B.display_matching()
    return w, p, q, iterations
    
    
        
