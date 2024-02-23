import pandas as pd
import numpy as np
import wfdb

# # NUMPY 
# sig, fields = wfdb.rdsamp('ecg_data/raw/1001/0b61746e-c5f4-4b54-8baa-4404c22e09b5')

# # Example of a numpy array
# print(sig)

# # Properties
# print(sig.ndim)     # Gives dimension of array
# print(sig.shape)    # Gives the lengths of the array
# print(sig.dtype)    # Gives the array type

# Numpy creation
# my_numpy = np.random.randn(6, 4)
my_numpy = np.arange(24).reshape(6, 4)
print(my_numpy)
print()
print(my_numpy[0:5, 2])
# np.zeros((3,4))
# np.arange(15).reshape(5, 3)

# Indexing and Slicing

# Combining arrays
print()
numpie1 = np.arange(12)
print(numpie1)

numpie2 = np.arange(12)
numpie2 = numpie2 * 3
print(numpie2)


numpie_combined = np.vstack((numpie1, numpie2))
print(numpie_combined)
# np.vstack()
# np.hstack()


# PANDAS
# # Reading a csv file
# csv = pd.read_csv('../ecg_data/SCR-002.Clinical.Data.csv', index_col=[0])
# print(csv)

# Creating a dataframe
# my_dataframe = pd.DataFrame(sig)
# print(my_dataframe)
my_panda = pd.DataFrame(data=np.random.randn(3,4))
my_panda.columns = ['A','B','C','D']
print(my_panda)

# Indexing and slicing

# Concat and merge

# my_dataframe.to_csv('myDataframe.csv')