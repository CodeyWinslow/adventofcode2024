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

def findNextFreeSpace(desiredSize):
    start = 0
    while start < len(output):
        while start < len(output) and output[start] >= 0:
            start += 1

        end = start
        while end < len(output) and output[end] < 0:
            end += 1
        size = end-start

        if size >= desiredSize:
            return (start, size)
        else:
            start += 1
    return (-1, 0)

def findNextFile(index):
    end = index-1
    while end >= 0 and output[end] < 0:
        end -= 1

    id = output[end]

    start = end
    while start >= 0 and output[start] == id:
        start -= 1

    if start < 0:
        return (-1, 0)
    
    size = end-start
    start += 1
    return (start, size)

# move memory
fileIndex = len(output)
while fileIndex >= 0:
    nextFile = findNextFile(fileIndex)
    fileIndex = nextFile[0]
    fileSize = nextFile[1]
    if fileSize > 0:
        freeSpace = findNextFreeSpace(nextFile[1])
        freeStart = freeSpace[0]
        if fileIndex > freeStart and freeSpace[1] > 0:
            for i in range(fileSize):
                left = freeStart + i
                right = fileIndex + i
                output[left] = output[right]
                output[right] = -1

# calculate checksum
result = 0
index = 0
for num in output:
    if num < 0:
        index += 1
        continue

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