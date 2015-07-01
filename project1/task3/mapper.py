import sys

currentLine = ''

def mapper(line):
    dataList = line.replace('\n', ' ').split('\t')
    if len(dataList) != 19 or (not dataList[0].strip('"').isdigit()) or (not dataList[3].strip('"').isdigit()):
        return
    tagnames = dataList[2].strip('"').split()
    type = dataList[5].strip('"')
    if type == 'question':
        for tagname in tagnames:
            print '0\t{0}\t{1}'.format(tagname, 1)

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
    