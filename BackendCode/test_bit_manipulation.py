import base64
from datetime import datetime
import bitarray
import struct

data = "UQaTy3l+2ZqC4NlP5hb35hlXD1us1S9JT2pJjN/9vm6RI3MNeUikbUU3tRdcseNxoW+31xG5NKGJIrR778XdrWxohdeI/8gTSg6uK252PsvixR+OSAMECSXpxLiecHul26IVGlfrA8mPg1YNaq0UjQYJP225M52sxQKNd/MzTbv30hQxjSpgeEcmeB6eOnmFVfcRpYiYq1mua8dc43zVMvhGijbtNJzVqdKRn3DAY+LiK3/50CywYBCT+e2V9NiLqZWJgH4vbmGPKI1ow9K1vRapnpt773uBVBqUKTIqmuxlwxMT+qjffgrG13hrgMW+fVT/vHvxHyNzUOWXSRiR1iLYO8UxrMNNNDhPoIFbtZ2FG18OJz07XZdf9OoFB020/6/NtS/Hf01FXilzKpKCA2A19AAgdMMGIX0GbgRz2JUW9n4gH2TgPRAoMb2VdHGQEUROgkskUGCnczlr78vEId55KQppomcjXK434LIv8otJNcFeijQnI30yvNXiIwL8H4UOmMLhFFn9U86N9tKoE5tWuFMRpulCQiVIZ+0/1IA86TYByrQWJYH0GZOdt5cprqf3nEYffXaAi7NHKwOCnVsQV7fH/QaorK4z/Aan+lmFjoGbjfzJ2zFp00qrK/DRlDSCYKwfjylJxqMkavKXc7gfoYE="
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









# date = datetime.now()
# print(f"{str(date)=}")
# weekNum = 0
# startDay = datetime(date.year, 1, 1)
# daysDiff = (date - startDay).days
# print(f"{daysDiff=}")


# if date.weekday == 6:
#     weekNum = daysDiff // 7 + 1
# else: 
#     weekNum = daysDiff // 7
# print(f"{weekNum}")
    
