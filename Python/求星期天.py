# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 14:49:31 2014
题目内容：
根据下列信息计算在1901年1月1日至2000年12月31日间共有多少个星期天落在每月的第一天上？

a)  1900.1.1是星期一
b)  1月，3月，5月，7月，8月，10月和12月是31天
c)  4月，6月，9月和11月是30天
d)  2月是28天，在闰年是29天
e)  公元年数能被4整除且又不能被100整除是闰年
f)  能直接被400整除也是闰年
@author: lzz
"""

mondays=0

def getmonthdays(year):
    isleapyear=year%400==0 or (year%4==0 and (not year%100==0))
    if isleapyear:
        return [31,29,31,30,31,30,31,31,30,31,30,31]
    return [31,28,31,30,31,30,31,31,30,31,30,31]

pastdays=1  

monthdays=getmonthdays(1900)
for month in range (0,12):
    pastdays+=monthdays[month]

for year in range(1901,2001):
    monthdays=getmonthdays(year)
    for month in range(0,12):
        if pastdays%7==0:
            mondays+=1
        pastdays+=monthdays[month]
print mondays