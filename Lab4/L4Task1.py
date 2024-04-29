import numpy as np
import urllib.request
import urllib3
import matplotlib.pyplot as plt
import re
from igraph import *
import leidenalg as la
#Works on igraph/leidenalg version 0.8.0 (not the newest)
url =  urllib.request.urlopen("http://vlado.fmf.uni-lj.si/pub/networks/data/sport/football.net")
data_file = url.readlines()

#Create Node List
countries = []
nodes = data_file[1:36]
for i in nodes:
    country = i.decode('utf-8')
    word_list = re.split(r'\s+', country)
    countries.append(word_list[2])
    country_list = [s.strip('"\'') for s in countries]



#Create Adjacency matrix
adjacency_matrix = np.zeros((35,35))
data = data_file[37:-1]
weightlist=[]
for entry in data:    
    line = entry.decode('utf-8')
    words_list = re.split(r'\s+', line)
    row = int(words_list[1])
    col = int(words_list[2])
    weight = int(words_list[3])
    weightlist.append(weight)
    adjacency_matrix[row-1,col-1] = weight

#Create and plot graph, use the Leiden algorithm to find clusters
lst_matrix = adjacency_matrix.tolist()
g = Graph.Weighted_Adjacency(lst_matrix)
g.vs["label"] = country_list
g.vs["label_size"] = 8
g.es["width"]= [x/3 for x in weightlist]
g.es["arrow_size"]= 0.8


partition = la.find_partition(g,la.ModularityVertexPartition)
plot(partition)
#Found clusters
clusterlist = [[1,7,13,14,15,18,25,29], [9,12,16,19,20,21,30,33],[2,5,10,23,24,28,31,34],[3,4,11,22,26,27],[0,6,8,17,32]]
clusters = [g.subgraph(i) for i in clusterlist]

#Compute Modularity
m = sum(weightlist)
mod_g = 0
for cluster in clusters:
    cluster_mx = cluster.get_adjacency(attribute='weight')
    edgesum = 0
    for row in cluster_mx:
        edgesum += sum(row)
    print(edgesum)

    mod_g += edgesum/m - edgesum**2/(4*m**2)
print(f' Modularity of partition: {mod_g}')
print((37+23+26+20+18)/m)