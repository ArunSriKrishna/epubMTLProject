from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException
from sys import exit
from time import sleep, time
from os import getcwd, path, makedirs
from random import randint

from tkinter.filedialog import askopenfilename

if not path.exists('output'):
    makedirs('output')

filename = askopenfilename()
source_filepath = filename
filename = path.basename(source_filepath)
filename = filename[0: filename.rfind('.')]
output_dir = getcwd() + "/output/"
random = randint(1, 2500)

file_source = open(source_filepath)
file_output = open(output_dir + f"/{filename}_{random}.txt", "a")
chromedriver = getcwd() + "/chromedriver"

if not path.exists('chromedriver'):
    exit("Chrome Driver not found")

source_language = "Korean"
target_language = "English"

language_code = {
    "Detect Language": "auto",
    "Korean": "ko",
    "English": "en",
    "Japanese": "ja",
    "Chinese Simplified": "zh-CN",
    "Chinese Traditional": "zh-TW",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Russian": "ru",
    "Portuguese": "pt",
    "Italian": "it",
    "Vietnamese": "vi",
    "Thai": "th",
    "Indonesian": "id",
    "Hindi": "hi"
}

webElements = {
    "input-textbox": ["id", "txtSource"],
    "output-textbox": ["id", "txtTarget"],
    "translate-btn": ["id", "btnTranslate"]
}


def find_webelement(element):
    webElement = driver.find_element(element[0], element[1])
    return webElement


driver = webdriver.Chrome(chromedriver)
driver.get(f"https://papago.naver.com/?sk={language_code[source_language]}&tk={language_code[target_language]}")

try:
    wait = WebDriverWait(driver, timeout=15)
    wait.until(ec.visibility_of_element_located(webElements["translate-btn"]))
except NoSuchElementException:
    exit("Webpage Timed out!")

start_time = time()
input_textbox = find_webelement(webElements["input-textbox"])
output_textbox = find_webelement(webElements["output-textbox"])

source_read = file_source.readlines()
source_text = ''.join(source_read)

last_index = len(source_text) - 1
curr_index = 0
batch_count = 0

while curr_index < last_index:
    source = ''

    if (last_index - curr_index) >= 4999:
        source = source_text[curr_index: curr_index + 5000]
    else:
        source = source_text[curr_index: last_index-curr_index]
        print("Batch has less than 5000 Characters! charcter_count = {len(source)}")

    i = len(source) - 1
    while i > 1:
        if source[i] == '\n':
            source = source[0: i]
            break
        i = i - 1
    print("\nBatch Character Count: " + str(len(source)))

    script = "var ele = " + repr(source) + ";" + "\n document.getElementById('txtSource').value=ele;"
    driver.execute_script(script)
    input_textbox.send_keys(" ")

    translated = "null"
    base_time = 0

    while translated == "null" or translated == "..." or translated == "":
        base_time += 1
        sleep(0.01)
        translated = output_textbox.text

    timeout = 0
    change_count = 0
    changelog = []
    timed_out = []

    while 1:
        sleep(0.1)
        timeout += 1
        translated_curr = output_textbox.text
        if translated_curr != translated:
            translated = translated_curr
            change_count += 1
        else:
            if timeout > 100:
                timed_out.append(batch_count + 1)
                print("Timed out!")
                break
            if change_count >= 3:
                print("Changes caught!")
                break

    translated = output_textbox.text
    file_output.write(translated)
    batch_count += 1
    curr_index += len(source) - 1
    progress = round((curr_index / last_index) * 100, 2)
    print(f"Batch count {batch_count} \nCharacters Processed: {curr_index} Progress <{progress}%>")

print(f"Completed in {round(time() - start_time, 2)} second(s)!\n Total Characters Processed: {curr_index}")
print(output_dir + f"{filename}_{random}.txt")
