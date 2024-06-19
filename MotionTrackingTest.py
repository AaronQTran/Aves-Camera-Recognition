import cv2
import torch

# Load YOLOv5 model
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

# Open the webcam
cap = cv2.VideoCapture(0)  # 0 for default webcam

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to RGB
    frame_rgb = frame[..., ::-1]

    # Run inference
    results = model(frame_rgb, size=640)

    # Process the results (draw bounding boxes)
    for det in results.pred[0]:
        x1, y1, x2, y2, conf, cls = det.tolist()
        if conf > 0.5:  # Set a confidence threshold
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(frame, f"{model.names[int(cls)]} {conf:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the processed frame
    cv2.imshow("YOLOv5 Webcam", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the webcam
cap.release()
cv2.destroyAllWindows()