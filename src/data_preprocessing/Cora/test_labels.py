
import numpy as np
import pickle
import networkx as nx


label_file = 'Cora_label.pkl'
label_dicts = None
with open(label_file, 'rb') as f:
    label_dicts = pickle.load(f)

labels = [l for l in label_dicts.values()]
unique, counts = np.unique(labels, return_counts=True)
print('unique label, counts \n', np.asarray((unique, counts)).T)