import time
import Matching.Online.graph as graph

filename = "./tests/test10.txt"

display = (input("Do you want to display the result? y/n\n"))
if(display=='y'):
    display=True
    steps = (input("Do you want to display the running of the algorithm step by step? y/n\n"))
    if(steps=='y'):
        steps=True
    else:
        steps=False
else:
    display=False
    steps=False
start_time = time.time()
graph.wat(filename,display,steps)
print("--- %s seconds ---" % (time.time() - start_time))