# epubProject

## DeepL Translate webscrapper - auto -> en_US
https://www.deepl.com/translator

### Prerequisites 
- Chromedriver present in the same directory.

### Usage:
- Execute the python executible using 
<pre>$ ./deepL-auto</pre>
- Select a text document when prompted.

<hr>

## epub2txt - Extract epub contents to a text document

### Usage:
- Execute the python executible using 
<pre>$ ./epub2txt</pre>
- Select a epub document when prompted.

<hr>

## Papago Translate webscrapper - ko -> en_US
https://papago.naver.com/

### Prerequisites 
- Chromedriver present in the same directory.

### Usage:
- Execute the python executible using 
<pre>$ ./papago-kr</pre>
- Select a text document when prompted.

<hr>

## regex-xlsx - Regular Expression Replace tool

### Prerequisites 
- Add Find and Replace regular expression patterns inside a <b>named</b> Sheet in ./src/Glossary.xlsx

### Usage:
- Execute the python executible in console using 
<pre>$ ./regex-xlsx</pre>
- Enter the name of the Sheet as series name.
- Select a text document when prompted.

<hr>

## txt2wxr - <br>Convert the text document output from epub2txt or templatated text document into importable WXR (WordPress eXtended RSS) File
### for easy population of your wordpress site

### Prerequisites 
- Templated text document -> new 'page' in wordpress is recognized from "#####\n" in the text document.

### Usage:
- Execute the python executible using 
<pre>$ ./txt2wxr</pre>
- Select the templated text document when prompted.

<hr>

## gif2png - Batch convert gif files to png files

### Prerequisites 
- Text document containing full directory and a linebreak of each file to be converted.

### Usage:
- Execute the python executible using 
<pre>$ ./gif2png</pre>
- Select the text document containing the list when prompted.
