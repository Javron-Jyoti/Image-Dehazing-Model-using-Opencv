import cv2
import numpy as np

cap = cv2.VideoCapture(0)  # '0' is for the default camera. You can change this if you have multiple cameras.

def remove_fog(frame):
    # Convert the frame to LAB color space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    # Apply CLAHE to the L channel
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    # Merge the processed L channel back with the original A and B channels
    lab = cv2.merge((l, a, b))

    # Convert the LAB image back to BGR color space
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Additional enhancements: adaptive thresholding and gamma correction
    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    result = cv2.bitwise_and(result, result, mask=mask)

    # Gamma correction for brightness adjustment
    gamma = 1.2
    result = np.clip(result ** gamma, 0, 255).astype(np.uint8)

    return result

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.imshow('Original with Fog', frame)
    
    frame_without_fog = remove_fog(frame)
    
    cv2.imshow('Enhanced Fog Removal', frame_without_fog)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
