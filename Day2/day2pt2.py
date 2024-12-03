data = ''
with open('input', 'r') as file:
    data = file.read()

reports = data.split('\n')

numSafeReports = 0

def isSafeReport(nums):
    safe = True
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

    return safe

'''
for report in reports:
    nums = report.split()
    originalnums = nums.copy()
    safe = True
    if len(nums) > 0:
        prevValue = int(nums[0])
        delta = 0
        faultIndex = -1

        # see if safe or you found an error
        for idx in range(1, len(nums)):
            num = int(nums[idx])

            # check delta
            newDelta = num - prevValue

            if abs(newDelta) > 3 or abs(newDelta) < 1:
                faultIndex = idx
                safe = False
                break

            if newDelta != 0:
                newDelta = abs(newDelta) / newDelta
            
            if delta == 0:
                delta = newDelta
            elif delta != newDelta:
                faultIndex = idx
                safe = False
                break

            prevValue = num
        

        if safe:
            numSafeReports += 1
        else:
            safe = True
            # try removing the error
            nums.pop(faultIndex)

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
            elif faultIndex == 1:
                nums = originalnums.copy()
                nums.pop(0)
                safe = True
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
'''

for report in reports:
    nums = report.split()
    if len(nums) < 1:
        continue

    isSafe = isSafeReport(nums)
    if isSafe:
        numSafeReports += 1
        #print('report safe')
    else:
        # go through each and test
        foundSafe = False
        newNums = nums
        for removeIdx in range(0, len(nums)):
            newNums = nums.copy()
            newNums.pop(removeIdx)
            if isSafeReport(newNums):
                foundSafe = True
                break

        if foundSafe:
            print('safe with removal')
            print(nums)
            print(newNums)
            numSafeReports += 1
        else:
            pass#print('never safe')

print(numSafeReports)

