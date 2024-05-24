import sys
sys.path.append('../')
from Utils import graph

def waterfilling(B, t, new_revealed,d):
    L=B.L
    # d is the current fractional degree
    # initialisation
    if d=={}:
        for e in L:
            d[e]=0
    
    # and find l such that sum(i neighbors of t) of max{l,d(i)} = 1 + sum of d(i)
    i=0
    dnj=0
    dn=[]
    for e in new_revealed:
        e,w=e.split(':')
        e=int(e)
        w=int(w)
        dnj+=d[e]
        B.M.add_edge(t,e,weight=0)
        dn.append(d[e])
        i=i+1
    dn.append(1)

    dn.sort()
    l=100
    current_addition = 0
    n=0
    while n<i:
        eq=0
        #calculate the number of entries we fill at the same time at this level
        while(n+eq+1<i and dn[n]==dn[n+eq+1]):
            eq=eq+1

        # (dn[n+eq+1]-dn[n])*(n+eq+1) + current_addition is the quantity we can increase before matching the height of the next water level
        
        # we are in the range of the actual l
        if ((dn[n+eq+1]-dn[n])*(n+eq+1) + current_addition)>=1:
            l = (1-current_addition)/(n+eq+1) + dn[n]
            n=i
        else:
            current_addition = current_addition + (dn[n+eq+1]-dn[n])*(n+eq+1)
            n=n+1+eq

    l=min(l,1)
    #cur=0
    for i in new_revealed:
        i,w=i.split(':')
        i=int(i)
        # if(d[i]<l):
        #     cur = cur + l - d[i]
        m = max(l,d[i])-d[i]
        B.M[i][t]["weight"]= m
        d[i]=d[i]+m
    #print(cur)
    
