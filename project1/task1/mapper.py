#!/usr/bin/python

import sys
import re

currentLine = ''

def mapper(line):
    dataList = line.replace('\n', ' ').split('\t')
    if len(dataList) != 19 or (not dataList[0].strip('"').isdigit()) or (not dataList[3].strip('"').isdigit()):
        return
    authorId = dataList[3].strip('"')
    activeTime = dataList[8].strip('"')
    pos1 = activeTime.find(' ')
    pos2 = activeTime.find(':', pos1)
    activeHour = activeTime[pos1+1:pos2]
    print '{0}\t{1}'.format(authorId, activeHour)

for line in sys.stdin:
    items = line.split('\t')
    if len(items) > 4 and items[0].strip('"').isdigit() and items[3].strip('"').isdigit():
        if currentLine:
            mapper(currentLine)
        currentLine = line
    else:
        if currentLine:
            currentLine += line

if currentLine:
    mapper(currentLine)
    