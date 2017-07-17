import os
import csv
import glob
import shutil
import argparse
import datetime
import re

parser = argparse.ArgumentParser(description="Fixes quotes and delimeters in files.")
parser.add_argument('-d', '--delimiter', dest="currentDelimiter", help="The current delimiter in your file.")
parser.add_argument('-df', '--date-format', dest="dateFormat",
					help="The current date format, will be converted to MSSQL format (implies -fd).")
parser.add_argument('-fd', '--fix-dates', dest="store_true", help="Fix dates?")
parser.add_argument('-r', '--replacement-delimiter', dest="newDelimiter", help='The new delimiter you want to use.')
parser.add_argument('-s', '--save-path', dest="savePath", help="The output path to save updated files in.")
parser.add_argument('-k', '--kill-quotes', dest="removeQuotes", action="store_true", help="Remove quotes from strings.")
args = parser.parse_args()
path = "./*.csv"

# Some defaults.
initialChar = ","
replaceChar = "|"
removeQuotes = False
savePath = "./fixed/"
dateFormat = "%d/%m/%Y"
sqlDateFormat = "%d/%b/%Y"
fixDates = False

if args.currentDelimiter: initialChar = args.currentDelimiter
if args.newDelimiter: replaceChar = args.newDelimiter
if args.savePath: savePath = "./" + args.savePath + "/"
if args.removeQuotes: removeQuotes = args.removeQuotes
if args.dateFormat:
	dateFormat = args.dateFormat
	fixDates = True


def main():
	print("#### Configured with")
	print("--- Current delimiter: " + initialChar)
	print("--- New delimiter: " + replaceChar)
	print("--- Save path: " + savePath)
	print("--- Kill Quotes: " + str(removeQuotes))
	print("#### Checking output directory exists.")
	create_save_dir(savePath)
	print(glob.glob(path))
	print("#### Checking for .csv files.")
	for fname in glob.glob(path):
		print("#### Got: " + fname)
		print("#### Processing " + os.path.basename(fname))
		# Remove any additional line breaks that appear in quoted text

		with open(fname) as csvFile:
			with open(savePath + fname, 'w') as fixedcsv:
				lineNumber = 1  # Line counter for output.

				# Fix out lines.
				for line in csvFile:
					if fixDates:
						try:
							line = re.sub(r'\d{2}/\d{2}/\d{4}', fix_date, line)
						except:
							print("Invalid Date")
							line = line
					fixedcsv.write(fix_line(line, lineNumber))
					lineNumber += 1

		print(os.path.basename(fname) + " Done")


####### Functions are down here.

def fix_date(rem):
	date_string = rem.group()
	return datetime.datetime.strptime(date_string, dateFormat).strftime(sqlDateFormat)


# Fix a line of our delimited file:
def fix_line(line, lineNumber=0):
	# Remove newlines from quoted text:
	cleanLine = line.replace("\n", "").replace("\r", "")
	# Split line in to a set of characters
	lineChars = list(cleanLine)
	inQuotes = False  # Because we will always start in an unquoted context.
	charNum = len(lineChars)
	i = 0
	while (i < charNum):
		# If we find a comma AND we're not inside quotes, replace away!
		if lineChars[i] == initialChar and not inQuotes:
			print("#### Replacing delimiter at character " + str(i + 1) + " on line " + str(lineNumber))
			lineChars[i] = replaceChar
		# If we find quotes, we flip-flop.
		if lineChars[i] == '"':
			print("#### Found quotes at character " + str(i + 1) + " on line " + str(lineNumber))
			# If we're not already in quotes, we are now entering a quoted string (inQuotes = True)
			if not inQuotes:
				if removeQuotes:
					print("#### Remove quote at character " + str(i + 1) + " on line " + str(lineNumber))
					lineChars[i] = ''
				inQuotes = True
			# IF we're in quotes, and we hit '"', then we're at the end of a quoted string,
			# or we're effed, because we're in a string with multiples of the same quotes.
			# If that's the case, go fix your source data first.
			elif inQuotes:
				if removeQuotes:
					print("#### Remove quote at character " + str(i + 1) + " on line " + str(lineNumber))
					lineChars[i] = ''
				inQuotes = False

		# If you forget to increment, it doesn't end nice.
		i += 1
	# Return the fixed string.
	return "".join(lineChars) + "\n"


# Create our save directory.
def create_save_dir(savePath):
	if os.path.exists(savePath):
		print("#### Found existing directory " + savePath + ", deleting all contents..")
		shutil.rmtree(savePath)
		os.makedirs(savePath)
	else:
		# No directory found.
		print("#### Creating output directory.")
		os.makedirs(savePath)


###### Let this bad boy run!

if __name__ == '__main__':
	main()