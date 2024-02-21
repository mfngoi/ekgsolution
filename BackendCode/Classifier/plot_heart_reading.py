import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Get 10,000 reading sample from file
input_data = []
with open("heart_samples/heartsample_5v_01.log", 'r') as file:
    while len(input_data) < 10000:
        line = file.readline().strip()
        if line.isdigit():
            input_data.append(int(line))
        if line == "":
            break
print(input_data)
print(len(input_data))

# Plot points
start = 300
points = 800
ecgLine = pd.Series(input_data[start:points+start], index=range(points))
ecgLine.plot()
plt.show()


