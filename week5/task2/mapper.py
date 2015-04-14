#!/usr/bin/python

import sys

lastLine = ''
firstLine = True

commonWord = ['the', 'be', 'to', 'of',
'and', 'a', 'in', 'that', 'have', 'I',
'it', 'for', 'not', 'on', 'with', 'he',
'as', 'you', 'do', 'at', 'this', 'but',
'his', 'by', 'from', 'they', 'we', 'say',
'her', 'she', 'or', 'an', 'will', 'my',
'one', 'all', 'would', 'there', 'their',
'what', 'so', 'up', 'out', 'if', 'about',
'who', 'get', 'which', 'go', 'me', 'when',
'make', 'can', 'like', 'time', 'no',
'just', 'him', 'know', 'take', 'person',
'into', 'year', 'your', 'good', 'some',
'could', 'them', 'see', 'other', 'than',
'then', 'now', 'look', 'only', 'come',
'its', 'over', 'think', 'also', 'back',
'after', 'use', 'two', 'how', 'our',
'work', 'first', 'well', 'way', 'even',
'new', 'want', 'because', 'any', 'these',
'give', 'day', 'most', 'us']

keywords = {}

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
    postId = dataList[0]
    bodyItems = body.split(' ')
    index = 0
    for item in bodyItems:
        index += 1
        if item not in commonWord:
            if item not in keywords:
                keywords[item] = {}
            if postId not in keywords[item]:
                keywords[item][postId] = index
    lastLine = ''

for key in keywords:
    for postId in keywords[key]:
        print '{0}\t{1}'.format(key, (postId, keywords[key][postId]))