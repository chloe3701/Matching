import sys
sys.path.append('../')
from Utils import graph
from Utils import data_generator
import optimal
import hungarian_classic as classic
import hungarian_classic_opt as classic_opt
import hungarian_learned as learned
import hungarian_mean as mean
import numpy as np
import learning
import time
import matplotlib.pyplot as plt
import copy

filename = "../Utils/tests/instance.txt"
graph_size= 80
size_graph_max=121

print("Do you want to :")
print("- run a simple primal dual algorithm(1)")
print("- run a primal dual algorithm using predictions(2)")
print("- compare the execution time between one regular and one learned dual primal instance(3)")
print("- compare the execution time between multiple regular and learned dual primal instances(4)?")
print("- compare the execution time when the standard deviation varies(5)?")
print("- compare the execution time of the O(mn²) and O(mnlog(n)) algorithm(6)?")
print("- compare the efficiency of the learned duals trained of the exact size of the problem and a more general learned dual(7)?")
scenario = (input())


if(scenario=='1'):
    print("Execution of a regular instance of the Primal-dual hungarian algorithm.")
    size = int((input("Choose a size n = |L|=|R|\n")))
    display = input("Display the steps of the algorithm ? y/n\n")
    print("Weights on the edges are generated using a normal distribution N=(100,20²).")
    opt=-1
    while(opt==-1):
        data_generator.gen(size,filename)
        B=graph.offline_init(filename)
        opt=optimal.optimal(B)
    B.display()
    verif,_,_,_ = classic_opt.hungarian_classic(B,display=(display=="y"))
    B.display_matching()
    if(verif==opt):
        print("The solution is correct.")
    else:
        print("Unexpected error, the optimal solution of the two algorithms is different:", verif, "!= opt =", opt)

elif(scenario=='2'):
    print("Execution of an instance of the Primal-dual hungarian algorithm using \"warm-started\" duals.")
    size = int((input("Choose a size n=|L|=|R|\n")))
    display = input("Display the steps of the algorithm ? y/n\n")
    print("Weights on the edges are generated using a normal distribution N=(100,20²).")
    model_p,model_q,_,_ = learning.learn(size)
    opt=-1
    while(opt==-1):
        B = data_generator.gen_no_file(size)
        opt=optimal.optimal(B)
    B.display()
    verif,_ = learned.hungarian_learned(B,model_p,model_q,display=(display=="y"))
    B.display_matching()
    if(verif==opt):
        print("The solution is correct.")
    else:
        print("Unexpected error, the optimal solution of the two algorithms is different")


elif(scenario=='3'):
    print("Comparison of the execution time of an instance of the problem with and without \"warm-started\" duals.")
    
    size = int((input("Choose a size n=|L|=|R|\n")))
    print("Choose a distribution to generate the weights:")
    d =int( input("Normal(1) - Uniform(2) - Exponential(3) - Binomial(4) - Gaussian Mixture(5)\n"))
    if(d==1):
        print("Normal distribution:")
        param1 = int((input("Choose a mean\n")))
        param2 = int((input("Choose a standard deviation\n")))
    elif(d==2):
        print("Uniform distribution:")
        param1 = int((input("Choose a 'low' parameter\n")))
        param2 = int((input("Choose a 'high' parameter\n")))
    elif(d==3):
        print("Exponential distribution:")
        param1 = int((input("Choose a 'high' parameter\n")))
        param2 = float((input("Choose a scale\n")))
    elif(d==4):
        print("Binomial distribution:")
        param1 = float((input("Choose a probability between 0 and 1\n")))
        param2 = int((input("Choose a number of trials\n")))
    else:    
        print("Gaussian mixture distribution:")
        print("Parameters of the first Gaussian")
        param1 = (int((input("Choose a mean\n"))),int((input("Choose a standard deviation\n"))))
        print("Parameters of the second Gaussian")
        param2 = (int((input("Choose a mean\n"))),int((input("Choose a standard deviation\n"))))
    
    model_p,model_q,p_mean,q_mean = learning.learn(size,param1=param1,param2=param2,distribution=d)

    opt=-1
    while(opt==-1):
        B = data_generator.gen_no_file(size,param1=param1,param2=param2,distribution=d)
        opt=optimal.optimal(B)
    temp = copy.copy(B)
    # Timing of the classic execution
    start=time.time()
    verif,_,_,_ = classic_opt.hungarian_classic(B,display=False)
    end=time.time()
    elapsed_time = end - start
    print(f"Elapsed time without learned duals: {elapsed_time} seconds")

    # Timing of the learned execution
    B = copy.copy(temp)
    start=time.time()
    verif,_ = learned.hungarian_learned(B,model_p,model_q)
    end=time.time()
    elapsed_time = end - start
    print(f"Elapsed time with learned duals: {elapsed_time} seconds")

    # Timing with the mean execution
    # B = temp
    # start=time.time()
    # mean.hungarian_mean(B,p_mean,q_mean)
    # end=time.time()
    # elapsed_time = end - start
    # print(f"Elapsed time with mean duals: {elapsed_time} seconds")

    if(verif==opt):
        print("The solution is correct")
    else:
        print("Unexpected error, the optimal solution of the two algorithms is different")


elif(scenario=='4'):
    print("Comparison of the execution time between multiple regular and learned dual primal instances")
    print("Execution on graph of size 'min_size' to size 'max_size'.")
    first = int(input("min_size: "))
    size_graph_max = int(input("max_size: "))
    
    
    print("Choose a distribution to generate the weights:")
    d =int( input("Normal(1) - Uniform(2) - Exponential(3) - Binomial(4) - Gaussian Mixture(5)\n"))
    if(d==1):
        print("Normal distribution:")
        param1 = int((input("Choose a mean\n")))
        param2 = int((input("Choose a standard deviation\n")))
    elif(d==2):
        print("Uniform distribution:")
        param1 = int((input("Choose a 'low' parameter\n")))
        param2 = int((input("Choose a 'high' parameter\n")))
    elif(d==3):
        print("Exponential distribution:")
        param1 = int((input("Choose a 'high' parameter\n")))
        param2 = float((input("Choose a scale\n")))
    elif(d==4):
        print("Binomial distribution:")
        param1 = float((input("Choose a probability between 0 and 1\n")))
        param2 = int((input("Choose a number of trials\n")))
    else:    
        print("Gaussian mixture distribution:")
        print("Parameters of the first Gaussian")
        param1 = (int((input("Choose a mean\n"))),int((input("Choose a standard deviation\n"))))
        print("Parameters of the second Gaussian")
        param2 = (int((input("Choose a mean\n"))),int((input("Choose a standard deviation\n"))))

    classic_time_average=[0] * (size_graph_max-first)
    classic_iteration_average=[0] * (size_graph_max-first)

    learned_time_average=[0] * (size_graph_max-first)
    learned_iteration_average=[0] * (size_graph_max-first)

    # mean_time_average=[0] * (size_graph_max-4)
    # mean_iteration_average=[0] * (size_graph_max-4)
    n_values = list(range(first, size_graph_max, 1))
    for i in n_values:
        print(i)
        model_p,model_q,p_mean,q_mean = learning.learn(i,param1=param1,param2=param2,distribution=d)
        for j in range(10):
            opt=-1
            while(opt==-1):
                B = data_generator.gen_no_file(i,param1=param1,param2=param2,distribution=d)
                opt=optimal.optimal(B)
            temp=copy.copy(B)
            # time for the classic algorithm
            start=time.time()
            verif,_,_,i_classic = classic_opt.hungarian_classic(B)
            end=time.time()
            elapsed_time_classic = end - start
            classic_time_average[i-first]+=elapsed_time_classic
            classic_iteration_average[i-first]+=i_classic
            B = copy.copy(temp)
            # time for the learned duals
            start=time.time()
            _,i_learned = learned.hungarian_learned(B,model_p,model_q)
            end=time.time()
            elapsed_time_learned = end - start
            learned_time_average[i-first]+=elapsed_time_learned
            learned_iteration_average[i-first]+=i_learned
            B = temp
            #time for the mean duals
            # start=time.time()
            # _,i_mean = mean.hungarian_mean(B,p_mean,q_mean)
            # end=time.time()
            # elapsed_time_mean = end - start
            # mean_time_average[i-4]+=elapsed_time_mean
            # mean_iteration_average[i-4]+=i_mean
        # mean_time_average[i-4]=mean_time_average[i-4]/10
        classic_time_average[i-first]=classic_time_average[i-first]/10
        learned_time_average[i-first]=learned_time_average[i-first]/10
        # mean_iteration_average[i-4]=mean_iteration_average[i-4]/10
        classic_iteration_average[i-first]=classic_iteration_average[i-first]/10
        learned_iteration_average[i-first]=learned_iteration_average[i-first]/10

    n_values_b = n_values.copy()
    for i in n_values_b:
        n_values[i-first]*=2
    # Time plot
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, classic_time_average, label ="Time without learned duals", color = "blue")
    plt.plot(n_values, learned_time_average, label ="Time with learned duals", color = "red")
    # plt.plot(n_values, mean_time_average, label ="Time with mean duals", color = "green")
    plt.title('Comparison between the execution time with and without learned duals')
    plt.xlabel('Size of the graph |V|')
    plt.ylabel('Execution time (sec)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Iteration plot
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, classic_iteration_average, label ="# of iterations without learned duals", color = "blue")
    plt.plot(n_values, learned_iteration_average, label ="# of iterations with learned duals", color = "red")
    # plt.plot(n_values, mean_iteration_average, label ="# of iterations with mean duals", color = "green")
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

    # mean_time_average=[0] * 11
    # mean_iteration_average=[0] * 11
    n_values = [0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
    print(n_values)
    for i in n_values:
        print(i)
        model_p,model_q,p_mean,q_mean = learning.learn(graph_size,std_dev=i*100,mean=100)
        for j in range(10):
            opt=-1
            while(opt==-1):
                B = data_generator.gen_no_file(graph_size,std_dev=i*100,mean=100)
                opt=optimal.optimal(B)
            temp = copy.copy(B)
            # time for the classic algorithm
            start=time.time()
            verif,_,_,i_classic = classic_opt.hungarian_classic(B)
            end=time.time()
            elapsed_time_classic = end - start
            classic_time_average[int(10*i)]+=elapsed_time_classic
            classic_iteration_average[int(10*i)]+=i_classic
            B = temp
            # time for the learned duals
            start=time.time()
            _,i_learned = learned.hungarian_learned(B,model_p,model_q)
            end=time.time()
            elapsed_time_learned = end - start
            learned_time_average[int(10*i)]+=elapsed_time_learned
            learned_iteration_average[int(10*i)]+=i_learned
        #     B = temp.copy()
        #     #time for the mean duals
        #     start=time.time()
        #     _,i_mean = mean.hungarian_mean(B,p_mean,q_mean)
        #     end=time.time()
        #     elapsed_time_mean = end - start
        #     mean_time_average[int(10*i)]+=elapsed_time_mean
        #     mean_iteration_average[int(10*i)]+=i_mean
        # mean_time_average[int(10*i)]=mean_time_average[int(10*i)]/10
        classic_time_average[int(10*i)]=classic_time_average[int(10*i)]/10
        learned_time_average[int(10*i)]=learned_time_average[int(10*i)]/10
        # mean_iteration_average[int(10*i)]=mean_iteration_average[int(10*i)]/10
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
    # plt.plot(std_dev_val, mean_time_average, label ="Time with mean duals", color = "green")
    #plt.fill_between(n_values, classic_time_min, classic_time_max, color='cyan', alpha=0.5, label='Min-Max Range classic')
    #plt.fill_between(n_values, learned_time_min, learned_time_max, color='orange', alpha=0.5, label='Min-Max Range learned')
    #plt.fill_between(n_values, mean_time_min, mean_time_max, color='olive', alpha=0.5, label='Min-Max Range mean')
    # plt.title('Comparison between the execution time with and without learned duals')
    plt.xlabel('Scale')
    plt.ylabel('Execution time (sec)')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Iteration plot
    plt.figure(figsize=(10, 6))
    plt.plot(std_dev_val, classic_iteration_average, label ="# of iterations without learned duals", color = "blue")
    plt.plot(std_dev_val, learned_iteration_average, label ="# of iterations with learned duals", color = "red")
    # plt.plot(std_dev_val, mean_iteration_average, label ="# of iterations with mean duals", color = "green")
    # plt.title('Comparison between the # of iterations with and without learned duals')
    plt.xlabel('Standard deviation')
    plt.ylabel("# of iterations")
    plt.legend()
    plt.grid(True)
    plt.show()
elif(scenario=="6"):
    print("Comparison between the classic and optimized Primal-dual algorithm execution time.")
    print("Execution on graph of size 'min_size' to size 'max_size'.")
    first = int(input("min_size: "))
    size_graph_max = int(input("max_size: ")) + 1

    classic_time_average=[0] * (size_graph_max-first)
    classic_opt_time_average=[0] * (size_graph_max-first)
    n_values = list(range(first, size_graph_max, 1))
    for i in n_values:
        print(i)
        for j in range(1):
            opt=-1
            while(opt==-1):
                B = data_generator.gen_no_file(i)
                opt=optimal.optimal(B)
            temp = copy.copy(B)
            # time for the classic algorithm
            start=time.time()
            verif,_,_,i_classic = classic.hungarian_classic(B)
            end=time.time()
            elapsed_time_classic = end - start
            classic_time_average[i-first]+=elapsed_time_classic
            # time for the opt algorithm
            start=time.time()
            verif,_,_,i_classic = classic_opt.hungarian_classic(temp)
            end=time.time()
            elapsed_time_classic = end - start
            classic_opt_time_average[i-first]+=elapsed_time_classic
        classic_time_average[i-first]=classic_time_average[i-first]/1
        classic_opt_time_average[i-first]=classic_opt_time_average[i-first]/1
    n_values_b = n_values.copy()
    for i in n_values_b:
        n_values[i-first]*=2
    # Time plot
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, classic_time_average, label ="Time classic", color = "blue")
    plt.plot(n_values, classic_opt_time_average, label ="Time opt", color = "red")
    #plt.fill_between(n_values, classic_time_min, classic_time_max, color='cyan', alpha=0.5, label='Min-Max Range classic')
    #plt.fill_between(n_values, learned_time_min, learned_time_max, color='orange', alpha=0.5, label='Min-Max Range learned')
    #plt.fill_between(n_values, mean_time_min, mean_time_max, color='olive', alpha=0.5, label='Min-Max Range mean')
    #plt.title('Comparison between the execution time with and without learned duals')
    plt.xlabel('Size of the graph |V|')
    plt.ylabel('Execution time (sec)')
    plt.legend()
    plt.grid(True)
    plt.show()
elif(scenario=="7"):
    print("Comparing the efficiency of keeping a model trained on one size or training a model for every instances.")
    size = int((input("Choose a size n. The general model will be trained on this size\n")))
    sizerange = int((input("Choose a parameter X. The tests will be done from size n-X to n+X\n")))
    print("Choose a distribution to generate the weights:")
    d =int( input("Normal(1) - Uniform(2) - Exponential(3) - Binomial(4) - Gaussian Mixture(5)\n"))
    if(d==1):
        print("Normal distribution:")
        param1 = int((input("Choose a mean\n")))
        param2 = int((input("Choose a standard deviation\n")))
    elif(d==2):
        print("Uniform distribution:")
        param1 = int((input("Choose a 'low' parameter\n")))
        param2 = int((input("Choose a 'high' parameter\n")))
    elif(d==3):
        print("Exponential distribution:")
        param1 = int((input("Choose a 'high' parameter\n")))
        param2 = float((input("Choose a scale\n")))
    elif(d==4):
        print("Binomial distribution:")
        param1 = float((input("Choose a probability between 0 and 1\n")))
        param2 = int((input("Choose a number of trials\n")))
    else:    
        print("Gaussian mixture distribution:")
        print("Parameters of the first Gaussian")
        param1 = (int((input("Choose a mean\n"))),int((input("Choose a standard deviation\n"))))
        print("Parameters of the second Gaussian")
        param2 = (int((input("Choose a mean\n"))),int((input("Choose a standard deviation\n"))))
    
    classic_time_average=[0] * (sizerange*2 +1)

    learned_time_generalized=[0] * (sizerange*2 +1)
    
    learned_time_exact=[0] * (sizerange*2 +1)
    n_values = list(range(size-sizerange, size+sizerange+1,1))
    
    model_p,model_q,_,_ = learning.learn(size,param1=param1,param2=param2,distribution=d)
    
    for i in n_values:
        model_p_bis,model_q_bis,_,_ = learning.learn(i,param1=param1,param2=param2,distribution=d)
        print(i)
        for j in range(10):
            opt=-1
            while(opt==-1):
                B = data_generator.gen_no_file(i,param1=param1,param2=param2,distribution=d)
                opt=optimal.optimal(B)
            temp=copy.copy(B)
             # time for the classic algorithm
            start=time.time()
            verif,_,_,_ = classic_opt.hungarian_classic(B)
            end=time.time()
            elapsed_time_classic = end - start
            #print("i",i-size+sizerange)
            classic_time_average[i-size+sizerange]+=elapsed_time_classic
            B = copy.copy(temp)
            # time for the learned duals
            start=time.time()
            _,_ = learned.hungarian_learned(B,model_p,model_q)
            end=time.time()
            elapsed_time_learned = end - start
            learned_time_generalized[i-size+sizerange]+=elapsed_time_learned
            
            B = temp
            # time for the learned duals
            start=time.time()
            _,_ = learned.hungarian_learned(B,model_p_bis,model_q_bis)
            end=time.time()
            elapsed_time_learned = end - start
            learned_time_exact[i-size+sizerange]+=elapsed_time_learned
            
        classic_time_average[i-size+sizerange]/=10
        learned_time_generalized[i-size+sizerange]/=10
        learned_time_exact[i-size+sizerange]/=10
    diff_exact=[0] * (sizerange*2 +1)
    diff_gen=[0] * (sizerange*2 +1)
    
    for i in n_values:
        diff_exact[i-size+sizerange] = classic_time_average[i-size+sizerange] - learned_time_exact[i-size+sizerange]
        diff_gen[i-size+sizerange] = classic_time_average[i-size+sizerange] - learned_time_generalized[i-size+sizerange]
    
    # Plotting the bar plot
    x = np.arange(len(n_values))  # The label locations
    width = 0.35  # The width of the bars

    fig, ax = plt.subplots(figsize=(12, 8))
    rects1 = ax.bar(x - width/2, diff_exact, width, label='Model trained on same size', color='green')
    rects2 = ax.bar(x + width/2, diff_gen, width, label='Model trained on an approximatedly close size', color='orange')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Size of the graph')
    ax.set_ylabel('Difference in execution time (sec)')
    ax.set_title('Difference in execution time by graph size and model training')
    interval = max(1, len(n_values) // 10)  # Adjust interval as needed
    ax.set_xticks(x[::interval])
    ax.set_xticklabels(n_values[::interval])
    plt.grid(True)
    ax.legend()

    #ax.bar_label(rects1, padding=3)
    #ax.bar_label(rects2, padding=3)

    fig.tight_layout()

    plt.show()
    
    # Time plot
    # plt.figure(figsize=(10, 6))
    # plt.plot(n_values,diff_exact,color='green',label="Time gain using model trained on same size")
    # plt.plot(n_values,diff_gen,color='orange',label="Time gain using model trained on an approximatedly close size")
    # # plt.plot(n_values, classic_time_average, label ="Time without learned duals", color = "blue")
    # # plt.plot(n_values, learned_time_average, label ="Time with learned duals", color = "red")
    # plt.xlabel('Size of the graph')
    # plt.ylabel('difference in execution time (sec)')
    # plt.legend()
    # plt.grid(True)
    # plt.show()



