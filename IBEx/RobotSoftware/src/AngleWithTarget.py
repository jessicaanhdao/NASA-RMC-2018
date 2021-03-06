"""
Sample program that uses a generated GRIP pipeline to detect red areas in an image and publish them to NetworkTables.
"""
import numpy  # requires the numpy+mkl pkg
# from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import time
import cv2
import math
#import CameraClient
# import matplotlib.pyplot as plt
#test commit
# from Pipeline import GripPipeline


from TargetPipeline import TargetFinder
#from grip import GripPipeline
#from pipeline_with_angle import Pipeline
#import serial

# ser = serial.Serial('/dev/ttyACM0', 9600)


cameraWidth = 640 #px
cameraHeight = 480 #px
#focalLength = 4 #mm http://support.logitech.com/en_us/article/17556
#widthOfObject = 292.1 #mm, 11.5in
widthOfObject = 152.4
widthOfTall = 100
widthOfWide = 200
widthOfTarget = 0

#CHANGE THIS TO THE REAL NUMBER
distToWall = 10;

dFoV = 74 #deg
dFoV_test = 60 #deg
foundAngle = 1
gotDist = False
diagonal = math.sqrt(math.pow(cameraWidth,2)+math.pow(cameraHeight,2))
# focalLength = (diagonal/2)/math.tan(math.radians(dFoV/2))     #Using a ratio with a known focal length and FOV of a similar logitech webcam
#focalLength = 3 #mm
focalLength = (diagonal/2)/math.tan(math.radians(dFoV_test/2))
print "first focal length",focalLength
#print "2nd focal length",focalLength2

# TODO##########
camera_x_center = cameraWidth/2   #in px
camera_y_center = cameraHeight/2  #in px

###############
def convertPxToMM(px):
   return (widthOfTarget*focalLength)/px

def getRobotAngle(heights, widths, minAreaIndex, maxAreaIndex):
    MAX_BOX_AREA = 1000
    MIN_BOX_AREA= 10
    curr_box1 = widths[maxAreaIndex]*heights[maxAreaIndex] #left
    curr_box2 = widths[minAreaIndex]*heights[minAreaIndex]
    side = ""  
    if heights[maxAreaIndex]> widths[maxAreaIndex]:
        widthOfTarget = widthOfTall
        ratio_angle = curr_box2/float(curr_box1)
        side = "Right" 
        


    #if we are closer to the wide rectangle
    elif heights[maxAreaIndex]< widths[maxAreaIndex]:
        widthOfTarget = widthOfWide
        ratio_angle = curr_box1/float(curr_box2)
        side = "Left"
        
   # try:
   #     angle = math.degrees(math.asin(ratio_angle))
   # except ValueError as e:
   #     angle = math.degrees(math.asin(1/float(ratio_angle)))
   # print "Angle = ", angle
    return side

def getContourAreas(heights, widths, minAreaIndex, maxAreaIndex):
    box1 = widths[maxAreaIndex]*heights[maxAreaIndex] #left
    box2 = widths[minAreaIndex]*heights[minAreaIndex] #right
    return box1, box2

def center(pipeline):
    """
    Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
    :param pipeline: the pipeline that just processed an image
    :return: None
    """
    center_x_positions = []
    center_y_positions = []
    widths = []
    heights = []
    numContours = 0
    side = ""



    # Find the bounding boxes of the contours to get x, y, width, and height
    for contour in pipeline:
        x, y, w, h = cv2.boundingRect(contour)
        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        widths.append(w)
        heights.append(h)
        numContours+=1
    
    if numContours == 2:
        area1 = widths[0]*heights[0]
        area2 = widths[1]*heights[1]

        if area2>area1:
            if center_x_positions[1] > center_x_positions[0]:
                side = "Right"
            else:
                side = "Left"
        else:
            if center_x_positions[0] > center_x_positions[1]:
                side = "Right"
            else:
                side = "Left"
            
        #areas = np.array(area)
        #maxAreaIndex = np.argsort(areas)[-1]
        #minAreaIndex = np.argsort(areas)[-2]


        #curr_angle = getRobotAngle(heights,widths,minAreaIndex,maxAreaIndex)
        return side


def main():
    print('Creating video capture')

    cap = cv2.VideoCapture(1)

    print('Creating pipeline')
    #pipeline = Pipeline()
    pipeline = RedRanger()
    print('Running pipeline')
    time.sleep(1)
    # ser.write('a')
    while cap.isOpened():
        have_frame, frame = cap.read()
        if have_frame:
            pipeline.process(frame)
            cv2.imshow("Contours",frame)
            print "contours:" + str(len(pipeline.process(frame)))

        if len(pipeline.process(frame)) == 2:
            cv2.imwrite("contours.jpg", frame)
            output = pipeline.process(frame)
            break

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    print('Capture closed')
    cap.release()
    center(output)

if __name__ == '__main__':
    main()
