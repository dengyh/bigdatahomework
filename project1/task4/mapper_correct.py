#!/usr/bin/python
import sys
 
#id title   tagnames    author_id   body    node_type   parent_id   abs_parent_id   added_at    score   state_string    last_edited_id  last_activity_by_id last_activity_at    active_revision_id  extra   extra_ref_id    extra_count marked
 
 
item_count = 19
curr_line = ""
 
def dequote(t):
    if t.startswith("\"") and t.endswith("\""):
        return t[1:-1]
    else:
        return t
 
def map_a_record(curr_line):
    items = curr_line.replace("\n"," ").split("\t")
    if len(items) != item_count:
        return
     
    id = dequote(items[0])
    abs_parent_id = dequote(items[7])
    node_type = dequote(items[5])
    author_id = dequote(items[3])
    if node_type not in ["question", "answer", "comment"]:
        return
     
    if node_type == "question":
        print "{0}\t{1}".format(id, author_id)
    elif node_type == "answer":
        print "{0}\t{1}".format(abs_parent_id, author_id)
    elif node_type == "comment":
        print "{0}\t{1}".format(abs_parent_id, author_id)
 
for line in sys.stdin:
     
    items = line.split("\t")
    if len(items)>4 and dequote(items[0]).isdigit() and dequote(items[3]).isdigit():
        # A new record
        if curr_line != None and curr_line != "":
            map_a_record(curr_line)
        curr_line = line
    else:
        curr_line += line
 
if curr_line != None and curr_line != "":
    map_a_record(curr_line)