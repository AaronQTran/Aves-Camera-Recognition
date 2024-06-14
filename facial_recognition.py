import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import numpy as np

# Determine the device to use
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load the models
mtcnn = MTCNN(keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

# Load the known faces
known_faces = torch.load('known_faces.pt')

# Function to calculate face embeddings
def get_face_embedding(face):
    return resnet(face.to(device))

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

# Define a threshold
threshold = 0.6

while True:
    ret, frame = cap.read()
    if ret:
        boxes, _ = mtcnn.detect(frame, landmarks=False)
        if boxes is not None and len(boxes) > 0:
            for box in boxes:
                x1, y1, x2, y2 = [int(coord) for coord in box]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # Extract face region from the frame
                face = frame[y1:y2, x1:x2]
                face_pil = Image.fromarray(face)
                face_cropped = mtcnn(face_pil)

                if face_cropped is not None:
                    # Ensure the cropped face tensor has the right shape
                    if len(face_cropped.shape) == 3:
                        face_cropped = face_cropped.unsqueeze(0).float()

                    embedding = get_face_embedding(face_cropped)

                    min_dist = float('inf')
                    identity = None
                    for name, known_embedding in known_faces.items():
                        dist = torch.dist(embedding, known_embedding.to(device)).item()
                        if dist < min_dist:
                            min_dist = dist
                            identity = name

                    if min_dist < threshold and identity is not None:
                        cv2.putText(frame, identity, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    else:
                        cv2.putText(frame, 'Unknown', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                else:
                    print("Face detected but not cropped properly.")
                    cv2.putText(frame, 'No face detected', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            print("No boxes detected.")
            cv2.putText(frame, 'No face detected', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()





