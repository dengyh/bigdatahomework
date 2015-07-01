#!/usr/bin/python
import sys
oldword = None
pos_set = set()
 
for line in sys.stdin:
    data_mapped = line.split()
    if len(data_mapped) != 2:
        continue
    thisword, thispos = data_mapped
    if oldword!= None and oldword != thisword:
         the_list = list(pos_set)
         the_list.sort()
         print oldword+"\t"+"\t".join(the_list)
         pos_set.clear()
    oldword = thisword
    pos_set.add(thispos)
 
if oldword != None:
    the_list = list(pos_set)
    the_list.sort()
    print oldword+"\t"+"\t".join(the_list)