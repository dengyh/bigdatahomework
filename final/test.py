import random
import sys
import time
import re

hashA = [random.randint(0, sys.maxint) for _ in xrange(100)]
hashB = [random.randint(0, sys.maxint) for _ in xrange(100)]

a = random.sample(range(100), 80)
b = random.sample(range(100), 80)

def minhash(lista, listb):
    count = 0
    for i in xrange(1000):
        temp = range(100)
        random.shuffle(temp)
        for num in temp:
            if num not in lista and num not in listb:
                continue
            if num in lista and num in listb:
                count += 1
                break
            else:
                break
    print count * 1.0 / 1000

def minhash_pro():
    count = 0
    sigA = []
    sigB = []
    for i in xrange(100):
        sigA.append(min([(num * hashA[i] + hashB[i]) % 10000 for num in a]))
        sigB.append(min([(num * hashA[i] + hashB[i]) % 10000 for num in b]))
    minhash(sigA, sigB)

def jaccard():
    countA = 0
    countB = 0
    for i in xrange(100):
        if i in a and i in b:
            countA += 1
        if i in a or i in b:
            countB += 1
    print countA * 1.0 / countB

def test():
    start = time.time()
    for i in xrange(100000000):
        a = 500 / 4 * 3
    end = time.time()
    print end - start

def test2():
    urlPattern = re.compile(r'((?<=GET\ ).+(?=\ HTTP/)|(?<=POST\ ).+(?=\ HTTP/))')
    text = '9719 - - [30/Apr/1998:21:31:19 +0000] "GET /french/splash_inet.html HTTP/1.0" 200 3781'
    result = urlPattern.search(text)
    print result.group()

def test3((a, (b, c))):
    print a, b, c

test3((1, (2, 3)))