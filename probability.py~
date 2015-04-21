#!/usr/bin/python

import numpy as np
import cv2
import math
import cv2.cv as cv
import colorsys
import time

def find_prob(sign1):
    probability_sum = sign1['circle']+sign1['triangle']+sign1['cruciform']
    sign1_probability = {'circle': sign1['circle']/probability_sum, 'triangle':sign1['triangle']/probability_sum, 'cruciform':sign1['cruciform']/probability_sum}
    return sign1_probability

sign1 = 'triangle'

sign1_sum = {'circle': 1.0, 'triangle': 2.0, 'cruciform': 3.0} #starting values

sign1_sum[sign1] = sign1_sum[sign1] + 1 #+1 for each frame

#sign1_sum = dict(sign1_id.items() + sign1_sum.items())

#print sign1_sum
print find_prob(sign1_sum)



