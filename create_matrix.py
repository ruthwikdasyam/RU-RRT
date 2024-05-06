import numpy as np

# crete a matrix with 600x400 dimensions, with 24 layers with empty lists
matrix = np.empty((600, 400, 24), dtype=object)
# insert empty lists in the matrix

matrix.fill([])
print(matrix.shape)
print(matrix[0,0,0])
#save the matrix externally, so that i can access it in other files
import numpy as np

np.save('flow_matrix.npy', matrix)


# create an empty numpy array and save it as a .npy file
query_trees = np.empty((20), dtype=object)
np.save('query_trees.npy', query_trees)
