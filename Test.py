# Facenet from Pytorch Pre-Trained Model
from facenet_pytorch import MTCNN
# PyTorch AI Library
import torch
import numpy as np
# Computer Vision Library
import mmcv, cv2
# Image Library
from PIL import Image, ImageDraw
# Computer Display Library
from IPython import display

# Detect if Computer has Cuda NVIDIA GPU, Else use CPU.
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# Tell What Device
print('Running on device: {}'.format(device))

# Create Neural Network
mtcnn = MTCNN(keep_all=True, device=device)

# Get Sample Video using MMCV Package.
video = mmcv.VideoReader('kamtest2.mp4')
frames = [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in video]

display.Video('kamtest2.mp4', width=1080)

# Run Video Through MTCNN
frames_tracked = []
for i, frame in enumerate(frames):
    print('\rTracking frame: {}'.format(i + 1), end='')
    
    # Detect faces
    boxes, _ = mtcnn.detect(frame)
    
    # Draw faces if any are detected
    if boxes is not None:
        frame_draw = frame.copy()
        draw = ImageDraw.Draw(frame_draw)
        for box in boxes:
            draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)
    else:
        # If no faces are detected, continue to the next frame
        frames_tracked.append(frame.resize((640, 360), Image.BILINEAR))
        continue
    
    # Add to frame list
    frames_tracked.append(frame_draw.resize((640, 360), Image.BILINEAR))
print('\nDone')

# Display NN Detections
d = None
try:
    for frame in frames_tracked:
        if d is None:
            d = display.display(frame, display_id=True)
        else:
            d.update(frame)
except KeyboardInterrupt:
    pass

# Get the total number of frames
total_frames = len(frames)

# Get the duration of the video in seconds
video_duration = total_frames / video.fps

# Calculate the frame rate
frame_rate = total_frames / video_duration

# Save Video
dim = frames_tracked[0].size
fourcc = cv2.VideoWriter_fourcc(*'mp4v')    
video_tracked = cv2.VideoWriter('video_tracked.mp4', fourcc, frame_rate, dim)
for frame in frames_tracked:
    video_tracked.write(cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))
video_tracked.release()