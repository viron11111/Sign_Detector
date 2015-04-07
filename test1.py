#!/usr/bin/python

import numpy as np
import cv2
from matplotlib import pyplot as plt

i = 0
j = 0
corner = []

img = cv2.imread('dock.jpg')
img_real = cv2.imread('dock.jpg')
imgblur = cv2.medianBlur(img,9)

imgray = cv2.cvtColor(imgblur,cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(imgray,240,255,cv2.THRESH_TOZERO)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

while i < len(contours):

	cnt = contours[i]

	M = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	#print area	

	if area >= 2000:

		epsilon = 0.1*cv2.arcLength(cnt,True)
		approx = cv2.approxPolyDP(cnt,epsilon,True)
		x,y,w,h = cv2.boundingRect(approx)
		corner.append(x)
		corner.append(y)
		corner.append(w)
		corner.append(h)

		j += 1
				
		cv2.rectangle(img_real,(x,y),(x+w,y+h),(0,255,0),2)	

	i += 1

one = img[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
two = img[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
three = img[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
one_a = img_real[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
two_a = img[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
three_a = img[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]

#**********************************************************************************************
imgray = cv2.cvtColor(one_a,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_TOZERO_INV)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
i = 0
area_max = 0.0

while i < len(contours):

	cnt = contours[i]

	M = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	if area > area_max:
		area_max = area
		hold = i
	i += 1

print len(contours[hold])
cnt = contours[hold]
cv2.drawContours(one, [cnt], 0, (0,255,0), 1)

#**********************************************************************************************

imgray = cv2.cvtColor(two_a,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_TOZERO_INV)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
i = 0
area_max = 0.0

while i < len(contours):

	cnt = contours[i]

	M = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	if area > area_max:
		area_max = area
		hold = i
	i += 1

print len(contours[hold])
cnt = contours[hold]
cv2.drawContours(two, [cnt], 0, (0,255,0), 1)

#**********************************************************************************************

imgray = cv2.cvtColor(three_a,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_TOZERO_INV)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
i = 0
area_max = 0.0

while i < len(contours):

	cnt = contours[i]

	M = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	if area > area_max:
		area_max = area
		hold = i
	i += 1

print len(contours[hold])
cnt = contours[hold]
cv2.drawContours(three, [cnt], 0, (0,255,0), 1)

#**********************************************************************************************

title = ['full image', 'Sign1', 'Sign2', 'Sign3']

image = [img_real, one, two, three]

for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(image[i],'gray')
    plt.title(title[i])
    plt.xticks([]),plt.yticks([])

plt.show()
