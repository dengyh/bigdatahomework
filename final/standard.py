import os, sys
from random import randrange
 
def url_to_id_mapper(line):
    # 51678 - - [01/Jun/1998:22:00:01 +0000] "GET /english/teams/relatedtem_138.htm HTTP/1.0" 200 5461
    
    idx = line.find(" ")
    assert (idx!=-1)
    user_idx = int(line[:idx])
    
    idx1 = line.find("\"GET")
    offset=5
    if idx1==-1:
        idx1 = line.find("\"POST")
        offset=6
    if idx1==-1:
        idx1 = line.find("\"HEAD")
        offset=6
        
    idx2 = line.rfind("HTTP")
    if idx1==-1 or idx2==-1:
        return []
    URL = line[idx1+offset:idx2-1]
    
    if not URL in shared_dict.value:
        return []
    else:
        return [(user_idx, shared_dict.value[URL])]
    
MAX_INDEX = 89997
num_hashes = 100
num_per_band = 20
 
def min_hash_fn(a, b, sig):
    hashes = [((a * x) + b) % MAX_INDEX for x in sig]
    return min(hashes)
 
def get_min_hash_row(sig):
    hashes = [min_hash_fn(a, b, sig) for a, b in zip(shared_a_hash.value, shared_a_hash.value)]
    return hashes
 
def get_band(l, n):
    for i in xrange(0, len(l), n):
        yield frozenset(l[i:i+n])
 
def minhash_signature_mapper(x):
    min_hash_row = get_min_hash_row(x[1])
    banded = get_band(min_hash_row, num_per_band)
    
    result = []
    for band_id, band in enumerate(banded):
        key = (band_id, hash(band))
        result.append( (key, x[0]) )
    return result
 
def generate_candidates(x):
    l = list(x[1])
    result = []
    for i in range(0, len(l)):
        for j in range(i+1, len(l)):
            if l[i]>l[j]:
               result.append((l[j], l[i]))
            else:
               result.append((l[i], l[j]))
    return result    
 
def mapper(x):
    user_idx1 = x[0]
    user_idx2 = x[1][0]
    user_idx1_url_ids = x[1][1]
    return (user_idx2, (user_idx1, user_idx1_url_ids))
 
def final_mapper(x):
    user_idx2 = x[0]
    (user_idx1, user_idx1_url_ids) = x[1][0]
    user_idx2_url_ids = x[1][1]
    
    s = len(user_idx1_url_ids.intersection(user_idx2_url_ids))
    s1 = len(user_idx1_url_ids)
    s2 = len(user_idx2_url_ids)
    
    if s==s1 and s==s2:
        jaccard = -1
    else:
        jaccard = float(s)/float(s1+s2-s)
    return (jaccard, (user_idx1, user_idx2))
    
PAGE_VISIT_THRESHOLD = 10
 
def main_func(sc, rdd, url_dict):
    
    # Share the minhasher 
    if __name__ == "__main__":
        # Only run this on the driver node
        global shared_dict
        shared_dict = sc.broadcast(url_dict)
        a_hash = [randrange(sys.maxint) for _ in xrange(0, num_hashes)]
        b_hash = [randrange(sys.maxint) for _ in xrange(0, num_hashes)]
        
        global shared_a_hash
        global shared_b_hash
        shared_a_hash = sc.broadcast(a_hash)
        shared_b_hash = sc.broadcast(b_hash)
    
    # key: user_idx, value: a list of url_idx
    rdd2 = rdd.flatMap(url_to_id_mapper).distinct().groupByKey().filter(lambda x: len(x[1])>PAGE_VISIT_THRESHOLD)
    
    # key: cluster id, value: a list of user_idx in this cluster
    rdd3 = rdd2.flatMap(minhash_signature_mapper).groupByKey().filter(lambda x: len(x[1])>1)
    
    # key: user id1, value: user id2
    rdd4 = rdd3.flatMap(generate_candidates).distinct()
    
    # key: jacard-similarity, value: user pair
    rddx = rdd2.mapValues(lambda x: set(x))
    rdd5 = rdd4.join(rddx).map(mapper).join(rddx).map(final_mapper)
    
    for t in rdd5.top(500):
        print "%.3f"%(t[0])+"\t"+str(t[1][0])+"\t"+str(t[1][1])
