import cv2
from facenet_pytorch import MTCNN, InceptionResnetV1
import torch
from PIL import Image
import numpy as np

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# Load the models
mtcnn = MTCNN(image_size=160, margin=20, keep_all=True, device=device)  # Increased margin
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

known_faces = torch.load('known_faces.pt') #given a frame, make a func that returns the box coords and label of the face

def get_face_embedding(face):
    return resnet(face.to(device)).detach()

def recognize_faces(frame, threshold=0.8):
    identities = []
    boxes, probs = mtcnn.detect(frame, landmarks=False)
    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            x1, y1, x2, y2 = [int(coord) for coord in box]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

            # Extract the face region directly using mtcnn
            face_cropped = mtcnn.extract(frame, [box], save_path=None)
            
            if face_cropped is not None and len(face_cropped) > 0:
                face_cropped = face_cropped[0]  # Take the first face
                
                # Ensure the cropped face tensor has the right shape
                if len(face_cropped.shape) == 3:
                    face_cropped = face_cropped.unsqueeze(0).float()

                # Get the face embedding
                embedding = get_face_embedding(face_cropped)

                # Normalize the embedding
                embedding = embedding / embedding.norm(dim=1, keepdim=True)

                min_dist = float('inf')
                identity = None
                for name, known_embedding in known_faces.items():
                    # Ensure known_embedding is 1-dimensional
                    if len(known_embedding.shape) == 1:
                        known_embedding = known_embedding.unsqueeze(0)
                    
                    # Normalize the known embedding
                    known_embedding = known_embedding / known_embedding.norm(dim=1, keepdim=True)
                    
                    dist = torch.dist(embedding, known_embedding.to(device)).item()
                    if dist < min_dist:
                        min_dist = dist
                        identity = name

                if min_dist < threshold and identity is not None:
                    identities.append((identity, (x1,y1,x2,y2)))
                    print(f"Identified as {identity} with distance {min_dist}")
                    print(identities)
                else:
                    identities.append(('unknown', (x1,y1,x2,y2)))
                    print(f"Face not recognized, minimum distance {min_dist}")
                    print(identities)
            else:
                print("No face detected ")
    return identities



# while True:
#         # Detect faces in the frame, boxes is a tuple, so like ({x1 ,y1, x2, y2}, etc etc)
#         boxes, probs = mtcnn.detect(frame, landmarks=False)
#         if boxes is not None and len(boxes) > 0:
#             for box in boxes:
#                 x1, y1, x2, y2 = [int(coord) for coord in box]
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

#                 # Extract the face region directly using mtcnn
#                 face_cropped = mtcnn.extract(frame, [box], save_path=None)
                
#                 if face_cropped is not None and len(face_cropped) > 0:
#                     face_cropped = face_cropped[0]  # Take the first face
#                     print(f"Face cropped successfully with shape: {face_cropped.shape}")
                    
#                     # Ensure the cropped face tensor has the right shape
#                     if len(face_cropped.shape) == 3:
#                         face_cropped = face_cropped.unsqueeze(0).float()

#                     # Get the face embedding
#                     embedding = get_face_embedding(face_cropped)

#                     # Normalize the embedding
#                     embedding = embedding / embedding.norm(dim=1, keepdim=True)

#                     min_dist = float('inf')
#                     identity = None
#                     for name, known_embedding in known_faces.items():
#                         # Ensure known_embedding is 1-dimensional
#                         if len(known_embedding.shape) == 1:
#                             known_embedding = known_embedding.unsqueeze(0)
                        
#                         # Normalize the known embedding
#                         known_embedding = known_embedding / known_embedding.norm(dim=1, keepdim=True)
                        
#                         dist = torch.dist(embedding, known_embedding.to(device)).item()
#                         print(f"Comparing with {name}, distance: {dist}")
#                         if dist < min_dist:
#                             min_dist = dist
#                             identity = name

#                     if min_dist < threshold and identity is not None:
#                         print(f"Identified as {identity} with distance {min_dist}")
#                     else:
#                         print(f"Face not recognized, minimum distance {min_dist}")
#                 else:
#                     print("Face detected but not cropped properly.")
#         else:
#             print("No boxes detected.")
        

# cap.release()
# cv2.destroyAllWindows()