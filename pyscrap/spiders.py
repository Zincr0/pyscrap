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
import socket
import urllib2
import os
import simplejson as json
from lxml import html, etree
from item import Item
from item import ItemList
#from item import customSaveItem
from settings import getHeaders
import inspect
#from IPython import embed


reload(sys)
sys.setdefaultencoding("utf-8")


def getHtml(url):
    """Download url and return lxml.html object"""
    return getWeb(url, False)


def getXml(url):
    """Download xml and return lxml.etree object"""
    return getWeb(url, True)


def getJson(url):
    """Download json and return simplejson object"""
    site = urllib2.urlopen(url, timeout=300)
    return json.load(site)


def getWeb(url, isFeed):
    """Download url and parse it with lxml.
    If "isFeed" is True returns lxml.etree
    else, returns lxml.html
    """
    socket.setdefaulttimeout(300)
    loadedWeb = urllib2.build_opener()
    loadedWeb.addheaders = getHeaders()
    if isFeed:
        web = etree.parse(loadedWeb.open(url))
    else:
        web = html.parse(loadedWeb.open(url))
    return web


def rmSelf(f):
    """f -> function.
    Decorator, removes first argument from f parameters.
    """
    def new_f(*args, **kwargs):
        newArgs = args[1:]
        result = f(*newArgs, **kwargs)
        return result
    return new_f


def processItem(item, theArgs, theSpider):
    if item.request is None:
        #print("is instance item "+str(item))
        if theSpider is None:
            aSpider = theArgs[0]
        else:
            aSpider = theSpider
        if aSpider.__pipes__ is not None:
            saveFunction = aSpider.__pipes__["items"].get(item.__class__.__name__)
            if saveFunction is not None:
                saveFunction(item)
            elif hasattr(aSpider, "__saveItem__"):
                if aSpider.__saveItem__ is not None:
                    aSpider.__saveItem__(item)
    else:
        function = item.request["callback"]
        aracnid = function.__self__
        url = item.request["url"]
        function = catchItem(function, theSpider=aracnid)
        #print("ejecutando callback")
        if item.request["data"] is None:
            function(url)
        else:
            function(url, data=item.request["data"])


def processItemList(itemlist, theArgs, theSpider):
    if theSpider is None:
        aSpider = theArgs[0]
    else:
        aSpider = theSpider
    if aSpider.__pipes__ is not None:
        saveFunction = aSpider.__pipes__["itemLists"].get(itemlist.__class__.__name__)
        if saveFunction is not None:
            saveFunction(itemlist)
        else:
            for item in itemlist:
                if isinstance(item, Item):
                    processItem(item, theArgs, theSpider)
                elif isinstance(item, str):
                    aSpider = theArgs[0]
                    aSpider.parse(url=item)


def catchItem(f, theSpider=None):
    """Decorador, ejecuta la función parse y procesa el resultado
    como una lista de items, ejecutando la función 'saveitem' que corresponda."""
    def new_f(*args, **kwargs):
        #print("thepath "+os.getcwd())
        #print("the spider")
        #print(str(theSpider))
        items = f(*args, **kwargs)
        if items is None:
            return items
        if isinstance(items, Item):
            processItem(items, args, theSpider)
        elif len(items) > 0:
            if isinstance(items, ItemList):
                    processItemList(items, args, theSpider)
            else:
                for item in items:
                    #print("procesando items")
                    if isinstance(item, ItemList):
                        processItemList(item, args, theSpider)
                    elif isinstance(item, Item):
                        processItem(item, args, theSpider)
                    elif isinstance(item, str):
                        aSpider = args[0]
                        aSpider.parse(url=item)
        return items
    return new_f


class metaSpider(type):

    #def __init__(cls, name, bases, dct):
    #    print("__init__ "+name)
    #    super(metaSpider, cls).__init__(name, bases, dct)

    def __new__(meta, classname, bases, classDict):
        """Metaclase captura return desde función parse crea un diccionario
        '__pipes__' según lo especificado en settings.py. También asigna el decorador
        catchitem a la función 'parse'."""
        if classname == "spider":
            return type.__new__(meta, classname, bases, classDict)
        nosettings = False
        nopipelines = False
        try:
            settings = __import__('settings', os.getcwd())
            #print("Using local settings.")
        except Exception, e:
            if str(e) != "No module named settings":
                errorOnSettings = str(type(e)) + "\n on settings.py: " + str(e)
                raise Exception(errorOnSettings)
            try:
                #import settings
                spiderpath = inspect.getfile(classDict['parse'])
                modulo = spiderpath.split("/")[-2]
                theimport = "from "+modulo+" import settings"
                exec theimport
            except Exception, e:
                #print("settings.py not found, ignoring")
                nosettings = True
        try:
            pipeline = __import__('pipeline', os.getcwd())
            #print("Using local pipeline.")
        except Exception, e:
            if str(e) != "No module named pipeline":
                errorOnPipeline = str(type(e)) + "\n on pipeline.py: " + str(e)
                raise Exception(errorOnPipeline)
            try:
                spiderpath = inspect.getfile(classDict['parse'])
                #print(spiderpath)
                spiderpath = spiderpath.split("/")
                modulo = spiderpath[-2]
                theimport = "from "+modulo+" import pipeline"
                exec theimport
            except Exception, e:
                #print(e)
                nopipelines = True
        getUrls = None
        getSearchData = None
        if nopipelines:
            #print("pipeline.py not found")
            pass
        else:
            getUrls = getattr(pipeline, "getUrls", None)
            getSearchData = getattr(pipeline, "getSearchData", None)
        if getUrls is None:
            getUrls = lambda: []
        if getSearchData is None:
            getSearchData = lambda: []
        getUrls = rmSelf(getUrls)
        getSearchData = rmSelf(getSearchData)
        getSearchData = classmethod(getSearchData)
        getUrls = classmethod(getUrls)
        classDict["getUrls"] = getUrls
        classDict["getSearchData"] = getSearchData
        if nopipelines or nosettings:
            return type.__new__(meta, classname, bases, classDict)
        pipes = settings.getPipes()
        #print(pipes)
        if pipes:
            if "items" in pipes:
                for itemName, functionName in pipes["items"].iteritems():    
                    pipes["items"][itemName] = getattr(pipeline, functionName, None)
            else:
                print("items not defined in settings.py!")
            if "itemLists" in pipes:
                for itemName, functionName in pipes["itemLists"].iteritems():    
                    pipes["itemLists"][itemName] = getattr(pipeline,
                                                           functionName, None)
            else:
                print("itemLists not defined in settings.py!")
            classDict["__pipes__"] = pipes
            if "spiders" in pipes:
                if pipes.get("spiders"):
                    saveFunction = pipes["spiders"].get(classname)
                    if saveFunction:
                        #print("save fucntion: "+str(saveFunction))
                        saveFunction = getattr(pipeline, saveFunction, None)
                        if saveFunction:
                            saveFunction = rmSelf(saveFunction)
                            classDict["__saveItem__"] = saveFunction
                        else:
                            classDict["__saveItem__"] = None
            else:
                print("spiders not defined in settings.py!")
        else:
            classDict["__pipes__"] = None
        funcion = classDict.get("parse")
        if funcion:
            classDict["parse"] = catchItem(funcion)
        return type.__new__(meta, classname, bases, classDict)


class spider(object):
    __metaclass__ = metaSpider

    def parse(self):
        return None

#class demoSpider(spider):
#    def parse(self, url=None):
#        print("processing url: "+str(url))
#        
#        if url=="http://www.google.com":
#            items=[]
#            web=getHtml(url)
#            title=web.find(".//title").text
#            normalItem=Item()
#            normalItem.add("title", title)
#            items.append( normalItem )
#            customItem=customSaveItem()
#            items.append( customItem )
#            childUrl="http://www.some_new_url_found.com"
#            items.append(childUrl)
#            urlcustomParse="http://www.some_custom_parse_url.com"
#            itemWithCustomParse=Item(urlcustomParse, self.customParse)
#            items.append( itemWithCustomParse )
#        else:
#            print("normal parse for url: ")
#            print(url)
#            items=None
#        return items
#        
#    def customParse(self, url):
#        print("executing custom parse for url: ")
#        print(url)
#        items=[]
#        customItem=customSaveItem()
#        items.append(customItem)
#        return items
#
#    def run(self):
#        start_urls=["http://www.google.com",
#                    ]
#        for url in start_urls: self.parse(url)
