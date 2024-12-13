from dataclasses import dataclass

data = []
with open('test', 'r') as file:
    data = file.readlines()

COST_A = 3
COST_B = 1

@dataclass
class ButtonConfiguration:
    AX = 0
    AY = 0
    BX = 0
    BY = 0
    Position = None

def parseConfigs(configs):
    whichLine = 0
    currentConfig = None
    for line in data:
        match whichLine:
            case 0:
                currentConfig = ButtonConfiguration()

                pos = line.find('X+')
                xposline = line[pos+2:]
                pos = xposline.find(',')
                xvalue = int(xposline[:pos])

                currentConfig.AX = xvalue

                pos = line.find('Y+')
                yposline = line[pos+2:]
                pos = yposline.find(',')
                yvalue = int(yposline[:pos])

                currentConfig.AY = yvalue
            case 1:
                pos = line.find('X+')
                xposline = line[pos+2:]
                pos = xposline.find(',')
                xvalue = int(xposline[:pos])

                currentConfig.BX = xvalue

                pos = line.find('Y+')
                yposline = line[pos+2:]
                pos = yposline.find(',')
                yvalue = int(yposline[:pos])

                currentConfig.BY = yvalue
            case 2:
                pos = line.find('X=')
                xposline = line[pos+2:]
                pos = xposline.find(',')
                xvalue = int(xposline[:pos])

                pos = line.find('Y=')
                yposline = line[pos+2:]
                pos = yposline.find(',')
                yvalue = int(yposline[:pos])

                currentConfig.Position = (xvalue, yvalue)

                configs.append(currentConfig)
            case 3:
                pass
        
        whichLine = (whichLine + 1) % 4


def generate_combinations(A, B, N):
    combinations = []
    # given A, B, and N, what combinations of A and B make N
    for xA in range(100):
        for xB in range(100):
            if A * xA + B * xB == N:
                combinations.append((xA, xB))

    return combinations

def generate_large_combinations(A, B, N):
    combinations = []

    maxA = N // A
    for xA in range(maxA+1):
        amountA = A * xA
        remaining = N - amountA
        
        xB = remaining // B
        if A * xA + B * xB == N:
            combinations.append((xA, xB))

    return combinations

    #OLD
    # given A, B, and N, what combinations of A and B make N
    xA = 0
    xB = 0
    maxA = N // A
    maxB = N // B
    for xA in range(maxA + 1):
        combo = 0
        for xB in range(maxB + 1):
            combo = A * xA + B * xB
            if combo == N:
                combinations.append((xA, xB))

    return combinations

def find_combo_overlaps(xCombos, yCombos):
    overlaps = []
    for x in xCombos:
        for y in yCombos:
            if x == y:
                overlaps.append(x)

    return overlaps

# returns (A,B) where A is num A presses, B is num B presses
def find_optimal_presses(config : ButtonConfiguration):
    xCombos = generate_combinations(config.AX, config.BX, config.Position[0])
    yCombos = generate_combinations(config.AY, config.BY, config.Position[1])
    if len(xCombos) == 0 or len(yCombos) == 0:
        return None

    overlaps = find_combo_overlaps(xCombos, yCombos)
    if len(overlaps) == 0:
        return None

    smallestAIndex = -1
    smallestA = 101
    i = 0
    for overlap in overlaps:
        if smallestA < overlap[0]:
            smallestAIndex = i
            smallestA = overlap[0]
        i += 1
    return overlaps[smallestAIndex]

def find_optimal_presses2(config : ButtonConfiguration):
    AX = config.AX
    AY = config.AY
    BX = config.BX
    BY = config.BY

    NX = config.Position[0]
    NY = config.Position[1]

    maxAX = NX // AX
    maxAY = NY // AY
    maxA = min(maxAX, maxAY)
    for nA in range(maxA + 1):
        amountAX = AX * nA
        amountAY = AY * nA
        remainingX = NX - amountAX
        remainingY = NY - amountAY

        nBX = remainingX // BX
        nBY = remainingY // BY
        amountBX = nBX * BX
        amountBY = nBY * BY

        if amountAX + amountBX == NX and amountAY + amountBY == NY and nBX == nBY:
            return (nA, nBX)

    return None

def find_optimal_presses3(config : ButtonConfiguration):
    AX = config.AX
    AY = config.AY
    BX = config.BX
    BY = config.BY

    NX = config.Position[0]
    NY = config.Position[1]

    lasti = None
    lastj = None

    maxA = min(NX // AX, NY // AY)
    i = 0
    while i <= maxA:
        amountAX = AX * i
        remaining = NX - amountAX
        j = remaining // BX

        amountBX = j * BX
        remaining -=  amountBX

        idelta = 1

        if remaining == 0:
            if lastj and lasti:
                thisCost = calculate_cost((i,j))
                lastCost = calculate_cost((lasti, lastj))
                if thisCost < lastCost:
                    lasti = i
                    lastj = j
                else:
                    return (lasti,lastj)
            else:
                lasti = i
                lastj = j
        else:
            idelta = remaining // AX
            remaining -= idelta * AX
            if remaining > 0:
                idelta += 1

        i += idelta
    
    if lasti and lastj:
        return (lasti, lastj)
    
    return None

def calculate_cost(presses):
    aPresses = presses[0]
    bPresses = presses[1]
    return aPresses * COST_A + bPresses * COST_B

def main():
    configs = []
    parseConfigs(configs)
    totalCost = 0
    for config in configs:
        bestpress = find_optimal_presses(config)
        if bestpress == None:
            continue
        totalCost += calculate_cost(bestpress)
    
    print(totalCost)

def main2():
    configs = []
    parseConfigs(configs)

    for config in configs:
        config.Position = (config.Position[0] + 10000000000000, config.Position[1] + 10000000000000)

    totalCost = 0
    for config in configs:
        bestpress = find_optimal_presses3(config)
        if bestpress == None:
            continue
        totalCost += calculate_cost(bestpress)
    
    print(totalCost)

main2()