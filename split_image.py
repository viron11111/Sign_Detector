#!/usr/bin/python

import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons
import math

i = 0
j = 0
corner = []

sign = [0,0,0]
cnt_hold = [0,0,0]

font = cv2.FONT_HERSHEY_SIMPLEX

pic = 'three_a.jpg'
#pic = 'Cruciform.jpg'
#pic = 'cross_red.png'
blank = cv2.imread('blank.jpg')

img = cv2.imread(pic)
img_real = cv2.imread(pic)
img_clear = cv2.imread(pic)

imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#imgray = cv2.medianBlur(imgray,3)

#kernel = np.ones((3,3),np.uint8)
#imgray = cv2.erode(imgray,kernel,iterations = 1)
#imgray = cv2.dilate(imgray,kernel,iterations = 1)

distance_from_center = 20

title = ['triangle', 'bar']

image = [img_real]

plt.subplot()
fig = plt.imshow(image[0],'gray')
plt.subplots_adjust(left=0.25, bottom=0.25)

axcolor = 'lightgoldenrodyellow'
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
slider_value = Slider(axfreq, 'Threshold value', 0, 10, valinit=10)

fig = plt.subplot()

def update(val):
    
    img_real = cv2.imread(pic)
    blank = cv2.imread('blank.jpg')

    t_val = slider_value.val

    imgray = cv2.cvtColor(img_real,cv2.COLOR_BGR2GRAY)
    imgray = cv2.medianBlur(imgray,3)

    #kernel = np.ones((3,3),np.uint8)
    #imgray = cv2.erode(imgray,kernel,iterations = 1)
    #imgray = cv2.dilate(imgray,kernel,iterations = 1)

    #kernel = np.ones((3,3),np.float32)/25
    #imgray = cv2.filter2D(imgray,-1,kernel) 

    #gray = np.float32(imgray)
    #dst = cv2.cornerHarris(gray,2,3,.001)
    #dst = cv2.dilate(dst,None)
    #dst = cv2.erode(dst,None)

    #kernel = np.ones((3,3),np.float32)/25
    #imgray = cv2.filter2D(imgray,-1,kernel)    

    ret,thresh = cv2.threshold(imgray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    ret,test = cv2.threshold(imgray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    width = imgray.shape[0]/2
    length = imgray.shape[1]/2

    biggest_area = 0
    biggest_cnt = [0]
    biggest_M = [0]
    biggest_approx = [0]
    cxmax = 0
    cymax = 0

    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.1*cv2.arcLength(cnt,True),True)

        M = cv2.moments(approx)

        if M['m00'] != 0.0:
            area = cv2.contourArea(approx)
	
			
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])

            d = math.sqrt((length-cx)*(length-cx) + (width-cy)*(width-cy))

            if area >= biggest_area and d < distance_from_center:
                biggest_area = area
                biggest_cnt[0] = cnt
                cxmax = cx
                cymax = cy
        if biggest_area != 0:
            #print len(biggest_cnt[0])

            cv2.drawContours(blank,[biggest_cnt[0]],0,(0,0,255),1)
            cv2.circle(img_real,(cxmax,cymax), 1, (0,255,0),-1)

            if len(biggest_cnt[0])==3:
                cv2.putText(img_real, "triangle", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
            elif (len(biggest_cnt[0]) == 12 or len(biggest_cnt[0]) == 24): 
                cv2.putText(img_real, "cruciform", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
            elif len(biggest_cnt[0]) >= 17:
                cv2.putText(img_real, "circle", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
            else:	
                cv2.putText(img_real, "None", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)

            cv2.circle(img_real,(length,width), 1, (255,255,0),-1)
            
            blank_gray = cv2.cvtColor(blank,cv2.COLOR_BGR2GRAY)
            
            dst = cv2.goodFeaturesToTrack(blank_gray,25,0.15,10)
            dst = np.int0(dst)

            for i in dst:
                x,y = i.ravel()
                cv2.circle(blank_gray,(x,y),4,0,-1)
            print len(dst)


            plt.imshow(blank_gray,'gray')
    #fig.canvas.draw_idle()
slider_value.on_changed(update)


plt.show()
