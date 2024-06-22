import cv2
import torch
from .tracker import *
import numpy as np

# Load Pre-Trained YoloV5 Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Tracking Module for YoloV5
def detectBody(frame):
    tracker = Tracker()
    # Inference
    results = model(frame)
    # Pandas Displays Data within Results
    # Classes, X & Y Coordinates, Name, etc.
    a = results.pandas().xyxy[0]

    boxes_list = []
    for index, row in a.iterrows():
        # X/Y Coordinates within Pandas Data
        x1 = int(row['xmin'])
        y1 = int(row['ymin'])
        x2 = int(row['xmax'])
        y2 = int(row['ymax'])
        name = str(row['name'])
        if 'person' in name:
            # Creating List of Coordinates for Updated System
            boxes_list.append([x1, y1, x2, y2])

    # Create IDs with Tracker
    boxes_ids = tracker.update(boxes_list)
    result = []
    for box_id in boxes_ids:
        # Parameters for Drawing Box
        # X, Y, Width, Height, ID
        x1, y1, x2, y2, id = box_id
        # X, Y, Width, Height, Color, Thickness
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        # Frame, ID, Coordinates, Font, Font Size, Color, Thickness
        cv2.putText(frame, str(id), (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        body_face = None
        result.append((x1, y1, x2, y2, id, body_face))
        print(result)

    return result
        