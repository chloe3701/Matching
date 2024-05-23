import random

# generate a txt file simulating an online scenario for bipartite graph
def gen(n,filename):
    with open(filename, "w") as f:
        f.write(f"{n}\n")
        for i in range(n):
            number = random.randint(1, n)
            to_write = random.sample(range(n), number)
            to_write = list(map(str, to_write))
            to_write = ' '.join(to_write)
            f.write(f"{to_write}\n")

n = int(input("Enter an integer n: "))
filename = input("Enter the filename: ")
gen(n,filename)