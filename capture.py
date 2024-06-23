import os
import cv2
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

#if ur folder already has images set frame_count 1 greater than the frame image number
dir = './faces_dataset/Kamryn'

cap = cv2.VideoCapture(0)
frame_count = 5736
save_every_n_frames = 2

while True:
    ret, frame = cap.read()
    if ret: 
        if frame_count % save_every_n_frames == 0:
            frame_path = os.path.join(dir, f'frame_{frame_count}.jpg')
            cv2.imwrite(frame_path, frame)
        frame_count += 1
        cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('brake')
        break

cap.release()
cv2.destroyAllWindows()
