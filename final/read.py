#!/usr/bin/env python
import os


f1 = open("test.txt", "w")
#f1.write(data)

count = os.path.getsize('wc_day88_1')
data = ""
f = open('wc_day88_1', 'rb')

while count > 0:
    if count < 1024:
        data = f.read(count)
        count = count - count
    else:
        data = f.read(1024)
        count = count -1024
    f1.write(data)
    
    #if count == 0:
    #   break
f.close()
f1.close()