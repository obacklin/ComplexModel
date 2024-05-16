import random
import igraph as ig
import numpy as np
import time
def ER_graph(n,p):
    G = ig.Graph()
    G.add_vertices(n)
    G.vs['label'] = [x for x in range(n)]
    for i in range(n):
        for j in range(n):
            r = random.random()
            if j>i and r<p:
                G.add_edge(i,j)
    return G

def is_connected(G):
    #The Breath First Search Algorithm
    vx=0
    discovered = [0]
    BFS_list = []
    nbhd = G.neighbors(vx)
    for x in nbhd:
        BFS_list.append(x)
        discovered.append(x)
    while len(BFS_list) > 0:
        vx = BFS_list[0]
        nbhd = G.neighbors(vx)
        for x in nbhd:
            if x not in discovered:
                BFS_list.append(x)
                discovered.append(x)
        BFS_list.pop(0)
    if len(discovered) == G.vcount():
        return True
    return False 
def prop_connected(steps):
    epsilon = 0.3
    n=500
    p = (1-epsilon)*np.log(n)/n
    q = (1+epsilon)*np.log(n)/n
    p_connected=0
    q_connected=0
    for i in range(steps):
        G_p = ER_graph(n,p)
        G_q = ER_graph(n,q)
        if is_connected(G_p):
            p_connected += 1
        if is_connected(G_q) == True:
            q_connected += 1
    print(f' Percentage of connected graphs when p is less or greater to (1-epsilon)log(n)/n\n Less: {p_connected/steps}\n Greater: {q_connected/steps}'
          )
#tSTART = time.perf_counter()
#prop_connected(100)
#tSTOP = time.perf_counter()
#print(f'Time: {round(tSTOP-tSTART,2)} seconds')

