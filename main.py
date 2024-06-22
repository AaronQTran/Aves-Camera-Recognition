import cv2
import threading
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from facial_recognition import recognize_faces
from YoloV5STracking.body import detectBody

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

mtcnn = MTCNN(image_size=160, margin=20, keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

cap = cv2.VideoCapture(0)

# Shared variables to store results
face_results = []
body_results = []
body_faces = {}  # Maps body_id to body_face

def process_faces(frame):
    global face_results
    face_results = recognize_faces(frame)

def process_bodies(frame):
    global body_results
    body_results = detectBody(frame)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Create threads for face and body processing
    face_thread = threading.Thread(target=process_faces, args=(frame,))
    body_thread = threading.Thread(target=process_bodies, args=(frame,))
    face_thread.start()
    body_thread.start()

    # Wait for both threads to finish
    face_thread.join()
    body_thread.join()

    #update body with face label and permanently assign it that label
    for i in range(len(body_results)):
        bx1, by1, bx2, by2, body_id, body_face = body_results[i][:6]
        if body_id not in body_faces:
            body_faces[body_id] = 'unknown'
        for identity, (fx1, fy1, fx2, fy2) in face_results:
            if fx1 >= bx1 and fy1 >= by1 and fx2 <= bx2 and fy2 <= by2:
                body_faces[body_id] = identity
                break
        body_face = body_faces[body_id]
        body_results[i] = (bx1, by1, bx2, by2, body_id, body_face)
        #update body result with the associated face

    for identity, (fx1, fy1, fx2, fy2) in face_results:
        label = identity
        cv2.putText(frame, label, (fx1, fy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
        cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), (255, 0, 0), 2)

    for (bx1, by1, bx2, by2, body_id, body_face) in body_results:
        cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 0), 2)
        cv2.putText(frame, str(body_id) + ' ' + str(body_face), (bx1, by1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
