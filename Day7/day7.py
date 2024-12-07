from bitarray import bitarray
data = []
with open('input', 'r') as file:
    data = file.readlines()

def operator_add(a, b):
    return a + b

def operator_mul(a, b):
    return a * b

def operator_concat(a, b):
    return int(str(a) + str(b))

def int_to_bit_array(num, desired_len):
    arr = [int(bit) for bit in bin(num)[2:]]  # [2:] removes '0b' prefix
    while len(arr) < desired_len:
        arr.insert(0, 0)

    return arr

def create_operator_index_combos(operatorCount):
    maxNum = pow(3, operatorCount)
    combos = []
    for i in range(maxNum):
        combo = list(0 for j in range(operatorCount))
        for n in range(operatorCount):
            combo[n] = (i // pow(3, n)) % 3
        combos.append(combo)
    return combos

operators = [ operator_add, operator_mul, operator_concat]
def has_valid_operators(target, nums):
    numOperators = len(nums)-1
    combos = create_operator_index_combos(numOperators)
    
    stack = []
    for i in range(len(nums)):
        num = nums[len(nums) - i - 1]
        stack.append(num)

    for combo in combos:
        workingStack = stack.copy()
        skipCombo = False

        for opIndex in combo:
            a = workingStack.pop()
            b = workingStack.pop()
            res = operators[opIndex](a, b)
            if res > target:
                skipCombo = True
                break
            workingStack.append(res)
        
        if skipCombo:
            continue

        assert(len(workingStack) == 1)
        if workingStack.pop() == target:
            return True
        
    return False

sum = 0
for line in data:
    parts = line.split(':')
    target = int(parts[0])
    nums = list(int(a) for a in parts[1].split())
    
    if has_valid_operators(target, nums):
        sum += target

print(sum)