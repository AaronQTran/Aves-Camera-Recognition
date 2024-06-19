import cv2
import torch
from PIL import Image

# Model Loading - yolo5vs is the lightest and fastest pre-trained model.
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

im1 = Image.open("zidane.jpg")  # PIL image
im2 = cv2.imread("bus.jpg")[..., ::-1]  # OpenCV image (BGR to RGB)


# Model Settings
# model.conf = 0.25  # NMS confidence threshold
# iou = 0.45  # NMS IoU threshold
# agnostic = False  # NMS class-agnostic
# multi_label = False  # NMS multiple labels per box
# classes = None  # (optional list) filter by class, i.e. = [0, 15, 16] for COCO persons, cats and dogs
# max_det = 1000  # maximum number of detections per image
# amp = False  # Automatic Mixed Precision (AMP) inference

# Inference
results = model([im1, im2], size=640)  # batch of images

# Results
results.print()
results.save()  # or .show()

results.xyxy[0]  # im1 predictions (tensor)
results.pandas().xyxy[0]  # im1 predictions (pandas)