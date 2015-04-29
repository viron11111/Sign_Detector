#!/usr/bin/python

import numpy as np
import cv2
import math
import cv2.cv as cv
import colorsys
import time

vid = 'Dock_Simulation_30_degrees.avi'
vid = '/home/andy/dock_simulation_vertical.avi'
vid = 'In_lab_test1.mp4'
vid = 'In_lab_test2.mp4'
#vid = 'In_lab_test3.mp4'
vid = 'In_lab_test4.mp4'
vid = 'In_lab_test5.mp4'

cap = cv2.VideoCapture(vid)

while(cap.isOpened()):
    ret, frame = cap.read()
    ret, frame_real = cap.read()

    height = frame_real.shape[0]
    width  = frame_real.shape[1]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray = cv2.medianBlur(gray,9)
    #cv2.imshow('distort', imgray)
    ret,thresh = cv2.threshold(imgray,220,255,cv2.THRESH_TOZERO)
    #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.imshow('actual', gray)
    """cv2.imshow('two', sign2[1])
    cv2.imshow('one', sign1[1])
    cv2.imshow('three', sign3[1])
    cv2.moveWindow('one', 20, 20)
    cv2.moveWindow('two', 20, 180)
    cv2.moveWindow('three', 20, 340)"""
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
