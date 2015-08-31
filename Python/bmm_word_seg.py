# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 15:05:41 2015
@author: lzz
题目内容：
实现逆向最大匹配分词算法，即从右向左扫描，找到最长的词并切分。如句子“研究生命的起源”，逆向最大匹配分词算法的输出结果为“研究 生命 的 起源”。

输入格式:
第一行是以utf-8格式输入的词表，每个词之间以空格分隔。
接下来是若干行以utf-8格式输入的中文句子。

输出格式：
以utf-8格式输出的逆向最大匹配的分词结果，每个词之间使用空格分隔。每个输入对应一行输出。

输入样例：
你 我 他 爱 北京 天安门 研究 研究生 命 生命 的 起源
研究生命的起源
我爱北京天安门

输出样例：
研究 生命 的 起源
我 爱 北京 天安门
"""

def Bmm_word_seg(sent,max_len,word_dict):
    end = len(sent)
    begin = 0
    words = []

    while end > 0:
        for start in range(end-max_len,end):
            if sent[start:end] in word_dict:
                words.append(sent[start:end])
                break
            elif start+1==end:
                words.append(sent[start:end])
                break
        end = start
    words.reverse()
    return words

set_words=set()
line_lst = raw_input()
line_lst = unicode(line_lst,'utf-8')
words = line_lst.strip().split()
MAX_LEN = 1
stopword = ""
context = ""

for word in words:
    if word not in set_words:
        set_words.add(word)
        if len(word) > MAX_LEN:
            MAX_LEN = len(word)


for line in iter(raw_input, stopword):
    context += (line + '#')

context = unicode(context,'utf-8')

for line in context.split('#'):
    if line !='':
        words_lst = Bmm_word_seg(line,MAX_LEN,set_words)
        lst = ' ' .join(words_lst)
        print lst.encode('utf-8')