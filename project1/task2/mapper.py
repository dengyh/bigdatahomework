import sys
import re

currentLine = ''

def mapper(line):
    dataList = line.replace('\n', ' ').split('\t')
    if len(dataList) != 19 or (not dataList[0].strip('"').isdigit()) or (not dataList[3].strip('"').isdigit()):
        return
    parentId = dataList[7].strip('"')
    questionId = dataList[0].strip('"')
    type = dataList[5].strip('"')
    body = dataList[4].strip('"')
    if type == 'answer':
        print '{0}\t{1}'.format(parentId, (type, len(body.strip())))
    elif type == 'question':
        print '{0}\t{1}'.format(questionId, (type, len(body.strip())))

for line in sys.stdin:
    items = line.split('\t')
    if len(items) > 4 and items[0].strip('"').isdigit() and items[3].strip('"').isdigit():
        if currentLine:
            mapper(currentLine)
        currentLine = line
    else:
        if currentLine:
            currentLine += line

if currentLine:
    mapper(currentLine)
    