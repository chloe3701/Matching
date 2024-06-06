import random
import math
import numpy as np


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

def generate():
    n = int(input("Enter an integer n: "))
    W = int(input("Enter a maximum weight W: "))
    filename = input("Enter the filename: ")
    gen(n,filename,W)