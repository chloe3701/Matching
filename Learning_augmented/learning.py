import sys
sys.path.append('../')
from Utils import graph
from Utils import data_generator
import hungarian_classic_opt as classic
import numpy as np
import pandas as pd
import optimal
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

filename = "../Utils/tests/instance.txt"
training_size = 20

def extract_features(B):
    features = []
    for node in B.nodes():
        neighbors = list(B.neighbors(node))
        degrees = [B.degree(n) for n in neighbors]
        weights = [B[node][n]['weight'] for n in neighbors]
        features.append({
            'node': node,
            'degree': B.degree(node),
            'avg_neighbor_degree': np.mean(degrees) if degrees else 0,
            'max_neighbor_degree': max(degrees) if degrees else 0,
            'min_neighbor_degree': min(degrees) if degrees else 0,
            'avg_edge_weight': np.mean(weights) if weights else 0,
            'max_edge_weight': max(weights) if weights else 0,
            'min_edge_weight': min(weights) if weights else 0
        })
    return pd.DataFrame(features)

def learn(graph_size,param1=100,param2=20,distribution=1):
    p_mean={u:0.0 for u in range(graph_size)}
    q_mean={v:0.0 for v in range(graph_size,2*graph_size)}
    
    solved_instances = []
    for i in range(training_size):
        # B = data_generator.gen_no_file(graph_size,std_dev=std_dev,mean=mean)
        B = data_generator.gen_no_file(graph_size,param1=param1,param2=param2,distribution=distribution)
        opt=optimal.optimal(B)
        if(opt!=-1):
            _,p,q,_ = classic.hungarian_classic(B)
            for u in range(graph_size):
                p_mean[u]+=p[u]
            for v in range(graph_size,2*graph_size):
                q_mean[v]+=q[v]
            solved_instances.append({
                'graph': B.B,
                'p': p,
                'q': q
            })
        else:
            i=i-1

    # Prepare dataset
    X = []
    y_p = []
    y_q = []

    for instance in solved_instances:
        B = instance['graph']
        features_df = extract_features(B)
        X.append(features_df.drop(columns=['node']).values)
        y_p.append([instance['p'].get(node, 0) for node in B.nodes()])
        y_q.append([instance['q'].get(node, 0) for node in B.nodes()])

    X = np.vstack(X)
    y_p = np.hstack(y_p)
    y_q = np.hstack(y_q)

    # Split data
    #X_train, X_test, y_p_train, y_p_test, y_q_train, y_q_test = train_test_split(X, y_p, y_q, test_size=0.2, random_state=42)

    # Train models
    model_p = RandomForestRegressor()
    model_q = RandomForestRegressor()

    model_p.fit(X, y_p)
    model_q.fit(X, y_q)
    # model_p.fit(X_train,y_p_train)
    # model_q.fit(X_train,y_q_train)
    
    for u in range(graph_size):
        p_mean[u]=p_mean[u]/training_size
    for v in range(graph_size,2*graph_size):
        q_mean[v]=q_mean[v]/training_size
    
    return model_p,model_q,p_mean,q_mean
        
