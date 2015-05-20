def insert(item, sortedList):
    index = len(sortedList)
    while index > 0 and item[2] < sortedList[index - 1][2]:
        index -= 1
    if index < 20:
        if len(sortedList) >= 20:
            sortedList.pop()
        sortedList.insert(index, item)
        return False
    return True

def mapper(line):
    datas = line.split(' ')
    language, title, count = datas[1], datas[2], int(datas[3])
    return (language + '\t' + title, count)

def reducer(x, y):
    return x + y

def filter1(values):
    return values[1] >= 10000

def main(rdds):
    mainRdd = rdds[0]
    for index in xrange(1, len(rdds)):
        mainRdd = mainRdd.union(rdds[index])
    items = mainRdd.map(mapper).reduceByKey(reducer).filter(filter1).sortBy(lambda x: x[1]).collect()
    sortedList = []
    length = len(items)
    for index in xrange(length - 1):
        for diff in xrange(1, 21):
            if index + diff < length:
                flag = insert((items[index + diff], items[index], items[index + diff][1] - items[index][1]), sortedList)
                if flag:
                    break
            else:
                break
    for result in sortedList:
        print result[0][0] + '\t' + str(result[0][1]) + '\t' + result[1][0] + '\t' + str(result[1][1])