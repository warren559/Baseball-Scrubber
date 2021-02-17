""" Extract GUID’s, Pitch types and Pitcher handedness  from Baseball data (based on predefined rules ).
 Output the GUID’s, Pitch types, Pitcher handedness and Rules broken in  a csv file for further analysis"""

import pandas as pd
from tkinter import filedialog as fd
import xlrd
import csv
import os

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# gets the filename to be scrubbed
fileName = fd.askopenfilename(initialdir=r"\\filestore\home\Warren Schilder\Python\FS Baseball Scrubber\Baseball Exports")

# check if the file selected in the file dialog box is a csv file or xlsx file
if fileName.split("/")[-1][-3:] == "csv":
	df = pd.read_csv(fileName)
else:
	# Convert the xlsx file into a csv file 
	wb = xlrd.open_workbook(fileName)
	sheets = wb.sheet_names()
	sh = wb.sheet_by_name(sheets[0])

	basename = os.path.basename(fileName)[:-5]

	output_file = basename + '.csv'
	print("output_file")
	print(output_file)

	your_csv_file = open(output_file , 'w', encoding="utf-8")
	wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

	for rownum in range(sh.nrows):
	    wr.writerow(sh.row_values(rownum))
	your_csv_file.close()

	# converts csv file to pandas dataframe
	df = pd.read_csv(output_file)


rules = {
	"1" : "1",
	"2" : "2",
	"3" : "3",
	"4" : "4",
	"5" : "5",
	"6" : "6"
}

# list containing six dataframes - each dataframe filtered on the six predefined rules 
li= [(df.Pitch_Type.str.contains('FF', case=False) | df.Pitch_Type.str.contains('FT', case=False) | df.Pitch_Type.str.contains('CH', case=False) | df.Pitch_Type.str.contains('SP', case=False) ) & (df.Pitcher_Hand.str.contains('L') | df.Pitcher_Hand.str.contains('R')) & (df['pfxz'] < 0),
(df.Pitch_Type.str.contains('CU', case=False)) & (df.Pitcher_Hand.str.contains('L') | df.Pitcher_Hand.str.contains('R')) & (df['pfxz'] > 0),
(df.Pitch_Type.str.contains('FF', case=False) | df.Pitch_Type.str.contains('FT', case=False) | df.Pitch_Type.str.contains('CH', case=False) | df.Pitch_Type.str.contains('SP', case=False) ) & (df.Pitcher_Hand.str.contains('L')) & (df['pfxx'] < 0),
(df.Pitch_Type.str.contains('FF', case=False) | df.Pitch_Type.str.contains('FT', case=False) | df.Pitch_Type.str.contains('CH', case=False) | df.Pitch_Type.str.contains('SP', case=False)) & (df.Pitcher_Hand.str.contains('R')) & (df['pfxx'] > 0),
(df.Pitch_Type.str.contains('CU', case=False)) & (df.Pitcher_Hand.str.contains('L')) & (df['pfxx'] > 0),
(df.Pitch_Type.str.contains('CU', case=False)) & (df.Pitcher_Hand.str.contains('R')) & (df['pfxx'] < 0)]

# for each of the six dataframes create smaller dataframes ( with only Pitch_Type,Pitcher_Hand,GUID, Rule Broken columns)
for i in range(len(li)):
	df1 = df[li[i]]

	if df1.empty:
		pass
	else:
		ruleID = df1[['Pitch_Type','Pitcher_Hand','GUID']]
		ruleID.name = str(i + 1)
		one_li = []
		for i in range(len(ruleID)):
			one_li.append(rules[ruleID.name])
		ruleID['Rule'] = one_li
		# convert the newly generated dataframes into csv file 
		ruleID.to_csv("output.csv", mode="a", header=False, index=False)


with open("output.csv",newline='') as f:
    r = csv.reader(f)
    data = [line for line in r]
with open("output.csv",'w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['Pitch_Type','Pitcher_Hand','GUID','Rule_Broken']) # add column headers to csv file 
    w.writerows(data)