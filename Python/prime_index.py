# -*- coding: utf-8 -*-
"""
Created on Tue Jan 06 06:36:03 2015

@author: lzz
定义一个 prime() 函数求整数 n 以内（不包括n）的所有素数（1不是素数），并返回一个按照升序排列的素数列表。使用递归来实现一个二分查找算法函数bi_search()，该函数实现检索任意一个整数在 prime() 函数生成的素数列表中位置（索引）的功能，并返回该位置的索引值，若该数不存在则返回 -1。

输入格式:
第一行为正整数 n
接下来若干行为待查找的数字，每行输入一个数字

输出格式：
每行输出相应的待查找数字的索引值

输入样例：
10
2
4
6
7

输出样例：
0
-1
-1
3
"""
import math

stopword = ""
str=""

N=int(raw_input())

def is_prime(x):
    for i in range(2,int(math.sqrt(x)+1)):
         if x % i == 0:
             return False
             break
    return True 

def bi_search(nums,low,high,value):
    if low <=high:
        mid = (low+high)/2
        if nums[mid]==value:
            return mid
        elif nums[mid] < value:
            return bi_search(nums,mid+1,high,value)
        elif nums[mid] > value:
            return bi_search(nums,low,mid-1,value)
    else:
        return -1
    
    
nums=[ x for x in range(2,N) if is_prime(x)==True]

for line in iter(raw_input, stopword):
    str += (line + '#')

for line in str.split('#'):
    if line !='':
        print bi_search(nums,0,len(nums)-1,int(line))
