from xlrd import open_workbook
from re import sub, findall
from tkinter.filedialog import askopenfilename
from random import randint
from os import getcwd, path, makedirs

if not path.exists('output'):
    makedirs('output')

series_name = input("Enter series name: ")
filename = askopenfilename()
source_filepath = filename
filename = path.basename(source_filepath)
filename = filename[0: filename.rfind('.')]
output_dir = getcwd() + "/output/"
random = randint(1, 2500)

file_source = open(source_filepath)
file_output = open(output_dir + f"/{filename}-regex_{random}.txt", "a")

source_text = file_source.readlines()
source_text = ' '.join(source_text)

modified_text = ''

find = []
replace = []
count = []

wb = open_workbook(getcwd() + "/src/Glossary.xlsx")
ws = wb.sheet_by_name(series_name)

rows = ws.get_rows()
next(rows)

for row in rows:
    find.append(row[0].value)
    replace.append(row[1].value)
i = 0
for item in zip(find, replace):
    x = findall(item[0], source_text)
    i+=1
    print(i, len(x), item[0], item[1])
    source_text = sub(item[0], item[1], source_text)

file_output.write(source_text)


