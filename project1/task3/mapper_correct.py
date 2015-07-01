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
    node_type = dequote(items[5])
    #assert(node_type in ["question", "answer", "comment"])
    if node_type == "question":
        tagnames = dequote(items[2])
        for tag in tagnames.split():
            print "0\t{0}\t{1}".format(tag, 1)
 
for line in sys.stdin:
 
    items = line.split("\t")
    if len(items)>4 and dequote(items[0]).isdigit() and dequote(items[3]).isdigit():
        # A new record
        if curr_line != None:
            map_a_record(curr_line)
        curr_line = line
    else:
        if curr_line!=None:
            curr_line += line
 
if curr_line != None:
    map_a_record(curr_line)