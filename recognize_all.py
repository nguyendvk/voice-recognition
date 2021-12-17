import os
from recognize import recognize

path = "./recognize"
count_true = 0
total_count = 0
for name in os.listdir(path):
    for file_wav in os.listdir(os.path.join(path, name)):
        file_wav = os.path.join(path, name, file_wav)
        print(f"{name}\t\t", end="")
        if recognize(file_wav) == name:
            count_true += 1
        total_count += 1

print(f"\nAccuracy = {count_true}/{total_count} = {count_true * 100/total_count}%")