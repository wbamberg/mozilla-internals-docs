import sys
import os
import requests
import time
import json
from bs4 import BeautifulSoup

base_url = "https://developer.mozilla.org/"

contributors_preamble = """<p>This page was originally written for <a href=\"https://developer.mozilla.org\">developer.mozilla.org</a> and is used here under the <a href=\"http://creativecommons.org/licenses/by-sa/2.5/\">Creative Commons Attribution-ShareAlike license</a> (CC-BY-SA).</p>
<p>Original contributors to this page: """

rootdir = './raw/en-US/docs'

page_template = """<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8">
    <link rel="stylesheet" href="https://code.cdn.mozilla.net/fonts/zilla-slab.css"/>
    <link rel="stylesheet" href="/css/page.css"/>
    <title>{}</title>
  </head>

  <body>{}</body>
</html>"""

contributors_preamble = """<p>This page was originally written for <a href=\"https://developer.mozilla.org\">developer.mozilla.org</a> and is used here under the <a href=\"http://creativecommons.org/licenses/by-sa/2.5/\">Creative Commons Attribution-ShareAlike license</a> (CC-BY-SA).</p>
<p>Original contributors to this page: """


link_map = {}
with open(os.path.join(os.getcwd(), "link_map.json")) as data_file:
    link_map = json.load(data_file)

def convert_href(href):
    if href.startswith("https://developer.mozilla.org/en-US/docs/Mozilla/Tech/"):
        return href[len("https://developer.mozilla.org"):]
    else:
        return href

def fix_links(page):
    soup = BeautifulSoup(page, "html.parser")
    links = soup.find_all("a")
    for link in links:
        if (link.get("href")):
            href = link["href"]
            if href.startswith("/"):
                href = "https://developer.mozilla.org" + href
            if link_map.get(href):
                mapped_href = link_map[href]
                link["href"] = convert_href(mapped_href)
    return soup.prettify()

def render_breadcrumbs(subdir):
    hierarchy = subdir.split(os.sep)[4:][::-1]
    prefix = ''
    breadcrumbs_array = []
    for entry in hierarchy:
        prefix = prefix + "../"
        breadcrumbs_array.append("<a href=\"{}.html\">{}</a>".format(prefix + entry, entry))
    return "<nav class=\"breadcrumbs\">{}</nav>".format("&raquo;".join(breadcrumbs_array[::-1]))

def render_contributors(contributors_list):
    return "<div id=\"footer\"><hr/>" + contributors_preamble + contributors_list + ".</p></div>"

def render_page(data, subdir):
    h1 = "<div class=\"content-heading\"><h1>" + data["title"] + "</h1></div>\n"
    page_content = "<div class=\"content\">" + fix_links(data["content"]) + "</div>"
    body = render_breadcrumbs(subdir) + h1 + page_content + render_contributors(data["contributors"])
    complete_page = page_template.format(data["title"], body.encode('utf-8'))
    return complete_page

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        breadcrumbs = render_breadcrumbs(subdir)
        with open(os.path.join(subdir, file)) as data_file:
            data = json.load(data_file)
            page = render_page(data, subdir)
            path = os.sep.join(subdir.split(os.sep)[2:])
            file_name = file.split(".")[0] + ".html"
            print file_name
            if not os.path.exists(path):
                os.makedirs(path)
            out = open(os.path.join(path, file_name), 'w')
            print >>out, page
            out.close()
