import cv2 as cv
import sys
import numpy as np
from motor import approach, move

cap = cv.VideoCapture(0)
cap.set(cv2.cv.CV_CAP_PROP_FPS, 10)
while(1):
    _, frame = cap.read()
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_pink = np.array([155,75,50])
    upper_pink = np.array([160,170,255])
    mask = cv.inRange(hsv, lower_pink, upper_pink)
    ret3,mask = cv.threshold(mask,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    kernel = np.ones((5,5),np.uint8)
    ##Reduces edge noise
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    ##Reduces internal noise
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

    points = []
    angles =[]
    for i in range(1,7):
        base = 450
        ##Get data for a particular row
        j = mask[base - i*50,:]
        ##Caclculate cumlative row total
        j = j.cumsum()
        ##Identify the ~median value
        ## -> the max value is the right edge of the mask
        k = j.max() / 2 / 255
        ##Find the position of the ~median value 
        ##-> given the first occurence of the max is the right edge, 
        ##and the max represent the cumulative total active pixels 
        ##in the row, we can identify the median pixel
        l = j.argmax() - k.astype(int)
        if l != 0:
            points.append([l, base-i*50])
            cv.arrowedLine(frame, (320,480),(l, base-i*50), (170,255-(i*40),255-(i*40)),thickness=2) 
            angle = abs(np.rad2deg(np.arctan2((base-i*50) - 480, l - 320))) - 90
            angles.append(angle)
            org = (10, 20*i)
            fontScale = .5
            font = cv.FONT_HERSHEY_SIMPLEX
            color = (170, 255-(i*40), 255-(i*40))
            thickness = 2
            cv.putText(frame, f'Angle {i}: {round(angle,2)}', org, font, fontScale, color, thickness, cv.LINE_AA)
        # else:
            # pass
            # points.append(False)
            # angles.append(False)
        # if angles:
        #     approach(angles)
        if points:
            approach(points[-1][0])
        else:
            move(timed=True)
            print('Lost the line...')
            sys.exit()
    cv.imshow('mask',mask)
    cv.imshow('frame', frame) 
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
