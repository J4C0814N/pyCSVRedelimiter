import os
import csv
import glob
import shutil

path = "./*.csv"
#Some defaults.
initialChar = ","
replaceChar = "|"
removeQuotes = False
savePath = "./fixed/" 

def main():
	print("#### Checking output directory exists.")
	create_save_dir(savePath)
	print(glob.glob(path))
	print("#### Checking for .csv files.")
	for fname in glob.glob(path):
		print("#### Got: "+fname)
		print("#### Processing "+os.path.basename(fname))
		#Remove any additional line breaks that appear in quoted text

		with open(fname) as csvFile:
			with open(savePath+fname, 'w') as fixedcsv:
				lineNumber = 1 #Line counter for output.

				#Fix out lines.
				for line in csvFile:
					fixedcsv.write(fix_line(line, lineNumber))
					lineNumber += 1

		print(os.path.basename(fname)+" Done")

#######Functions are down here.

#Fix a line of our delimited file:
def fix_line(line, lineNumber=0):
	#Remove newlines from quoted text:
	cleanLine = line.replace("\n", "").replace("\r", "")
	#Split line in to a set of characters
	lineChars = list(cleanLine)
	inQuotes = False #Because we will always start in an unquoted context.
	charNum = len(lineChars)
	i = 0
	while (i < charNum):
		#If we find a comma AND we're not inside quotes, replace away!
		if lineChars[i] == initialChar and not inQuotes:
			print("#### Replacing delimiter at character "+str(i+1)+" on line "+str(lineNumber))
			lineChars[i] = replaceChar
		#If we find quotes, we flip-flop.
		if lineChars[i] == '"':
			print("#### Found quotes at character "+str(i+1)+" on line "+str(lineNumber))
			#If we're not already in quotes, we are now entering a quoted string (inQuotes = True)
			if not inQuotes:
				if removeQuotes:
					print("#### Remove quote at character "+str(i+1)+" on line "+str(lineNumber))
					lineChars[i] = ''
				inQuotes = True
			#IF we're in quotes, and we hit '"', then we're at the end of a quoted string, 
			#or we're effed, because we're in a string with multiples of the same quotes.
			#If that's the case, go fix your source data first.
			elif inQuotes:
				if removeQuotes:
					print("#### Remove quote at character "+str(i+1)+" on line "+str(lineNumber))
					lineChars[i] = ''
				inQuotes = False
		
		#If you forget to increment, it doesn't end nice.
		i += 1
	#Return the fixed string.
	return "".join(lineChars)+"\n"
		

#Create our save directory.
def create_save_dir(savePath):

	if os.path.exists(savePath):
		print("#### Found exsiting directory "+savePath+", deleting all contents..")
		shutil.rmtree(savePath)
		os.makedirs(savePath)
	else:
		#No directory found.
		print("#### Creating output directory.")
		os.makedirs(savePath)

###### Let this bad boy run!

if __name__ == '__main__':
	main()