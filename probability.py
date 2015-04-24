#!/usr/bin/python

import numpy as np
import cv2
import math
import cv2.cv as cv
import colorsys
import time
import operator

def find_prob(result):

    probability_sum = result['circle']+result['triangle']+result['cruciform']

    if probability_sum > 0.0:
        sign_probability = {'circle': result['circle']/probability_sum, 'triangle':result['triangle']/probability_sum, 'cruciform':result['cruciform']/probability_sum}
    else:
        sign_probability = {'circle': 0.0, 'triangle': 0.0, 'cruciform': 0.0}
    return sign_probability

def find_highest_percentage(percentages):
    most_likely = max(percentages, key=percentages.get)
    prcnt = percentages[most_likely]
    
    return most_likely, prcnt

def add_sign(sign, sign_sum):

    for number in reversed(xrange(9)):      #shift everything left by one
        sign_sum[number + 1] = sign_sum[number]

    sign_sum[0] = {'circle': 0.0, 'triangle': 0.0, 'cruciform': 0.0}     #set first dictionary to zero

    if sign != 'none':
        sign_sum[0][sign] = sign_sum[0][sign] + 1.0

    result = {}
    for myDict in sign_sum:
        for key, value in myDict.items():
            result.setdefault(key, 0)
            result[key] += value

    percentage = find_prob(result)
    sign,prcnt = find_highest_percentage(percentage)
    return sign, prcnt, result




sign1 = 'none'

#***************************************  fill up blank dictionary *************************************
i = 0
sign1_sum = []

for i in xrange(10):
    sign1_sum.append({'circle': 0.0, 'triangle': 0.0, 'cruciform': 0.0})

#***********************************************  Add up all circles, triangles, cruciforms  ***************
"""result = {}
for myDict in sign1_sum:
    for key, value in myDict.items():
        result.setdefault(key, 0)
        result[key] += value"""

symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'circle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'none'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'none'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'none'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'none'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)
sign1 = 'triangle'
symbol, percentage, sign_sum = add_sign(sign1, sign1_sum)

print symbol
print percentage
print sign_sum










