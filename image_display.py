#!/usr/bin/python

import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

i = 0
j = 0
corner = []

sign = [0,0,0]
cnt_hold = [0,0,0]

font = cv2.FONT_HERSHEY_SIMPLEX

img = cv2.imread('dock.jpg')
img_real = cv2.imread('dock.jpg')
img = cv2.imread('dock_simulation.png')
img_real = cv2.imread('dock_simulation.png')

img_cruciform = cv2.imread('Cruciform.jpg', 0)
img_triangle = cv2.imread('triangle_black.png', 0)
img_circle = cv2.imread('Circle.jpg', 0)

edges3 = cv2.Canny(img_cruciform,100, 200)
contours,hierarchy = cv2.findContours(edges3,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnt_cruciform = contours[0]

edges2 = cv2.Canny(img_triangle,100,200)
contours,hierarchy = cv2.findContours(edges2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnt_triangle = contours[0]

edges1 = cv2.Canny(img_circle,100,200)
contours,hierarchy = cv2.findContours(edges1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnt_circle = contours[0]

imgblur = cv2.medianBlur(img,9)
imgray = cv2.cvtColor(imgblur,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,240,255,cv2.THRESH_TOZERO)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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

for i in xrange(3):
	epsilon = 0.1*cv2.arcLength(cnt_hold[i],True)
	approx = cv2.approxPolyDP(cnt_hold[i],epsilon,True)
	x,y,w,h = cv2.boundingRect(approx)
	corner.append(x)
	corner.append(y)
	corner.append(w)
	corner.append(h)

	cv2.rectangle(img_real,(x,y),(x+w,y+h),(0,255,0),2)	

one = img[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
two = img[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
three = img[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
one_a = img_real[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
two_a = img[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
three_a = img[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]

#cv2.imwrite ("hard_image2.jpg", three_a)

distance_from_center = 20

#********************************************************************************************** ONEEEE
imgray = cv2.cvtColor(one_a,cv2.COLOR_BGR2GRAY)
imgray = cv2.medianBlur(imgray,3)

kernel = np.ones((3,3),np.uint8)
imgray = cv2.erode(imgray,kernel,iterations = 1)
imgray = cv2.dilate(imgray,kernel,iterations = 1)

ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_TOZERO_INV)
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
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)

	M = cv2.moments(approx)

	if M['m00'] != 0.0:
		area = cv2.contourArea(approx)
		#print area		
			
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		d = math.sqrt((length-cx)*(length-cx) + (width-cy)*(width-cy))

		if area >= biggest_area and d < distance_from_center:
			biggest_area = area
			biggest_cnt[0] = cnt
			cxmax = cx
			cymax = cy
			#biggest_M[0] = M
			#biggest_approx = approx
if biggest_area != 0:

	try_circ = (1 - cv2.matchShapes(biggest_cnt[0],cnt_circle,1,0.0))*100
	try_tria = (1 - cv2.matchShapes(biggest_cnt[0],cnt_triangle,1,0.0))*100
	try_cruc = (1 - cv2.matchShapes(biggest_cnt[0],cnt_cruciform,1,0.0))*100

	print "ONE"
	print "circle:    %3.2f" % try_circ
	print "triangle:  %3.2f" % try_tria
	print "cruciform: %3.2f" % try_cruc
	print "****"

	cv2.drawContours(one,[biggest_cnt[0]],0,(0,0,255),2)
	cv2.circle(one,(cxmax,cymax), 1, (0,255,0),-1)

	if len(biggest_cnt[0])==3:
	    cv2.putText(one, "triangle", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
	elif len(biggest_cnt[0]) == 12 or len(biggest_cnt[0]) == 24 or (try_cruc > try_circ and try_cruc > try_tria):
	    cv2.putText(one, "cruciform", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
	elif len(biggest_cnt[0]) >= 17:
	    cv2.putText(one, "circle", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
	else:	
	    cv2.putText(one, "None", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)	
	    
cv2.circle(one,(length,width), 1, (255,255,0),-1)



#********************************************************************************************** TWOOOOOO

imgray = cv2.cvtColor(two_a,cv2.COLOR_BGR2GRAY)
imgray = cv2.medianBlur(imgray,3)

kernel = np.ones((3,3),np.uint8)
imgray = cv2.erode(imgray,kernel,iterations = 1)
imgray = cv2.dilate(imgray,kernel,iterations = 1)

ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_TOZERO_INV)
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
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)

	M = cv2.moments(approx)

	if M['m00'] != 0.0:
		area = cv2.contourArea(approx)
		#print area		
			
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		d = math.sqrt((length-cx)*(length-cx) + (width-cy)*(width-cy))

		if area >= biggest_area and d < distance_from_center:
			biggest_area = area
			biggest_cnt[0] = cnt
			cxmax = cx
			cymax = cy
			#biggest_M[0] = M
			#biggest_approx = approx
if biggest_area != 0:

	try_circ = (1 - cv2.matchShapes(biggest_cnt[0],cnt_circle,1,0.0))*100
	try_tria = (1 - cv2.matchShapes(biggest_cnt[0],cnt_triangle,1,0.0))*100
	try_cruc = (1 - cv2.matchShapes(biggest_cnt[0],cnt_cruciform,1,0.0))*100

	print "TWO"
	print "circle:    %3.2f" % try_circ
	print "triangle:  %3.2f" % try_tria
	print "cruciform: %3.2f" % try_cruc
	print len(biggest_cnt[0])
	print "****"

	cv2.drawContours(two,[biggest_cnt[0]],0,(0,0,255),2)
	cv2.circle(two,(cxmax,cymax), 1, (0,255,0),-1)

	if len(biggest_cnt[0])==3:
	    cv2.putText(two, "triangle", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
	elif (len(biggest_cnt[0]) == 12 or len(biggest_cnt[0]) == 24) and (try_cruc > try_circ and try_cruc > try_tria):
	    cv2.putText(two, "cruciform", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
	elif len(biggest_cnt[0]) >= 17:
	    cv2.putText(two, "circle", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
	else:	
	    cv2.putText(two, "None", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)

cv2.circle(two,(length,width), 1, (255,255,0),-1)

#********************************************************************************************** THREEEEE

imgray = cv2.cvtColor(three_a,cv2.COLOR_BGR2GRAY)
imgray = cv2.medianBlur(imgray,3)

kernel = np.ones((3,3),np.uint8)
imgray = cv2.erode(imgray,kernel,iterations = 1)
imgray = cv2.dilate(imgray,kernel,iterations = 1)

ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_TOZERO_INV)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#cv2.drawContours(three,[contours],0,(0,0,255),2)

width = imgray.shape[0]/2
length = imgray.shape[1]/2

biggest_area = 0
biggest_cnt = [0]
biggest_M = [0]
biggest_approx = [0]
cxmax = 0
cymax = 0

for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
	
	M = cv2.moments(approx)

	if M['m00'] != 0.0:
		area = cv2.contourArea(approx)
		#print area		
		
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])

		d = math.sqrt((length-cx)*(length-cx) + (width-cy)*(width-cy))

		if area >= biggest_area and d < distance_from_center:
			biggest_area = area
			biggest_cnt[0] = cnt
			cxmax = cx
			cymax = cy
			#biggest_M[0] = M
			#biggest_approx = approx



if biggest_area != 0:
	try_circ = (1 - cv2.matchShapes(biggest_cnt[0],cnt_circle,1,0.0))*100
	try_tria = (1 - cv2.matchShapes(biggest_cnt[0],cnt_triangle,1,0.0))*100
	try_cruc = (1 - cv2.matchShapes(biggest_cnt[0],cnt_cruciform,1,0.0))*100

	print "THREE"	
	print "circle:    %3.2f" % try_circ
	print "triangle:  %3.2f" % try_tria
	print "cruciform: %3.2f" % try_cruc
	print "****"

	cv2.drawContours(three,[biggest_cnt[0]],0,(0,0,255),2)
	cv2.circle(three,(cxmax,cymax), 1, (0,255,0),-1)

	if len(biggest_cnt[0])==3:
	    cv2.putText(three, "triangle", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
	elif len(biggest_cnt[0]) == 12 or len(biggest_cnt[0]) == 24 or (try_cruc > try_circ and try_cruc > try_tria):
	    cv2.putText(three, "cruciform", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
	elif len(biggest_cnt[0]) >= 17:
	    cv2.putText(three, "circle", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)
	else:	
	    cv2.putText(three, "None", (cxmax - 20, cymax + 20), font, .5,(255,0,0),1, cv2.CV_AA)	
	    
cv2.circle(three,(length,width), 1, (255,255,0),-1)

#*********************************************************************************************

title = ['full image', 'first', 'second', 'third']

image = [img_real, one, two, three]

for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(image[i],'gray')
    plt.title(title[i])
    plt.xticks([]),plt.yticks([])

plt.show()
