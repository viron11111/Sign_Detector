#!/usr/bin/python

import numpy as np
import cv2
import math
import cv2.cv as cv
import colorsys
import time

sign = [0,0,0]
cnt_hold = [0,0,0]

vid = 'Dock_Simulation_30_degrees.avi'
vid = '/home/andy/dock_simulation_vertical.avi'

cap = cv2.VideoCapture(vid)

while(cap.isOpened()):
    ret, frame = cap.read()
    ret, frame_real = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray = cv2.medianBlur(gray,9)
    #cv2.imshow('distort', imgray)
    ret,thresh = cv2.threshold(imgray,240,255,cv2.THRESH_TOZERO)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    i = 0

    sign = [0,0,0]

    while i < len(contours):
        
        cnt = contours[i]

        M = cv2.moments(cnt)
        area = cv2.contourArea(cnt)

        if area >= sign[0]:
            sign[2] = sign[1]
            cnt_hold[2] = cnt_hold[1]
            sign[1] = sign[0]
            cnt_hold[1] = cnt_hold[0]
            sign[0] = area
            cnt_hold[0] = cnt
        elif area >= sign[1]:
            sign[2] = sign[1]
            cnt_hold[2] = cnt_hold[1]
            sign[1] = area
            cnt_hold[1] = cnt
        elif area >= sign[2]:
            sign[2] = area
            cnt_hold[2] = cnt
	
        i += 1

    i = 0
    corner = []    
    for i in xrange(3):
        epsilon = 0.1*cv2.arcLength(cnt_hold[i],True)
        approx = cv2.approxPolyDP(cnt_hold[i],epsilon,True)
        x,y,w,h = cv2.boundingRect(approx)
        corner.append(x)
        corner.append(y)
        corner.append(w)
        corner.append(h)

        cv2.rectangle(frame_real,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.circle(frame_real,(x,y), 2, (128,0,0),-1)
