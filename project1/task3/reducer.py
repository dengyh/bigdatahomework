#!/usr/bin/python

import sys

lastTag = None
tagCount = 0
sortedList = []

def insert(item, sortedList):
    index = len(sortedList)
    while index > 0 and item['count'] > sortedList[index - 1]['count']:
        index -= 1
    if index < 10:
        if len(sortedList) >= 10:
            sortedList.pop()
        sortedList.insert(index, item)

for line in sys.stdin:
    datas = line.strip().split('\t')
    if len(datas) != 2:
        continue
    tag, count = datas
    if lastTag and lastTag != tag:
        insert({'tag': lastTag, 'count': tagCount}, sortedList)
        tagCount = 0
    tagCount += int(count)
    lastTag = tag

if tagCount != 0:
    insert({'tag': lastTag, 'count': tagCount}, sortedList)

for item in sortedList:
    print '{0}\t{1}'.format(item['tag'], item['count'])