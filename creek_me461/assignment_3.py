import numpy as np
import cv2
from creekStones import creekImage
from math import *
kernel = np.ones((7, 7), np.uint8)
minStoneArea = 600
maxStride = 110

img0 = creekImage(0.99)

mask_green = cv2.inRange(img0,  np.array([50,199,50]),  np.array([50,201,50]))
temp1 = img0.copy()
temp1[mask_green == 0] = 0
temp1[mask_green != 0] = img0[mask_green != 0]
green_filtered = cv2.bitwise_xor(img0, temp1)

mask_red = cv2.inRange(green_filtered,  np.array([249,90,90]),  np.array([251,90,90]))
temp2 = green_filtered.copy()
temp2[mask_red == 0] = 0
temp2[mask_red != 0] = green_filtered[mask_red != 0]
red_filtered = cv2.bitwise_xor(green_filtered, temp2)

mask_blue = cv2.inRange(red_filtered,  np.array([0,0,200]),  np.array([255,255,250]))
temp3 = red_filtered.copy()
temp3[mask_blue == 0] = 0
temp3[mask_blue != 0] = red_filtered[mask_blue != 0]
blue_filtered = cv2.bitwise_xor(red_filtered, temp3)

blurred = cv2.GaussianBlur(blue_filtered,(3,3),cv2.BORDER_DEFAULT)
blurred_grey =  cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)

ret, thresh1 = cv2.threshold(blurred_grey, 70, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

modified_contours = []
for contour in contours:
    if cv2.contourArea(contour) > 100:
        modified_contours.append(contour)

green_contour = []
red_contour = []
green_points = []
red_points = []

for contour in modified_contours:
    if cv2.contourArea(contour) > minStoneArea:
        green_contour.append(contour)
    else:
        red_contour.append(contour)

for i in green_contour:
    M = cv2.moments(i)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        green_points.append([cx,cy])

for i in red_contour:
    M = cv2.moments(i)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        red_points.append([cx,cy])


def DrawOnImage(img, coord, box=False, diagonals = True, dpen = (255,0,0)):
    '''
    This funciton takes an image, and a coordinate pair in the form of ((y1,x1), (y2,x2))
    These two points can either belown to the two ends of a line, 
    or the two opposite corners of a box
    if box = False, a line is drawn between these two points,
    else a box with its diagonals are drawn. So that you do not need to worry about the center of it
    if you do not want the diagonal, make it False
    The final parameter is the pen to draw with, by default lines will be RED
    everything is drawn on a copy of the image sent, and this copy is returned
    '''
    # create a copy of the image
    img_new = img.copy()
    P1, P2 = coord # get the points out of the coordinates list
    # assume that line or box extends from P1(y1,x1) to P2(y2,x2), note that y preceeds x to be consistent with matrix indexing convention
    maxNP = max(( abs(P2[0]-P1[0]) , abs(P2[1]-P1[1])))
    if box: # then draw a box 
        img_new[P1[0], P1[1]:P2[1], :] = dpen
        img_new[P1[0]:P2[0], P2[1], :] = dpen
        img_new[P2[0], P1[1]:P2[1], :] = dpen
        img_new[P1[0]:P2[0], P1[1], :] = dpen
        if diagonals:
            img_new[ np.linspace(P1[0],P2[0], maxNP).astype('int'), np.linspace(P1[1],P2[1], maxNP).astype('int'), :] = dpen
            img_new[ np.linspace(P2[0],P1[0], maxNP).astype('int'), np.linspace(P1[1],P2[1], maxNP).astype('int'), :] = dpen
    else: # draw a line
        img_new[ np.linspace(P1[0],P2[0], maxNP).astype('int'), np.linspace(P1[1],P2[1], maxNP).astype('int'), :] = dpen
    return img_new

# test the funciton
penRed = (255,0, 0)
penGreen = (0,255,0)


for green in green_points:
    img0 = DrawOnImage(img0, ((green[1]-20,green[0]-20),(green[1]+20,green[0]+20)), box=True, diagonals = False, dpen=penGreen)

for red in red_points:
    img0 = DrawOnImage(img0, ((red[1]-20,red[0]-20),(red[1]+20,red[0]+20)), box=True) 


start_points = []

def Sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j]= sub_li[j + 1]
                sub_li[j + 1]= tempo
    return sub_li

min_path = 99999
minimum_path  = []

def shortest_path(start_point,previous_point):
    global minimum_path,min_path

    connected_points = []
    previous_point.append(start_point)

    if start_point[1] < maxStride:

        previous_point.append([previous_point[-1][0],previous_point[-1][1]-maxStride])
        
        c = False
        while True:
            i = 0
            for i in range(len(previous_point)-1):
                if previous_point[i][1] < previous_point[i+1][1]+5:
                    del previous_point[i]
                    c = True
                    break
            if c:
                c = False
                continue
            break

        return previous_point
    
    for gp in green_points:
        if gp != start_point:
            distance = dist(gp, start_point)
            if distance < maxStride and not start_point[1]-5 < gp[1]:
                connected_points.append(gp)

    connected_points = Sort(connected_points)

    for points in connected_points:
        path = shortest_path(points,previous_point)

        if path is not None:
            if len(path) < min_path:
                min_path = len(path)
                minimum_path = path

    if not len(connected_points):
        del previous_point[-1]
        return

for gp in green_points: 
    if abs(gp[1] - green_points[0][1]) < 5 + maxStride:
        start_points.append(gp)

for start_point in start_points: 
    path = shortest_path(start_point,[])

minimum_path.insert(0,[minimum_path[0][0],800])
for i in range(len(minimum_path)-1):
    cv2.line(img0, minimum_path[i],minimum_path[i+1],(255,255,255),5)
    cv2.circle(img0, (minimum_path[i][0],minimum_path[i][1]), 13, (155, 0, 0), 3)

img0 = cv2.cvtColor(img0, cv2.COLOR_RGB2BGR)
cv2.imshow("modified", img0)
cv2.waitKey(0)
cv2.destroyAllWindows()
