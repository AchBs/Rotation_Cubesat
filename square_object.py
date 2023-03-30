import cv2
import math 
import numpy as np
import time

# Open the default camera
cap = cv2.VideoCapture(0)

# Set the camera resolution to 640x480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Loop through the frames of the video stream
while True:
    # Read the next frame from the camera
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the red color in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([4, 255, 255])
    # Define the lower and upper bounds of the Blue color in HSV
    lower_blue = np.array([38, 86, 0])
    upper_blue = np.array([121, 255, 255])

    # Create a mask for the red color using the lower and upper bounds
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_Blue = cv2.inRange(hsv, lower_blue, upper_blue)

    #centre (moment)
    moments1 = cv2.moments(mask_red, 0)
    moments2 = cv2.moments(mask_Blue, 0)




    area1=moments1['m00']
    area2=moments2['m00']

    #initialize x and y
    x1,y1,x2,y2=(1,2,3,4)
    coord_list=[x1,y1,x2,y2]
    for x in coord_list:
        x=0

    if area1 > 200000:
            # x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
            x2 = int(moments1['m10'] / area1)
            y2 = int(moments1['m01'] / area1)

    cv2.circle(frame,(x1,y1),2,(0,255,0),20)

    
    if area2 > 200000:
            # x and y coordinates of the center of the object is found by dividing the 1,0 and 0,1 moments by the area
            x1 = int(moments2['m10'] / area2)
            y1 = int(moments2['m01'] / area2)

    cv2.circle(frame,(x2,y2),2,(0,255,0),20)

    
    cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),4,cv2.LINE_AA)

    x1=float(x1)
    x2=float(x2)
    y1=float(y1)
    y2=float(y2)

    cv2.line(frame, (int(x1), int(y1)), (frame.shape[1], int(y1)), (100, 100, 100, 100), 4, cv2.LINE_AA)

    if y2>y1:
        if x2>x1:  

            angle = int(math.atan((y2-y1)/(x2-x1))*180/math.pi)

        elif x2<x1:
             
             angle= 180 +(int(math.atan((y1-y2)/(x1-x2))*180/math.pi))
        else: 
             
             angle = 90
    else :
        if x2<x1:  
            angle =180+(int(math.atan((y1-y2)/(x1-x2))*180/math.pi))
        elif x2>x1:
             
             angle= 360 -(int(math.atan((y1-y2)/(x2-x1))*180/math.pi))
        else: 
             angle = 270
         

        
    

    

    font = cv2.FONT_HERSHEY_SIMPLEX

    # Define font properties
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 2

    # Put text on the frame
    cv2.putText(frame, str(angle), (int(x1)+50, int((y2+y1)/2)), font, fontScale, (0,0,255), thickness)

       
    cv2.imshow('frame',frame)
    cv2.imshow('mask red', mask_red)
    cv2.imshow('mask Blue', mask_Blue)
        

    # Wait for a key press and check if the user wants to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera

cap.release()
cv2.destroyAllWindows()