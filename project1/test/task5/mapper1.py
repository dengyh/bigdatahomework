#!/usr/bin/python
import sys
 
common_words = ["the", "be", "to", "of", "and", "a", "in", "that", "have",  \
"I",  "it",  "for",  "not",  "on",  "with",  "he",  "as",  "you",  "do",  "at",  \
"this",  "but",  "his",  "by",  "from",  "they",  "we",  "say",  "her",  "she",  \
"or",  "an",  "will",  "my",  "one",  "all",  "would",  "there",  "their",  "what", \
"so",  "up",  "out",  "if",  "about",  "who",  "get",  "which",  "go",  "me",  "when",  \
"make",  "can",  "like",  "time",  "no",  "just",  "him",  "know",  "take",  "person",  \
"into",  "year",  "your",  "good",  "some",  "could",  "them",  "see",  "other",  "than",  \
"then",  "now",  "look",  "only",  "come",  "its",  "over",  "think",  "also",  "back",  \
"after",  "use",  "two",  "how",  "our",  "work",  "first","well",\
"way","even","new","want","because","any","these","give","day","most","us"]
 
#!/usr/bin/python
import sys
curr_line = None
 
def dequote(t):
    if t.startswith("\"") and t.endswith("\""):
        return t[1:-1]
    else:
        return t
 
 
def map_a_record(curr_line):
    items = curr_line.replace("\n"," ").split("\t")
    if len(items)!=19 or items[0]=="id":
        return
    
    id = dequote(items[0])
    body = dequote(items[4])
    covered = set()
    for word in body.split():
        if not word in common_words and not word in covered:
            covered.add(word)
            pos = body.find(word)
            print "{0}\t{1}".format(word.lower(), str(id)+":"+str(pos+1))
        
 
for line in sys.stdin:
 
    items = line.split("\t")
    if len(items)>4 and dequote(items[0]).isdigit() and dequote(items[3]).isdigit():
        # A new record
        if curr_line != None:
            map_a_record(curr_line)
        curr_line = line
    else:
        if curr_line != None:
            curr_line += line
 
if curr_line != None:
    map_a_record(curr_line)