# -*- coding: utf-8 -*-
"""
Created on Tue Dec 23 16:03:45 2014

@author: lzz
如在汉诺塔游戏中，我们希望将塔A上的n个盘子，通过塔B移动到塔C，则对于任意输入的n，给出移动的步骤。

输入格式:
一个正整数n

输出格式：
移动的步骤

输入样例：
2

输出样例：
Move 1 from A to B
Move 2 from A to C
Move 1 from B to C
"""

N=int(raw_input())

def hanoi(n,A,B,C):
    if n==1:
        print 'Move', n, 'from', A, 'to', C
    else:
        hanoi(n-1,A,C,B)
        print 'Move', n, 'from', A, 'to', C
        hanoi(n-1,B,A,C)
        
hanoi(N,'A','B','C')