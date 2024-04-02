

import random

text = ""

for x in range(10000):
    r = random.randint(0,4095)
    text += str(r) + ","

print(text)


