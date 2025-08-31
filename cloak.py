import cv2
import numpy as np
import time

# Open the webcam
cap = cv2.VideoCapture(0)

# Let the camera warm up
time.sleep(3)

# Capture background
for i in range(60):
    ret, background = cap.read()
background = np.flip(background, axis=1)

# Define codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')   # Codec (XVID works well)
out = cv2.VideoWriter('invisibility.avi', fourcc, 20.0, (640,480))  # filename, codec, fps, frame size

while cap.isOpened():
    ret, img = cap.read()
    if not ret:
        break

    img = np.flip(img, axis=1)

    # Convert to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Red color
    lower_red1 = np.array([0,150,120])    # raise S and V min
    upper_red1 = np.array([10,255,255])

    lower_red2 = np.array([170,150,120])
    upper_red2 = np.array([180,255,255])



    # Create masks
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 + mask2

    # Refine mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3,3), np.uint8))

    # Inverse mask (to get everything except cloak)
    mask_inv = cv2.bitwise_not(mask)
    

    # Cloak area replaced with background
    cloak_area = cv2.bitwise_and(background, background, mask=mask)
    
    # Rest of frame (everything except cloak)
    non_cloak_area = cv2.bitwise_and(img, img, mask=mask_inv)
    
    # Combine both
    final_output = cv2.addWeighted(cloak_area, 1, non_cloak_area, 1, 0)
    
    # Show
    cv2.imshow('Invisibility Cloak', final_output)

    # Write frame to file
    out.write(final_output)

    # Quit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
