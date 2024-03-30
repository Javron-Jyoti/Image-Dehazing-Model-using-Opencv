import cv2
import urllib
import numpy as np
import image_dehazer

# Define the IP URL of the device camera
url = "http://192.168.0.101:8080/shot.jpg"

# Create a VideoCapture object to capture the video stream
cap = cv2.VideoCapture(url)

# Check if the VideoCapture object was successfully created
if not cap.isOpened():
    print("Error: Could not open video stream")
    exit()

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = cap.get(5)

# Define the codec and create a VideoWriter object for the output
output_path = r'C:\Users\sjyot\OneDrive\Desktop\video2.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Loop over the frames in the video stream
while True:
    # Read the next frame from the video stream
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
        break

    # Dehaze the frame using the image_dehazer library
    dehazed_frame, haze_map = image_dehazer.remove_haze(frame)

    # Display the dehazed frame
    cv2.imshow('Dehazed Frame', dehazed_frame)

    # Write the dehazed frame to the output video file
    out.write(dehazed_frame)

    # Check if the user pressed the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.waitKey(50000)
cv2.destroyAllWindows()