import io

data = ''
with open('input', 'r') as file:
    data = file.read()

list1 = []
list2 = []

lines = data.split()

count = 0
for x in lines:
    if count % 2 == 0:
        list1.append(int(x))
    else:
        list2.append(int(x))
    count += 1

occurrences = {}
for x in list2:
    if x in occurrences:
        occurrences[x] += 1
    else:
        occurrences[x] = 1

similarity = 0
for x in list1:
    numOccurred = 0 if x not in occurrences else occurrences[x]
    similarity += x * numOccurred

print(similarity)