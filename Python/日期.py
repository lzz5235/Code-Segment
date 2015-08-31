# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 15:46:14 2014

@author: lzz
若已知1800年1月1日为星期3，则对于一个给定的年份和月份，输出这个月的最后一天是星期几。

"""

Year=int(raw_input())
Month=int(raw_input())


def is_leap_year(year):
    if year % 4 ==0 and year%100 !=0 or year % 400 ==0:
        return True
    return False

def get_num_of_days_in_month(year,month):
    if month in (1,3,5,7,8,10,12):
        return 31
    elif month in (4,6,9,11):
        return 30
    elif is_leap_year(year):
        return 29
    else:
        return 28
        
def get_total_num_of_day(year,month):
    days=0
    for y in range(1800,year):
        if is_leap_year(y):
            days +=366
        else:
            days +=365
         
    for m in range(1,month+1):
        days += get_num_of_days_in_month(year,m)
    
    return days-1
    
def get_start_day(year,month):
    return (3+get_total_num_of_day(year,month))%7
    
print get_start_day(Year,Month)