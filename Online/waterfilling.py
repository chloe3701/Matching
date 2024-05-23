# from ortools.linear_solver import pywraplp

# def waterfilling(B,L,R,E,t,new,d={}):
#     solver = pywraplp.Solver.CreateSolver("GLOP")
#     if d=={}:
#         for e in L:
#             d[e]=0
#             list_neighbors=B.neighbors(e)
#             for n in list_neighbors:
#                 d[e]=d[e]+B.edges[(e,n)]['weight']
#     dnj=0
#     for n in new:
#         dnj+=d[n]
#     l = solver.NumVar(0,solver.infinity(), "l")
#     y = solver.NumVar(0,solver.infinity(), "y")

#     solver.Add(y == 1+dnj)
# cplex gurobi


def waterfilling(B, t, new_revealed,d):
    L=B.L
    R=B.R
    N=B.B.neighbors(t)
    # current fractional degree
    if d=={}:
        for e in L:
            d[e]=0
            # list_neighbors=B.M.neighbors(e)
            # for n in list_neighbors:
            #     d[e]=d[e]+B.M.edges[(e,n)]['weight']
    
    # add the corresponding edges with weight set to O 
    # and find l such that sum(i neighbors of t) of max{l,d(i)} = 1 + sum of d(i)
    i=0
    dnj=0
    for e in new_revealed:
        dnj+=d[e]
        i=i+1
        B.M.add_edge(t,e,weight=0)

    l=(dnj/i)+1/i
    l=min(l,1)
    for i in new_revealed:
        B.M[i][t]["weight"]=max(l,d[i])-d[i]
        d[i]=d[i]+B.M[i][t]["weight"]
    
    

#waterfilling(1,[3,3,3],1,1,1,1)