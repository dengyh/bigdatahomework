def mapper(line):
    datas = line.strip().split(' ')
    language, title, count = datas[1], datas[2], int(datas[3])
    return (language + '\t' + title, count)

def reducer(x, y):
    return x + y

def keyFunc(value):
    return -int(value[1])

def main(rdds):
    mainRdd = rdds[0]
    for index in xrange(1, len(rdds)):
        mainRdd = mainRdd.union(rdds[index])
    for result in firstRdd.map(mapper).reduceByKey(reducer).takeOrdered(10, key=keyFunc):
        print result[0] + '\t' + str(result[1])