#!/usr/bin/python

import numpy as np
import cv2
import math
import cv2.cv as cv
import colorsys

pic = "three_a.jpg"

img = cv2.imread(pic)
img_true = cv2.imread(pic)

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

biggest_area = 0
biggest_cnt = [0]
biggest_M = [0]
biggest_approx = [0]
cxmax = 0
cymax = 0

distance_from_center = 20

height = imgray.shape[0]
width  = imgray.shape[1]

width_cent = width/2
height_cent = height/2

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)

    M = cv2.moments(approx)

    if M['m00'] != 0.0:
        area = cv2.contourArea(approx)	

        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])

        d = math.sqrt((width_cent-cx)*(width_cent-cx) + (height_cent-cy)*(height_cent-cy))
        
        #if area >= 1000:

            #print d 

        if area >= biggest_area and d < distance_from_center:
            biggest_area = area
            biggest_cnt[0] = cnt
            cxmax = cx
            cymax = cy
            #print biggest_area
if biggest_area != 0:

    #cv2.drawContours(img_true, [biggest_cnt[0]], 0,(0,0,255),1)

    for h,cnt in enumerate(biggest_cnt[0]):
        mask = np.zeros(imgray.shape,np.uint8)
        cv2.drawContours(mask,[biggest_cnt[0]],0,255,-1)
        mean = cv2.mean(img_true,mask = mask)

#print mean
mean = colorsys.rgb_to_hsv(mean[2]/255, mean[1]/255, mean[0]/255)
hsv = list(mean)
hsv[0] = hsv[0]*360
print hsv

if hsv[2] < 0.1:
    color = 'black'
elif (hsv[0]<11 or hsv[0]>351) and hsv[1]>.7 and hsv[2]>.1:
    color = 'red'
elif (hsv[0]>64 and hsv[0]<150) and hsv[1]>.15 and hsv[2]>.1:
    color = 'green'
elif (hsv[0]>180 and hsv[0]<255) and hsv[1]>.15 and hsv[2]>.1:
    color = 'blue'
else:
    color = 'unknown'

print color

#cv2.imshow('image', mask)
#cv2.namedWindow('image', cv2.CV_WINDOW_AUTOSIZE)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
