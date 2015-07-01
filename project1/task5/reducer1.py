#!/usr/bin/python
import sys

lastWord = None
positionSet = set()
 
for line in sys.stdin:
    data = line.split()
    if len(data) != 2:
        continue
    word, position = data
    if lastWord != None and lastWord != word:
         positionList = list(positionSet)
         positionList.sort()
         print lastWord + '\t' + '\t'.join(positionList)
         positionSet.clear()
    lastWord = word
    positionSet.add(position)
 
if lastWord != None or len(positionSet) != 0:
    positionList = list(positionSet)
    positionList.sort()
    print lastWord + '\t' + '\t'.join(positionList)