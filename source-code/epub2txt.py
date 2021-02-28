from abc import ABC
from zipfile import ZipFile
from os import getcwd, path, makedirs
from html.parser import HTMLParser
from tkinter.filedialog import askopenfilename
from random import randint

if not path.exists('output'):
    makedirs('output')

filename = askopenfilename()
filepath = filename
fileBaseName = path.basename(filepath)
fileBaseName = fileBaseName[0: fileBaseName.rfind('.')]

textFiles = []
textContents = []

output_dir = getcwd() + "/output/"
output_file = f"{output_dir}{fileBaseName}-src_{randint(0, 2500)}.txt"

outfile = open(output_file, 'a')


class HTMLFilter(HTMLParser, ABC):
    text = ""

    def handle_data(self, data):
        self.text += data


with ZipFile(filepath, 'r') as zipobj:
    dirlist = zipobj.namelist()
    for name in dirlist:
        if "OEBPS/Text/" in name:
            textFiles.append(name)
    textFiles.remove("OEBPS/Text/")
    for name in textFiles:
        print(name)
        textContents.append(zipobj.read(name).decode('utf8'))

    for content in textContents:
        new = content.splitlines()
        new[0] = new[0].replace('<p id="L1">', '\n<br /><br />\n<p id="L1">')
        for i, n in enumerate(new):
            new[i] = new[i].replace('<br />', '\n')
        content = '\n'.join(new)

        outfile.write("#####\n\n")
        f = HTMLFilter()
        f.feed(content)
        outfile.write(f.text)
