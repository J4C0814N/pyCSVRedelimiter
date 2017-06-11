import os
import csv
import glob
path = "./*.csv"

#Some defaults.
initialChar = ","
replaceChar = "|"
removeQuotes = True
savePath = "./fixed/" 
tempString = "temp_"

def main():

	create_save_dir(savePath)

	for fname in glob.glob(path):
		print("Processing "+os.path.basename(fname))
		#Remove any additional line breaks that appear in quoted text
		tempFile = savePath+tempString+os.path.basename(fname)
		with open(fname, "rb") as input, open(savePath+tempString+os.path.basename(fname), "wb") as output:
			w = csv.writer(output)
			for record in csv.reader(input):
				w.writerow(tuple(s.replace("\r\n","") for s in record))
			
		with open(tempFile) as csvFile:
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

					fixedcsv.write("".join(lineList))
		print(os.path.basename(fname)+" Done")
		os.remove(tempFile)

#Create our save directory.
def create_save_dir(savePath):
	if not os.path.exists(savePath):
		os.makedirs(savePath)

if __name__ == '__main__':
	main()