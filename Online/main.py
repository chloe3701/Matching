import waterfilling as w
import optimal
import math
import matplotlib.pyplot as plt
import sys
sys.path.append('../')
from Utils import graph
from Utils import data_generator

def instance(n=0,filename=None,display=False):
    if(filename == None):
        data_generator.gen(n,"../Utils/tests/instance.txt",100)
        filename = "../Utils/tests/instance.txt"
    # Reading the file step by step to simulate an online scenario
    f = open(filename, "r")
    n = f.readline()
    B=graph.Bipartite_graph(int(n))
    t=B.n
    d={}
    # approx is what needs to be maximized : the number of edge selected (TODO: add weight)
    approx = 0

    for x in f:
        new_revealed=[]
        for e in x.split():
            new_revealed.append(e)
        B.revealed(t,new_revealed)
        w.waterfilling(B, t, new_revealed,d)
        B.display_matching()
        t=t+1
    f.close()
    for (u,v,weight) in B.get_edges_matching():
        approx=approx+weight
    opt=optimal.optimal(B)
    if(display):
        B.display()
        B.display_matching()
    if(approx>opt):
        print("Warning: The approximation solution is higher than the optimal solution by",approx - opt ,".\n")
    return (approx,opt)



scenario = (input("Do you want to :\n- run a comparison (1)\n- run a specific instance (2)\n- create a nex random file (3)?\n"))

if(scenario == '1'):
    approx=[]
    opt=[]
    n_values = list(range(4, 101, 1))
    for i in n_values:
        a,o=instance(n=i)
        approx.append(a)
        opt.append(o)
    n_values = list(range(8,202,2))

    # print("n ",n_values)
    # print("appr ",approx)
    # print("opt ",opt)
    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, approx, label ="Result of the waterfilling algorithm", color = "blue")
    plt.plot(n_values, opt, label ="Optimal result", color = "red")
    e_opt = [( (math.e - 1)/math.e) * x for x in opt]
    plt.plot(n_values,e_opt, label ="(e-1/e) * optimal (lower bound)", color = "green")

    # Adding title and labels
    #plt.title('Comparison between the approximated and the optimal solution of\n the maximal online unweighted bipartite matching')
    plt.xlabel('Number of edges in the graph')
    plt.ylabel('Value of the objective function')
    plt.legend()

    # Display the plot
    plt.grid(True)
    plt.show()

elif(scenario=='2'):
    # Setting up the display by the user
    display = (input("Do you want to display the result? y/n\n"))
    if(display=='y'):
        display=True
    else:
        display=False

    filename = "../Utils/tests/test_debug.txt"
    max_edge,opt=instance(filename=filename,display=display)
    print("The optimal solution is: ", opt)
    print("The number of edges selected is: ",max_edge)
elif(scenario=='3'):
    data_generator.generate()
    






