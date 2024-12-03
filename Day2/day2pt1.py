data = ''
with open('input', 'r') as file:
    data = file.read()

reports = data.split('\n')

numSafeReports = 0

for report in reports:
    nums = report.split()
    safe = True
    if len(nums) > 0:
        prevValue = int(nums[0])
        delta = 0
        for idx in range(1, len(nums)):
            num = int(nums[idx])

            # check delta
            newDelta = num - prevValue

            if abs(newDelta) > 3 or abs(newDelta) < 1:
                safe = False
                break

            if newDelta != 0:
                newDelta = abs(newDelta) / newDelta
            
            if delta == 0:
                delta = newDelta
            elif delta != newDelta:
                safe = False
                break

            prevValue = num
        
        if safe:
            numSafeReports += 1

print(numSafeReports)


