class language:

    def __init__(self, code):
        self.jumpLine = 0
        self.operons = ['+', '-', '*', '/']
        self.conditionals = ['>', '<', '>=', '<=', '==', '!=', 'and', 'or', 'not']
        self.codeSplitLinePos = []
        self.code = code
        self.lineToParse = 0
        self.codeSplit = []
        # code with empty lines (to keep track of call location)
        self.rawCode = []
        self.indentData = []
        self.vars = {}
        self.funcs = {}
        self.split()
        self.parse(self.rawCode)
        self.currentLine = 0

    @staticmethod
    def error(message):
        print("! " + message + " !")
        quit()

    def listVars(self):
        toList = self.vars.keys()
        toList = str(toList)
        toList = toList.replace("dict_keys([", '')
        toList = toList.replace("'", '')
        toList = toList.replace("])", '')
        print("Variables: " + toList)

    def listVarVals(self):
        toList = self.vars.values()
        toList = str(toList)
        toList = toList.replace("dict_keys([", '')
        toList = toList.replace("'", '')
        toList = toList.replace("])", '')
        print("(Work On More) Values: " + toList)

    def split(self):
        codeToSplit = self.code.split("\n")

        for i, val in enumerate(codeToSplit):
            lines = val.split("\n")

            for line in lines:

                numSpaces = len(line) - len(line.lstrip())
                if line.startswith("//"):
                    line = line.lstrip("\n")

                lineData = [line.lstrip(), i]
                
                self.indentData.append(int(numSpaces / 4))
                self.rawCode.append(lineData)

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

    # added code param, so I can choose the code to parse
    # added startLinePos to keep track of line pos in loops
    def parse(self, code):
        for task in code:

            self.currentLine = task[1] + 1
            task[0] = task[0].lstrip()
            if self.jumpLine != 0:
                self.jumpLine -= 1
            elif task[0] != "":
                # semicolons
                if task[0].endswith(";"):
                    task[0] = task[0].rstrip(";")
                # print
                if task[0].startswith("print"):
                    start_index = task[0].find("(")
                    end_index = task[0].find(")")
                    if start_index != -1 and end_index != -1:
                        # Extract content between parentheses
                        content = task[0][start_index + 1:end_index]

                        self.printUtils(content)
                # comment
                elif task[0].startswith("//"):
                    pass
                # create variables
                elif task[0].startswith("make"):
                    self.createVar(task)
                # insert var to list
                elif task[0].startswith("insert"):
                    self.insertList(task)
                # remove var from list
                elif task[0].startswith("remove"):
                    self.removeList(task)
                # replace value in list
                elif task[0].startswith("swap"):
                    self.swapList(task)
                # write to variables
                elif task[0].startswith("set"):
                    self.setVar(task)
                # delete variables (bcuz why not)
                elif task[0].startswith("del"):
                    self.delVar(task)
                # loop
                elif task[0].startswith("loop"):
                    self.loopFunc(task)
                # conditional
                elif task[0].startswith("if"):
                    self.conditional(task)
                # functions
                elif task[0].startswith("func"):
                    self.createFunction(task)
                elif task[0].startswith("call"):
                    self.callFunction(task)
                # input
                elif task[0].startswith("input"):
                    start_index = task[0].find("(")
                    end_index = task[0].find(")")
                    if start_index != -1 and end_index != -1:
                        # Extract content between parentheses
                        content = task[0][start_index + 1:end_index]
                        split = content.split(',', 1)

                        varName = split[0]

                        question = split[1]
                        question = question.replace('"', '')
                        question = question.replace(' ', '', 1)

                        varValue = input(question + "\n")

                        varToCreate = ["make " + varName + ' = "' + varValue + '"', task[1]]

                        self.createVar(varToCreate)
                # blank line
                elif task[0] == "blank()" or task[0] == "nl()" or task[0] == "el()":
                    print("")
                # debug methods
                elif task[0].startswith("rh."):
                    task[0] = task[0].replace("rh.", '')
                    self.debug(task)
                # error
                elif not task[0].isspace():
                    language.error(f"Unknown Task | Task: {task[0]} | Line: {self.currentLine}")

    def evaluateVar(self, content):
        # handling var types in python, maybe change later if feel like :|
        varType = "NaN"
        # see if it's an existing var

        if content in self.vars:
            varType = self.vars[content][1]
            content = self.vars[content][0]
            return content, varType

        if content.startswith("len:"):

            content = content.replace('len:', '', 1)
            # find index of var content using "=" char

            contentEval = self.evaluateVar(content)

            if contentEval[1] != "list":
                language.error(
                    f"List does not exist | list: {content} Type: {contentEval[0]} | Line: {self.currentLine}")
            else:
                content = len(contentEval[0])
            return content, "int"
        if content.find("/") != -1:
            forwardSlashIndex = content.index("/")
            # grab content of var (cuts at declarationIndex)
            searchIndexes = content[forwardSlashIndex + 1:].strip()

            # grab name of var (cuts before declarationIndex)
            listName = content[:forwardSlashIndex].strip()

            if listName not in self.vars:
                language.error(f"List does not exist | list: {listName} | Line: {self.currentLine}")

            listContent = self.vars[listName][0]

            searchIndexes = searchIndexes.split("/")
            searchIndexes = [self.evaluateVar(index)[0] for index in searchIndexes]

            currentVar = listContent
            currentContent = None

            for current_index in searchIndexes:

                cVar = currentVar[current_index][0]
                cContent = currentVar[current_index][1]
                currentVar = cVar
                if not isinstance(currentVar, list):
                    break

                currentContent = "list"

            content = currentVar
            varType = currentContent

            return content, varType

        if varType == "NaN" and content.startswith('[') and content.endswith(']'):

            varType = "list"
            content = content.strip()
            items = content[1:len(content) - 1]

            # looping through every char, so I can find where nested lists occur
            currentVar = ""
            listVar = []
            openBracket = False

            for i in range(len(items)):
                if openBracket:
                    if items[i - 1] == ']':
                        openBracket = False
                elif items[i] == ",":
                    listVar.append(currentVar.strip())
                    currentVar = ''
                elif items[i] == "[":
                    endBracketIndex = items.find("]")
                    if endBracketIndex != -1:
                        listVar.append(items[i:endBracketIndex + 1])
                    else:
                        language.error(f"No ']' found in nested list | Var: {content} | Line: {self.currentLine}")
                    openBracket = True

                else:
                    currentVar += items[i]
                    if i == len(items) - 1:
                        listVar.append(currentVar.strip())

            listContent = []

            for item in listVar:
                var = self.evaluateVar(item)
                listContent.append([var[0], var[1]])
            content = listContent

            return content, varType

        # str detection
        if varType == "NaN" and content.startswith('"') and content.endswith('"'):
            varType = "str"
            content = content[1:-1]
            return content, varType

        # checking if num is neg and getting rid of neg for simplicity

        if varType == "NaN" and content.count('.') == 1:
            varType = "float"
            if content.startswith('-') and content[1:].isdigit():
                content = content.replace('-', '')
                isNeg = True
            else:
                isNeg = False
            if isNeg:
                content = '-' + content
            content = float(content)
            return content, varType

        if varType == "NaN" and content.isdigit():
            varType = "int"
            if content.startswith('-') and content[1:].isdigit():
                content = content.replace('-', '')
                isNeg = True
            else:
                isNeg = False

            if isNeg:
                content = '-' + content
            content = int(content)
            return content, varType

        if varType == "NaN":
            language.error(f"Var type NaN | Var: {content} | Line: {self.currentLine}")

        return content, varType

    def createVar(self, task):
        taskContent = task[0]

        taskContent = taskContent.replace('make', '', 1)
        # find index of var content using "=" char

        declarationIndex = taskContent.index("=")
        # grab content of var (cuts at declarationIndex)
        varContent = taskContent[declarationIndex + 1:].strip()
        # grab name of var (cuts before declarationIndex)
        varName = taskContent[:declarationIndex].strip()

        if varContent.startswith("calc"):
            self.vars[varName] = self.calcVar(varContent)
        else:
            varEval = self.evaluateVar(varContent)
            self.vars[varName] = varEval

    # write existing variable to new val
    def setVar(self, task):
        # again letting python handle the operation :(
        taskContent = task[0]
        taskContent = taskContent.replace('set', '', 1)
        # find index of var content using "=" char
        declarationIndex = taskContent.index("=")
        # grab content of var (cuts at declarationIndex)
        varContent = taskContent[declarationIndex + 1:].strip()
        # grab name of var (cuts before declarationIndex)
        varName = taskContent[:declarationIndex].strip()

        if not (varName in self.vars):
            language.error(f"Var does not exist | Var: {varName} | Line: {self.currentLine}")

        if varContent.startswith("calc"):
            self.vars[varName] = self.calcVar(varContent)
        else:
            varEval = self.evaluateVar(varContent)
            self.vars[varName] = varEval

    def delVar(self, task):
        taskContent = task[0]
        taskContent = taskContent.replace('del ', '', 1)

        try:
            del self.vars[taskContent]
        except KeyError:
            language.error(f"Var does not exist | Var: {taskContent} | Line: {self.currentLine}")

    def createFunction(self, task):
        name = task[0]
        name = name.replace('func ', '', 1)
        pIndex = name.find("(")
        name = name[:pIndex]

        start_index = task[0].find("(")
        end_index = task[0].find(")")
        params = None
        if start_index != -1 and end_index != -1:
            # Extract content between parentheses
            params = task[0][start_index + 1:end_index]
        else:
            language.error(f"Syntax Error | Function: {task[0]} | Line: {self.currentLine}")
        params = params.split(",")
        params = [param.strip() for param in params]

        funcCode = []
        for line in self.rawCode[self.currentLine:]:

            if self.indentData[line[1]] > self.indentData[self.currentLine - 1]:
                funcCode.append(line)
            else:
                break


        self.funcs[name] = [funcCode, params]

        self.jumpLine += len(funcCode)

    def callFunction(self, task):
        name = task[0]
        name = name.replace('call ', '', 1)
        pIndex = name.find("(")
        name = name[:pIndex]

        start_index = task[0].find("(")
        end_index = task[0].find(")")
        params = None
        if start_index != -1 and end_index != -1:
            # Extract content between parentheses
            params = task[0][start_index + 1:end_index]
        else:
            language.error(f"Syntax Error | Function: {task[0]} | Line: {self.currentLine}")
        params = params.split(",")
        params = [param.strip() for param in params]

        if len(params) != len(self.funcs[name][1]):
            language.error(f"Parameter Error | Function: {task[0]} | Line: {self.currentLine}")

        for i, param in enumerate(params):
            self.vars[self.funcs[name][1][i]] = self.evaluateVar(param)

        self.parse(self.funcs[name][0])

        for i, param in enumerate(params):
            del self.vars[self.funcs[name][1][i]]

    def insertList(self, task):
        taskContent = task[0]

        taskContent = taskContent.replace('insert', '', 1)
        # find index of var content using "=" char

        forwardSlashIndex = taskContent.index("/")
        colinIndex = taskContent.index(":")
        # grab content of var (cuts at declarationIndex)
        searchIndexes = taskContent[forwardSlashIndex + 1:colinIndex].strip()
        valueToInsert = taskContent[colinIndex + 1:].strip()
        valueToInsert = self.evaluateVar(valueToInsert)

        # grab name of var (cuts before declarationIndex)
        listName = taskContent[:forwardSlashIndex].strip()

        if listName not in self.vars:
            language.error(f"List does not exist | list: {listName} | Line: {self.currentLine}")

        searchIndexes = searchIndexes.split("/")
        searchIndexes = [self.evaluateVar(index)[0] for index in searchIndexes]

        # Initialize the variable to hold the current nested list
        subList = self.vars[listName][0]
        # Iterate through each index in the search_indices except the last one
        for index in searchIndexes[:-1]:
            # Update the result to be the sublist at the current index
            subList = subList[index]

        # Append the value_to_append to the sublist at the last index in search_indices
        subList.insert(searchIndexes[-1], valueToInsert)

    def removeList(self, task):
        taskContent = task[0]

        taskContent = taskContent.replace('remove', '', 1)
        # find index of var content using "=" char

        forwardSlashIndex = taskContent.index("/")
        # grab content of var (cuts at declarationIndex)
        searchIndexes = taskContent[forwardSlashIndex + 1:].strip()

        # grab name of var (cuts before declarationIndex)
        listName = taskContent[:forwardSlashIndex].strip()

        if listName not in self.vars:
            language.error(f"List does not exist | list: {listName} | Line: {self.currentLine}")

        searchIndexes = searchIndexes.split("/")

        searchIndexes = [self.evaluateVar(index)[0] for index in searchIndexes]

        # Initialize the variable to hold the current nested list
        subList = self.vars[listName][0]
        # Iterate through each index in the search_indices except the last one
        for index in searchIndexes[:-1]:
            # Update the result to be the sublist at the current index
            subList = subList[index]

        # Append the value_to_append to the sublist at the last index in search_indices
        del subList[searchIndexes[-1]]

    def swapList(self, task):
        taskContent = task[0]

        taskContent = taskContent.replace('swap', '', 1)
        # find index of var content using "=" char

        forwardSlashIndex = taskContent.index("/")
        colinIndex = taskContent.index(":")
        # grab content of var (cuts at declarationIndex)
        searchIndexes = taskContent[forwardSlashIndex + 1:colinIndex].strip()
        valueToSwap = taskContent[colinIndex + 1:].strip()
        valueToSwap = self.evaluateVar(valueToSwap)

        # grab name of var (cuts before declarationIndex)
        listName = taskContent[:forwardSlashIndex].strip()

        if listName not in self.vars:
            language.error(f"List does not exist | list: {listName} | Line: {self.currentLine}")

        searchIndexes = searchIndexes.split("/")
        searchIndexes = [self.evaluateVar(index)[0] for index in searchIndexes]

        # Initialize the variable to hold the current nested list
        subList = self.vars[listName][0]
        # Iterate through each index in the search_indices except the last one
        for index in searchIndexes[:-1]:
            # Update the result to be the sublist at the current index
            subList = subList[index]

        # Append the value_to_append to the sublist at the last index in search_indices
        subList[searchIndexes[-1]] = valueToSwap

    def loopFunc(self, task):
        taskContent = task[0]
        taskContent = taskContent.replace('loop', '', 1)
        declarationIndex = taskContent.index(",")
        # grab content of var (cuts at declarationIndex)
        loopLength = taskContent[declarationIndex + 1:].strip()

        # grab name of var (cuts before declarationIndex)
        indexName = taskContent[:declarationIndex].strip()
        # create a new index var, so it can be used in the loop
        loopLength = self.evaluateVar(str(loopLength))
        if loopLength[1] != "int":
            language.error(f"loop length not int | Var: {indexName} | Line: {self.currentLine}")

        self.vars[indexName] = [0, "int"]
        # all the lines of code between the loop
        loopCode = []
        for line in self.rawCode[self.currentLine:]:
            if self.indentData[line[1]] > self.indentData[self.currentLine - 1]:
                loopCode.append(line)
            else:
                break

        for i in range(loopLength[0]):
            self.vars[indexName] = [i, "int"]
            self.parse(list(loopCode))
        del self.vars[indexName]
        # delete the index var after loop is over

        self.jumpLine = len(loopCode)

    def calcVar(self, content):
        content = content.replace('calc', '', 1)
        c_content = content

        usedOperons = []

        for i, char in enumerate(content.strip()):

            if char in self.operons:
                usedOperons.append(char)
                c_content = c_content.replace(char, "~")

        splitString = (c_content.strip()).split(" ~ ")

        operationList = []
        for i in range(len(splitString)):
            operationList.append(str(splitString[i]))
            if i != len(splitString) - 1:
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
                result = float(result)
        except SyntaxError:
            language.error(f"Calc syntax error | Expression: {operation} | Line: {self.currentLine}")

        return self.evaluateVar(str(result))

    def printUtils(self, content):
        # Make List
        content = content.split("+")
        content = [item.strip() for item in content]

        contentEval = []
        for item in content:
            itemEval = self.evaluateVar(item)
            if itemEval[1] == "list":
                newItem = [listItem[0] for listItem in itemEval[0]]
                contentEval.append(str(newItem))
            else:
                contentEval.append(str(self.evaluateVar(item)[0]))
        result = ''.join(contentEval)
        print(result)


    def debug(self, task):
        taskContent = task[0]
        if taskContent.startswith("variables."):
            taskContent = taskContent.replace("variables.", '')
            if taskContent == "list()":
                self.listVars()
            elif taskContent.startswith("list("):
                taskContent = taskContent.replace('list(', '')
                taskContent = taskContent.replace(')', '')
                language.error(
                    f'"rh.variables.list()" does not take any arguments | Argument: "{taskContent}" | Line: {self.currentLine}')
            elif taskContent == "values()":
                self.listVarVals()
            elif taskContent.startswith("values("):
                taskContent = taskContent.replace('values(', '')
                taskContent = taskContent.replace(')', '')
                language.error(
                    f'"rh.variables.values()" does not take any arguments | Argument: "{taskContent}" | Line: {self.currentLine}')
        elif taskContent.startswith("error("):
            start_index = taskContent.find("(")
            end_index = taskContent.find(")")
            if start_index != -1 and end_index != -1:
                # Extract content between parentheses
                content = taskContent[start_index + 1:end_index]

                content = content.replace('"', '')

                language.error(content)
        else:
            language.error(f'Unknown function in "rh" | Expression: {taskContent} | Line: {self.currentLine}')

    def conditional(self, task):
        content = task[0].replace('if', '', 1)

        splitContent = list(content.split(" "))

        splitContent = [i for i in splitContent if i]

        for i in range(len(splitContent)):
            if splitContent[i] in self.conditionals:
                splitContent[i] = str(" " + splitContent[i] + " ")
            elif splitContent[i] in self.vars.keys():
                splitContent[i] = str(self.vars[splitContent[i]][0])
        operators = ['>', '<', '>=', '<=', '==', '!=']
        newContent = []
        for item in splitContent:
            if item.strip() not in operators:

                newContent.append(str(self.evaluateVar(item.strip())[0]))
            else:
                newContent.append(item)

        modContent = ''.join(newContent)
        doCondition = eval(str(modContent))
        conCode = []
        for line in self.rawCode[self.currentLine:]:
            if self.indentData[line[1]] > self.indentData[self.currentLine - 1]:
                conCode.append(line)
        if doCondition:
            self.parse(list(conCode))
        self.jumpLine = len(conCode)
