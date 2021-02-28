from random import randint
from os import getcwd, path, makedirs
from tkinter.filedialog import askopenfilename

if not path.exists('output'):
    makedirs('output')

output_dir = getcwd() + "/output/"
filename = askopenfilename()
source_filepath = filename
filename = path.basename(source_filepath)

series_name = filename[0: filename.rfind('.')]

website_title = "Website"
website_description = "Website Description"
post_id = randint(1, 10000000)

chapters = []
chapter_title = []
current_line = 0
chapter_count = 0
chapter_start = 0
chapter_end = 0

file_source = open(source_filepath, "r")
raw_content = file_source.readlines()


def chapter_url(count):
    if count < 10:
        return f"{series_name}-0000{count}"
    elif count < 100:
        return f"{series_name}-000{count}"
    elif count < 1000:
        return f"{series_name}-00{count}"
    elif count < 10000:
        return f"{series_name}-0{count}"
    else:
        return f"{series_name}-{count}"


def chapter_number(count):
    if count < 10:
        return f"0000{count}"
    elif count < 100:
        return f"000{count}"
    elif count < 1000:
        return f"00{count}"
    elif count < 10000:
        return f"0{count}"
    else:
        return f"{count}"


xml_header = f"""
<?xml version="1.0" encoding="UTF-8" ?>\n
<rss version="2.0"
xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
xmlns:content="http://purl.org/rss/1.0/modules/content/"
xmlns:wfw="http://wellformedweb.org/CommentAPI/"
xmlns:dc="http://purl.org/dc/elements/1.1/"
xmlns:wp="http://wordpress.org/export/1.2/">\n
<channel>\n
    <title>{website_title}</title>\n
    <link>http://localhost/wordpress</link>\n
    <description>{website_description}</description>\n
    <pubDate>Fri, 02 Oct 2020 16:14:42 +0000</pubDate>\n
    <language>en-US</language>\n
    <wp:wxr_version>1.2</wp:wxr_version>\n
    <wp:base_site_url>http://localhost/wordpress</wp:base_site_url>\n
    <wp:base_blog_url>http://localhost/wordpress</wp:base_blog_url>\n
    <wp:author><wp:author_id>1</wp:author_id><wp:author_login><![CDATA[user]]></wp:author_login><wp:author_email><![CDATA[123@gmail.com]]></wp:author_email><wp:author_display_name><![CDATA[user]]></wp:author_display_name><wp:author_first_name><![CDATA[]]></wp:author_first_name><wp:author_last_name><![CDATA[]]></wp:author_last_name></wp:author>\n
    <generator>https://wordpress.org/?v=5.5.1</generator>\n
"""


def chaptertitle(chapter_no):
    return chapter_title[chapter_no - 1]


def chapter_entry(chapter_no):
    return f"""
<item>
<title>{chapter_number(chapter_no)}-{chaptertitle(chapter_no)}</title>
<link>http://localhost/wordpress/{chapter_url(chapter_no)}/</link>
<pubDate>Fri, 02 Oct 2020 16:12:47 +0000</pubDate>
<dc:creator><![CDATA[user]]></dc:creator>
<guid isPermaLink="false">http://localhost/wordpress/?page_id={post_id}</guid>
<description></description>
<content:encoded><![CDATA[
"""


def chapter_exit(chapter_no):
    return f"""]]></content:encoded>\n
excerpt:encoded><![CDATA[]]></excerpt:encoded>\n
<wp:post_id>{post_id}</wp:post_id>\n
<wp:post_date><![CDATA[2020-10-02 16:12:47]]></wp:post_date>\n
<wp:post_date_gmt><![CDATA[2020-10-02 16:12:47]]></wp:post_date_gmt>\n
<wp:comment_status><![CDATA[closed]]></wp:comment_status>\n
<wp:ping_status><![CDATA[closed]]></wp:ping_status>\n
<wp:post_name><![CDATA[{chapter_url(chapter_no)}]]></wp:post_name>\n
<wp:status><![CDATA[publish]]></wp:status>\n
<wp:post_parent>0</wp:post_parent>\n
<wp:menu_order>0</wp:menu_order>\n
<wp:post_type><![CDATA[page]]></wp:post_type>\n
<wp:post_password><![CDATA[]]></wp:post_password>\n
<wp:is_sticky>0</wp:is_sticky>\n
</item>\n
"""


xml_footer = "</channel>\n </rss>\n"

while current_line < len(raw_content):

    if raw_content[current_line].find("#####") != -1:
        # outfile = open(f"{output_filepath}{chapter_count}.txt", "a")
        # outfile.write("\n")
        chapters.append("<br>\n")

        chapter_title.append(raw_content[current_line + 2])

        print(f"Chapter {chapter_number(chapter_count + 1)}: {chapter_title[chapter_count - 1]} Loaded!")
        chapter_count += 1
        current_line += 1

    else:
        # outfile.write(raw_content[current_line])
        html_line = raw_content[current_line].replace("\n", "<br>\n")
        chapters[chapter_count - 1] += html_line
        current_line += 1

# fileout =open(output_filepath, "w")
# fileout.write(''.join(chapters[0:2]))

print(f"\n\n* Generating {series_name}.xml file *\n\n")

fileout = open(f"{output_dir}{series_name}.xml", "a")
fileout.write(xml_header)
for chapter_num in range(1, chapter_count + 1):
    post_id += 1
    fileout.write(chapter_entry(chapter_num) + chapters[chapter_num - 1] + chapter_exit(chapter_num))
    print(f"Chapter {chapter_num} is now added!")
fileout.write(xml_footer)

print(f"{output_dir}{series_name}.xml")
