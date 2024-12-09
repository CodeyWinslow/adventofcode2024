data = []
with open('input', 'r') as file:
    data = file.read()

class BlockMember:
    def __init__(self, id, position):
        self.Id = id
        self.num = 0

# build initial state
id = 0
output = []
for index in range(len(data)):
    if index % 2 == 0:
        for i in range(int(data[index])):
            output.append(id)
        id += 1
    else:
        repeat = data[index]
        for i in range(int(data[index])):
            output.append(-1)

right = len(output) - 1
left = 0

# move memory
while (left < right):
    while left < len(output) and output[left] >= 0:
        left += 1

    while right >= 0 and output[right] < 0:
        right -= 1

    if left < right:
        output[left] = output[right]
        output[right] = -1

while left < len(output):
    output[left] = -1
    left += 1

# calculate checksum
result = 0
index = 0
for num in output:
    if num < 0:
        break

    result += num * index
    index += 1

print(result)
'''
outStr = ''
for num in output:
    if num < 0:
        outStr += '.'
    else:
        outStr += str(num)

print(outStr)
'''