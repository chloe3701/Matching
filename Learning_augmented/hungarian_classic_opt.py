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
            if (not visited[neighbor]) and ((B.B[node][neighbor]["weight"] == p[left] + q[right]) ) and ((alternate == (not next_alternate))):
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
        P.add_edge(e[0],e[1],weight=float(B.B[e[0]][e[1]]["weight"]))
    B.M=nx.symmetric_difference(B.M,P)

   
# This adjust some of the dual vaiables to make additional edges tight
def adjust(B, p, q):
    # Starting an adjustement phase
    
    # variables of the phase    
    # hungarian tree set : T is for the left vertices, S for the right
    T = {u for u in B.L if B.M.degree[u] == 0}
    S = set()
    # si and sj keeps track at which step the vertex was added to hungarian tree
    si= {}
    sj={v:None for v in B.R}
    for u in T:
        si[u]=0
    # s is the number of the current step of the phase
    s=0
    # Delta[s] is delta(1)+delta(2)+...+delta(s)
    Delta={0:float(0)}
    # priority queue of the phase
    # initialized to all edges containing u in T
    queue = collections.deque()
    for u in T:
        for v in B.B.neighbors(u):
            queue.appendleft((u,v,B.B[u][v]["weight"] - p[u] - q[v] + Delta[si[u]]))
    
    while True:
        delta_s = float(math.inf)
        s+=1
        
        # extract minimum element of priority queue : min{B.B[u][v]["weight"] - p[u] - q[v] + Delta[si(u)] | v ∈ R\S}
        min_edge = None
        for (u,v,w) in queue:
            if w < delta_s:
                min_edge = (u,v,w)
                delta_s = w
        queue.remove(min_edge)
        # update Delta
        delta_s = delta_s - Delta[s-1]
        Delta[s] = Delta[s-1] + delta_s
        
        # There is at least one tight edge e = (u, v) from L ∩ T to R \ S
        for u in T:
            for v in B.B.neighbors(u):
                if v not in S and B.B[u][v]["weight"] == p[u] + Delta[s] - Delta[si[u]] + q[v]:
                    # v is a free vertex
                    if B.M.degree[v] == 0:
                        # Augmentation step
                        #update all the p and q's:
                        for u in T:
                            p[u] += Delta[s] - Delta[si[u]]
                        for v in S:
                            q[v] -= Delta[s] - Delta[sj[v]]
                        
                        start = [u for u in B.L if B.M.degree(u)== 0]
                        for st in start:
                            path = find_augmenting(B,p,q,st)
                            if path != None:
                                break
                        # Error handling
                        if(path==None):
                            print("Error path empty")
                            print(p,q)
                            B.display_matching()
                        augment(B,path)
                        # end of the phase
                        return s
                    
                    else:
                        # Identify e = (u', v) ∈ M and add v and u' to T
                        # Tree growing step
                        # there should only be one
                        for u in B.M.neighbors(v):
                            if u not in T:
                                u_prime = u
                                break
                        T.add(u_prime)
                        si[u_prime] = s
                        S.add(v)
                        sj[v] = s
                        for j in B.B.neighbors(u_prime):
                            if(j not in S):
                                queue.appendleft((u_prime,j,B.B[u_prime][j]["weight"] - p[u_prime] - q[j] + Delta[si[u_prime]]))
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


# Initialisation: M = ∅ p=q=0
def init_dual(B):
    p = {u: float(0) for u in B.L}
    q = {v: float(0) for v in B.R}
    return p,q

# Hungarian algorithm after initialisation of the dual variables
def hungarian(B,p,q,display=False):
    i=0
    # While the matching built is not perfect:
    while(not B.perfect()):
        path = None
        start = [u for u in B.L if B.M.degree(u)== 0]
        for s in start:
            path = find_augmenting(B,p,q,s)
            if(path != None):
                break
        if (path == None):
            i+=adjust(B,p,q)
            if(display):
                B.display_matching()
            
        else:
            i+=1
            augment(B,path)
            if(display):
                B.display_matching()
    # return the value of the matching
    w = 0
    for e in B.M.edges():
        w = w + B.B[e[0]][e[1]]["weight"]
    
    return w,i

# Classic hungarian algorithm
def hungarian_classic(B,display=False):
    p,q = init_dual(B)
    w, iterations = hungarian(B,p,q,display=display)
    if(display):
        verify(B,p,q)
    return w, p, q, iterations
    
    
        
