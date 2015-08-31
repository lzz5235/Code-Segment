# -*- coding: utf-8 -*-
"""
Created on Tue Dec 16 09:40:19 2014

@author: lzz
"""


from math import sqrt
N=int(raw_input())
sum=0

def is_prime(x):
    if x in [2,3,5,7,11,13,17,19]:
        return True
    elif x%2==0:
        return False
    elif x%3==0:
        return False
    elif x%5==0:
        return False
    elif x%7==0:
        return False
    elif x%11==0:
        return False
    elif x%13==0:
        return False
    elif x%17==0:
        return False
    elif x%19==0:
        return False
    else:
        for j in range(23,int(sqrt(x)+1),2):
            if x%j==0:
                return False
                break
        else:
            return True
    
for i in range(2,N):
    if is_prime(i)==True:
        sum+=i
        
print sum

