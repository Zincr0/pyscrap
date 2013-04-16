# -*- coding=utf-8 -*-
#Copyright 2012 Daniel Osvaldo Mondaca Seguel
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def createSetup(name):
    return """# -*- coding=utf-8 -*-
import sys
import os
from setuptools import setup

reload(sys)
sys.setdefaultencoding('utf-8')

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...

files = [\""""+name+"""/*\"]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = \""""+name+"""\",
    version = \"0.0.1\",
    author = \"author\",
    author_email = \"author@example.com\",
    description = (\"just a web spider made with pyscrap\"),
    license = \"custom\",
    keywords = \"web scraping\",
    url = \"http://www.example.com\",
    packages=[\""""+name+"""\"],
    install_requires = [\"simplejson\"],
    long_description=read(\"README.txt\"),
    package_data = {\"package\": files },
    classifiers=[
        \"Development Status :: 4 - Beta\",
        \"Topic :: Software Development\",
        \"License :: custom\",
        \"Operating System :: POSIX :: Linux\",
        \"Programming Language :: Python\",
    ],
)"""


def createManifest(name):
    return """include README.txt
recursive-include """ + name + """ *.py"""


def createGitIgnore():
    return """*.py[co]

# Packages
*.egg
*.egg-info
dist
build
eggs
parts
bin
var
sdist
develop-eggs
.installed.cfg

# Installer logs
pip-log.txt

# Unit test / coverage reports
.coverage
.tox

#Translations
*.mo

#Mr Developer
.mr.developer.cfg
"""


def createSettings():
    return """# -*- coding=utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding(\"utf-8\")


def getHeaders():
    headers = [(\"User-agent\", \"Feedfetcher-pyscrap\")]
    return headers


def getPipes():
    pipes = {"spiders":
             {
             },
             "items":
             {
             "feedErrorItem": "saveError"
             },
             "itemLists":
             {
             "feedList": "feedSave"
             }
             }
    return pipes

"""


def createPipeline():
    return """# -*- coding=utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding(\"utf-8\")


def getUrls():
    urls = ["http://www.example.com", "http://www.example2.com"]
    return urls


def getSearchData():
    data = {"example": "value", "example2": "value2"}
    return data


def customSave(items):
    print("Custom list url: ")
    print(items["url"])
    for item in items:
        print("Custom save for item: " + str(item))

"""


def createItem():
    return """# -*- coding=utf-8 -*-
import sys
from pyscrap.item import Item
from pyscrap.item import ItemList

reload(sys)
sys.setdefaultencoding('utf-8')


class customItem(Item):
    def __init__(self):
        Item.__init__(self)
        self.newfield("scriptText")


class customList(ItemList):
    def __init__(self):
        ItemList.__init__(self)
        self.newfield("url")

"""


def createSpider():
    return """# -*- coding=utf-8 -*-
import sys
from pyscrap.spiders import spider
from pyscrap.spiders import getHtml
from pyscrap.item import Item
from item import customList
from item import customItem

reload(sys)
sys.setdefaultencoding('utf-8')


class demoSpider(spider):
    def parse(self, url):
        print("processing url: " + str(url))
        web = getHtml(url)
        items = []
        myList = customList()
        myList["url"] = url
        for script in web.xpath(".//script"):
            anItem = customItem()
            anItem["scriptText"] = script.text
            myList.append(anItem)
        items.append(myList)
        anItem = Item("http://www.example.com", self.customParse)
        items.append(anItem)
        return items

    def customParse(self, url):
        print("executing custom parse for : ")
        print(url)
        return None

    def run(self):
        #No need to import getUrls from pipline.py
        print demoSpider.getUrls()
        #No need to import getSearchData from pipline.py
        print demoSpider.getSearchData()
        start_urls = ["http://www.google.com", ]
        for url in start_urls:
            self.parse(url)


def main():
    d = demoSpider()
    d.run()


if __name__ == "__main__":
    main()

"""

