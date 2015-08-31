# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 15:26:05 2014

@author: lzz
"""
import math

N = int(raw_input(''))
sum = 0

def is_prime(x):
    for i in range(2,int(math.sqrt(x)+1)):
         if x % i == 0:
             return False
             break
    return True           
 
def is_round_prime(x):

    if x in [2,3,5,7,11,13,17,31,37,71,73,79,97]:
        return True 
        
    if is_prime(x)==False:
        return False
        

    n=int(math.floor(math.log10(x)))
    t=n
    
    while t != 0:
        m = x % 10
        b = x // 10
        t = t - 1
        x = m * 10**n+b
        if is_prime(x)==False:
            return False
    
    return True
          


for i in range(2,N+1):
    if is_round_prime(i)==True: 
        sum+=1 
print sum
 