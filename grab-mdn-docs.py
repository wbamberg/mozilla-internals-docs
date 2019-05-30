import sys
import os
import requests
import time
from bs4 import BeautifulSoup

base_url = "https://developer.mozilla.org/"

urls = [
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech'
]

more_urls = [
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/APNG',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/Places/Manipulating_bookmarks_using_Places',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XPCOM',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XPCOM/Guide/Creating_components/Using_XPCOM_Utilities_to_Make_Things_Easier',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XPCOM/Reference',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XPCOM/Reference/Interface',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XPCOM/Reference/Interface/amIWebInstaller',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XPCOM/Reference/Interface/mozIAsyncFavicons',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XUL',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XUL/Attribute/chromemargin',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XUL/conditions',
'https://developer.mozilla.org/en-US/docs/Mozilla/Tech/XUL/Tutorial/Anonymous_Content'
]

def get_file_raw(url):
    r = requests.get(url + "?raw&macros")
    return r.text

def get_title(url):
    r = requests.get(url + "$json")
    return r.json()["title"]

def get_contributors(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    contributors_div = soup.find_all("div", class_="contributors-sub")[1]
    contributors = contributors_div.find_all("a")
    contributors_list = "<ul>"
    for contributor in contributors:
        contributor_href = "https://developer.mozilla.org" + contributor["href"]
        contributors_list += "<li><a href=\"" + contributor_href + "\">" + contributor.string+ "</a></li>"
    contributors_list += "</ul>"
    return contributors_list

def wrap_in_page(content):
    preamble = """<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="/css/page.css"/>
    <title>example page</title>
  </head>

  <body>
    <div class="content">
"""

    postamble = """
    </div>
  </body>
</html>"""

    return preamble + content + postamble

for url in urls:

    title = "<div class=\"content-heading\"><h1>" + get_title(url)+ "</h1></div>\n"
    contributors_list = "<hr/><strong>Contributors to this page:</strong><br/>" + get_contributors(url)
    file_text_raw = get_file_raw(url)
    page_content = title + file_text_raw + contributors_list
    complete_page = wrap_in_page(page_content)

    file_path = url.replace(base_url, "")
    pieces = file_path.split("/")
    file_name = pieces[-1] + ".html"
    path = "/".join((pieces[:-1]))
    path = "/".join([os.getcwd(), path])

    if not os.path.exists(path):
        os.makedirs(path)

    out = open(os.path.join(path, file_name), 'w')
    print >>out, complete_page.encode('utf-8')
    out.close()
    print(file_path)
    time.sleep(1)
