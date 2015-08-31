# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 16:31:09 2015

@author: lzz
倒排索引（Inverted index），也常被称为反向索引，是一种索引方法，用来存储某个单词存在于哪些文档之中。是信息检索系统中最常用的数据结构。通过倒排索引，可以根据单词快速获取包含这个单词的文档列表。

本作业主要完成以下四个功能：

(1). 建立索引：首先输入100行字符串，用于构建倒排索引，每行字符串由若干不含标点符号的、全部小写字母组成的单词构成，每个单词之间以空格分隔。依次读入每个单词，并组成一个由<单词, 每个单词出现的行号集合>构成的字典，其中行号从1开始计数。

(2). 打印索引：按照字母表顺序依次输出每个单词及其出现的位置，每个单词出现的位置则按行号升序输出。例如，如果“created”出现在第3, 20行，“dead”分别出现在14, 20, 22行。则输出结果如下（冒号和逗号后面都有一个空格，行号不重复）：

…
created: 3, 20
dead: 14, 20, 22
…

(3). 检索：接下来输入查询(Query)字符串，每行包含一个查询，每个查询由若干关键字(Keywords)组成，每个关键字用空格分隔且全部为小写字母单词。要求输出包含全部单词行的行号（升序排列），每个查询输出一行。若某一关键字在全部行中从没出现过或没有一行字符串包含全部关键字，则输出“None”。遇到空行表示查询输入结束。如对于上面创建的索引，当查询为“created”时，输出为“3, 20”；当查询为“created dead”时，输出为“20”；当查询为“abcde dead”时，输出为“None”；

(4). 高级检索：当输入的Query以“AND: ”开始，则执行“与”检索，即要求输出包含全部关键字的行；如果输入的Query以“OR:”开始，则执行“或”检索，即某行只要出现了一个关键字就满足条件。默认情况（不以“AND: ”或“OR: ”开始），执行“与”检索。

输入格式:
首先输入100行字符串，每行字符串由若干不含标点符号的、全部小写字母组成的单词构成，每个单词之间以空格分隔。
若干个查询，每个查询占一行，既可能是普通检索，也可能是高级检索。

输出格式：
首先打印索引，然后将每个查询的结果输出到一行。
"""

dict={}
for row in range(2):
    sentence = raw_input()
    words = sentence.split()
    for word in words:
        if word in dict:
            dict[word].add(row+1)
        else:
            dict[word]= set()
            dict[word].add(row+1)
            
word_row_lst = dict.items()
word_row_lst.sort(key=lambda x:x[0])

for word,rows in word_row_lst:
    lst_row = list(rows)
    lst_row.sort()
    
    for i in range(len(lst_row)):
        lst_row[i]=str(lst_row[i])
        
    print word +':',', '.join(lst_row)
    
def judge_in_dict(query,dic):
    word_lst = query.split()
    for word in word_lst:
        if word not in dic:
            return 0
    return 1
    
def print_set(pset):
    empty_set = set()									
    if empty_set == pset:
        print 'None'
    else:
        pset_list=list(pset)
        pset_list.sort()

#        print pset_list
        print ', '.join([__builtins__.str(i) for i in pset_list])
    
stopword = ""
str = ""
for line in iter(raw_input, stopword):
    str += (line + '#')
    
for line in str.split('#'):
    if line !='':
        qset = set()
        if 'OR:' in line:
            line = line[3:]
            word_lst = line.split();            
            for word in word_lst:
                if word !='' and word in dict:
                    qset = qset | dict[word]  
        elif 'AND:' in line:
            line = line[4:]
            word_lst = line.split(); 
            if   word_lst!=[]:
                if word_lst[0] in dict:
                    qset =  dict[word_lst[0]]         
                    for word in word_lst:
                        if word in dict:
                            qset = qset & dict[word]
                        else:
                            qset = set()
                            break
                else:
                     qset = set()
            else:
                  qset = set()             
        else:
            word_lst = line.split(); 
            if   word_lst!=[]:
                if word_lst[0] in dict:
                    qset =  dict[word_lst[0]]         
                    for word in word_lst:
                        if word in dict:
                            qset = qset & dict[word]
                        else:
                            qset = set()
                            break
                else:
                     qset = set()
            else:
                  qset = set()  
                
        print_set(qset)
        
            
                