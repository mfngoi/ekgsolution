import base64
from datetime import datetime
import bitarray
import struct

data = "hEjMhykClBlqoEnWn7ognqpFnKiwhoeoc/bWZea1ZsZcaeYjaPaCZXapZKbDa9awaIYRaOZ9aFaUZfbZaMZia1ZbbAZ0Z4bZbEeWdtdledbtddbUbHeUckewmO7Z+j8YY0d8f5gxfGhbhZhlj2hPioioismolin0pRpMrmpsplo9mVnfj/jbiBe2dmdWbuddcGbob7aHbwbrakbzZXbFawaSbRaIbXbaZtagZUaxZ1Y8awZIbAZlZGbGaJcecYcIc3bYdGb3bfdTYzh/1T+k+ZXichdrdCgBeEhkgsgJijg1jPjBjWmQk+nBndmfozm+nQnHknlLiHhLhPfkh4hRfKhNfwegeJcAdScPboc1bTbwbDahcJbhdhdMcIcka3cPbIbUcCazcTbQaZbfaTbdbncFeldWfEcbcOeebwfsfRdoh8xI+o+lpjcXeQfLe7fViGhBiwh6g4jTh8jflOk1nOmZnFn3mEoXnJnWl7iEfVd5aQarZTZuacZ+bQaNZRbRaQcPcJcGdKbRbraXZwaVaEcIbYaib8avb/awbbdHcEeddJcodkbbdgcAdjgye8jEhjg8jggojJigiCjyfeql+e+p+Wc+gnhggnjnidjykojck7j8kdmgmwmAlojxmOkijqimfegfe2dHcqaEbKaUZvauZjY="
data = data.strip()

decoded_bytes = base64.b64decode(data)
print(f"{decoded_bytes=}")
b_array = bitarray.bitarray()
b_array.frombytes(decoded_bytes)

print(f"{b_array=}")
print(f"{len(b_array)=}")

count = 0
signals = []
for i in range(len(b_array)//12):
    start_idx = i * 12
    end_idx = (i+1) * 12
    num = int(b_array[start_idx : end_idx].to01(), 2)
    # print(f"{num=}")
    signals.append(num)
    count += 1

print(f"Signals: {signals}")
print(f"Count: {count}")



# 111010111100     001111010111
# 000001101111
# 100010100001
# 111111110111
# 000110001001


    
