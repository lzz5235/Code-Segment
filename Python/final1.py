def comp(a, b):
    if len(a)<len(b):
        return 1
    elif len(a)>len(b):
        return -1
    else:
        if a[0]<b[0]:
            return 1
        elif a[0]>b[0]:
            return -1
        else:
            return 0
 
words=[]
word=raw_input()
while word!='':
    words.append(word)
    word=raw_input()
s1=set()
s=[]
s2=[]
for word in words:
    s2.append(word)
    words.remove(word)
    for i in range(0,len(word)):
        s1.add(word[i])
    for word2 in words:
        if len(word)==len(word2):
            for i in range(0,len(word)):
                if word2[i] not in s1:
                    break
            else:
                s2.append(word2)
                words.remove(word2)
    s.append(s2)
    s2=[]
 
for ss in s:
    ss.sort()
 
s.sort(cmp=comp)
for ss in s:
    for word in ss:
        print word,
    print ''