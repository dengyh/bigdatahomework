#!/usr/bin/python

import sys

lastParent = None
answerCount = 0
questionLength = 0
answerLength = 0

for line in sys.stdin:
    datas = line.strip().split('\t')
    if len(datas) != 2:
        continue
    parentId, dataTuple = datas
    type, length = eval(dataTuple)
    if lastParent and lastParent != parentId:
        if answerCount != 0:
            print '{0}\t{1}\t{2}'.format(lastParent, questionLength,
                answerLength * 1.0 / answerCount)
        else:
            print '{0}\t{1}\t{2}'.format(lastParent, questionLength, 0)
        answerCount = 0
        questionLength = 0
        answerLength = 0
    if type == 'question':
        questionLength = int(length)
    else:
        answerCount += 1
        answerLength += int(length)
    lastParent = parentId

if questionLength != 0:
    if answerCount != 0:
        print '{0}\t{1}\t{2}'.format(lastParent, questionLength,
            answerLength * 1.0 / answerCount)
    else:
        print '{0}\t{1}\t{2}'.format(lastParent, questionLength, 0)