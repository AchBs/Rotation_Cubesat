import cv2
import numpy as np

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
    upper_red = np.array([10, 255, 255])

    # Create a mask for the red color using the lower and upper bounds
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through the contours to find the square
    max_area = 0
    best_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
            if len(approx) == 4:
                max_area = area
                best_cnt = cnt

    # Draw the square contour on the frame
    cv2.drawContours(frame, [best_cnt], 0, (0, 255, 0), 3)

    # Calculate the centroid of the square
    M = cv2.moments(best_cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])

    # Find the vertex of the square closest to the centroid
    pts = approx.reshape((-1, 2))
    distances = np.sqrt(np.sum((pts - [cx, cy])**2, axis=1))
    min_index = np.argmin(distances)

    # Draw a line from the centroid to the vertex
    cv2.line(frame, (cx, cy), tuple(pts[min_index]), (255, 0, 0), 2)

    # Calculate the angle between the line and the x-axis
    angle = np.arctan2(pts[min_index][1] - cy, pts[min_index][0] - cx) * 180 / np.pi

    # Print the angle
    print('Angle:', angle)

    # Display the frame
    cv2.imshow('frame', frame)

    # Wait for a key press and check if the user wants to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera

cap.release()
cv2.destroyAllWindows()