import sys
sys.path.append('../')
from Utils import graph
import math

def waterfilling(B, new_edge, new_revealed,fract_degree):
    L=B.L
    # fract_degree is the current fractional degree
    # initialisation
    if fract_degree=={}:
        for e in L:
            fract_degree[e]=0
    
    # and find l such that sum(i neighbors of t) of max{l,fract_degree(i)} = 1 + sum of fract_degree(i)
    num_neigh=0
    fract_neigh=[]
    for e in new_revealed:
        e,w=e.split(':')
        e=int(e)
        w=int(w)
        B.M.add_edge(new_edge,e,weight=0)
        fract_neigh.append(fract_degree[e])
        num_neigh=num_neigh+1
    fract_neigh.append(1)

    fract_neigh.sort()
    l=math.inf
    current_addition = 0
    n=0
    while n<num_neigh:
        # same_degree is the number of edges having the same degree in this iteration of the while
        same_degree=0
        #calculate the number of entries we fill at the same time at this level
        while(n+same_degree+1<num_neigh and fract_neigh[n]==fract_neigh[n+same_degree+1]):
            same_degree=same_degree+1

        # (fract_neigh[n+same_degree+1]-fract_neigh[n])*(n+same_degree+1) + current_addition is the quantity we can increase before matching the height of the next water level
        
        # we are in the range of the actual l
        if ((fract_neigh[n+same_degree+1]-fract_neigh[n])*(n+same_degree+1) + current_addition)>=1:
            l = (1-current_addition)/(n+same_degree+1) + fract_neigh[n]
            n=num_neigh
        else:
            current_addition = current_addition + (fract_neigh[n+same_degree+1]-fract_neigh[n])*(n+same_degree+1)
            n=n+1+same_degree

    l=min(l,1)
    for edge in new_revealed:
        edge,w=edge.split(':')
        edge=int(edge)
        # rise is the number by which we increase the degree for each neighbor of the new edge
        rise = max(l,fract_degree[edge])-fract_degree[edge]
        B.M[edge][new_edge]["weight"]= rise
        fract_degree[edge]=fract_degree[edge]+rise
    
