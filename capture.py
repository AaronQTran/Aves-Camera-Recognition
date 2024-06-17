import os
import cv2
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

dir = './faces_dataset/Aaron'

cap = cv2.VideoCapture(0)
frame_count = 0
save_every_n_frames = 5  

while True:
    ret, frame = cap.read()
    if ret: 
        if frame_count % save_every_n_frames == 0:
            frame_path = os.path.join(dir, f'frame_{frame_count}.jpg')
            cv2.imwrite(frame_path, frame)
        frame_count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print('q')
        break

cap.release()
cv2.destroyAllWindows()
