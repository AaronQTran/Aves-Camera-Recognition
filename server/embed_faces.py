import os
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image, UnidentifiedImageError
import json

# Initialize MTCNN and InceptionResnetV1 models
mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20)
resnet = InceptionResnetV1(pretrained='vggface2').eval()

# Supported image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png'}

# Paths for known faces and progress files
data_dir = os.path.join(os.path.dirname(__file__), 'ptdata')
known_faces_file = os.path.join(data_dir, 'known_faces.pt')
progress_file = os.path.join(data_dir, 'progress.json')

def is_image_file(file_path):
    return os.path.splitext(file_path)[1].lower() in IMAGE_EXTENSIONS

def process_image(image_path):
    print(f"Processing image: {image_path}")
    if not is_image_file(image_path):
        os.remove(image_path)
        print(f"Non-image file deleted: {image_path}")
        return None

    try:
        img = Image.open(image_path)
        img.verify()
        img = Image.open(image_path)

        boxes, _ = mtcnn.detect(img)
        if boxes is None or len(boxes) != 1:
            os.remove(image_path)
            print(f'No face or multiple faces detected, image deleted: {image_path}')
            return None
        else:
            img_cropped = mtcnn(img)
            if img_cropped is not None:
                embedding = resnet(img_cropped.unsqueeze(0))
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

def load_known_faces(file_path):
    if os.path.exists(file_path):
        return torch.load(file_path)
    return {}

def save_known_faces(file_path, known_faces):
    torch.save(known_faces, file_path)

def load_progress(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_progress(file_path, progress):
    with open(file_path, 'w') as f:
        json.dump(progress, f)

def process_person(person_dir, known_faces, progress, processed_count, chunk_size):
    embeddings = []
    person_name = os.path.basename(person_dir)
    processed_images = progress.get(person_name, [])
    
    for image_name in os.listdir(person_dir):
        if processed_count >= chunk_size:
            break
        if image_name in processed_images:
            continue
        
        image_path = os.path.join(person_dir, image_name)
        embedding = process_image(image_path)
        if embedding is not None:
            embeddings.append(embedding)
            processed_images.append(image_name)
            processed_count += 1

    if embeddings:
        embeddings = torch.cat(embeddings)
        mean_embedding = embeddings.mean(dim=0)
        known_faces[person_name] = mean_embedding

    progress[person_name] = processed_images
    return processed_count

def main():
    base_dir = './faces_dataset'
    chunk_size = 1000  #processes however many jpgs

    known_faces = load_known_faces(known_faces_file)
    progress = load_progress(progress_file)

    person_dirs = [os.path.join(base_dir, person_name) for person_name in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, person_name))]

    processed_count = 0

    for person_dir in person_dirs:
        if processed_count >= chunk_size:
            break
        processed_count = process_person(person_dir, known_faces, progress, processed_count, chunk_size)

    save_known_faces(known_faces_file, known_faces)
    save_progress(progress_file, progress)

if __name__ == '__main__':
    main()
