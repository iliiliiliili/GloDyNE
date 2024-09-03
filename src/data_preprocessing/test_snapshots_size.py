
import numpy as np
import pickle
import networkx as nx


data_file = 'FacebookWall/FacebookWall_new.pkl'
data_dicts = None
with open(data_file, 'rb') as f:
    data_dicts = pickle.load(f)

cnt = 0
total_nodes = 0
total_edges = 0
for g in data_dicts:
    print('snapshot @ ', cnt)
    nodes = g.number_of_nodes()
    edges = g.number_of_edges()
    print('# of nodes ', nodes)
    print('# of edges ', edges)
    total_nodes += nodes
    total_edges += edges
    cnt += 1

print('# of total nodes ', total_nodes)
print('# of total edges ', total_edges)