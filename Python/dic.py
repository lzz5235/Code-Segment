# -*- coding: utf-8 -*-
"""
Created on Mon Jan 12 15:05:41 2015

@author: lzz
"""


def load_dic(filename):
    f = open(filename)
    word_dic = set()
    max_length = 1
    for line in f:
        word = unicode(line.strip(),'utf-8')
        word_dic.add(word)
        if len(word) > max_length:
            max_length = len(word)
    
    return max_length,word_dic
    
def fmm_word_seg(sent,max_len,word_dict):
    begin = 0
    words = []

    sent = unicode(sent, 'utf-8')
    
    while begin < len(sent):
        for end in range(min(begin + max_len,len(sent)),begin,-1):
            if sent[begin:end] in word_dict:
                words.append(sent[begin:end])
                break
        begin = end
        
    return words

def Bmm_word_seg(sent,max_len,word_dict):
    end = len(sent)
    begin = 0
    words = []
    
    sent = unicode(sent, 'utf-8')
 
    while end >begin:
        for start in range(begin,max(begin+max_len,len(sent)),1):
            if sent[start:end] in word_dict:
                words.append(sent[start:end])
                break
        end = start
        
    return words
    
max_len,word_dict = load_dic('lexicon.dic')

sent = raw_input()

words =  Bmm_word_seg(sent,max_len,word_dict)

for i in range(len(words)):
    print words[i]
