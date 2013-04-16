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
#from types import MethodType

reload(sys)
sys.setdefaultencoding('utf-8')


class FieldNotDefined(Exception):
    def __init__(self, fieldName, itemName):
        self.fieldName = fieldName
        self.itemName = itemName

    def __str__(self):
        return "Field " + self.fieldName + \
               " not defined in item.py for item: " + self.itemName


class ItemList(list):
    def __init__(self):
        list.__init__(self)
        self.__fields__ = {}

    def newfield(self, name, default=None):
        self.__fields__[name] = default

    def getfields(self):
        return self.__fields__

    def __setitem__(self, keyField, value):
        if type(keyField) == type(int()):
            list.__setitem__(self, keyField, value)
        else:
            if keyField in self.__fields__:
                self.__fields__[keyField] = value
            else:
                raise FieldNotDefined(keyField, self.__class__.__name__)

    def __getitem__(self, keyField):
        if type(keyField) == type(int()):
            return list.__getitem__(self, keyField)
        else:
            if keyField in self.__fields__:
                return self.__fields__.get(keyField)
            else:
                raise FieldNotDefined(keyField, self.__class__.__name__)


class Item(object):
    def __init__(self, url=None, callback=None, data=None):
        self.__fields__ = {}
        if url is not None and callback is not None:
            self.request = {"url": url, "callback": callback, "data": data}
        else:
            self.request = None

    def newfield(self, name, default=None):
        self.__fields__[name] = default

    #def add(self, field, value=None):
    #    if value is not None:
    #        self.fields[field]=value
    #    else:
    #        self.fields.update(field)

    def get(self, keyField):
        return self.__fields__.get(keyField)

    def getDict(self):
        return self.__fields__

    def __getitem__(self, keyField):
        if keyField in self.__fields__:
            return self.__fields__.get(keyField)
        else:
            raise FieldNotDefined(keyField, self.__class__.__name__)

    def __setitem__(self, keyField, value):
        if keyField in self.__fields__:
            self.__fields__[keyField] = value
        else:
            #print("field '"+keyField+"' not defined!, ignoring.")
            raise FieldNotDefined(keyField, self.__class__.__name__)


class customSaveItem(Item):
    def __init__(self):
        Item.__init__(self)
