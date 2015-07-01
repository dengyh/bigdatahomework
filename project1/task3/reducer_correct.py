#!/usr/bin/python
import sys, heapq
 
oldKey = None
tags = {}
 
for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 3:
        # Something has gone wrong. Skip this line.
        continue
    _, tag, one = data_mapped
    if not tag in tags.keys():
        tags[tag]=0
    tags[tag]+=1
 
top10 = heapq.nlargest(10, tags, key=tags.get)
 
for item in top10:
    print item, tags[item]