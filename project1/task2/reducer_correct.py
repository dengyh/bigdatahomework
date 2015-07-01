#!/usr/bin/python
import sys
 
oldKey = None
answers = []
question = None
 
for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue
 
    question_id, tlen = data_mapped
    if oldKey and oldKey != question_id:
        if len(answers)==0:
            avg=0
        else:
            avg = sum(answers)/float(len(answers))
        print oldKey,question, avg
        answers=[]
        question = None
 
    oldKey = question_id
    if tlen[0]=="q":
        question = int(tlen[1:])
    elif tlen[0]=="a":
        answers.append(int(tlen[1:]))
    
 
if oldKey != None:
    if len(answers)==0:
        avg=0
    else:
        avg = sum(answers)/float(len(answers))
    print oldKey,question, avg