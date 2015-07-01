#!/usr/bin/python

import sys

lastAuthor = None
activeHour = [0] * 24

for line in sys.stdin:
    datas = line.strip().split('\t')
    if len(datas) != 2:
        continue
    authorId, hour = datas
    hour = int(hour)
    if lastAuthor and lastAuthor != authorId:
        maxActiveHour = max(activeHour)
        for index in xrange(24):
            if maxActiveHour == activeHour[index]:
                print '{0}\t{1}'.format(lastAuthor, index)
                break
        activeHour = [0] * 24
    activeHour[hour] += 1
    lastAuthor = authorId

if activeHour != [0] * 24:
    maxActiveHour = max(activeHour)
    for index in xrange(24):
        if maxActiveHour == activeHour[index]:
            print '{0}\t{1}'.format(lastAuthor, index)
            break