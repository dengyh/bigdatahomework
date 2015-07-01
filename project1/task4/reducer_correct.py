#!/usr/bin/python
 
import sys
import string
 
IDs = []
oldKey = None
 
for line in sys.stdin:
    data_mapped = line.strip().split("\t")
    if len(data_mapped) != 2:
        # Something has gone wrong. Skip this line.
        continue
 
    thisKey, thisID = data_mapped
 
    if oldKey and oldKey != thisKey:
        print oldKey, "\t", sorted(IDs)
        oldKey = thisKey
        IDs = []
 
    oldKey = thisKey
    IDs.append(string.atoi(thisID))
 
if oldKey != None:
    print oldKey, "\t", sorted(IDs)