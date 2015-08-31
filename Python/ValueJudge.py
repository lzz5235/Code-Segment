# -*- coding: utf-8 -*-
"""
Created on Fri Jan 02 16:32:24 2015

@author: lzz
题目内容：
依次判断一系列给定的字符串是否为合法的 Python 标识符。

输入格式:
一系列字符串，每个字符串占一行。

输出格式：
判断每行字符串是否为合法的 Python 标示符，如果合法则输出 True，否则输出 False。

"""

import string 
import keyword
 
alphas = string.letters  
symbols = "_"
nums = string.digits
keywords = keyword.kwlist
 
stopword = ""
str = ""
for line in iter(raw_input, stopword):
    str += line + " "

def isValue(myIn):
    if myIn in keywords:
        return False

    if len(myIn) == 1:
        if myIn not in alphas:
            return False
        else:
            return True
             
    if myIn[0] not in alphas + symbols:
        return False

    for otherChar in myIn[1:]:
        if otherChar not in alphas + symbols + nums:
            return False
    else:
        return True
       
for line in str.split():
    if isValue(line)==False:
        print "False"
    else:
        print "True"
