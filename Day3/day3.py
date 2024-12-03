data = ''
with open('input', 'r') as file:
    data = file.read()

STATE_KEYWORD = 1
STATE_OPENPAREN = 2
STATE_FIRSTARG = 3
STATE_COMMA = 4
STATE_SECONDARG = 5
STATE_CLOSEPAREN = 6
STATE_COMPLETE = 7

class PersistentState:
    FirstArg = 0
    SecondArg = 0
    ProcessStatements = True
    MaintainState = False

class State:
    Finished = False
    Persistent = PersistentState()

    def __init__(self, persistent):
        self.Persistent = persistent

    def MarkFinished(self):
        self.Finished = True

    def GetStateId(self):
        pass

    def process_char(self, char, nextChar):
        pass

class KeywordState(State):
    # keyword 1
    keywordMul = 'mul'
    # keyword 2
    keywordDo = 'do()'
    # keyword 3
    keywordDont = "don't()"

    targetKeyword = 0
    expectedIndex = 0



    def GetStateId(self):
        return STATE_KEYWORD

    def process_char(self, char, nextChar):
        if self.targetKeyword == 0:
            if char == self.keywordMul[0]:
                self.targetKeyword = 1
            elif char == self.keywordDo[0]:
                self.targetKeyword = 2
            else:
                return False

        doesMatch = self.match_current_keyword(char, nextChar)
        if not doesMatch and self.targetKeyword == 2:
                self.targetKeyword = 3
                doesMatch = self.match_current_keyword(char, nextChar)
        
        if not doesMatch:
            return False
        else:
            self.expectedIndex += 1

            expectedLength = len(self.keywordMul) if self.targetKeyword == 1 else len(self.keywordDo) if self.targetKeyword == 2 else len(self.keywordDont)
            if self.expectedIndex >= expectedLength:
                if self.targetKeyword == 2:
                    self.Persistent.MaintainState = True
                    self.Persistent.ProcessStatements = True
                elif self.targetKeyword == 3:
                    self.Persistent.MaintainState = True
                    self.Persistent.ProcessStatements = False
                self.MarkFinished()

        return True
    
    def match_current_keyword(self, char, nextChar):
        match self.targetKeyword:
            case 1:
                return char == self.keywordMul[self.expectedIndex]
            case 2:
                return char == self.keywordDo[self.expectedIndex]
            case 3:
                return char == self.keywordDont[self.expectedIndex]
    
class OpenParenState(State):

    def GetStateId(self):
        return STATE_OPENPAREN

    def process_char(self, char, nextChar):
        if char == '(':
            self.MarkFinished()
            return True

        return False
    
class FirstArgState(State):
    accumulator = ''

    def GetStateId(self):
        return STATE_FIRSTARG

    def process_char(self, char, nextChar):
        if char.isdigit():
            self.accumulator += char
        else:
            return False
        
        if not nextChar.isdigit() or len(self.accumulator) == 3:
            self.Persistent.FirstArg = self.GetNumber()
            self.MarkFinished()

        return True
    
    def GetNumber(self):
        return int(self.accumulator)
    
class CommaState(State):

    def GetStateId(self):
        return STATE_COMMA

    def process_char(self, char, nextChar):
        if char == ',':
            self.MarkFinished()
            return True
        
        return False

class SecondArgState(State):
    accumulator = ''

    def GetStateId(self):
        return STATE_SECONDARG

    def process_char(self, char, nextChar):
        if char.isdigit():
            self.accumulator += char
        else:
            return False
        
        if not nextChar.isdigit() or len(self.accumulator) == 3:
            self.Persistent.SecondArg = self.GetNumber()
            self.MarkFinished()

        return True
    
    def GetNumber(self):
        return int(self.accumulator)
    
class CloseParenState(State):

    def GetStateId(self):
        return STATE_CLOSEPAREN

    def process_char(self, char, nextChar):
        if char == ')':
            self.MarkFinished()
            return True
        
        return False

def increment_state(state):
    persistent = state.Persistent
    stateFlag = state.GetStateId() + 1

    if persistent.MaintainState:
        stateFlag -= 1
        persistent.MaintainState = False

    if stateFlag == STATE_KEYWORD:
            state = KeywordState(persistent)
    if stateFlag == STATE_OPENPAREN:
            state = OpenParenState(persistent)
    elif stateFlag == STATE_FIRSTARG:
            state = FirstArgState(persistent)
    elif stateFlag == STATE_COMMA:
            state = CommaState(persistent)
    elif stateFlag == STATE_SECONDARG:
            state = SecondArgState(persistent)
    elif stateFlag == STATE_CLOSEPAREN:
            state = CloseParenState(persistent)

    return state

def reset_state(state):
    persistent = PersistentState()
    persistent.ProcessStatements = state.Persistent.ProcessStatements
    return KeywordState(persistent)

def main():
    sum = 0
    state = KeywordState(PersistentState())
    num = len(data)
    for index in range(num):
        char = data[index]
        next = '' if index >= num-1 else data[index + 1]

        success = state.process_char(char, next)
        if success is False:
            state = reset_state(state)
        elif state.Finished:
            if state.GetStateId() == STATE_CLOSEPAREN:
                shouldProcess = state.Persistent.ProcessStatements
                if shouldProcess:
                    first = state.Persistent.FirstArg
                    second = state.Persistent.SecondArg
                    sum += first * second
                state = reset_state(state)
            else:
                state = increment_state(state)

    print(sum)


main()