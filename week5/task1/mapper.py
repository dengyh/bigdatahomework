#!/usr/bin/python

import sys

lastLine = ''
firstLine = True

totalLength = 0
totalNumber = 0

for line in sys.stdin:
    if firstLine:
        firstLine = False
        continue
    line = lastLine + line
    dataList = line.strip().split('\t')
    if len(dataList) < 19:
        lastLine = line
        continue
    body = dataList[4].strip('"')
    totalNumber += 1
    totalLength += len(body.strip())
    lastLine = ''

print '{0}\t{1}'.format('key', (totalLength, totalNumber))