class language:
    def __init__(self, code):
        self.code = code
        self.lineToParse = 0
        self.codeSplit = []
        self.vars = {}
        self.split()
        self.clean()
        self.parse()

    def error(self, message):
        print("!!!" + message + "!!!")
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
        for val in range(len(codeToClean)):
            if codeToClean[val] != '':
                cleanedCode.append(codeToClean[val])
        self.codeSplit = cleanedCode
        
    def parse(self):
        for task in self.codeSplit:
            #print
            if task.startswith("print"):
                start_index = task.find("(")
                end_index = task.find(")")
                if start_index != -1 and end_index != -1:
                    # Extract content between parentheses
                    content = task[start_index + 1:end_index]
                    self.printUtils(content)
            #comment
            elif task.startswith("//"):
                print("comment")
            #variables
            elif task.startswith("let"):
                self.createVar(task)
    
    def printUtils(self, content):
        #Make List
        contentAsList = []
        for element in range(0, len(content)):
            contentAsList.append(content[element])
        
        #Create Item To Print
        value = ""
        insideQuotes = False
        variable = False
        tempString = ""
        variableName = ""
        
        for char in contentAsList:
            if char == '"':
                if insideQuotes:
                    insideQuotes = False
                else:
                    insideQuotes = True
            elif char == ' ' and not(insideQuotes):
                pass
            elif char == '+' and not(insideQuotes):
                tempString += ' '
            elif char == ',' and not(insideQuotes):
                tempString += ' '
            elif not(char.isnumeric()) and not(insideQuotes):
                self.error("string outside of quotation marks")
            else:
                tempString += char
        value += tempString
        
        print(value)
    
    def createVar(self, line):
        line = line.replace('let', '', 1)
        
        codeToClean = line
        cleanedCode = []
        for val in range(len(codeToClean)):
            if codeToClean[val] != ' ':
                cleanedCode.append(codeToClean[val])
        line = ''
        for char in cleanedCode:
            line += char
        
        mid = line.find("=")
        
        name = line[0 : mid]
        value = line[mid + 1 : len(line)]
        
        if value == 'true':
            value = True
        elif value == 'false':
            value = False
        elif '-' in value or value.isnumeric():
            value = int(value)
        elif '.' in value and not('"' in value):
            value = float(value)
        elif value.startswith("["):
            value = "LIST (DO LATER)"
        
        self.vars[name] = value