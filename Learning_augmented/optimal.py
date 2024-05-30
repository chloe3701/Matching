from ortools.linear_solver import pywraplp

def optimal(B):
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        raise Exception("Solver not created.")
    edges = B.get_edges()

    # decision variable x = 0 if edge is not selected x>0 otherwise
    x = {}
    # weight
    we = {}
    # add a variable for every edges
    for (u,v,w) in edges:
        x[(u,v)] = solver.NumVar(0,1,f'x_{u}_{v}')
        we[(u,v)] = w

    # add constraint for all i sum(over j) of xij <= 1
    # left vertex matched to at most one right vertex
    for i in B.L:
        solver.Add(sum(x[(i_,j)] for (i_,j,_) in edges if i==i_) == 1)

    # add constraint for all j sum(over i) of xij <= 1
    # right vertex matched to at most one left vertex
    for j in B.R:
        solver.Add(sum(x[(i,j_)] for (i,j_,_) in edges if j==j_) == 1)

    # objective function maximizing the number of edges selected
    solver.Minimize(solver.Sum((x[(i, j)]*w) for (i, j, w) in edges))

    # Solve the problem
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        print('Optimal matching found using the solver:')
        for (u, v, w) in edges:
            if x[(u, v)].solution_value() > 0:
                print(f'{u} - {v} : {x[(u, v)].solution_value()}')
        return solver.Objective().Value()
    else:
        print('The problem does not have an optimal solution.')
        return -1