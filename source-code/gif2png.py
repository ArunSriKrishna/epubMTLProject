from tkinter.filedialog import askopenfilename
from PIL import Image
from os import makedirs, path, getcwd

if not path.exists("output"):
    makedirs("output")

file_list = open(askopenfilename(), 'r')
output_dir = getcwd() + "/output/"
list = open(getcwd() + "/list-output.txt", 'a')
output_file_list = []

images = file_list.readlines()


for image in images:
    fileBaseName = path.basename(image)
    fileBaseName = fileBaseName[0: fileBaseName.rfind('.')]
    image = image[0: image.rfind('\n')]
    print(image)
    img = Image.open(image)
    img.save(f"{output_dir}{fileBaseName}.png", 'png', optimize=True, quality=100)
    output_file_list.append(f"{output_dir}{fileBaseName}.png")


print(output_file_list)
list.writelines(output_file_list)