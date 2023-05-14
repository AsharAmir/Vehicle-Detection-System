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

