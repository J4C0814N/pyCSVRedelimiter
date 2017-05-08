import os
import glob
path = "./*.csv"

initialChar = ","
replaceChar = "|"
removeQuotes = True
savePath = "./fixed/" #Directory currently needs to exist first

for fname in glob.glob(path):
	print(os.path.basename(fname))
	with open(fname) as csvFile:
		with open(savePath+fname, 'w') as fixedcsv:
			for line in csvFile:
				#Split line in to a set of characters
				lineList = list(line)

				notInQuotes = True #Because we will always start in an unquoted context.

				charNum = len(lineList)

				i = 0

				while (i < charNum):
					if lineList[i] == initialChar and notInQuotes:
						lineList[i] = replaceChar

					if lineList[i] == '"':
						if notInQuotes:
							if removeQuotes:
								lineList[i] = ''
							notInQuotes = False
						elif not notInQuotes:
							if removeQuotes:
								lineList[i] = ''
							notInQuotes = True

					i += 1

				print("".join(lineList))
				fixedcsv.write("".join(lineList))

	
