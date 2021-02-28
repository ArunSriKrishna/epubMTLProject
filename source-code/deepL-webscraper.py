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

if not path.exists('chromedriver'):
    exit("Chrome Driver not found")

chromedriver = getcwd() + "/chromedriver"

webElements = {
    "input-textbox": ["xpath", "//textarea[@dl-test='translator-source-input']"],
    "output-textbox": ["xpath", "//textarea[@dl-test='translator-target-input']"],
    "suspended-popup": ["xpath", "//b[text() = 'temporarily suspended']"]
}


def find_webElement(element):
    webElement = driver.find_element(element[0], element[1])
    return webElement


driver = webdriver.Chrome(chromedriver)
driver.get("https://www.deepl.com/en/translator")

wait = WebDriverWait(driver, timeout=15)
wait.until(ec.visibility_of_element_located(webElements["input-textbox"]))

start_time = time()
source_read = file_source.readlines()
source_text = ''.join(source_read)

last_index = len(source_text)
curr_index = 0
batch_count = 0
flag = 0
timedout = []

input_textbox = find_webElement(webElements["input-textbox"])
output_textbox = find_webElement(webElements["output-textbox"])

suspended_index = 0
suspended_count = 0
source_lastlength = 0


def read_translated():
    return output_textbox.get_attribute("value")


while curr_index < last_index:

    suspended = False
    source = ''

    if (last_index - curr_index) > 5000:
        source = source_text[curr_index: curr_index + 5000]

    else:
        source = source_text[curr_index: last_index + 1]
        flag = 1

    i = len(source) - 1
    while i > 1 and flag == 0:
        if source[i] == '\n':
            source = source[0: i]
            break
        i = i - 1

    print("\nBatch Character Count: " + str(len(source)))
    script = f"document.getElementsByTagName('textarea')[0].value = {repr(source)}"
    driver.execute_script(script)
    input_textbox.send_keys(" ")
    base_time = 0

    translated = read_translated()

    while 1:
        sleep(1)
        base_time += 1
        translated_curr = read_translated()

        if base_time > 120:

            try:
                suspended = find_webElement(webElements["suspended-popup"]).is_displayed()

            except NoSuchElementException:
                suspended = False
                timedout.append(f"Current Batch:{curr_index}-{curr_index + len(source)} Batch Count :{batch_count + 1}")

            if suspended:
                if curr_index == suspended_index:
                    suspended_count += 1
                    if suspended_count > 1:
                        exit(f"Try again some other time!\nCurrent Index: {curr_index}")

                suspended_index = curr_index
                print(f"Suspended! Restarting session\nCurrent Index: {curr_index}")

                driver.delete_all_cookies()
                driver.stop_client()
                driver.close()
                driver = webdriver.Chrome(chromedriver)
                driver.get("https://www.deepl.com/en/translator")

                input_textbox = find_webElement(webElements["input-textbox"])
                output_textbox = find_webElement(webElements["output-textbox"])

                source_lastlength = len(source) + 1
                break
            else:
                exit(f"Timed out! Batch-count: {batch_count} - ({curr_index - len(source)}/{curr_index})")

        elif translated_curr != translated:
            translated = translated_curr
            break

    if not suspended:
        file_output.write(translated)
        batch_count += 1
        curr_index += len(source)
        progress = round((curr_index / last_index) * 100, 2)
        print(f"Batch count {batch_count}: ({curr_index - len(source)}/{curr_index})\nProgress <{progress}%>")

print(f"\nCompleted in {round(time() - start_time, 2)} second(s)!\nTotal Characters Processed: {curr_index}")

print(timedout)
print(output_dir + f"{filename}_{random}.txt")
