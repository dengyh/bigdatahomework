#!/usr/bin/python
import sys
 
oldKey = None
hours = [0]*24
 
for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue
 
    author_id, hour = data_mapped
 
    if oldKey and oldKey != author_id:
        max_hour=0
        max_hour_count=0
        for i in range(0, 24):
            if max_hour_count<hours[i]:
                max_hour=i
                max_hour_count=hours[i]
        print oldKey,max_hour
        hours = [0]*24
 
    oldKey = author_id
    hours[int(hour)]+=1
    
if oldKey != None:
    max_hour=0
    max_hour_count=0
    for i in range(0, 24):
        if max_hour_count<hours[i]:
            max_hour=i
            max_hour_count=hours[i]
    print oldKey,max_hour