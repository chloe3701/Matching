import random
import math
import numpy as np
from Utils import graph


# generate a random txt file simulating either :
# - an online scenario for bipartite graph
# - an instance of an offline bipartite graph
# W is the maximum weight of an edge

# The file reads as follows:
# on the first line is the number n of vertices in L
# for each line after is the list of vertices the new vertex v is associated
# a:w means that the vertex v is linked to vertex a with a weight of w
def gen(n,filename,std_dev=20,mean=100):
    with open(filename, "w") as f:
        f.write(f"{n}\n")
        for i in range(n):
            number = random.randint(1, math.floor(n/2))
            # Ensure weights are positive and within the maximum weight W
            weight = [abs(int(np.random.normal(mean, std_dev))) for k in range(number)]
            #weight = [random.randint(1, 150) for k in range(number)]
            vertices = random.sample(range(n), number)
            for j in range(number):
                vertices[j]= str(vertices[j]) + ':' + str(int(weight[j]))
            vertices = ' '.join(vertices)
            f.write(f"{vertices}\n")
            
            
def gen_no_file(n,param1=20,param2=100,distribution=1):
    B = graph.Bipartite_graph(n)
    for t in range(n):
        #number of incident edges of vertex t+n
        number = random.randint(1, math.floor(n/2))
        if(distribution==1):
            weight = [abs(np.random.normal(param1, param2)) for k in range(number)]
        elif(distribution==2):
            weight = [abs(np.random.uniform(param1, param2)) for k in range(number)]
        elif(distribution==3):
            # Generate n exponential random numbers with the given scale
            exponential_numbers = np.random.exponential(param2, n)
            # Normalize the numbers to the range 0-1
            normalized_numbers = exponential_numbers / np.max(exponential_numbers)
            # Scale the normalized numbers to the range 0-high
            weight = normalized_numbers * param1
        elif(distribution==4):
            # Generate n binomial random numbers
            binomial_numbers = np.random.binomial(param2, param1, n)
            # Clip the numbers to the range 0-100 to ensure they fall within the desired range
            weight = np.clip(binomial_numbers, 0, 100)
        else:
            m1,s1=param1
            m2,s2=param2
            w1 = [abs(np.random.normal(m1, s1)) for k in range(number)]
            w2 = [abs(np.random.normal(m2, s2)) for k in range(number)]
            weight=[]
            for i in range(0, len(w1)):
                weight.append((w1[i]+w2[i])/2)
        
        vertices = random.sample(range(n), number)
        B.B.add_node(t+n,bipartite=1)
        B.M.add_node(t+n,bipartite=1)
        B.R.append(t+n)
        for j in range(number):
            B.B.add_edge(t+n,vertices[j],weight=int(weight[j]))
    return B

    

def generate():
    n = int(input("Enter an integer n: "))
    W = int(input("Enter a maximum weight W: "))
    filename = input("Enter the filename: ")
    gen(n,filename,W)