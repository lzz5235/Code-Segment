# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 09:58:24 2014

@author: lzz

一个斐波那契数列的前10项为：1, 2, 3, 5, 8, 13, 21, 34, 55, 89，对于一个最大项的值不超过n的斐波那契数列，求值为偶数的项的和。

输入格式:
一个正整数n，如100。

输出格式：
值为偶数的项的和，如 2 + 8 + 34 = 44。
"""

N=int(raw_input())

def is_Even(x):
    if x%2==0:
        return True
    return False
    
def fib_loop(n):
    Sum=0
    if n==1 or n==2:
        return 1
    else:
        i=2
        f1=1
        f2=1
        while(i<n):
            f3=f1+f2
            f1=f2
            f2=f3
            i=i+1
            if f3>n:
                break
            if is_Even(f3)==True:
                Sum+=f3
    return Sum

print fib_loop(N)