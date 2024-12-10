data = []
with open('input', 'r') as file:
    data = file.readlines()

width = len(data[0].strip())
height = len(data)

def is_valid_position(position):
    x = position[0]
    y = position[1]
    return x >= 0 and x < width and y >= 0 and y < height

def get_height(position):
    char = data[position[1]][position[0]]
    return int(char)

def add_or_replace_path(paths, path):
    for i in range(len(paths)):
        prev = paths[i]
        if prev[0] == path[0]:
            if prev[1] < path[1]:
                paths[i] = path
            return
    # never found an existing one
    paths.append(path)


# returns a list of (trail heads, pathLength)
def find_trails(position, path, allPaths):
    if not is_valid_position(position):
        return
       
    newPath = path.copy() + [ position ]
    cur_height = get_height(position)
    if cur_height == 9:
        allPaths.append(newPath)
        return

    next = position
    # up
    next = (next[0],next[1]-1)
    if is_valid_position(next) and get_height(next) == cur_height + 1:
        find_trails(next, newPath, allPaths)

    # left
    next = (next[0]-1,next[1]+1)
    if is_valid_position(next) and get_height(next) == cur_height + 1:
        find_trails(next, newPath, allPaths)

    # right
    next = (next[0]+2,next[1])
    if is_valid_position(next) and get_height(next) == cur_height + 1:
        find_trails(next, newPath, allPaths)

    # down
    next = (next[0]-1,next[1]+1)
    if is_valid_position(next) and get_height(next) == cur_height + 1:
        find_trails(next, newPath, allPaths)

def calculate_trailhead_score(trailhead):
    allTrails = []
    find_trails(trailhead, [], allTrails)

    # (peak, len)
    uniqueTrails = []
    for i in range(len(allTrails)):
        candidate = allTrails[i]
        candidatePeak = candidate[len(candidate) - 1]
        isUnique = True
        for j in range(len(uniqueTrails)):
            bestLen = uniqueTrails[j][1]
            bestPeak = uniqueTrails[j][0]
            if bestPeak == candidatePeak:
                isUnique = False
                if bestLen < len(candidate):
                    uniqueTrails[j] = (candidatePeak, len(candidate))
                break

        if isUnique:
            uniqueTrails.append((candidatePeak, len(candidate)))
    
    score = len(uniqueTrails)
    return score

def calculate_trailhead_score_with_rating(trailhead):
    allTrails = []
    find_trails(trailhead, [], allTrails)
    return len(allTrails)
    # (peak, len)
    uniqueTrails = []
    for i in range(len(allTrails)):
        candidate = allTrails[i]
        candidatePeak = candidate[len(candidate) - 1]
        isUnique = True
        for j in range(len(uniqueTrails)):
            bestLen = uniqueTrails[j][1]
            bestPeak = uniqueTrails[j][0]
            if bestPeak == candidatePeak:
                isUnique = False
                if bestLen < len(candidate):
                    uniqueTrails[j] = (candidatePeak, len(candidate))
                break

        if isUnique:
            uniqueTrails.append((candidatePeak, len(candidate)))
    
    score = len(uniqueTrails)
    return score

def main():
    totalScore = 0
    for y in range(height):
        for x in range(width):
            pos = (x,y)
            if get_height(pos) == 0:
                totalScore += calculate_trailhead_score(pos)

    print(totalScore)

def main2():
    totalScore = 0
    for y in range(height):
        for x in range(width):
            pos = (x,y)
            if get_height(pos) == 0:
                totalScore += calculate_trailhead_score_with_rating(pos)

    print(totalScore)
    
main2()