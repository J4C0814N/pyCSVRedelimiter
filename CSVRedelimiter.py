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
				for line in csvFile:
					#Remove newlines from quoted text:
					cleanLine = line.replace("\n", "").replace("\r", "")
					#Split line in to a set of characters
					lineChars = list(cleanLine)
					inQuotes = False #Because we will always start in an unquoted context.
					charNum = len(lineChars)
					i = 0
					print(line)
					print("".join(lineChars))
					while (i < charNum):
						
						if lineChars[i] == initialChar and not inQuotes:
							print("#### Replacing delimiter")
							lineChars[i] = replaceChar
						if lineChars[i] == '"':
							print("#### Found quotes")
							if not inQuotes:
								if removeQuotes:
									lineChars[i] = ''
								inQuotes = True
							elif inQuotes:
								if removeQuotes:
									lineChars[i] = ''
								inQuotes = False

						i += 1

					fixedcsv.write("".join(lineChars)+"\n")
		print(os.path.basename(fname)+" Done")

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

if __name__ == '__main__':
	main()