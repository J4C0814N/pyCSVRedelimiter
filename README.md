# pyCSVRedelimiter
Updates the delimiter of all CSV files in a directory.

Originally built to solve a specific problem, where a database could only be exported as a comma delimited CSV with columns containing commas surrounded with quotes:

```
1,Some text,"Sentence, with a comma",More text, -- 4 columns
```

The issue is that SQL Server `BULK INSERT` does not recognise the quotes and in the above example would try to populate 5 columns and error.

## Usage
1. Place CSVRedelimiter.py in folder with the CSV file(s)
2. Create the output directory (Default: ./Fixed)
3. Run `python3 CSVRedelimiter.py -d "," -r "^" -s "fixed" -k`
4. OR - Update variables to meet your needs
    * `initialChar` - Character you want replaced 
    * `replaceChar` - Character to replace with
    * `removeQuotes` - True to also remove quotes, False keeps quotes
    * `savePath` - The directory to save the updated CSV(s) to. Must exist before running
    * `dateFormat` - The date format for any date values in the csv
    * `dateFormatRegex` - The regex equivalent of `dateFormat` used to find all instances of the date to replace
    * `sqlDateFormat` - The date format accepted by the database or destination 
    * `fixDates` - True to convert any content matching `dateFormat` to `sqlDateFormat`

4. Run `python CSVRedelimiter.py`

Originally developed by [@Rollinginsanity](https://github.com/rollinginsanity), extended by me.
