from ecgclassifier import ecgClassify
import pickle

# Load model
with open('target/ecgClassifier.pkl', 'rb') as f:
    ecgClassifier = pickle.load(f)

# Load label encoders
with open('target/condition_encoder.pkl', 'rb') as f:
    condition_encoder = pickle.load(f)
with open('target/sex_encoder.pkl', 'rb') as f:
    sex_encoder = pickle.load(f)
with open('target/ethnicity_encoder.pkl', 'rb') as f:
    ethnicity_encoder = pickle.load(f)

# Store encoders
encoders = {
    'condition': condition_encoder,
    'sex': sex_encoder,
    'ethnicity': ethnicity_encoder,
}

profile = {"sex":"M","age":23,"height":180.5,"weight":67.8,"ethnicity":"ASIAN"}

# Get #### reading sample from file
input_data = []
with open("target/heartsample_5v_100_5sec.log", 'r') as file:
    while len(input_data) < 100:
        line = file.readline().strip()
        if line.isdigit():
            input_data.append(int(line))
        if line == "":
            break

# Signals into text
print(f"{input_data=}")
ecg_signals = ""
for i in range(len(input_data)):
    ecg_signals += str(input_data[i]) + ","


ecg_signals = ecg_signals.split(',')
ecg_signals.pop() # Clean end of signal (loose string)

# Get condition in result
result = ecgClassify(profile, ecg_signals, ecgClassifier, encoders)
print(f"{result}")


import random

text = "2273, 2415, 2333, 2112, 2303, 2329, 2374, 2182, 2156, 1407, 2138, 2195, 2362, 2320, 1957, 1907, 2030, 1906, 1989, 1947, 2580, 1908, 1999, 2160, 2311, 2225, 1877, 2016, 1979, 1994, 2086, 1949, 3370, 1918, 1965, 2118, 2334, 2265, 1869, 2045, 2024, 1985, 2033, 2022, 2772, 1712, 1819, 2007, 2168, 2087, 1654, 1989, 2047, 2056, 2026, 2051, 2012, 2792, 1889, 1996, 2160, 2153, 1929, 1987, 2076, 2013, 2012, 1914, 2027, 2031, 4000, 1818, 1985, 2118, 2114, 1942, 1862, 1968, 1903, 1928, 1815, 1852, 1988, 1897, 3127, 1792, 1846, 1983, 2096, 2016, 1782, 1956, 1944, 1992, 1879, 2011, 1956, 1951, 1939, 3857"

# for x in range(10000):
#     r = random.randint(0,4095)
#     text += str(r) + ","

print(text.replace(" ", ""))


