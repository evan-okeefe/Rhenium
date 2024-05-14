class language:

    def __init__(self, code):
        self.operons = ['+', '-', '*', '/']
        self.codeSplitLinePos = []
        self.code = code
        self.lineToParse = 0
        self.codeSplit = []
        self.vars = {}
        self.split()
        self.clean()
        self.parse()
        self.currentLine = 0

    @staticmethod
    def error(message):
        print("! " + message + " !")
        quit()

    def debug(self):
        print(self.vars)

    def split(self):
        codeToSplit = self.code.split(";")
        for val in codeToSplit:
            lines = val.split("\n")
            for line in lines:
                if line.startswith("//"):
                    line = line.lstrip("\n")
                    self.codeSplit.extend(line.split(";"))
                else:
                    self.codeSplit.append(line)

    def clean(self):
        codeToClean = self.codeSplit
        cleanedCode = []
        # keeping track of line pos for debug
        cleanedCodeLinePos = []

        for val in range(len(codeToClean)):
            if codeToClean[val] != '':
                cleanedCode.append(codeToClean[val])
                cleanedCodeLinePos.append(val + 1)
        self.codeSplit = cleanedCode
        self.codeSplitLinePos = cleanedCodeLinePos

    def parse(self):

        for i, task in enumerate(self.codeSplit):
            self.currentLine = self.codeSplitLinePos[i]
            # print
            if task.startswith("print"):
                start_index = task.find("(")
                end_index = task.find(")")
                if start_index != -1 and end_index != -1:
                    # Extract content between parentheses
                    content = task[start_index + 1:end_index]

                    self.printUtils(content)
            # comment
            # elif task.startswith("//"):
            #     print(f"comment at line: {self.currentLine}")
            # variables
            elif task.startswith("var"):
                self.createVar(task)
            # write to variables
            elif task.startswith("write"):
                self.writeToVar(task)

    def evaluateVar(self, content):
        # handling var types in python, maybe change later if feel like :|
        varType = "NaN"
        # see if it's an existing var
        if content in self.vars:
            varType = self.vars[content][1]
            content = self.vars[content][0]

        # str detection
        if varType == "NaN" and content.startswith('"') and content.endswith('"'):
            varType = "str"
            content = content[1:-1]

        # checking if num is neg and getting rid of neg for simplicity
        if varType == "NaN" and content.startswith('-') and content[1:].isdigit():
            content = content.replace('-', '')
            isNeg = True
        else:
            isNeg = False

        if varType == "NaN" and content.count('.') == 1:
            varType = "float"
            if isNeg:
                content = '-' + content
            content = float(content)

        if varType == "NaN" and content.isdigit():
            varType = "int"
            if isNeg:
                content = '-' + content
            content = int(content)

        if varType == "NaN":
            return "error"

        return content, varType

    def createVar(self, task):

        task = task.replace('var', '', 1)
        # find index of var content using "=" char
        declarationIndex = task.index("=")
        # grab content of var (cuts at declarationIndex)
        varContent = task[declarationIndex + 1:].strip()
        # grab name of var (cuts before declarationIndex)
        varName = task[:declarationIndex].strip()

        varEval = self.evaluateVar(varContent)
        if varEval == "error":
            language.error(f"Incorrect var declaration | Var: {varName} | Line: {self.currentLine}")
        # creating var key in vars dictionary
        self.vars[varName] = varEval

    # write existing variable to new val
    def writeToVar(self, task):
        # again letting python handle the operation :(

        task = task.replace('write', '', 1)
        # find index of var content using "=" char
        declarationIndex = task.index("=")
        # grab content of var (cuts at declarationIndex)
        varContent = task[declarationIndex + 1:].strip()
        # grab name of var (cuts before declarationIndex)
        varName = task[:declarationIndex].strip()


        if not (varName in self.vars):
            language.error(f"Var does not exist | Var: {varName} | Line: {self.currentLine}")

        if varContent.startswith("calc"):
            self.vars[varName] = self.calcVar(varContent)
        else:
            varEval = self.evaluateVar(varContent)
            self.vars[varName] = varEval

    def calcVar(self, content):
        content = content.replace('calc', '', 1)
        c_content = content
        splitContent = []
        usedOperons = []

        for i, char in enumerate(content.strip()):

            if char in self.operons:
                usedOperons.append(char)
                c_content = c_content.replace(char, "~")


        splitString = (c_content.strip()).split(" ~ ")

        operationList = []
        for i in range(len(splitString)):
            operationList.append(str(splitString[i]))
            if i != len(splitString)-1:
                operationList.append(str(usedOperons[i]))
        valueList = []
        for item in operationList:
            if not (item in self.operons):
                itemEval = self.evaluateVar(item)
                if itemEval[1] == "str":
                    language.error(f"Can't use str in 'calc' operation | Value: {item} | Line: {self.currentLine}")
                valueList.append(str(itemEval[0]))
            else:
                valueList.append(item)

        operation = ' '.join(valueList)

        try:
            result = eval(operation)
            if result == int(result):
                result = int(result)
            else:
                result = float_value
        except SyntaxError:
            language.error(f"Calc syntax error | Expression: {operation} | Line: {self.currentLine}")

        return self.evaluateVar(str(result))

    def printUtils(self, content):
        # Make List
        contentAsList = []
        for element in range(0, len(content)):
            contentAsList.append(content[element])
        # Create Item To Print
        value = ""
        insideQuotes = False
        variable = False
        tempString = ""
        variableName = ''

        for char in contentAsList:
            if char == '"':
                if insideQuotes:
                    insideQuotes = False
                else:
                    insideQuotes = True

            if char == "{":
                variable = True
            elif char == "}":
                variable = False

            if variable:
                if char == '{' or char == '}':
                    pass
                else:
                    variableName += char
            elif not (variable):
                if variableName == '':
                    if char == ' ' and not (insideQuotes):
                        pass
                    elif char == '+' and not (insideQuotes):
                        tempString += ' '
                    elif char == ',' and not (insideQuotes):
                        tempString += ''
                    elif char == '"':
                        pass
                    elif not (char.isnumeric()) and not (insideQuotes):
                        print(tempString)
                        print(char)
                        print(insideQuotes)
                        self.error(f"String outside of quotation marks | Line: {self.currentLine}")
                    else:
                        tempString += char
                else:

                    tempString += str(self.vars[variableName][0])
                    variableName = ''
        value += tempString

        print(value)
