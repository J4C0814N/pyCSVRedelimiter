import os

replaceChar = "|"

with open("test.csv") as csvFile:
    for line in csvFile:
        #Split line in to a set of characters
        lineList = list(line)

        notInQuotes = True #Because we will always start in an unquoted context.

        charNum = len(lineList)

        i = 0

        while (i < charNum):
            if lineList[i] == "," and notInQuotes:
                lineList[i] = replaceChar

            if lineList[i] == '"':
                if notInQuotes:
                    notInQuotes = False
                elif not notInQuotes:
                    notInQuotes = True

            i += 1

        print("".join(lineList))
