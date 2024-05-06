# add mode_dict to query_trees numpy array and save it

import numpy as np

query_trees = np.load('query_trees.npy', allow_pickle=True)

# get the index for which the query_trees is empty
# query_id = np.where(query_trees == None)[0][0]

# query_trees[query_id] = node_dict
print(query_trees[0][(447, 256)])
print(query_trees[0][(447, 256)].children)
# print(query_trees[0][(216, 173)].children)
# print(query_trees[0][(231, 182)])

# print(query_trees[2])




# load flow_matrix
# flow_matrix = np.load('flow_matrix.npy', allow_pickle=True)
# print(flow_matrix.shape)