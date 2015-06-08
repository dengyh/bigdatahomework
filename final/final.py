import random
import sys
import re

MAX_URL_INDEX = 89997
HASH_NUMBER = 100
MAX_HASH_FACTOR = sys.maxint / MAX_URL_INDEX
BAND_SIZE = 20

def main_func(sparkContext, rdd, urlDict):
    initializeGlobalVariable(sparkContext)
    userRdd = rdd.map(urlMapper).groupByKey().mapValues(lambda x: set(x)).filter(lambda x: len(x[1]) > 10)
    bandRdd = rdd2.flatMap(bandMapper).groupByKey().filter(lambda x: len(x[1]) > 1)
    pairRdd = rdd3.flatMap(pariMapper).distinct()
    resultRdd = pariRdd.join(userRdd).map(lambda x: (x[1][0], (x[0], x[1][1]))).join(userRdd).map(jaccardMapper)

def initializeGlobalVariable(sparkContext, urlDict):
    if __name__ == '__main__':
        global URLS
        URLS = sparkContext.broadcast(urlDict)

        global HASHS
        hashs = random.sample(range(MAX_HASH_FACTOR), HASH_NUMBER)
        HASHS = sparkContext.broadcast(hashs)

def urlMapper(line):
    urlPattern = re.compile(r'((?<=GET\ ).+(?=\ HTTP/)|(?<=POST\ ).+(?=\ HTTP/))')
    result = urlPattern.search(line)
    userId = int(line[:line.find(' ')])
    return (userId, URLS.value[result.group()])

def bandMapper((userId, urlSet)):
    minHashList = []
    for factor in HASHS:
        minHashList.append(min([factor * x for x in urlSet]))
    bands = [tuple(minHashList[i:i+BAND_SIZE]) for i in xrange(0, len(minHashList), BAND_SIZE)]
    for index in xrange(len(bands)):
        yield ((index, hash(bands[index])), userId)

def pairMapper((bandHash, userIterator)):
    userList = list(userIterator)
    for i in xrange(0, len(userList)):
        for j in xrange(i + 1, len(userList)):
            if userList[i] < userList[j]:
                yield (userList[i], userList[j])
            else:
                yield (userList[j], userList[i])

def jaccardMapper((userId1, (userId2, userSet2, userSet1))):
    intersection = userSet1.intersection(userSet2)
    jaccardValue = len(intersection) * 1.0 / (len(userSet1) + len(userSet2) - len(intersection))
    return (jaccardValue, (userId1, userId2)) 
