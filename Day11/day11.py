data = []
with open('input', 'r') as file:
    data = file.read().split()

def get_new_stones(stone):
    size = len(stone)
    if size % 2 == 0:
        half = stone[0:size//2]
        otherHalf = stone[size//2:size]
        return [str(int(half)), str(int(otherHalf))]

    if stone == '0':
        return ['1']
    
    return [str(int(stone) * 2024)]

def blink(stones):
    newStones = []
    for stone in stones:
        newStones += get_new_stones(stone)

    return newStones

def blinkStone(stone, blinkIter, numBlinks, stoneCache):
    if blinkIter == numBlinks:
        return 1
    
    if (stone, blinkIter) in stoneCache:
        return stoneCache[(stone, blinkIter)]

    newStones = get_new_stones(stone)
    numStones = 0
    for innerStone in newStones:
        numStones += blinkStone(innerStone, blinkIter+1, numBlinks, stoneCache)

    stoneCache[(stone, blinkIter)] = numStones
    return numStones
    
def main():
    numBlinks = 25
    stones = data.copy()
    for i in range(numBlinks):
        stones = blink(stones)

    print(len(stones))

def main2():
    # key: (stone, blinkNum) val: numStones
    stoneCache = {}
    numBlinks = 75
    stones = 0
    for stone in data:
        stones += blinkStone(stone, 0, numBlinks, stoneCache)

    print(stones)

main2()