#!/usr/bin/python

import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

i = 0
j = 0
corner = []

font = cv2.FONT_HERSHEY_SIMPLEX

#img = cv2.imread('dock.jpg')
img = cv2.imread('dock.jpg')

img_cruciform = cv2.imread('Cruciform.jpg', 0)
img_triangle = cv2.imread('triangle_black.png', 0)
img_circle = cv2.imread('Circle.jpg', 0)

#img_cruciform = cv2.medianBlur(img_cruciform,9)
edges3 = cv2.Canny(img_cruciform,100, 200)
contours,hierarchy = cv2.findContours(edges3,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnt_cruciform = contours[0]

edges2 = cv2.Canny(img_triangle,0,0)
#imgray = cv2.cvtColor(one_a,cv2.COLOR_BGR2GRAY)
#ret,thresh = cv2.threshold(img_triangle,230,255,cv2.THRESH_TOZERO_INV)
contours,hierarchy = cv2.findContours(edges2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnt_triangle = contours[0]
epsilon = 0.1*cv2.arcLength(cnt_triangle, True)
cnt_triangle = cv2.approxPolyDP(cnt_triangle,epsilon,True)

edges1 = cv2.Canny(img_circle,100,200)
contours,hierarchy = cv2.findContours(edges1,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
cnt_circle = contours[0]

img_real = cv2.imread('dock.jpg')
imgblur = cv2.medianBlur(img,9)


imgray = cv2.cvtColor(imgblur,cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(imgray,240,255,cv2.THRESH_TOZERO)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

while i < len(contours):

	cnt = contours[i]

	M = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	#print area	

	if area >= 2000:

		epsilon = 0.1*cv2.arcLength(cnt,True)
		approx = cv2.approxPolyDP(cnt,epsilon,True)
		x,y,w,h = cv2.boundingRect(approx)
		corner.append(x)
		corner.append(y)
		corner.append(w)
		corner.append(h)

		j += 1
				
		cv2.rectangle(img_real,(x,y),(x+w,y+h),(0,255,0),2)	

	i += 1

one = img[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
two = img[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
three = img[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]
one_a = img_real[corner[1]:corner[1]+corner[3], corner[0]:corner[0]+corner[2]]
two_a = img[corner[5]:corner[5]+corner[7], corner[4]:corner[4]+corner[6]]
three_a = img[corner[9]:corner[9]+corner[11], corner[8]:corner[8]+corner[10]]


distance_from_center = 20

#**********************************************************************************************
imgray = cv2.cvtColor(one_a,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_TOZERO_INV)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

width = imgray.shape[0]/2
length = imgray.shape[1]/2
#print width
#print length

for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)
	#print len(approx)
	#cv2.drawContours(one,[cnt],0,(0,0,255),2)

	M = cv2.moments(approx)
	#print M	
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])


	d = math.sqrt((width-cx)*(width-cx) + (length-cy)*(length-cy))

        if len(approx)==3 and d < distance_from_center:
            cv2.drawContours(one,[cnt],0,(0,0,255),2)
	    cv2.putText(one, "triangle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
	    cv2.circle(one,(cx,cy), 1, (0,255,0),-1)
	elif len(approx) == 12 and d < distance_from_center:
            cv2.drawContours(one,[cnt],0,(0,0,255),2)
	    cv2.putText(one, "cruciform", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
	    cv2.circle(one,(cx,cy), 1, (0,255,0),-1)
	elif len(approx) >= 8 and d < distance_from_center:
            cv2.drawContours(one,[cnt],0,(0,0,255),2)
	    cv2.putText(one, "circle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)	
	    cv2.circle(one,(cx,cy), 1, (0,255,0),-1)
	    print d
	    
cv2.circle(one,(length,width), 1, (255,255,0),-1)


"""i = 0
area_max = 0.0

while i < len(contours):

	cnt = contours[i]

	M = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	if area > area_max:
		area_max = area
		cnt_max = contours[i]
		hold = i
	i += 1

x,y,w,h = cv2.boundingRect(cnt_max)
aspect_ratio = float (w)/h
#print aspect_ratio

try_circ = (1 - cv2.matchShapes(cnt_max,cnt_circle,1,0.0))*100
try_tria = (1 - cv2.matchShapes(cnt_max,cnt_triangle,1,0.0))*100
try_cruc = (1 - cv2.matchShapes(cnt_max,cnt_cruciform,1,0.0))*100

print "CIRCLE"
print "circle:    %3.2f" % try_circ
print "triangle:  %3.2f" % try_tria
print "cruciform: %3.2f" % try_cruc
print "****"

if try_circ > try_tria and try_circ > try_cruc:
	cv2.putText(one, "circle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
elif try_tria > try_circ and try_tria > try_cruc:
	cv2.putText(one, "triangle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
elif try_cruc > try_circ and try_cruc > try_tria:
	cv2.putText(one, "cruciform", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
else:
	cv2.putText(one, "error", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)	

#print len(contours[hold])
cnt = contours[hold]
cv2.drawContours(one, [cnt], 0, (0,255,0), 1)"""

#**********************************************************************************************

imgray = cv2.cvtColor(two_a,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_TOZERO_INV)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

width = imgray.shape[0]/2
length = imgray.shape[1]/2



for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)

	M = cv2.moments(approx)
	#print M	
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	d = math.sqrt((width-cx)*(width-cx) + (length-cy)*(length-cy))
	#print d

        if len(approx)==3 and d < distance_from_center:
            cv2.drawContours(two,[cnt],0,(0,0,255),2)
	    cv2.putText(two, "triangle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
	    cv2.circle(two,(cx,cy), 1, (0,255,0),-1)
	    print d
	elif len(approx) == 12 and d < distance_from_center:
            cv2.drawContours(two,[cnt],0,(0,0,255),2)
	    cv2.putText(two, "cruciform", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
	    cv2.circle(two,(cx,cy), 1, (0,255,0),-1)
	elif len(approx) >= 13 and d < distance_from_center:
            cv2.drawContours(two,[cnt],0,(0,0,255),2)
	    cv2.putText(two, "circle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)		
	    cv2.circle(two,(cx,cy), 1, (0,255,0),-1)

cv2.circle(two,(length,width), 1, (255,255,0),-1)

"""
while i < len(contours):

	cnt = contours[i]

	M = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	if area > area_max:
		area_max = area
		cnt_max = contours[i]
		hold = i
	i += 1

x,y,w,h = cv2.boundingRect(cnt_max)
aspect_ratio = float (w)/h
#print aspect_ratio

try_circ = (1 - cv2.matchShapes(cnt_max,cnt_circle,1,0.0))*100
try_tria = (1 - cv2.matchShapes(cnt_max,cnt_triangle,1,0.0))*100
try_cruc = (1 - cv2.matchShapes(cnt_max,cnt_cruciform,1,0.0))*100

print "TRIANGLE"
print "circle:    %3.2f" % try_circ
print "triangle:  %3.2f" % try_tria
print "cruciform: %3.2f" % try_cruc
print "****"

#if try_circ > try_tria and try_circ > try_cruc:
#	cv2.putText(two, "circle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
#elif try_tria > try_circ and try_tria > try_cruc and aspect_ration < 1.0:
#	cv2.putText(two, "triangle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
#elif try_cruc > try_circ and try_cruc > try_tria:
#	cv2.putText(two, "cruciform", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
#else:
#	cv2.putText(two, "error", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)

#print len(contours[hold])
#cnt = contours[hold]
#print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#print len(cnt)
#print cnt
#print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
#cv2.drawContours(two, [cnt], 0, (0,255,0), 1)"""

#**********************************************************************************************

imgray = cv2.cvtColor(three_a,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,230,255,cv2.THRESH_TOZERO_INV)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

width = imgray.shape[0]/2
length = imgray.shape[1]/2

for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.02*cv2.arcLength(cnt,True),True)

	M = cv2.moments(approx)
	#print M	
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	d = math.sqrt((length-cx)*(length-cx) + (width-cy)*(width-cy))

        if len(approx)==3 and d < distance_from_center:
            cv2.drawContours(three,[cnt],0,(0,0,255),2)
	    cv2.putText(three, "triangle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
	    cv2.circle(three,(cx,cy), 1, (0,255,0),-1)
	elif len(approx) == 12 and d < distance_from_center:
            cv2.drawContours(three,[cnt],0,(0,0,255),2)
	    cv2.putText(three, "cruciform", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
	    cv2.circle(three,(cx,cy), 1, (0,255,0),-1)
	    print d
	elif len(approx) >= 13 and d < distance_from_center:
            cv2.drawContours(three,[cnt],0,(0,0,255),2)
	    cv2.putText(three, "circle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)	
	    cv2.circle(three,(cx,cy), 1, (0,255,0),-1)

cv2.circle(three,(length,width), 1, (255,255,0),-1)


"""i = 0
area_max = 0.0

while i < len(contours):

	cnt = contours[i]

	M = cv2.moments(cnt)
	area = cv2.contourArea(cnt)
	if area > area_max:
		area_max = area
		cnt_max = contours[i]
		hold = i
	i += 1

x,y,w,h = cv2.boundingRect(cnt_max)
aspect_ratio = float (w)/h
#print aspect_ratio

try_circ = (1 - cv2.matchShapes(cnt_max,cnt_circle,1,0.0))*100
try_tria = (1 - cv2.matchShapes(cnt_max,cnt_triangle,1,0.0))*100
try_cruc = (1 - cv2.matchShapes(cnt_max,cnt_cruciform,1,0.0))*100

print "CRUCIFORM"
print "circle:    %3.2f" % try_circ
print "triangle:  %3.2f" % try_tria
print "cruciform: %3.2f" % try_cruc
print "****"

if try_circ > try_tria and try_circ > try_cruc:
	cv2.putText(three, "circle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
elif try_tria > try_circ and try_tria > try_cruc:
	cv2.putText(three, "triangle", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
elif try_cruc > try_circ and try_cruc > try_tria:
	cv2.putText(three, "cruciform", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)
else:
	cv2.putText(three, "error", (3,43), font, .5,(255,0,0),1, cv2.CV_AA)

#print len(contours[hold])
cnt = contours[hold]
cv2.drawContours(three, [cnt], 0, (0,255,0), 1)"""

#**********************************************************************************************

title = ['full image', 'circle', 'triangle', 'cruciform']

image = [img_real, one, two, three]

for i in xrange(4):
    plt.subplot(2,2,i+1),plt.imshow(image[i],'gray')
    plt.title(title[i])
    plt.xticks([]),plt.yticks([])

plt.show()
