# Import Libraries
import cv2
import torch
from tracker import *
import numpy as np

# Load Pre-Trained YoloV5 Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Open Video Capture of CCTV for Testing
cap = cv2.VideoCapture("cctv.mp4")

# Function to Show X & Y Coordinates of Mouse Cursor
def POINTS(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)
        
# Opens Frame - Autosize to Avoid cv2 GUI Error
cv2.namedWindow("FRAME", cv2.WINDOW_AUTOSIZE)
# Calls Mouse Events to POINTS Function Works
cv2.setMouseCallback("FRAME", POINTS)

# Tracking Module for YoloV5
tracker = Tracker()
while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture frame")
        break
    
    frame = cv2.resize(frame, (1020, 500))
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

    cv2.imshow('FRAME', frame)
    
    # Wait for Esc key to exit
    # Replace 1 with 0 to Freeze Frame
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
