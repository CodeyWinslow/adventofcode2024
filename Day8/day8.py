data = []
with open('input', 'r') as file:
    data = file.readlines()
firstLine = data[0].strip()
width = len(firstLine)
height = len(data)

def is_in_range(position):
    x = position[0]
    y = position[1]
    return x >= 0 and x < width and y >= 0 and y < height

def collect_tower_map():
    map = {}

    for y in range(height):
        for x in range(width):
            char = data[y][x] 
            if char != '.':
                if char in map:
                    map[char].append((x,y))
                else:
                    map[char] = [(x,y)]

    return map

def generate_antinodes(towerA, towerB, uniqueNodes):
    diffX = towerB[0] - towerA[0]
    diffY = towerB[1] - towerA[1]
    #backward nodes
    iter = 1
    node = (towerB[0] - diffX, towerB[1] - diffY)
    while is_in_range(node):
        if node not in uniqueNodes:
            uniqueNodes.add(node)
        iter += 1
        node = (towerB[0] - diffX*iter, towerB[1] - diffY*iter)

def generate_unique_antinodes(towersByFreq):
    antinodes = set()
    for freq in towersByFreq.keys():
        towers = towersByFreq[freq]
        for i in range(len(towers)):
            towerA = towers[i]
            for j in range(len(towers)):
                if i == j:
                    continue
                towerB = towers[j]
                generate_antinodes(towerA, towerB, antinodes)

    return list(antinodes)

def debug_print_antinodes(antinodes):
    output = data.copy()
    for node in antinodes:
        x = node[0]
        y = node[1]

        if output[y][x] == '.':
            output[y] = output[y][:x] + "#" + output[y][x+1:]
    for line in output:
        print(line.strip())

def main():
    all_towers = collect_tower_map()
    antinodes = generate_unique_antinodes(all_towers)
    #debug_print_antinodes(antinodes)
    print(len(antinodes))

main()