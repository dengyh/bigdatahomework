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
    body = dataList[4].strip('"')
    # if len(body) == 238:
    #     print body
    if type == 'answer':
        print '{0}\t{1}'.format(parentId, (type, len(body.strip())))
    else:
        print '{0}\t{1}'.format(questionId, (type, len(body.strip())))
    lastLine = ''