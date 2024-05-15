from L4Task2 import ER_graph
import igraph as ig
import numpy as np
import matplotlib.pyplot as plt
def cluster_coeff(G):
    adj_data = G.get_adjacency()
    adj_mx = np.array(adj_data.data)
    #num = np.trace(np.linalg.matrix_power(adj_mx,3))
    num=0
    for i in range(G.vcount()):
        for j in range(G.vcount()):
            for k in range(G.vcount()):
                num += adj_mx[i,j]*adj_mx[j,k]*adj_mx[k,i]

    denom = 0
    for row in adj_mx:
        n_i = np.sum(row)
        denom += n_i*(n_i-1)
    if denom == 0:
        return 0
    return num/denom
def plot_C(n,nr_graphs):
    p_lst = [x/10 for x in range(1,10)]
    c_coeffs = []
    for p in p_lst:
        mean_c_coeff = 0
        for i in range(nr_graphs):
            G = ER_graph(n,p)
            mean_c_coeff += cluster_coeff(G)/nr_graphs
        c_coeffs.append(mean_c_coeff)
    print(c_coeffs)
    plt.plot(p_lst,c_coeffs,"blue",label=("Calculated"))
    plt.xlabel("p")
    plt.ylabel("C")
    plt.title("Clustering coefficient C vs proabilities p")
    plt.legend()
    plt.show()
plot_C(50,10)
p = 0.4
n = 100
G = ER_graph(n,p)
C = cluster_coeff(G)


