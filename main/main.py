#importing the prerequisite libraries
import cv2
import numpy as nm
import os
import datetime
import time
import webbrowser
from config import * #importing the config file

#loading the video feed 
frameCapture = cv2.VideoCapture(vid_source)


if not frameCapture.isOpened():
    print("Error: Could not open video file.")

#initialising the background subtractor
bgSubtractor = cv2.bgsegm.createBackgroundSubtractorMOG()

#variable initialisation
vehicleCounterArray = [] #the array which stores x,y for the vehicle midpoints
vehicleCounter = 0 #counts the number of vehicles crossing the line


#function to calculate the midpoint of our contour frame around a vehicle
def vehiclePointer(x, y, w, h):
    xMid = int(w / 2)
    yMid = int(h / 2)
    midX = x + xMid
    midY = y + yMid
    return midX, midY


while True:
    #reading the video feed
    frameReturn, mainFrame = frameCapture.read()
    greyFrame = cv2.cvtColor(mainFrame, cv2.COLOR_BGR2GRAY) #converting to greyscale as it reduces the model complexity
    blurFrame = cv2.GaussianBlur(greyFrame, (5, 5), 5) #adding a blur frame to increase robustness
    imgSubtract = bgSubtractor.apply(blurFrame) #bgSubtractor function to reduce memory usage
    dilateFrame = cv2.dilate(imgSubtract, nm.ones((5, 5))) #dilating the pixels to increase the size of the said frames, and increase accuracy
    kernelFrame = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) #creating a structuring element of a particular shape
    dilateApply = cv2.morphologyEx(dilateFrame, cv2.MORPH_CLOSE, kernelFrame) #applying the dilate frames
    dilateApply = cv2.morphologyEx(dilateApply, cv2.MORPH_CLOSE, kernelFrame)
    vehicleContour, h = cv2.findContours(dilateApply, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) #retrieving the contours in a numpy array
    
    #countLine rendering
    cv2.line(mainFrame, (1, linePosY), (1300, linePosY), (225, 225, 225), 2)
    
    #using enumerate loop thru the numpy array of contours to generate the rectangles around the vehicles
    for (i, n) in enumerate(vehicleContour):
        (x, y, w, h) = cv2.boundingRect(n)
        #validating if its a vehicle to minimise errors
        if not ((w >= min_Width) and (h >= min_Height)):
            continue
        #text rendering
        cv2.putText(mainFrame, "Vehicle#" + str(vehicleCounter), (x, y - 22), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0, 0, 255), 1)
        #rectangle rendering
        cv2.rectangle(mainFrame, (x, y), (x + w, y + h), (rect_r, rect_g, rect_b), rect_t)
        
        #midPoint variable
        midPointer = vehiclePointer(x, y, w, h)
        #adding the midpoints to our array
        vehicleCounterArray.append(midPointer)
        #rendering the midpoint
        cv2.circle(mainFrame, midPointer, 10, (0, 0, 255), -1)
        #cv2.drawContours(mainFrame, vehicleContour, -1, (255, 0, 255), 1)
        for(x, y) in vehicleCounterArray:
            #setting a range 
            if y < (linePosY + pixelOffsetMargin) and y > (linePosY - pixelOffsetMargin):
                vehicleCounter += 1
            #rendering gui elements
            cv2.line(mainFrame, (1, linePosY), (1300, linePosY), (0, 157, 0), 2)
            vehicleCounterArray.remove((x, y))
            print("Current Vehicle Count: " + str(vehicleCounter))

        if vehicleCounter > MAX_VEHICLE:
            # Draw alert
            cv2.rectangle(mainFrame, (rectX, rectY), (rectX + rectWidth, rectY + rectHeight), (0, 0, 255), -1)
            cv2.putText(mainFrame, text, (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, textSize, (255, 255, 255), textThickness)

