import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch

# Load the models
mtcnn = MTCNN()
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Load the known faces
known_faces = torch.load('known_faces.pt')

# Function to calculate face embeddings
def get_face_embedding(face):
    return resnet(face.unsqueeze(0))

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

#ADD THRESHHOLD

while True:
    ret, frame = cap.read()
    if ret:
        boxes, faces = mtcnn.detect(frame, landmarks=False)
        if boxes is not None:
            for box, face in zip(boxes, faces):
                x1, y1, x2, y2 = [int(coord) for coord in box]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

                face_tensor = torch.tensor(face).permute(2, 0, 1).unsqueeze(0).float()
                embedding = get_face_embedding(face_tensor)
                
                min_dist = float('inf')
                identity = None
                for name, known_embedding in known_faces.items():
                    dist = torch.dist(embedding, known_embedding).item()
                    if dist < min_dist:
                        min_dist = dist
                        identity = name
                
                if identity is not None:
                    cv2.putText(frame, identity, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
