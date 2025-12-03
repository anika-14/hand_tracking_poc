import cv2
import numpy as np

# Thresholds for distance (pixels)
SAFE_DIST = 150
WARNING_DIST = 70

# Virtual object coordinates
obj_x1, obj_y1, obj_x2, obj_y2 = 300, 100, 500, 300

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # Mirror image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Skin color range (adjust if needed)
    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Remove noise
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    state = "SAFE"
    
    if contours:
        hand_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(hand_contour)
        if M["m00"] != 0:
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])
            cv2.circle(frame, (cx, cy), 7, (255, 0, 0), -1)

            # Distance to object center
            obj_cx = (obj_x1 + obj_x2)//2
            obj_cy = (obj_y1 + obj_y2)//2
            dist = np.sqrt((cx - obj_cx)**2 + (cy - obj_cy)**2)

            if dist < WARNING_DIST:
                state = "DANGER"
            elif dist < SAFE_DIST:
                state = "WARNING"

    # Draw virtual object
    color = (0, 255, 0) if state == "SAFE" else (0, 255, 255) if state == "WARNING" else (0, 0, 255)
    cv2.rectangle(frame, (obj_x1, obj_y1), (obj_x2, obj_y2), color, 2)

    # Overlay state
    cv2.putText(frame, f"STATE: {state}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    if state == "DANGER":
        cv2.putText(frame, "DANGER DANGER", (200, 400), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 3)

    cv2.imshow("Hand Tracking POC", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
