import os
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import numpy as np

# Initialize the models
mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Function to process a single image and get the face embedding
def process_image(image_path):
    try:
        img = Image.open(image_path)  # Open the image
        img_cropped = mtcnn(img)  # Detect and crop the face
        if img_cropped is not None:
            embedding = resnet(img_cropped.unsqueeze(0))  # Get the embedding of the cropped face
            return embedding
        else:
            print(f"No face detected in {image_path}")  # Print a message if no face is detected
            return None
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None


# Directory containing subfolders of images for each person
base_dir = 'path_to_your_base_directory'

# Dictionary to store mean embeddings for each person
known_faces = {}

# Loop through each subfolder (each person's folder)
for person_name in os.listdir(base_dir):
    person_dir = os.path.join(base_dir, person_name)
    if os.path.isdir(person_dir):
        embeddings = []
        for image_name in os.listdir(person_dir):
            image_path = os.path.join(person_dir, image_name)
            embedding = process_image(image_path)
            if embedding is not None:
                embeddings.append(embedding)
        
        # Combine all embeddings into a single tensor and calculate the mean embedding
        if embeddings:
            embeddings = torch.cat(embeddings)
            mean_embedding = embeddings.mean(dim=0)
            known_faces[person_name] = mean_embedding
            # Save the mean embedding to a file (optional)
            torch.save(mean_embedding, f'{person_name}_embedding.pt')

# Save the known_faces dictionary
torch.save(known_faces, 'known_faces.pt')

# To load the known_faces dictionary in your face recognition program
# known_faces = torch.load('known_faces.pt')
