#!/usr/bin/python
import sys
 
words = ["the", "be", "to", "of", "and", "a", "in", "that", "have",  \
"I",  "it",  "for",  "not",  "on",  "with",  "he",  "as",  "you",  "do",  "at",  \
"this",  "but",  "his",  "by",  "from",  "they",  "we",  "say",  "her",  "she",  \
"or",  "an",  "will",  "my",  "one",  "all",  "would",  "there",  "their",  "what", \
"so",  "up",  "out",  "if",  "about",  "who",  "get",  "which",  "go",  "me",  "when",  \
"make",  "can",  "like",  "time",  "no",  "just",  "him",  "know",  "take",  "person",  \
"into",  "year",  "your",  "good",  "some",  "could",  "them",  "see",  "other",  "than",  \
"then",  "now",  "look",  "only",  "come",  "its",  "over",  "think",  "also",  "back",  \
"after",  "use",  "two",  "how",  "our",  "work",  "first","well",\
"way","even","new","want","because","any","these","give","day","most","us"]

currentLine = ''

def mapper(line):
    dataList = line.replace('\n', ' ').split('\t')
    if len(dataList) != 19 or (not dataList[0].strip('"').isdigit()) or (not dataList[3].strip('"').isdigit()):
        return
    id = dataList[0].strip('"')
    body = dataList[4].strip('"')
    existed = set()
    for word in body.split():
        if word not in words and word not in existed:
            existed.add(word)
            position = body.find(word)
            print "{0}\t{1}".format(word.lower(), str(id) + ':' + str(position + 1))
        

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
    