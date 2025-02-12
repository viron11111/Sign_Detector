#!/usr/bin/python

import numpy as np
import cv2
import math
import cv2.cv as cv # here

pic1 = 'ellipse.jpg'
pic2 = 'cruciform.jpg'
pic3 = 'triangle.jpg'

p1 = 100
p2 = 14
nr = 20
mr = 30

#*************************************************************************************************

img = cv2.imread(pic1, 0)
cimg = cv2.imread(pic1)
#cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

width = img.shape[0]/2
length = img.shape[1]/2   

circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1, width, param1=p1,param2=p2,minRadius=nr,maxRadius=mr)
print circles

if circles != None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('ellipse', cimg)
#*************************************************************************************************

img = cv2.imread(pic2, 0)
cimg = cv2.imread(pic2)
#cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

width = img.shape[0]/2
length = img.shape[1]/2   

circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1, width, param1=p1,param2=p2,minRadius=nr,maxRadius=mr)
print circles

if circles != None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('cruciform', cimg)
#*************************************************************************************************

img = cv2.imread(pic3, 0)
cimg = cv2.imread(pic3)
#cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

width = img.shape[0]/2
length = img.shape[1]/2   

circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1, width, param1=p1,param2=p2,minRadius=nr,maxRadius=mr)
print circles

if circles != None:
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('triangle', cimg)

cv2.moveWindow('ellipse', 20, 20)
cv2.moveWindow('cruciform', 20, 180)
cv2.moveWindow('triangle', 20, 340)

cv2.waitKey(0)
cv2.destroyAllWindows()
