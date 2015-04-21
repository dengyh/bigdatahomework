#!/usr/bin/python

import sys
import random

for line in sys.stdin:
    number = random.randint(1, 100)
    if number != 1:
        continue
    price = line.strip().split('\t')[4]
    print price
