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
    # given A, B, and N, what combinations of A and B make N
    xA = 0
    xB = 0
    while True:
        combo = 0
        while True:
            combo = A * xA + B * xB
            if A * xA + B * xB == N:
                combinations.append((xA, xB))
            elif combo > N:
                break
            xB += 1
        if combo > N:
            break
        xA += 1

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
    xCombos = generate_large_combinations(config.AX, config.BX, config.Position[0])
    yCombos = generate_large_combinations(config.AY, config.BY, config.Position[1])
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
        bestpress = find_optimal_presses2(config)
        if bestpress == None:
            continue
        totalCost += calculate_cost(bestpress)
    
    print(totalCost)

main2()