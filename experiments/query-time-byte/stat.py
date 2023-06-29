with open('./8byte.raw.dat', 'r') as f:
    data = [int(float(line.strip()) * 1000) for line in f.readlines()]

lower_bound = min(data)
upper_bound = max(data)
width = (upper_bound - lower_bound) / 200

freq = [0] * 201
for d in data:
    index = int((d - lower_bound) / width)
    freq[index] += 1

with open('8byte.dat', 'w') as f:
    for i in range(201):
        midpoint = (lower_bound + width/2) + i * width
        frequency = freq[i] / len(data)
        f.write(f"{midpoint}\t{frequency}\n")

with open('./128byte.raw.dat', 'r') as f:
    data = [int(float(line.strip()) * 1000) for line in f.readlines()]

lower_bound = min(data)
upper_bound = max(data)
width = (upper_bound - lower_bound) / 200

freq = [0] * 201
for d in data:
    index = int((d - lower_bound) / width)
    freq[index] += 1

with open('128byte.dat', 'w') as f:
    for i in range(201):
        midpoint = (lower_bound + width/2) + i * width
        frequency = freq[i] / len(data)
        f.write(f"{midpoint}\t{frequency}\n")

with open('./1024byte.raw.dat', 'r') as f:
    data = [int(float(line.strip()) * 1000) for line in f.readlines()]

lower_bound = min(data)
upper_bound = max(data)
width = (upper_bound - lower_bound) / 200

freq = [0] * 201
for d in data:
    index = int((d - lower_bound) / width)
    freq[index] += 1

with open('1024byte.dat', 'w') as f:
    for i in range(201):
        midpoint = (lower_bound + width/2) + i * width
        frequency = freq[i] / len(data)
        f.write(f"{midpoint}\t{frequency}\n")
