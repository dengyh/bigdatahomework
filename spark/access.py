import re

urlPattern = re.compile(r'(?<=").+(?=")')

def mapper(line):
    url = urlPattern.search(line)
    datas = line.strip().split(' ')
    return (url.group().strip(), datas[0])

def keyFunc(values):
    return values[1]

def mapper2(values):
    return (values[0], len(values[1]))

def main(rdd):
    for result in rdd.map(mapper).distinct().groupByKey().map(mapper2).takeOrdered(20, key=keyFunc):
        print result[0] + '\t' + str(result[1])