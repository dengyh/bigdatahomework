#!/usr/bin/python

import sys

lastParent = None
threadList = []

for line in sys.stdin:
    datas = line.strip().split('\t')
    if len(datas) != 2:
        continue
    parentId, authorId = datas
    parentId = int(parentId)
    authorId = int(authorId)
    if lastParent and lastParent != parentId:
        print '{0}\t{1}'.format(lastParent, threadList)
        threadList = []
    threadList.append(authorId)
    lastParent = parentId

if threadList != []:
    print '{0}\t{1}'.format(lastParent, threadList)