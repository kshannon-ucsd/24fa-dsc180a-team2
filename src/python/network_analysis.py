#!/usr/bin/env python
# coding: utf-8

# ### Network Analysis

# In[113]:


import pandas as pd
from collections import defaultdict
import numpy as np
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import random
import os
random.seed(2)
np.random.seed(30)


# In[107]:


X = pd.read_csv("../../lca_data.csv")
y = pd.read_csv("../../subgroups.csv")["six_classes"]


# In[109]:


try:
    X = X.drop(columns=["Unnamed: 0"])
except: pass
X['class'] = y


# In[116]:


def generate_network(class_num, X):
    class_data = X[X['class'] == class_num]
    class_data = class_data.drop(columns=['class'])
    total_patients = len(class_data)
    morbidity_frequency = defaultdict(int)
    
    for i in range(len(class_data)):
        for j in range(3, len(class_data.columns)):
            if class_data.iloc[i][class_data.columns[j]] == 1:
                morbidity_frequency[class_data.columns[j]] += 1
                
    cooccurrence_matrix = pd.DataFrame(0, index=morbidity_frequency.keys(), columns=morbidity_frequency.keys())
    combos = list(combinations(morbidity_frequency.keys(), 2))
    
    # Building up the cooccurrence matrix
    for i in range(len(class_data)):
        for j in range(len(combos)):
            if class_data.iloc[i][combos[j][0]] == 1 and class_data.iloc[i][combos[j][1]] == 1:
                cooccurrence_matrix.loc[combos[j][0], combos[j][1]] += 1
                cooccurrence_matrix.loc[combos[j][1], combos[j][0]] += 1
    
    # Normalize the cooccurrence matrix by dividing by the total number of patients
    for i in range(len(cooccurrence_matrix)):
        for j in range(len(cooccurrence_matrix)):
            cooccurrence_matrix.iloc[i, j] = cooccurrence_matrix.iloc[i, j] / total_patients
    
    # Create network where node size is proportional to the frequency of the morbidity and edge width is proportional to the cooccurrence frequency
    G = nx.Graph()
    for i in range(len(morbidity_frequency)):
        G.add_node(list(morbidity_frequency.keys())[i], size=morbidity_frequency[list(morbidity_frequency.keys())[i]])
        
    for i in range(len(cooccurrence_matrix)):
        for j in range(len(cooccurrence_matrix)):
            if cooccurrence_matrix.iloc[i, j] > 0.01:
                G.add_edge(cooccurrence_matrix.index[i], cooccurrence_matrix.columns[j], weight=cooccurrence_matrix.iloc[i, j], alpha=cooccurrence_matrix.iloc[i, j])
                
    return G 


# In[115]:


# Plotting the networks for each class
os.makedirs("../../res/_networks", exist_ok=True)
for i in range(1, 7):
    G = generate_network(i, X)
    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G, k=1.1, seed=42)
    node_sizes = [G.nodes[n]['size']*0.2 for n in G]
    edge_widths = [G[u][v]['weight']*20 for u, v in G.edges()]
    edge_opacities = [G[u][v]['alpha']*1.2 for u, v in G.edges()]

    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=edge_opacities)
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black', font_family='sans-serif')
    plt.title(f"Network of Morbidities for Class {i}")
    plt.axis('off')
    plt.savefig(f"../../res/_networks/network_class_{i}.png")
    plt.close()

