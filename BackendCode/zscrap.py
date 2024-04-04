

# Get #### reading sample from file
input_data = []
with open("target/heartsample_5v_100_5sec_03.log", 'r') as file:
    while len(input_data) < 100:
        line = file.readline().strip()
        if line.isdigit():
            input_data.append(int(line))
        if line == "":
            break

# Signals into text
# print(f"{input_data=}")
ecg_signals = ""
for i in range(len(input_data)):
    ecg_signals += str(input_data[i]) + ","

print(ecg_signals)


