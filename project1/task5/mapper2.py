#!/usr/bin/python
import sys, heapq

results = [] 

for line in sys.stdin:
    
    dataList = line.split()
    results.append(dataList)
    results = heapq.nlargest(100, results, key=lambda x: (len(x) - 1, x[0]))
    
for result in results:
    print '0\t' + '\t'.join(result)