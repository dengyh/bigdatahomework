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
    tagnames = dataList[2].split(' ')
    type = dataList[5]
    if type == 'question':
        for tagname in tagnames:
            print '{0}\t{1}'.format(tagname, 1)
    lastLine = ''