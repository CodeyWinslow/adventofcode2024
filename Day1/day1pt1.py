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

list1.sort()
list2.sort()

totalDiff = 0
for x in range(len(list1)):
    num1 = list1[x]
    num2 = list2[x]
    totalDiff += abs(num1 - num2)

print(totalDiff)