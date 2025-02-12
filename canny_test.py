#!/usr/bin/python

import numpy as np
import cv2
from matplotlib import pyplot as plt

img_triangle = cv2.imread('triangle_black.png', 0)
img = cv2.imread('triangle_black.png', 0)

edges2 = cv2.Canny(img_triangle,0,0)
contours,hierarchy = cv2.findContours(edges2,1,2)

for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
        if len(approx)==3:
            cv2.drawContours(img,[cnt],0,(0,255,0),2)
            tri = approx

for vertex in tri:
    cv2.circle(img,(vertex[0][0],vertex[0][1]),5,255,-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
