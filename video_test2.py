#!/usr/bin/python

import numpy as np
import cv2
import math
import cv2.cv as cv
import colorsys
import time

#88264580  //37706939
#63447314   

def find_shape(orig_img, blank_img, p1, p2, nr, mr, dst_frm_cnt):
    imgray = cv2.cvtColor(orig_img,cv2.COLOR_BGR2GRAY)

    kernel = np.ones((7,7),np.float32)/25
    imgray_triangle = cv2.filter2D(imgray,-1,kernel)

    height = imgray.shape[0]
    width  = imgray.shape[1]
    
    width_cent = width/2
    height_cent = height/2

    #blank_img[0:height,0:width] = 255

    #blank_img = np.zeros((corner[3],corner[2],3), np.uint8)
    #blank_img[:,0:corner[2]] = (255,255,255)  

    ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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
        #cv2.imshow('holder12', blank_img)

        cv2.drawContours(blank_img,[biggest_cnt[0]],0,(0,0,255),1)

        blank_gray = cv2.cvtColor(blank_img,cv2.COLOR_BGR2GRAY)
        
        #cv2.circle(blank_gray,(cx,cy),4,0,-1)

        circles = cv2.HoughCircles(blank_gray,cv.CV_HOUGH_GRADIENT,1, width, param1=p1,param2=p2,minRadius=nr,maxRadius=mr)          

        dst = cv2.goodFeaturesToTrack(blank_gray,25,0.15,10)
        dst = np.int0(dst)

        for i in dst:
            x,y = i.ravel()
            cv2.circle(blank_gray,(x,y),4,0,-1)
        
        if circles != None:
            symbol_type = 'circle'
        else:
            if len(dst) == 12:
                symbol_type = 'cruciform'
            elif len(dst) == 3:
                symbol_type = 'triangle'
            else:
                blank_img[0:height,0:width] = 255
                
                ret,thresh = cv2.threshold(imgray_triangle,230,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
                
                
                contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

                        #print area

                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])

                        d = math.sqrt((width_cent-cx)*(width_cent-cx) + (height_cent-cy)*(height_cent-cy))

                        #if area >= 600:

                            #print d                        

                        if area >= biggest_area and d < distance_from_center:
                            biggest_area = area
                            biggest_cnt[0] = cnt
                            cxmax = cx
                            cymax = cy
                if biggest_area != 0:

                    cv2.drawContours(blank_img,[biggest_cnt[0]],0,(0,0,255),1)

                    blank_gray = cv2.cvtColor(blank_img,cv2.COLOR_BGR2GRAY)

                    dst = cv2.goodFeaturesToTrack(blank_gray,25,0.15,10)
                    dst = np.int0(dst)
                


                    for i in dst:
                        x,y = i.ravel()
                        cv2.circle(blank_gray,(x,y),4,0,-1)

                    if len(dst) == 3:
                        symbol_type = 'triangle'
                    else:
                        symbol_type = 'circle'
                else:
                    symbol_type = 'none'
                    blank_gray = cv2.cvtColor(blank_img,cv2.COLOR_BGR2GRAY)
    else:
        symbol_type = 'none'
        

    if symbol_type != 'none':

        for h,cnt in enumerate(biggest_cnt[0]):
            mask = np.zeros(imgray.shape,np.uint8)
            cv2.drawContours(mask,[biggest_cnt[0]],0,255,-1)
            mean = cv2.mean(orig_img,mask = mask)

        mean = colorsys.rgb_to_hsv(mean[2]/255, mean[1]/255, mean[0]/255)
        hsv = list(mean)
        hsv[0] = hsv[0]*360
        #print hsv

        if hsv[2] < 0.1:
            color = 'black'
        elif (hsv[0]<11 or hsv[0]>351) and hsv[1]>.7 and hsv[2]>.1:
            color = 'red'
        elif (hsv[0]>64 and hsv[0]<150) and hsv[1]>.15 and hsv[2]>.1:
            color = 'green'
        elif (hsv[0]>180 and hsv[0]<255) and hsv[1]>.15 and hsv[2]>.1:
            color = 'blue'
        else:
            #cv2.drawContours(orig_img,[biggest_cnt[0]], 0, (255, 0, 255), -1)        
            color = 'can\'t find'
            #cv2.imshow('image', orig_img)

    if symbol_type == 'none':
        blank_gray = cv2.cvtColor(blank_img,cv2.COLOR_BGR2GRAY)
        cxmax = width_cent
        cymax = height_cent

        mask = np.zeros(imgray.shape, np.uint8)
        cv2.circle(mask,(cxmax,cymax), 5, 255,-1)
        mean = cv2.mean(orig_img,mask = mask)

        mean = colorsys.rgb_to_hsv(mean[2]/255, mean[1]/255, mean[0]/255)
        hsv = list(mean)
        hsv[0] = hsv[0]*360


        if hsv[2] < 0.1:
            color = 'black'
        elif (hsv[0]<11 or hsv[0]>351) and hsv[1]>.7 and hsv[2]>.1:
            color = 'red'
        elif (hsv[0]>64 and hsv[0]<150) and hsv[1]>.15 and hsv[2]>.1:
            color = 'green'
        elif (hsv[0]>180 and hsv[0]<255) and hsv[1]>.15 and hsv[2]>.1:
            color = 'blue'
        else:        
            color = 'can\'t find'
   
    
    #print color
    #time.sleep(.5)

    return (symbol_type, blank_gray, cxmax, cymax, color)


#*****************************************************  Probability portion  *******************************************
def find_prob(sign):
    probability_sum = sign['circle']+sign['triangle']+sign['cruciform']

    if probability_sum > 0.0:
        sign_probability = {'circle': sign['circle']/probability_sum, 'triangle':sign['triangle']/probability_sum, 'cruciform':sign['cruciform']/probability_sum}
    else:
        sign_probability = {'circle': 0.0, 'triangle': 0.0, 'cruciform': 0.0}
    return sign_probability

def find_highest_percentage(percentages):
    most_likely = max(percentages, key=percentages.get)
    prcnt = percentages[most_likely]
    
    return most_likely, prcnt

def add_sign(sign, sign_sum):

    if sign != 'none':
        sign_sum[sign] = sign_sum[sign] + 1.0 #+1 for each frame

    percentage = find_prob(sign_sum)
    sign,prcnt = find_highest_percentage(percentage)
    return sign, prcnt, sign_sum

#************************************************************************************************************************
    
font = cv2.FONT_HERSHEY_SIMPLEX

sign1_sum = {'circle': 0.0, 'triangle': 0.0, 'cruciform': 0.0} #starting values
sign2_sum = {'circle': 0.0, 'triangle': 0.0, 'cruciform': 0.0} #starting values
sign3_sum = {'circle': 0.0, 'triangle': 0.0, 'cruciform': 0.0} #starting values

#Hough_circle values
p1 = 100
p2 = 13
nr = 20
mr = 30
#*******************

#blur Blank_gray images
kern1 = 7
kern2 = 7

i = 0
j = 0
corner = []
distance_from_center = 10.0

vid = 'Dock_Simulation_30_degrees.avi'
vid = '/home/andy/dock_simulation_vertical.avi'

cap = cv2.VideoCapture(vid)

while(cap.isOpened()):
    ret, frame = cap.read()
    ret, frame_real = cap.read()

    height = frame_real.shape[0]
    width  = frame_real.shape[1]

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    imgray = cv2.medianBlur(gray,9)
    #cv2.imshow('distort', imgray)
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
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
        d = []

        numbers = len(coordsx)

        for z in xrange(numbers):
            d.append(int(math.sqrt((coordsx[z-1]-cx)*(coordsx[z-1]-cx) + (coordsy[z-1]-cy)*(coordsy[z-1]-cy))))
        
        for j in d:
            if j < 60:
                same_moment += 1
        #************************************************************************************

        epsilon = 0.1*cv2.arcLength(cnt_hold[i],True)
        approx = cv2.approxPolyDP(cnt_hold[i],epsilon,True)
        x,y,w,h = cv2.boundingRect(approx)
        
        #check for white signs
        if y < (height/2 + 200) and y > (height/2 - 200) and same_moment == 0:
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
    
    if (corner[0] < corner[4] and corner[0] < corner[8] and corner[0] != width):
        one_a = frame[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
        blank_one = np.zeros((corner[3],corner[2],3), np.uint8)
        blank_one[:,0:corner[2]] = (255,255,255)  
        sign1 = find_shape(one_a, blank_one, p1, p2, nr, mr, distance_from_center)  
        
        symbol1,percentage1,sign1_sum = add_sign(sign1[0], sign1_sum)

        if sign1[0] != 'none' or sign1[0] != 'none_found':        
            cv2.circle(frame_real,(sign1[2]+corner[0],sign1[3]+corner[1]), 2, (255,0,0),-1) 
            cv2.putText(frame_real, "%s (%1.2f)" % (symbol1,percentage1) , (sign1[2]+corner[0], sign1[3]+corner[1] + 15), font, .6,(0,0,255),1, cv2.CV_AA)
            cv2.putText(frame_real, sign1[4] , (sign1[2]+corner[0], sign1[3]+corner[1] - 15), font, .6,(0,0,255),1, cv2.CV_AA)   

        cv2.putText(frame_real, "Sign1" , (corner[0], corner[1] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    elif (corner[0] > corner[4] and corner[0] > corner[8] and corner[0] != width):
        three_a = frame[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
        blank_three = np.zeros((corner[3],corner[2],3), np.uint8)
        blank_three[:,0:corner[2]] = (255,255,255)
        sign3 = find_shape(three_a, blank_three, p1, p2, nr, mr, distance_from_center)  

        symbol3,percentage3,sign3_sum = add_sign(sign3[0], sign3_sum)

        if sign3[0] != 'none' or sign3[0] != 'none_found':        
            cv2.circle(frame_real,(sign3[2]+corner[0],sign3[3]+corner[1]), 2, (255,0,0),-1) 
            cv2.putText(frame_real, "%s (%1.2f)" % (symbol3,percentage3) , (sign3[2]+corner[0], sign3[3]+corner[1] + 15), font, .6,(0,0,255),1, cv2.CV_AA)
            cv2.putText(frame_real, sign3[4] , (sign3[2]+corner[0], sign3[3]+corner[1] - 15), font, .6,(0,0,255),1, cv2.CV_AA)
          
        cv2.putText(frame_real, "Sign3" , (corner[0], corner[1] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    elif (corner[0] != width):
        two_a = frame[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
        blank_two = np.zeros((corner[3],corner[2],3), np.uint8)
        blank_two[:,0:corner[2]] = (255,255,255) 
        sign2 =  find_shape(two_a, blank_two, p1, p2, nr, mr, distance_from_center)

        symbol2,percentage2,sign2_sum = add_sign(sign2[0], sign2_sum)

        if sign2[0] != 'none' or sign2[0] != 'none_found':        
            cv2.circle(frame_real,(sign2[2]+corner[0],sign2[3]+corner[1]), 2, (255,0,0),-1) 
            cv2.putText(frame_real, "%s (%1.2f)" % (symbol2,percentage2) , (sign2[2]+corner[0], sign2[3]+corner[1] + 15), font, .6,(0,0,255),1, cv2.CV_AA)
            cv2.putText(frame_real, sign2[4] , (sign2[2]+corner[0], sign2[3]+corner[1] - 15), font, .6,(0,0,255),1, cv2.CV_AA)

        cv2.putText(frame_real, "Sign2" , (corner[0], corner[1] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
        

    if (corner[4] < corner[0] and corner[4] < corner [8] and corner[4] != width and corner[4] != width):
        one_a = frame[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
        blank_one = np.zeros((corner[7],corner[6],3), np.uint8)
        blank_one[:,0:corner[6]] = (255,255,255)
        sign1 =  find_shape(one_a, blank_one, p1, p2, nr, mr, distance_from_center) 

        symbol1,percentage1,sign1_sum = add_sign(sign1[0], sign1_sum)

        if sign1[0] != 'none' or sign1[0] != 'none_found':        
            cv2.circle(frame_real,(sign1[2]+corner[4],sign1[3]+corner[5]), 2, (255,0,0),-1) 
            cv2.putText(frame_real, "%s (%1.2f)" % (symbol1,percentage1) , (sign1[2]+corner[4], sign1[3]+corner[5] + 15), font, .6,(0,0,255),1, cv2.CV_AA) 
            cv2.putText(frame_real, sign1[4] , (sign1[2]+corner[4], sign1[3]+corner[5] - 15), font, .6,(0,0,255),1, cv2.CV_AA)
 
        cv2.putText(frame_real, "Sign1" , (corner[4], corner[5] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    elif (corner[4] > corner[0] and corner[4] > corner[8] and corner[4] != width):
        three_a = frame[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
        blank_three = np.zeros((corner[7],corner[6],3), np.uint8)
        blank_three[:,0:corner[6]] = (255,255,255)
        sign3 =  find_shape(three_a, blank_three, p1, p2, nr, mr, distance_from_center) 

        symbol3,percentage3,sign3_sum = add_sign(sign3[0], sign3_sum)
     
        if sign3[0] != 'none' or sign3[0] != 'none_found':        
            cv2.circle(frame_real,(sign3[2]+corner[4],sign3[3]+corner[5]), 2, (255,0,0),-1) 
            cv2.putText(frame_real, "%s (%1.2f)" % (symbol3,percentage3) , (sign3[2]+corner[4], sign3[3]+corner[5] + 15), font, .6,(0,0,255),1, cv2.CV_AA) 
            cv2.putText(frame_real, sign3[4] , (sign3[2]+corner[4], sign3[3]+corner[5] - 15), font, .6,(0,0,255),1, cv2.CV_AA)     

        cv2.putText(frame_real, "Sign3" , (corner[4], corner[5] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    elif (corner[4] != width):
        two_a = frame[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
        blank_two = np.zeros((corner[7],corner[6],3), np.uint8)
        blank_two[:,0:corner[6]] = (255,255,255)    
        sign2 =  find_shape(two_a, blank_two, p1, p2, nr, mr, distance_from_center)    

        symbol2,percentage2,sign2_sum = add_sign(sign2[0], sign2_sum)
        print symbol2

        if sign2[0] != 'none' or sign2[0] != 'none_found':        
            cv2.circle(frame_real,(sign2[2]+corner[4],sign2[3]+corner[5]), 2, (255,0,0),-1) 
            cv2.putText(frame_real, "%s (%1.2f)" % (symbol2,percentage2) , (sign2[2]+corner[4], sign2[3]+corner[5] + 15), font, .6,(0,0,255),1, cv2.CV_AA) 
            cv2.putText(frame_real, sign2[4] , (sign2[2]+corner[4], sign2[3]+corner[5] - 15), font, .6,(0,0,255),1, cv2.CV_AA) 

        cv2.putText(frame_real, "Sign2" , (corner[4], corner[5] - 5), font, .75,(255,0,255),2, cv2.CV_AA)

    if (corner[8] < corner[4] and corner[8] < corner [0] and corner[8] != width):
        one_a = frame[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
        blank_one = np.zeros((corner[11],corner[10],3), np.uint8)
        blank_one[:,0:corner[10]] = (255,255,255)

        symbol1,percentage1,sign1_sum = add_sign(sign1[0], sign1_sum)

        if sign1[0] != 'none' or sign1[0] != 'none_found':        
            cv2.circle(frame_real,(sign1[2]+corner[8],sign1[3]+corner[9]), 2, (255,0,0),-1) 
            cv2.putText(frame_real, "%s (%1.2f)" % (symbol1,percentage1) , (sign1[2]+corner[8], sign1[3]+corner[9] + 15), font, .6,(0,0,255),1, cv2.CV_AA) 
            cv2.putText(frame_real, sign1[4] , (sign1[2]+corner[8], sign1[3]+corner[9] - 15), font, .6,(0,0,255),1, cv2.CV_AA)

        sign1 =  find_shape(one_a, blank_one, p1, p2, nr, mr, distance_from_center)  
        cv2.putText(frame_real, "Sign1" , (corner[8], corner[9] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    elif (corner[8] > corner[0] and corner[8] > corner[4] and corner[8] != width):
        three_a = frame[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
        blank_three = np.zeros((corner[11],corner[10],3), np.uint8)
        blank_three[:,0:corner[10]] = (255,255,255)
        sign3 =  find_shape(three_a, blank_three, p1, p2, nr, mr, distance_from_center)

        symbol3,percentage3,sign3_sum = add_sign(sign3[0], sign3_sum)

        if sign3[0] != 'none' or sign3[0] != 'none_found':        
            cv2.circle(frame_real,(sign3[2]+corner[8],sign3[3]+corner[9]), 2, (255,0,0),-1) 
            cv2.putText(frame_real, "%s (%1.2f)" % (symbol3,percentage3) , (sign3[2]+corner[8], sign3[3]+corner[9] + 15), font, .6,(0,0,255),1, cv2.CV_AA) 
            cv2.putText(frame_real, sign3[4] , (sign3[2]+corner[8], sign3[3]+corner[9] - 15), font, .6,(0,0,255),1, cv2.CV_AA)
 
        cv2.putText(frame_real, "Sign3" , (corner[8], corner[9] - 5), font, .75,(255,0,255),2, cv2.CV_AA)
    elif (corner[8] != width):
        two_a = frame[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
        blank_two = np.zeros((corner[11],corner[10],3), np.uint8)
        blank_two[:,0:corner[10]] = (255,255,255)
        sign2 =  find_shape(two_a, blank_two, p1, p2, nr, mr, distance_from_center)

        symbol2,percentage2,sign2_sum = add_sign(sign2[0], sign2_sum)
        print symbol2

        if sign2[0] != 'none' or sign2[0] != 'none_found':        
            cv2.circle(frame_real,(sign2[2]+corner[8],sign2[3]+corner[9]), 2, (255,0,0),-1) 
            cv2.putText(frame_real, "%s (%1.2f)" % (symbol2,percentage2) , (sign2[2]+corner[8], sign2[3]+corner[9] + 15), font, .6,(0,0,255),1, cv2.CV_AA) 
            cv2.putText(frame_real, sign2[4] , (sign2[2]+corner[8], sign2[3]+corner[9] - 15), font, .6,(0,0,255),1, cv2.CV_AA)

        cv2.putText(frame_real, "Sign2" , (corner[8], corner[9] - 5), font, .75,(255,0,255),2, cv2.CV_AA)

    #print "sign1: " + sign1[0]
    #print "sign2: " + sign2[0]
    #print "sign3: " + sign3[0]
    cv2.putText(frame_real, ("%d"% no_of_signs) , (1600, 50), font, .75,(255,0,255),2, cv2.CV_AA)

    cv2.imshow('actual', frame_real)
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

    


"""
#***************************************************************************************** One One One
    imgray = cv2.cvtColor(one_a,cv2.COLOR_BGR2GRAY)

    kernel = np.ones((kern1,kern2),np.float32)/25
    imgray_triangle = cv2.filter2D(imgray,-1,kernel)

    #kernel = np.ones((kern1,kern2),np.float32)/25
    #imgray_cruciform = cv2.filter2D(imgray,-1,kernel)


    width = imgray.shape[0]/2
    length = imgray.shape[1]/2   

    ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #need to move this
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

            circles = cv2.HoughCircles(blank_gray1,cv.CV_HOUGH_GRADIENT,1, width, param1=p1,param2=p2,minRadius=nr,maxRadius=mr)          

            dst = cv2.goodFeaturesToTrack(blank_gray1,25,0.15,10)
            dst = np.int0(dst)

            for i in dst:
                x,y = i.ravel()
                cv2.circle(blank_gray1,(x,y),4,0,-1)
            #print len(dst)

            cv2.circle(frame_real,(cxmax + corner[0],cymax + corner[1]), 1, (0,255,0),-1)
            
            if circles != None:
                cv2.putText(blank_gray1, "circle", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)
            else:
                if len(dst) == 12:
                    cv2.putText(blank_gray1, "cruciform", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)
                else:
                    #blank_one[:,0:corner[2]] = (255,255,255)
                    ret,thresh = cv2.threshold(imgray_triangle,230,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

                    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

                            #cv2.drawContours(blank_one,[biggest_cnt[0]],0,(0,0,255),1)

                            blank_gray1 = cv2.cvtColor(blank_one,cv2.COLOR_BGR2GRAY)

                            circles = cv2.HoughCircles(blank_gray1,cv.CV_HOUGH_GRADIENT,1, width, param1=p1,param2=p2,minRadius=nr,maxRadius=mr)          

                            dst = cv2.goodFeaturesToTrack(blank_gray1,25,0.15,10)
                            dst = np.int0(dst)

                            for i in dst:
                                x,y = i.ravel()
                                #cv2.circle(blank_gray1,(x,y),4,0,-1)
                            #print len(dst)

                            #cv2.circle(frame_real,(cxmax + corner[0],cymax + corner[1]), 1, (0,255,0),-1)

                            if circles != None:
                                if len(dst) == 3:
                                    cv2.putText(blank_gray1, "triangle", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)
                                else:
                                    cv2.putText(blank_gray1, "circle", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)  

            #if circles != None:
            #    cv2.putText(frame_real, "circle", (cxmax + corner[0] - 20, cymax + corner[1] + 20), font, .5,(0,0,255),1, cv2.CV_AA)
            #else:
            #    if len(dst)==3:
            #        cv2.putText(frame_real, "triangle", (cxmax + corner[0] - 20, cymax + corner[1] + 20), font, .5,(0,0,255),1, cv2.CV_AA)
            #    elif len(dst) == 12:
            #        cv2.putText(frame_real, "cruciform", (cxmax + corner[0] - 20, cymax + corner[1] + 20), font, .5,(0,0,255),1, cv2.CV_AA)
            #    else:
            #        cv2.putText(frame_real, "circle", (cxmax + corner[0] - 20, cymax + corner[1] + 20), font, .5,(0,0,255),1, cv2.CV_AA)

#***************************************************************************************** Two Two Two
    imgray = cv2.cvtColor(two_a,cv2.COLOR_BGR2GRAY)

    #kernel = np.ones((kern1,kern2),np.float32)/25
    #imgray = cv2.filter2D(imgray,-1,kernel)

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

            

            blank_gray2 = cv2.cvtColor(blank_two,cv2.COLOR_BGR2GRAY)

            circles = cv2.HoughCircles(blank_gray2,cv.CV_HOUGH_GRADIENT,1, width, param1=p1,param2=p2,minRadius=nr,maxRadius=mr)
            
            dst = cv2.goodFeaturesToTrack(blank_gray2,25,0.15,10)
            dst = np.int0(dst)

            for i in dst:
                x,y = i.ravel()
                cv2.circle(blank_gray2,(x,y),4,0,-1)
            #print len(dst)

            cv2.circle(frame_real,(cxmax + corner[4],cymax + corner[5]), 1, (0,255,0),-1)

            if circles != None:
                cv2.putText(blank_gray2, "circle", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)
            else:
                if len(dst)==3:
                    cv2.putText(blank_gray2, "triangle", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)
                elif len(dst) == 12:
                    cv2.putText(blank_gray2, "cruciform", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)
                else:
                    cv2.putText(blank_gray2, "circle", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA) 

#***************************************************************************************** Three Three Three

    imgray = cv2.cvtColor(three_a,cv2.COLOR_BGR2GRAY)

    kernel = np.ones((kern1,kern2),np.float32)/25
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

            circles = cv2.HoughCircles(blank_gray3,cv.CV_HOUGH_GRADIENT,1, width, param1=p1,param2=p2,minRadius=nr,maxRadius=mr)
            
            dst = cv2.goodFeaturesToTrack(blank_gray3,25,0.15,10)
            dst = np.int0(dst)

            for i in dst:
                x,y = i.ravel()
                cv2.circle(blank_gray3,(x,y),4,0,-1)
            #print len(dst)

            cv2.circle(frame_real,(cxmax + corner[8],cymax + corner[9]), 1, (0,255,0),-1)

            #print len(dst)

            if circles != None:
                cv2.putText(blank_gray3, "circle", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)
            else:
                if len(dst)==3:
                    cv2.putText(blank_gray3, "triangle", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)
                elif len(dst) == 12:
                    cv2.putText(blank_gray3, "cruciform", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA)
                else:
                    cv2.putText(blank_gray3, "circle", (cxmax+10, cymax + 25), font, .5,(0,0,255),1, cv2.CV_AA) 

#***************************************************************************************** Display
"""        
