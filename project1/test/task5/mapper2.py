#!/usr/bin/python
import sys, heapq
 
top100 = []
for line in sys.stdin:
    
    the_list = line.split()
    top100.append(the_list)
    top100 = heapq.nlargest(100, top100, key=lambda x:(len(x)-1, x[0]))
    
for l in top100:
    print "0\t"+"\t".join(l)