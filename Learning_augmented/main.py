import sys
sys.path.append('../')
from Utils import graph
from Utils import data_generator
from Online import optimal as o
import optimal
import primaldual

# t=0
# for i in range(200):
filename = "../Utils/tests/instance.txt"
data_generator.gen(10,filename,100)
B = graph.offline_init(filename)
# B.display()
possible=o.optimal(B)
opt=optimal.optimal(B)
#print(opt)
if((possible)==B.n):
    verif = primaldual.hungarian(B)
    if(verif==opt):
        print("The solution is correct")
        # t=t+1
    else:
        print("Unexpected error, the optimal solution of the two algorithms is different")
# print(t)

