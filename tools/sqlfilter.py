#coding:utf8
import re
import logging
import copy
import urllib

__author__ = 'Liang Yejin'
__doc__ = """
Detect SQL-Injection action by keywords.
How to use: see function "unitTest".
"""

SQL_FILTERED_KEYWORD = [" union ", " select ", " update ", " delete ", " join ", ";--",
                        " and ", " or ", "(\/\*.*?\*\/)", " limit", " group by", " hex",
                        " substr", " reverse"," md5", "etc/passwd", "cmdshell", "etc/shadow"]

class SqlFilter():
    def __init__(self, argument=None, mode="strict", ruleDepth=1):
        # @:parameter mode:
        #     strict, return ""(empty string) if filter rule hit (most secure)
        #     lenient, return argument which is filter the keywords (less secure)
        #     warning, only make a "waring info" when filter rule hit. (insecure)
        # @:parameter ruleDepth: 0-4 less is faster but less filter rule will be applied.
        # @:return (maybe NOT same as input)
        self.argument = argument
        self._argument = copy.copy(argument)
        if self._argument:
            self._argument = self._argument.lower()
        self.rules = []
        self.mode = mode
        if self.argument:
            self.rules = self.genFilter(ruleDepth)


    def genFilter(self, ruleDepth):
        ruleDepth = int(ruleDepth)
        allrules = [
            self._ruleCheckLenth,
            self._ruleUrlDecode,
            self._ruleDoubleUrlDecode,
            self._ruleTripleUrlDecode,
        ]
        if ruleDepth > len(allrules)+1 or ruleDepth < 0:
            ruleDepth = 2
        return allrules[:ruleDepth + 1]

    def filter(self):
        ret = self._filter()
        if not ret:
            return self.argument
        if self.mode == "strict":
            return ""
        elif self.mode == "lenient":
            return self._removeKeyWord(self.argument)
        else:
            logging.warning("sql filter detect a attact, parameter is {0}".format(self.argument))
            return self.argument

    def _detectKeyWord(self, t):
        arr = ["+", "-", "(", ")", "%0", "%0a", "%0b", "%0c", "%0d", "%09", "%a0"]
        for a in arr:
            t = t.replace(a, "")
        t = t.lower()
        regex = ""
        for key in SQL_FILTERED_KEYWORD:
            regex += "{0}|".format(key)
        regex = regex[:-1]
        # print "detecting : {0}".format(t)
        # print "regex: {0}".format( regex )
        reObj = re.compile(regex, re.DOTALL)
        ret = reObj.search(t)
        if ret:
            return True
        return False

    def _removeKeyWord(self, t):
        max = 6
        regex = ""
        t = t.lower()
        for key in SQL_FILTERED_KEYWORD:
            regex += "{0}|".format(key)
        regex = regex[:-1]
        reObj = re.compile(regex)
        while self._detectKeyWord(t) and max > 0:
            t = reObj.sub("", t)
            max -= 1

        if max <= 0:
            return ""
        else:
            return t


    def _filter(self, mode=""):
        for rule in self.rules:
            hit = rule()
            if hit:
                return True
        return False

    def _ruleCheckLenth(self, max = 512):
        l = len(self.argument)
        if l > max:
            return True

    def _ruleUrlDecode(self):
        t = self._argument
        t = urllib.unquote_plus(t)
        self._argument = t
        return self._detectKeyWord(t)

    def _ruleDoubleUrlDecode(self):
        t = self._argument
        for i in range(2):
            t = urllib.unquote_plus(t)
        return self._detectKeyWord(t)

    def _ruleTripleUrlDecode(self):
        t = self._argument
        for i in range(3):
            t = urllib.unquote_plus(t)
        return self._detectKeyWord(t)


def unitTest():

    bad_param = "ID=66+UnIoN+aLL+SeLeCt+1,2,3,4,5,6,7,(SELECT+concat(0x3a,id,0x3a,password,0x3a)+\
FROM+information_schema.columns+WHERE+table_schema=0x6334706F645F666573746976616C5F636D73+AND+\
table_name=0x7573657273),9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30--"
    nice_param = "this is%20la%09vAlue%20contains 大小写混合"
    #strict mode (defualt mode , most secure)
    for param in [bad_param,nice_param]:
        print "[strict mode] input is : {0}".format(param)
        sqlfilter = SqlFilter(param, mode="strict")
        param_filtered = sqlfilter.filter()
        print "[strict mode] output is : {0}".format(param_filtered)
    print "="*100
    #lenient mode (less secure)
    for param in [bad_param,nice_param]:
        print "[lenient mode] input is : {0}".format(param)
        sqlfilter = SqlFilter(param, mode="lenient")
        param_filtered = sqlfilter.filter()
        print "[lenient mode] output is : {0}".format(param_filtered)
    print "="*100
    #warning mode (insecure)
    for param in [bad_param,nice_param]:
        print "[warning mode] input is : {0}".format(param)
        sqlfilter = SqlFilter(param, mode="warning")
        param_filtered = sqlfilter.filter()
        print "[warning mode] output is : {0}".format(param_filtered)

if __name__ == "__main__":
    unitTest()
