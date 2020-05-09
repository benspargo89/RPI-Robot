import cv2 as cv
import numpy as np
cap = cv.VideoCapture(0)
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
        j = mask[base - i*50,:]
        ##Get cumlative row total
        j = j.cumsum()
        ##Identify the ~median value
        k = j.max() / 2 / 255
        ##Find the position of the ~median value
        l = j.argmax() - k.astype(int)
        if l != 0:
            points.append([l, base-i*50])
            cv.arrowedLine(frame, (320,480),(l, base-i*50), (170,255-(i*40),255-(i*40)),thickness=2) 
            angle = np.rad2deg(np.arctan2((base-i*50) - 480, l - 320))
            angles.append(angle)
            org = (10, 20*i)
            fontScale = .5
            font = cv.FONT_HERSHEY_SIMPLEX
            color = (170, 255-(i*40), 255-(i*40))
            thickness = 2
            cv.putText(frame, f'Angle {i}: {round(angle,2)}', org, font, fontScale, color, thickness, cv.LINE_AA)
        else:
            points.append(False)
            angles.append(False)
    cv.imshow('mask',mask)
    cv.imshow('frame', frame) 
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break
cv.destroyAllWindows()
