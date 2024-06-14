import cv2
from facenet_pytorch import MTCNN

# Create a face detection pipeline using MTCNN:
mtcnn = MTCNN()

# Open a connection to the webcam:
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam:
    ret, frame = cap.read()

    # If a frame was successfully read:
    if ret:
        # Detect faces in the frame:
        boxes, _ = mtcnn.detect(frame)

        # If at least one face was detected:
        if boxes is not None:
            # Draw a rectangle around each face:
            for box in boxes:
                x1, y1, x2, y2 = [int(coord) for coord in box]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Display the frame with bounding boxes:
        cv2.imshow('Video', frame)

        # If the 'q' key is pressed, break the loop:
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release the webcam and destroy all windows:
cap.release()
cv2.destroyAllWindows()

