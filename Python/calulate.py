# -*- coding: utf-8 -*-
"""
Created on Fri Jan 02 18:13:03 2015

@author: lzz
题目内容：
依次计算一系列给定字符串的字母值，字母值为字符串中每个字母对应的编号值（A对应1，B对应2，以此类推，不区分大小写字母，非字母字符对应的值为0）的总和。例如，Colin 的字母值为 3 + 15 + 12 + 9 + 14 = 53

输入格式:
一系列字符串，每个字符串占一行。

输出格式：
计算并输出每行字符串的字母值。

输入样例：
Colin
ABC

输出样例：
53
6

注意一行输入 Colin ABC这种情况！
"""

import string
alphas = string.letters

stopword = ""
str = ""
for line in iter(raw_input, stopword):
    str += (line + '#')
    
def compute(str):
    temp=0
    for char in str:
        if char in alphas:
            temp +=(ord(char)-64)        
    return temp
        

for line in str.split('#'):
    if line !='':
        line = line.upper()
        print compute(line)