data = []
with open('input', 'r') as file:
    data = file.readlines()

class Update:
    def __init__(self):
        self.pages = []

    def parse(self, line):
        nums = line.split(',')
        for num in nums:
            self.pages.append(int(num))

    def toString(self):
        return str(self.pages)

class Rule:
    requiredPage = -1
    targetPage = -1

    def parse(self, line):
        nums = line.split('|')
        self.requiredPage = int(nums[0])
        self.targetPage = int(nums[1])

    def toString(self):
        return str(self.requiredPage) + "|" + str(self.targetPage)

rules = []
updates = []

def parseRule(line):
    rule = Rule()
    rule.parse(line)
    rules.append(rule)

def parseUpdate(line):
    update = Update()
    update.parse(line)
    updates.append(update)

def doesConflictingRuleExist(page, prev):
    for rule in rules:
        if rule.requiredPage == page and rule.targetPage == prev:
            return True
        
    return False

def isPageInOrder(page, prevPages):
    for prev in prevPages:
        if doesConflictingRuleExist(page, prev):
            return False
    
    return True

def swap(arr, i, j):
    temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp

def fixUpdate(update):
    pages = update.pages.copy()

    testIndex = 0
    while (testIndex < len(pages)):
        page = pages[testIndex]
        prevIndex = 0
        while (prevIndex < testIndex):
            prevPage = pages[prevIndex]

            if doesConflictingRuleExist(page, prevPage):
                swap(pages, testIndex, prevIndex)
                testIndex = prevIndex
                break

            prevIndex += 1
        testIndex += 1

    newUpdate = Update()
    newUpdate.pages = pages
    return newUpdate


def main():
    sum = 0
    # parse rules
    readingRules = True
    for line in data:
        if line.strip() == '':
            readingRules = False
        else:
            if readingRules:
                parseRule(line)
            else:
                parseUpdate(line)
    for update in updates:
        allInOrder = True
        for i in range(len(update.pages)):
            page = update.pages[i]
            prevPages = [] if i == 0 else update.pages[:i]
            if not isPageInOrder(page, prevPages):
                allInOrder = False
                break

        if not allInOrder:
            newUpdate = fixUpdate(update)
            middleNum = newUpdate.pages[int(len(newUpdate.pages)/2)]
            sum += middleNum
    print(sum)

main()