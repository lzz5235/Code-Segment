# -*- coding: utf-8 -*-
"""
Created on Tue Jan 06 12:05:58 2015

@author: lzz
题目内容：
帕斯卡三角形，又称杨辉三角形是二项式系数在三角形中的一种几何排列。帕斯卡三角形通常从第0行开始枚举，并且每一行的数字是上一行相邻两个数字的和。在第0行只写一个数字1，然后构造下一行的元素。将上一行中数字左侧上方和右侧上方的数值相加。如果左侧上方或者右侧上方的数字不存在，用0替代。下面给出6行的帕斯卡三角形：
     1
    1 1
   1 2 1
  1 3 3 1
 1 4 6 4 1
1 5 10 10 5 1
编写程序，输入帕斯卡三角形的高度 n，然后生成和上面例子一样风格的三角形。

输入格式:
一个正整数 n

输出格式：
相应高度的帕斯卡三角形，两个数字之间有一个空格

输入样例：
6

输出样例：
     1
    1 1
   1 2 1
  1 3 3 1
 1 4 6 4 1
1 5 10 10 5 1
"""

level = int(raw_input())
list_length =  level  * 2 -1
initial_value = 0
arr = [[ initial_value for i in range(list_length )] for i in range(level)] 
 
arr[0][list_length/2] = 1  
  
for i in range(1,level):
    for j in range(list_length):
        if ( j == 0 ) :
            arr[i][j] = arr[i-1][j+1]
        elif (j ==  list_length-1) :
            arr[i][j] = arr[i-1][j-1] 
        else :
            arr[i][j]=arr[i-1][j-1]+arr[i-1][j+1]

lineoutput = "" 
for i in range(level):   
    flag=0
    for j in range(list_length):
        if flag ==i+1:
            lineoutput += "\n"
            break
        elif arr[i][j] == 0 :
            lineoutput += " "
        elif arr[i][j] !=0:
            lineoutput += str(arr[i][j])
            flag +=1            
            

print lineoutput