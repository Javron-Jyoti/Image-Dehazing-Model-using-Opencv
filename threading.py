import cv2
import numpy as np
import image_dehazer
import urllib.request
import threading

# Define the IP URL of the device camera
url = "http://192.168.0.101:8080/shot.jpg"

# Create a VideoCapture object to capture the video stream
cap = cv2.VideoCapture(url)

# Function to continuously fetch frames from the camera
def fetch_frames():
    global cap
    while True:
        try:
            stream = urllib.request.urlopen(url)
            bytes_data = bytearray(stream.read())
            frame = np.array(bytes_data)
            frame = cv2.imdecode(frame, -1)
            if frame is not None:
                cap = frame
        except Exception as e:
            print("Error occurred: ", e)

# Start a separate thread to continuously fetch frames
thread = threading.Thread(target=fetch_frames)
thread.daemon = True
thread.start()

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

skip_frames = 0
max_skip_frames = 10  # Number of frames to skip

# Loop over the frames in the video stream
while True:
    # Skip frames to reduce processing load
    skip_frames += 1
    if skip_frames < max_skip_frames:
        continue
    else:
        skip_frames = 0

    # Read a frame from the video stream
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
        break

    # Convert the frame to a NumPy array
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Resize the frame to improve processing speed
    resized_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # Dehaze the frame using the image_dehazer library
    dehazed_frame, _ = image_dehazer.remove_haze(resized_frame)

    # Display the dehazed frame
    cv2.imshow('Dehazed Frame', dehazed_frame)

    # Write the dehazed frame to the output video file
    out.write(dehazed_frame)

    # Check if the user pressed the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
out.release()
cv2.destroyAllWindows()