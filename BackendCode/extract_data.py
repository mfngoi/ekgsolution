import wfdb
import numpy as np
from IPython.display import display

sig, fields = wfdb.rdsamp('ecg_data/raw/1001/0b61746e-c5f4-4b54-8baa-4404c22e09b5')

# https://pypi.org/project/wfdb/0.1.2/
# https://numpy.org/doc/stable/user/quickstart.html
# https://github.com/MIT-LCP/wfdb-python

print(sig)

# Properties
print(sig.ndim)
print(sig.shape)
print(sig.dtype)

# Indexing, Slicing and Iterating
# https://numpy.org/doc/stable/user/quickstart.html
leadII = sig[:,1]
print("Leads II")
print(leadII)
print(leadII.shape)

print()
print("===========================")
print()

print(fields)

# wfdb.plot_wfdb(sig=sig, fields=fields)
record = wfdb.rdrecord('ecg_data/raw/1001/0b61746e-c5f4-4b54-8baa-4404c22e09b5') 
wfdb.plot_wfdb(record=record, title='Training Data') 
display(record.__dict__)


