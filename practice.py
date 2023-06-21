import cv2

# Load the pre-trained cascade classifier for hand
hand_cascade = cv2.CascadeClassifier('path/to/haarcascade_hand.xml')

# Start the video capture
cap = cv2.VideoCapture(0)

while True:
    # Read frames from the camera
    ret, frame = cap.read()
    # Convert each frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect hand in the frame
    hands = hand_cascade.detectMultiScale(gray, 1.3, 5)
    # Draw rectangle over the detected hand
    for (x, y, w, h) in hands:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # Display the resulting frame
    cv2.imshow('Hand Detection', frame)
    # Exit the loop if the user presses "q" key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
