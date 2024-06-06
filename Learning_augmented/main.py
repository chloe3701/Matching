import sys
sys.path.append('../')
from Utils import graph
from Utils import data_generator
from Online import optimal as o
import optimal
import hungarian_classic as classic
import hungarian_learned as learned
import hungarian_mean as mean
import learning
import time
import matplotlib.pyplot as plt

filename = "../Utils/tests/instance.txt"
graph_size=90
size_graph_max=101

scenario = (input("Do you want to :\n- run a simple primal dual algorithm (1)\n- run a primal dual algorithm using predictions (2)\n- compare the execution time between one regular and learned dual primal instance(3)\n- compare the execution time between multiple regular and learned dual primal instances(4)?\n"))

if(scenario=='1'):
    size = int((input("Choose a size n = |L|=|R|\n")))
    opt=-1
    while(opt==-1):
        data_generator.gen(size,filename,100)
        B = graph.offline_init(filename)
        opt=optimal.optimal(B)
    verif,_,_,_ = classic.hungarian_classic(B,True)
    if(verif==opt):
        print("The solution is correct")
    else:
        print("Unexpected error, the optimal solution of the two algorithms is different")
        
elif(scenario=='2'):
    size = int((input("Choose a size n=|L|=|R|\n")))
    m = int((input("For the normal distribution, choose a mean\n")))
    std = int((input("For the normal distribution, choose a standard deviation\n")))
    model_p,model_q,_,_ = learning.learn(size,mean=m,std_dev=std)
    opt=-1
    while(opt==-1):
        data_generator.gen(size,filename,mean=m,std_dev=std)
        B = graph.offline_init(filename)
        opt=optimal.optimal(B)
    if(opt!=-1):
        verif,_ = learned.hungarian_learned(B,model_p,model_q,display=True)
        if(verif==opt):
            print("The solution is correct")
        else:
            print("Unexpected error, the optimal solution of the two algorithms is different")
    

elif(scenario=='3'):
    size = int((input("Choose a size n=|L|=|R|\n")))
    m = int((input("For the normal distribution, choose a mean\n")))
    std = int((input("For the normal distribution, choose a standard deviation\n")))
    
    model_p,model_q,p_mean,q_mean = learning.learn(size,mean=m,std_dev=std)
    
    opt=-1
    while(opt==-1):
        data_generator.gen(size,filename,std_dev=std,mean=m)
        B = graph.offline_init(filename)
        opt=optimal.optimal(B)
        
    # Timing of the classic execution
    start=time.time()
    verif,_,_,_ = classic.hungarian_classic(B,display=False)
    end=time.time()
    elapsed_time = end - start
    print(f"Elapsed time without learned duals: {elapsed_time} seconds")
    
    # Timing of the learned execution
    B = graph.offline_init(filename)
    start=time.time()
    verif,_ = learned.hungarian_learned(B,model_p,model_q)
    end=time.time()
    elapsed_time = end - start
    print(f"Elapsed time with learned duals: {elapsed_time} seconds")
    
    # Timing with the mean execution
    B = graph.offline_init(filename)
    start=time.time()
    mean.hungarian_mean(B,p_mean,q_mean)
    end=time.time()
    elapsed_time = end - start
    print(f"Elapsed time with mean duals: {elapsed_time} seconds")
    
    if(verif==opt):
        print("The solution is correct")
    else:
        print("Unexpected error, the optimal solution of the two algorithms is different")
        

elif(scenario=='4'):
    m = int((input("For the normal distribution, choose a mean\n")))
    std = int((input("For the normal distribution, choose a standard deviation\n")))
    
    classic_time_average=[0] * (size_graph_max-4)
    classic_iteration_average=[0] * (size_graph_max-4)
    
    learned_time_average=[0] * (size_graph_max-4)
    learned_iteration_average=[0] * (size_graph_max-4)
    
    mean_time_average=[0] * (size_graph_max-4)
    mean_iteration_average=[0] * (size_graph_max-4)
    n_values = list(range(4, size_graph_max, 1))
    for i in n_values:
        model_p,model_q,p_mean,q_mean = learning.learn(i,std_dev=std,mean=m)
        for j in range(10):
            opt=-1
            while(opt==-1):
                data_generator.gen(i,filename,std_dev=std,mean=m)
                B = graph.offline_init(filename)
                opt=optimal.optimal(B)
            # time for the classic algorithm
            start=time.time()
            verif,_,_,i_classic = classic.hungarian_classic(B)
            end=time.time()
            elapsed_time_classic = end - start
            classic_time_average[i-4]+=elapsed_time_classic
            classic_iteration_average[i-4]+=i_classic
            B = graph.offline_init(filename)
            # time for the learned duals
            start=time.time()
            _,i_learned = learned.hungarian_learned(B,model_p,model_q)
            end=time.time()
            elapsed_time_learned = end - start
            learned_time_average[i-4]+=elapsed_time_learned
            learned_iteration_average[i-4]+=i_learned
            B = graph.offline_init(filename)
            #time for the mean duals
            start=time.time()
            _,i_mean = mean.hungarian_mean(B,p_mean,q_mean)
            end=time.time()
            elapsed_time_mean = end - start
            mean_time_average[i-4]+=elapsed_time_mean
            mean_iteration_average[i-4]+=i_mean
        mean_time_average[i-4]=mean_time_average[i-4]/10
        classic_time_average[i-4]=classic_time_average[i-4]/10
        learned_time_average[i-4]=learned_time_average[i-4]/10
        mean_iteration_average[i-4]=mean_iteration_average[i-4]/10
        classic_iteration_average[i-4]=classic_iteration_average[i-4]/10
        learned_iteration_average[i-4]=learned_iteration_average[i-4]/10

    n_values_b = n_values.copy()
    for i in n_values_b:
        n_values[i-4]*=2
    # Time plot
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, classic_time_average, label ="Time without learned duals", color = "blue")
    plt.plot(n_values, learned_time_average, label ="Time with learned duals", color = "red")
    plt.plot(n_values, mean_time_average, label ="Time with mean duals", color = "green")
    #plt.fill_between(n_values, classic_time_min, classic_time_max, color='cyan', alpha=0.5, label='Min-Max Range classic')
    #plt.fill_between(n_values, learned_time_min, learned_time_max, color='orange', alpha=0.5, label='Min-Max Range learned')
    #plt.fill_between(n_values, mean_time_min, mean_time_max, color='olive', alpha=0.5, label='Min-Max Range mean')
    #plt.title('Comparison between the execution time with and without learned duals')
    plt.xlabel('Size of the graph |V|')
    plt.ylabel('Execution time (sec)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Iteration plot
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, classic_iteration_average, label ="# of iterations without learned duals", color = "blue")
    plt.plot(n_values, learned_iteration_average, label ="# of iterations with learned duals", color = "red")
    plt.plot(n_values, mean_iteration_average, label ="# of iterations with mean duals", color = "green")
    plt.title('Comparison between the # of iterations with and without learned duals')
    plt.xlabel('Size of the graph')
    plt.ylabel("# of iterations")
    plt.legend()
    plt.grid(True)
    plt.show()
elif(scenario=='5'):
    classic_time_average=[0] * 11
    classic_iteration_average=[0] * 11
    
    learned_time_average=[0] * 11
    learned_iteration_average=[0] * 11
    
    mean_time_average=[0] * 11
    mean_iteration_average=[0] * 11
    n_values = [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    print(n_values)
    for i in n_values:
        print(i)
        model_p,model_q,p_mean,q_mean = learning.learn(graph_size,std_dev=i*100,mean=100)
        for j in range(10):
            opt=-1
            while(opt==-1):
                data_generator.gen(graph_size,filename,std_dev=i*100,mean=100)
                B = graph.offline_init(filename)
                opt=optimal.optimal(B)
            # time for the classic algorithm
            start=time.time()
            verif,_,_,i_classic = classic.hungarian_classic(B)
            end=time.time()
            elapsed_time_classic = end - start
            classic_time_average[int(10*i)]+=elapsed_time_classic
            classic_iteration_average[int(10*i)]+=i_classic
            B = graph.offline_init(filename)
            # time for the learned duals
            start=time.time()
            _,i_learned = learned.hungarian_learned(B,model_p,model_q)
            end=time.time()
            elapsed_time_learned = end - start
            learned_time_average[int(10*i)]+=elapsed_time_learned
            learned_iteration_average[int(10*i)]+=i_learned
            B = graph.offline_init(filename)
            #time for the mean duals
            start=time.time()
            _,i_mean = mean.hungarian_mean(B,p_mean,q_mean)
            end=time.time()
            elapsed_time_mean = end - start
            mean_time_average[int(10*i)]+=elapsed_time_mean
            mean_iteration_average[int(10*i)]+=i_mean
        mean_time_average[int(10*i)]=mean_time_average[int(10*i)]/10
        classic_time_average[int(10*i)]=classic_time_average[int(10*i)]/10
        learned_time_average[int(10*i)]=learned_time_average[int(10*i)]/10
        mean_iteration_average[int(10*i)]=mean_iteration_average[int(10*i)]/10
        classic_iteration_average[int(10*i)]=classic_iteration_average[int(10*i)]/10
        learned_iteration_average[int(10*i)]=learned_iteration_average[int(10*i)]/10

    std_dev_val=n_values.copy()
    for i in n_values:
        std_dev_val[int(i*10)]*=graph_size 
    print(std_dev_val)
    # Time plot
    plt.figure(figsize=(10, 6))
    plt.plot(std_dev_val, classic_time_average, label ="Time without learned duals", color = "blue")
    plt.plot(std_dev_val, learned_time_average, label ="Time with learned duals", color = "red")
    plt.plot(std_dev_val, mean_time_average, label ="Time with mean duals", color = "green")
    #plt.fill_between(n_values, classic_time_min, classic_time_max, color='cyan', alpha=0.5, label='Min-Max Range classic')
    #plt.fill_between(n_values, learned_time_min, learned_time_max, color='orange', alpha=0.5, label='Min-Max Range learned')
    #plt.fill_between(n_values, mean_time_min, mean_time_max, color='olive', alpha=0.5, label='Min-Max Range mean')
    # plt.title('Comparison between the execution time with and without learned duals')
    plt.xlabel('Standard deviation')
    plt.ylabel('Execution time (sec)')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Iteration plot
    plt.figure(figsize=(10, 6))
    plt.plot(std_dev_val, classic_iteration_average, label ="# of iterations without learned duals", color = "blue")
    plt.plot(std_dev_val, learned_iteration_average, label ="# of iterations with learned duals", color = "red")
    plt.plot(std_dev_val, mean_iteration_average, label ="# of iterations with mean duals", color = "green")
    # plt.title('Comparison between the # of iterations with and without learned duals')
    plt.xlabel('Standard deviation')
    plt.ylabel("# of iterations")
    plt.legend()
    plt.grid(True)
    plt.show()

    


