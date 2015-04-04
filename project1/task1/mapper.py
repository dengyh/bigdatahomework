#!/usr/bin/python

import sys
import re

hourPattern = re.compile(r'(?<=\ )[0-9]+?(?=:)')

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
    authorId = dataList[3]
    activeTime = dataList[8]
    activeHour = hourPattern.search(activeTime).group()
    print '{0}\t{1}'.format(authorId, activeHour)
    lastLine = ''