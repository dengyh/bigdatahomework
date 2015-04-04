#!/usr/bin/python

import sys

lastLine = ''
firstLine = True

for line in sys.stdin:
    if firstLine:
        firstLine = False
        continue
    line = lastLine + line
    dataList = line.strip().split('\t')
    if len(dataList) < 19:
        lastLine = line
        continue
    parentId = dataList[7]
    questionId = dataList[0]
    type = dataList[5]
    authorId = dataList[3]
    if type == 'answer' or type == 'comment':
        print '{0}\t{1}'.format(parentId, authorId)
    else:
        print '{0}\t{1}'.format(questionId, authorId)
    lastLine = ''