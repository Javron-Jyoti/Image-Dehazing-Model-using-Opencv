import cv2
import image_dehazer

# Open the video file
video_path = r'C:\Users\sjyot\OneDrive\Desktop\dense.mp4'
cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
if not cap.isOpened():
    print("Error opening video file")
    exit()

# Get video properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
fps = cap.get(5)

# Define the codec and create a VideoWriter object for the output
output_path = r'C:\Users\sjyot\OneDrive\Desktop\video2.avi'
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# Process each frame
while True:
    ret, frame = cap.read()


    # Break the loop if the video is over
    if not ret:
        break

    # Apply dehazing
    dehaze_frame, haze_map = image_dehazer.remove_haze(frame)

    # Display the dehazed frame
    cv2.imshow('Dehazed Frame', dehaze_frame)

    # Write the dehazed frame to the output video file
    out.write(dehaze_frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
