#!/usr/bin/python

import sys

lastKey = None
indexList = []

def printOut(key, list):
    listString = key
    for item in list:
        listString += '\t' + item[0] + ':' + str(item[1])
    print listString

for line in sys.stdin:
    datas = line.strip().split('\t')
    if len(datas) != 2:
        continue
    key, indexTuple = datas
    postID, index = eval(indexTuple)
    if lastKey and lastKey != key:
        printOut(lastKey, indexList)
        indexList = []
    lastKey = key
    indexList.append((postID, index))

if indexList != []:
    printOut(lastKey, indexList)