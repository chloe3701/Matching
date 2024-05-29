import sys
sys.path.append('../')
from Utils import graph
from Utils import data_generator
from Online import optimal as o
import optimal
import primaldual

t=0
for i in range(200):
    data_generator.gen(30,"../Utils/tests/test2.txt",100)
    filename = "../Utils/tests/instance.txt"
    B = graph.offline_init("../Utils/tests/test2.txt")
    # B.display()
    possible=o.optimal(B)
    opt=optimal.optimal(B)
    # print(opt)
    if((possible)==B.n):
        verif = primaldual.hungarian(B)
        if(verif==opt):
            print("Solution optimale")
            t=t+1
print(t)

