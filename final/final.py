import random
import sys
import re

MAX_URL_INDEX = 89997
HASH_NUMBER = 100
MAX_HASH_FACTOR = 1000000
BAND_SIZE = 10

def main_func(sparkContext, rdd, urlDict):
    f = open('result', 'w')
    initializeGlobalVariable(sparkContext, urlDict)
    f.write('1\n')
    userRdd = rdd.flatMap(urlMapper).groupByKey().mapValues(lambda x: set(x)).filter(lambda x: len(x[1]) > 10)
    f.write('2\n')
    bandRdd = userRdd.flatMap(bandMapper).groupByKey().filter(lambda x: len(x[1]) > 1)
    f.write('3\n')
    pairRdd = bandRdd.flatMap(pairMapper).distinct()
    f.write('4\n')
    resultRdd = pairRdd.join(userRdd).map(lambda x: (x[1][0], (x[0], x[1][1]))).join(userRdd).map(jaccardMapper)
    for t in resultRdd.top(500):
        f.write(str(t[0]) + ' ' + str(t[1][0]) + ' ' + str(t[1][1]) + '\n')
    f.close()

def initializeGlobalVariable(sparkContext, urlDict):
    if __name__ == '__main__':
        global URLS
        URLS = sparkContext.broadcast(urlDict)

        global HASHS
        hashs = random.sample(range(MAX_HASH_FACTOR), HASH_NUMBER)
        HASHS = sparkContext.broadcast(hashs)

def urlMapper(line):
    urlPattern = re.compile(r'((?<=GET\ ).+(?=\ HTTP/)|(?<=POST\ ).+(?=\ HTTP/)|(?<=HEAD\ ).+(?=\ HTTP/))')
    result = urlPattern.search(line)
    userId = int(line[:line.find(' ')])
    if result is not None:
        url = result.group()
        if url in URLS.value:
            return [(userId, URLS.value[url])]
        else:
            return []
    else:
        return []

def bandMapper((userId, urlSet)):
    minHashList = []
    for factor in HASHS.value:
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

def jaccardMapper((userId1, ((userId2, userSet2), userSet1))):
    intersection = userSet1.intersection(userSet2)
    jaccardValue = len(intersection) * 1.0 / (len(userSet1) + len(userSet2) - len(intersection))
    return (jaccardValue, (userId2, userId1))

from pyspark import SparkContext

if __name__ == '__main__':
    sc = SparkContext(appName='Co-occurrence')
    urlDict = {}
    f = open('object_mappings.sort', 'r')
    for line in f:
        line = line.strip()
        idx = line.find(' ')
        urlId = int(line[:idx])
        url = line[idx+1:].rstrip()
        urlDict[url] = urlId
    f.close()
    rdd = sc.textFile('test.txt')
    main_func(sc, rdd, urlDict)

