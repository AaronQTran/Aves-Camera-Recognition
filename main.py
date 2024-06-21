import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import numpy as np
from facial_recognition import recognize_faces
from YoloV5STracking.body import detectBody


device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load the models
mtcnn = MTCNN(image_size=160, margin=20, keep_all=True, device=device)  # Increased margin
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

def get_face_embedding(face):
    return resnet(face.to(device)).detach()

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    detectBody(frame)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()