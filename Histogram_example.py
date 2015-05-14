#!/usr/bin/python

import numpy as np
import cv2
import math
import cv2.cv as cv
import colorsys
import time

#img = cv2.imread('wiki.jpg',0)

vid = 'Dock_Simulation_30_degrees.avi'
vid = '/home/andy/dock_simulation_vertical.avi'
vid = 'In_lab_test1.mp4'
vid = 'In_lab_test2.mp4'
#vid = 'In_lab_test3.mp4'
vid = 'In_lab_test4.mp4'
#vid = 'In_lab_test5.mp4'

cap = cv2.VideoCapture(vid)

while(cap.isOpened()):

    ret, frame = cap.read()
    ret, frame_real = cap.read()

    height = frame_real.shape[0]
    width  = frame_real.shape[1]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    imgray = cv2.medianBlur(gray,9)

    ret,thresh = cv2.threshold(imgray,240,255,cv2.THRESH_TOZERO)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    i = 0

    sign = [0,0,0,0,0,0]
    cnt_hold = [0,0,0,0,0,0]

    while i < len(contours):
        
        cnt = contours[i]

        M = cv2.moments(cnt)
        area = cv2.contourArea(cnt)

        if area >= sign[0]:
            sign[5] = sign[4]
            cnt_hold[5] = cnt_hold[4]
            sign[4] = sign[3]
            cnt_hold[4] = cnt_hold[3]
            sign[3] = sign[2]
            cnt_hold[3] = cnt_hold[2]
            sign[2] = sign[1]
            cnt_hold[2] = cnt_hold[1]
            sign[1] = sign[0]
            cnt_hold[1] = cnt_hold[0]
            sign[0] = area
            cnt_hold[0] = cnt
        elif area >= sign[1]:
            sign[5] = sign[4]
            cnt_hold[5] = cnt_hold[4]
            sign[4] = sign[3]
            cnt_hold[4] = cnt_hold[3]
            sign[3] = sign[2]
            cnt_hold[3] = cnt_hold[2]
            sign[2] = sign[1]
            cnt_hold[2] = cnt_hold[1]
            sign[1] = area
            cnt_hold[1] = cnt
        elif area >= sign[2]:
            sign[5] = sign[4]
            cnt_hold[5] = cnt_hold[4]
            sign[4] = sign[3]
            cnt_hold[4] = cnt_hold[3]
            sign[3] = sign[2]
            cnt_hold[3] = cnt_hold[2]
            sign[2] = area
            cnt_hold[2] = cnt
        elif area >= sign[3]:
            sign[5] = sign[4]
            cnt_hold[5] = cnt_hold[4]
            sign[4] = sign[3]
            cnt_hold[4] = cnt_hold[3]
            sign[3] = area
            cnt_hold[3] = cnt
        elif area >= sign[4]:
            sign[5] = sign[4]
            cnt_hold[5] = cnt_hold[4]
            sign[4] = area
            cnt_hold[4] = cnt
        elif area >= sign[5]:
            sign[5] = area
            cnt_hold[5] = cnt
	
        i += 1

    i = 0
    corner = []    
    no_of_signs = 0
    avg_area = np.mean(sign)

    no_of_signs = 0
    coordsx = []
    coordsy = []
    z = 0
    j = 0

    for i in xrange(6):

        #check if centroids of moments are close to each other
        #************************************************************************************
        same_moment = 0
        M = cv2.moments(cnt_hold[i])

        if (M['m00'] != 0.0):
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        else:
            cx = 0
            cy = 0

        d = []

        numbers = len(coordsx)

        for z in xrange(numbers):
            d.append(int(math.sqrt((coordsx[z-1]-cx)*(coordsx[z-1]-cx) + (coordsy[z-1]-cy)*(coordsy[z-1]-cy))))
        
        for j in d:
            if j < 60:
                same_moment += 1
        #************************************************************************************
        if (M['m00'] != 0.0):  
            epsilon = 0.1*cv2.arcLength(cnt_hold[i],True)
            approx = cv2.approxPolyDP(cnt_hold[i],epsilon,True)
            x,y,w,h = cv2.boundingRect(approx)
            
            #check for white signs
            if y < (height/2 + 300) and y > (height/2 - 300) and same_moment == 0:  #y values viewing area, greater values = more search area
                coordsx.append(cx) #append for centroid distance checking
                coordsy.append(cy) #append for centroid distance checking       
                corner.append(x)
                corner.append(y)
                corner.append(w)
                corner.append(h)

                cv2.rectangle(frame_real,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.circle(frame_real,(x,y), 2, (128,0,0),-1)
                no_of_signs += 1


    #if there are no signs or less than three signs visible
    if no_of_signs == 2:
            x,y,w,h = width,height,0,0
            corner.append(x)
            corner.append(y)
            corner.append(w)
            corner.append(h)
    elif no_of_signs == 1:
            x,y,w,h = width,height,0,0
            corner.append(x)
            corner.append(y)
            corner.append(w)
            corner.append(h)
            x,y,w,h = width,height,0,0
            corner.append(x)
            corner.append(y)
            corner.append(w)
            corner.append(h)
    elif no_of_signs == 0:
            x,y,w,h = width,height,0,0
            corner.append(x)
            corner.append(y)
            corner.append(w)
            corner.append(h)
            x,y,w,h = width,height,0,0
            corner.append(x)
            corner.append(y)
            corner.append(w)
            corner.append(h)
            x,y,w,h = width,height,0,0
            corner.append(x)
            corner.append(y)
            corner.append(w)
            corner.append(h)

    cv2.imshow('actual', frame_real)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
