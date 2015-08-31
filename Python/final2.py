# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 17:55:57 2015

@author: lzz
题目内容：
两位整数相乘形成的最大回文数是 9009 = 99 × 91。编写程序，求得任意输入的 n 位整数相乘形成的最大回文数。

输入格式:
正整数 n 

输出格式：
n 位整数相乘形成的最大回文数

输入样例：
2

输出样例：
9009
"""

def is_cycle(n):
    lenN = len(str(n))
    for i in xrange(lenN/2):
        if str(n)[i] != str(n)[-1-i]:
            return False
    return True
 
n=int(raw_input())

bigcycle=0
begin = 10**(n-1)-1
end = 10**n-1
for i in range(end,begin,-2):
    for j in range(i,end-begin,-2):
        temp = i*j
        if temp>bigcycle:
            if is_cycle(temp)==True:
                bigcycle=temp
print bigcycle