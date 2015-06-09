import random
import sys
import re

MAX_URL_INDEX = 89997
HASH_NUMBER = 100
MAX_HASH_FACTOR = sys.maxint / MAX_URL_INDEX
BAND_SIZE = 20
MOD_NUMBER = 1000000

def main_func(sparkContext, rdd, urlDict):
    initializeGlobalVariable(sparkContext, urlDict)
    userRdd = rdd.flatMap(urlMapper).groupByKey().mapValues(lambda x: set(x)).filter(lambda x: len(x[1]) > 10)
    bandRdd = userRdd.flatMap(bandMapper).groupByKey()
    pairRdd = bandRdd.flatMap(pairMapper).distinct()
    resultRdd = pairRdd.join(userRdd).map(lambda x: (x[1][0], (x[0], x[1][1]))).join(userRdd).flatMap(jaccardMapper).top(1000)

    for item in resultRdd:
        print '%.5f\t%d\t%d' % (item[0], item[1][0], item[1][1])

def initializeGlobalVariable(sparkContext, urlDict):
    if __name__ == '__main__':
        global URLS
        URLS = sparkContext.broadcast(urlDict)

        global KHASHS
        global BHASHS
        kHashs = list(getRandomList(MAX_HASH_FACTOR, HASH_NUMBER))
        bHashs = list(getRandomList(MAX_HASH_FACTOR, HASH_NUMBER))
        KHASHS = sparkContext.broadcast(kHashs)
        BHASHS = sparkContext.broadcast(bHashs)

def getRandomList(upper, num):
    for i in xrange(num):
        yield random.randint(0, upper)

def urlMapper(line):
    urlPattern = re.compile(r'((?<=GET\ ).+(?=\ HTTP/)|(?<=POST\ ).+(?=\ HTTP/)|(?<=HEAD\ ).+(?=\ HTTP/))')
    result = urlPattern.search(line)
    userId = int(line[:line.find(' ')])
    if result is not None:
        url = result.group()
        if url in URLS.value:
            yield (userId, URLS.value[url])

def bandMapper((userId, urlSet)):
    minHashList = []
    size = len(KHASHS.value)
    for index in xrange(size):
        k = KHASHS.value[index]
        b = BHASHS.value[index]
        minHashList.append(min([(k * x + b) % MAX_URL_INDEX for x in urlSet]))
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

def jaccardMapper((userId2, ((userId1, userSet1), userSet2))):
    if userSet1 != userSet2:
        intersection = userSet1.intersection(userSet2)
        jaccardValue = len(intersection) * 1.0 / (len(userSet1) + len(userSet2) - len(intersection))
        yield (jaccardValue, (userId1, userId2))
