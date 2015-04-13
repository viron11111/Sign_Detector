#!/usr/bin/python

import numpy as np
import cv2
import math

font = cv2.FONT_HERSHEY_SIMPLEX

i = 0
j = 0
corner = []
distance_from_center = 20

sign = [0,0,0]
cnt_hold = [0,0,0]

vid = 'Dock_Simulation_30_degrees.avi'
#vid = '/home/andy/dock_simulation_vertical.avi'
cap = cv2.VideoCapture(vid)

while(cap.isOpened()):
    ret, frame = cap.read()
    ret, frame_real = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray = cv2.medianBlur(gray,9)
    ret,thresh = cv2.threshold(imgray,240,255,cv2.THRESH_TOZERO)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    i = 0

    sign = [0,0,0]

    while i < len(contours):
        
        cnt = contours[i]
	    #print cnt

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

    one_a = frame[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
    blank_one = np.zeros((corner[3],corner[2],3), np.uint8)
    blank_one[:,0:corner[2]] = (255,255,255)
        
    if (corner[0] < corner[4] and corner[0] < corner [8]):
        one_a = frame[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
        blank_one = np.zeros((corner[3],corner[2],3), np.uint8)
        blank_one[:,0:corner[2]] = (255,255,255)        
        cv2.putText(frame_real, "Sign1" , (corner[0], corner[1] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    elif (corner[0] > corner[4] and corner[0] > corner[8]):
        three_a = frame[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
        blank_three = np.zeros((corner[3],corner[2],3), np.uint8)
        blank_three[:,0:corner[2]] = (255,255,255)        
        cv2.putText(frame_real, "Sign3" , (corner[0], corner[1] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    else:
        two_a = frame[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
        blank_two = np.zeros((corner[3],corner[2],3), np.uint8)
        blank_two[:,0:corner[2]] = (255,255,255)        
        cv2.putText(frame_real, "Sign2" , (corner[0], corner[1] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
        

    if (corner[4] < corner[0] and corner[4] < corner [8]):
        one_a = frame[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
        blank_one = np.zeros((corner[7],corner[6],3), np.uint8)
        blank_one[:,0:corner[6]] = (255,255,255)
        cv2.putText(frame_real, "Sign1" , (corner[4], corner[5] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    elif (corner[4] > corner[0] and corner[4] > corner[8]):
        three_a = frame[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
        blank_three = np.zeros((corner[7],corner[6],3), np.uint8)
        blank_three[:,0:corner[6]] = (255,255,255)        
        cv2.putText(frame_real, "Sign3" , (corner[4], corner[5] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    else:
        two_a = frame[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
        blank_two = np.zeros((corner[7],corner[6],3), np.uint8)
        blank_two[:,0:corner[6]] = (255,255,255)        
        cv2.putText(frame_real, "Sign2" , (corner[4], corner[5] - 5), font, .75,(255,0,255),2, cv2.CV_AA)

    if (corner[8] < corner[4] and corner[8] < corner [0]):
        one_a = frame[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
        blank_one = np.zeros((corner[11],corner[10],3), np.uint8)
        blank_one[:,0:corner[10]] = (255,255,255)
        cv2.putText(frame_real, "Sign1" , (corner[8], corner[9] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    elif (corner[8] > corner[0] and corner[8] > corner[4]):
        three_a = frame[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
        blank_three = np.zeros((corner[11],corner[10],3), np.uint8)
        blank_three[:,0:corner[10]] = (255,255,255)
        cv2.putText(frame_real, "Sign3" , (corner[8], corner[9] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    else:
        two_a = frame[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
        blank_two = np.zeros((corner[11],corner[10],3), np.uint8)
        blank_two[:,0:corner[10]] = (255,255,255)
        cv2.putText(frame_real, "Sign2" , (corner[8], corner[9] - 5), font, .75,(255,0,255),2, cv2.CV_AA)

    #one = frame[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
    #two = frame[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
    #three = frame[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
    #two_a = frame[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
    #three_a = frame[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]

    #two_a = frame[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
    #blank_two = np.zeros((corner[7],corner[6],3), np.uint8)
    #blank_two[:,0:corner[6]] = (255,255,255)



#***************************************************************************************** One One One
    imgray = cv2.cvtColor(one_a,cv2.COLOR_BGR2GRAY)

    kernel = np.ones((5,5),np.float32)/25
    imgray = cv2.filter2D(imgray,-1,kernel)

    ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    width = imgray.shape[0]/2
    length = imgray.shape[1]/2    
        
    cv2.circle(frame_real,(length + corner[0],width + corner[1]), 2, (0,255,255),-1)

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

            cv2.drawContours(blank_one,[biggest_cnt[0]],0,(0,0,255),1)

            blank_gray1 = cv2.cvtColor(blank_one,cv2.COLOR_BGR2GRAY)
            
            dst = cv2.goodFeaturesToTrack(blank_gray1,25,0.15,10)
            dst = np.int0(dst)

            for i in dst:
                x,y = i.ravel()
                cv2.circle(blank_gray1,(x,y),4,0,-1)
            print len(dst)

            cv2.circle(frame_real,(cxmax + corner[0],cymax + corner[1]), 1, (0,255,0),-1)

            if len(dst)==3:
                cv2.putText(frame_real, "triangle", (cxmax + corner[0] - 20, cymax + corner[1] + 20), font, .5,(0,0,255),1, cv2.CV_AA)
            elif len(dst) == 12:
                cv2.putText(frame_real, "cruciform", (cxmax + corner[0] - 20, cymax + corner[1] + 20), font, .5,(0,0,255),1, cv2.CV_AA)
            else:
                cv2.putText(frame_real, "circle", (cxmax + corner[0] - 20, cymax + corner[1] + 20), font, .5,(0,0,255),1, cv2.CV_AA)                

#***************************************************************************************** Two Two Two

    imgray = cv2.cvtColor(two_a,cv2.COLOR_BGR2GRAY)

    kernel = np.ones((5,5),np.float32)/25
    imgray = cv2.filter2D(imgray,-1,kernel)

    ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    width = imgray.shape[0]/2
    length = imgray.shape[1]/2    
        
    cv2.circle(frame_real,(length + corner[4],width + corner[5]), 2, (0,255,255),-1)

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

            cv2.drawContours(blank_two,[biggest_cnt[0]],0,(0,0,255),1)

            blank_gray2 = cv2.cvtColor(blank_two,cv2.COLOR_BGR2GRAY)
            
            dst = cv2.goodFeaturesToTrack(blank_gray2,25,0.15,10)
            dst = np.int0(dst)

            for i in dst:
                x,y = i.ravel()
                cv2.circle(blank_gray2,(x,y),4,0,-1)
            print len(dst)

            cv2.circle(frame_real,(cxmax + corner[4],cymax + corner[5]), 1, (0,255,0),-1)

            if len(dst)==3:
                cv2.putText(frame_real, "triangle", (cxmax + corner[4] - 20, cymax + corner[5] + 20), font, .5,(0,0,255),1, cv2.CV_AA)
            elif len(dst) == 12:
                cv2.putText(frame_real, "cruciform", (cxmax + corner[4] - 20, cymax + corner[5] + 20), font, .5,(0,0,255),1, cv2.CV_AA)
            else:
                cv2.putText(frame_real, "circle", (cxmax + corner[4] - 20, cymax + corner[5] + 20), font, .5,(0,0,255),1, cv2.CV_AA) 

#***************************************************************************************** Two Two Two

    imgray = cv2.cvtColor(three_a,cv2.COLOR_BGR2GRAY)

    kernel = np.ones((5,5),np.float32)/25
    imgray = cv2.filter2D(imgray,-1,kernel)

    ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    width = imgray.shape[0]/2
    length = imgray.shape[1]/2    
        
    cv2.circle(frame_real,(length + corner[8],width + corner[9]), 2, (0,255,255),-1)

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

            cv2.drawContours(blank_three,[biggest_cnt[0]],0,(0,0,255),1)

            blank_gray3 = cv2.cvtColor(blank_three,cv2.COLOR_BGR2GRAY)
            
            dst = cv2.goodFeaturesToTrack(blank_gray3,25,0.15,10)
            dst = np.int0(dst)

            for i in dst:
                x,y = i.ravel()
                cv2.circle(blank_gray3,(x,y),4,0,-1)
            print len(dst)

            cv2.circle(frame_real,(cxmax + corner[8],cymax + corner[9]), 1, (0,255,0),-1)

            if len(dst)==3:
                cv2.putText(frame_real, "triangle", (cxmax + corner[8] - 20, cymax + corner[9] + 20), font, .5,(0,0,255),1, cv2.CV_AA)
            elif len(dst) == 12:
                cv2.putText(frame_real, "cruciform", (cxmax + corner[8] - 20, cymax + corner[9] + 20), font, .5,(0,0,255),1, cv2.CV_AA)
            else:
                cv2.putText(frame_real, "circle", (cxmax + corner[8] - 20, cymax + corner[9] + 20), font, .5,(0,0,255),1, cv2.CV_AA) 

#***************************************************************************************** Display
	    
    cv2.imshow('actual', frame_real)
    cv2.imshow('two', blank_gray2)    
    cv2.imshow('one', blank_gray1)
    cv2.imshow('three', blank_gray3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
