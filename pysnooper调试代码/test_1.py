#!/usr/bin/env python

import pysnooper

@pysnooper.snoop()
def number_to_bits(number):
    if number:
        bits = []
        while number:
            number, remainder = divmod(number, 2)
            bits.insert(0, remainder)
        return bits
    else:
        return [0]

#number_to_bits(6)

@pysnooper.snoop()
def handle():
    for i in range(100):
        print(i)
        pass

handle()
