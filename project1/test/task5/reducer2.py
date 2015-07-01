#!/usr/bin/python
import sys, heapq
 
local_top100s = [] 
for line in sys.stdin:
    items = line.split()    
    local_top100s.append(items[1:])
 
top100 = heapq.nlargest(100, local_top100s, key=lambda x:(len(x)-1, x[0]))
for l in top100:
    print "\t".join(l)