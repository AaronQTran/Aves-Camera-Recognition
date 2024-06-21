# Import Libraries
import cv2
import torch
from .tracker import *
import numpy as np

# Load Pre-Trained YoloV5 Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Tracking Module for YoloV5
def detectBody(frame):
    box_id = None
    tracker = Tracker()
    # Inference
    results = model(frame)
    # Pandas Displays Data within Results
    # Classes, X & Y Coordinates, Name, etc.
    a = results.pandas().xyxy[0]
    # print(a) - Test to View Data

    list=[]
    for index, row in a.iterrows():
        # X/Y Coordinates within Pandas Data
        x1=int(row['xmin'])
        y1=int(row['ymin'])
        x2=int(row['xmax'])
        y2=int(row['ymax'])
        b=str(row['name'])
        if 'person' in b:
        # Frame, Coordinates, Color, Thickness
        # cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,255), 2)
        # Frame, Coordinates, Font, Font Size, Color, Thickness
        # cv2.putText(frame, b, (x1, y1), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)

        # Creating List of Coordinates for Updated System
            list.append([x1,y1,x2,y2])

    # Create ID's with Tracker
    boxes_ids=tracker.update(list)
    for box_id in boxes_ids:
        # Parameters for Drawing Box
        # X, Y, Width, Height, ID
        x,y,w,h,id=box_id
        # X, Y, Width, Height, Color, Thickness
        cv2.rectangle(frame, (x,y), (w,h), (0,0,255), 2)
        # Frame, ID, Coordinates, Font, Font Size, Color, Thickness
        cv2.putText(frame, str(id), (x,y), cv2.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
        print(box_id)
    return box_id
        