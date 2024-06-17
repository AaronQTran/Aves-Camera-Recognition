import os
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, UnidentifiedImageError
import numpy as np

# Initialize the models
mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Supported image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# Function to check if a file is an image
def is_image_file(file_path):
    return os.path.splitext(file_path)[1].lower() in IMAGE_EXTENSIONS

# Function to process a single image and get the face embedding
def process_image(image_path):
    if not is_image_file(image_path):
        os.remove(image_path)
        print(f"Non-image file deleted: {image_path}")
        return None

    try:
        img = Image.open(image_path)  # Open the image
        img.verify()  # Verify that it is an image
        img = Image.open(image_path)  # Reopen the image (verify() function might close it)

        boxes, _ = mtcnn.detect(img)
        if boxes is None or len(boxes) != 1:
            os.remove(image_path)
            print(f'No face or multiple faces detected, image deleted: {image_path}')
            return None
        else:
            img_cropped = mtcnn(img)  # Detect and crop the face
            if img_cropped is not None:
                embedding = resnet(img_cropped.unsqueeze(0))  # Get the embedding of the cropped face
                return embedding
            else:
                os.remove(image_path)
                print(f"No face detected after cropping, image deleted: {image_path}")
                return None
    except UnidentifiedImageError:
        os.remove(image_path)
        print(f"Unidentified image file deleted: {image_path}")
        return None
    except PermissionError:
        print(f"Permission error, could not delete file: {image_path}")
        return None
    except Exception as e:
        try:
            os.remove(image_path)
            print(f"Error processing {image_path}: {e}. Image deleted.")
        except PermissionError:
            print(f"Permission error, could not delete file: {image_path}")
        return None

# Directory containing subfolders of images for each person
base_dir = './faces_dataset'

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

# Save the known_faces dictionary
torch.save(known_faces, 'known_faces.pt')

# To load the known_faces dictionary in your face recognition program
# known_faces = torch.load('known_faces.pt')

