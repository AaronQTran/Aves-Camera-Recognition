from api import create_app
import cv2
import threading
import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from facial_recognition import recognize_faces
from YoloV5STracking.body import detectBody
import json
import time
import datetime as dt

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

mtcnn = MTCNN(image_size=160, margin=20, keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

cap = cv2.VideoCapture(0)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Frame width: {frame_width}, Frame height: {frame_height}")

# Shared variables to store results
face_results = []
body_results = []
body_faces = {}  # Maps body_id to body_face

# Lock for JSON file access
json_lock = threading.Lock()

def process_faces(frame):
    global face_results
    face_results = recognize_faces(frame)

def process_bodies(frame):
    global body_results
    body_results = detectBody(frame)

def video_processing():
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

        # Update body with face label and permanently assign it that label
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
            # print(body_results[i])
            # update body result with the associated face

        for identity, (fx1, fy1, fx2, fy2) in face_results:
            label = identity
            cv2.putText(frame, label, (fx1, fy1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)
            cv2.rectangle(frame, (fx1, fy1), (fx2, fy2), (255, 0, 0), 2)

        for (bx1, by1, bx2, by2, body_id, body_face) in body_results:
            cv2.rectangle(frame, (bx1, by1), (bx2, by2), (0, 255, 0), 2)
            cv2.putText(frame, str(body_id) + ' ' + str(body_face), (bx1, by1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Detection if Tracked Person is Within Door Border
        # Not Implemented, but Placeholder for Door Coordinates System?
        
        

        # Find Area of Door Box
        # When Coordinates Implemented
        # doorCoordinates = [x1, y1, x2, y2]
        doorCoordinates = [0, 0, 0, 0]
        doorHeight = doorCoordinates[3] - doorCoordinates[1]
        doorWidth = doorCoordinates[2] - doorCoordinates[0]
        doorArea = doorHeight * doorWidth
          
        # Find Area of Persons Box
        for (bx1, by1, bx2, by2, body_id, body_face) in body_results:
            if body_face == 'unknown':
                continue
            personHeight = by2 - by1
            personWidth = bx2 - bx1
            personArea = personHeight*personWidth

            # Tuples to Store Coordinates of All 4 Corners
            topLeft = (bx1, by1)
            bottomLeft = (bx1, by2)
            topRight = (bx2, by1)
            bottomRight = (bx2, by2)
            # Check if Persons X Values are Within Doors X Values+1
            # Check if Area of Persons Box is Equal to or Less Than the Doors Area
            # Tuple of Bottom Left X Value, and Bottom Right X Value
            if all((doorCoordinates[0] <= point[0] <= doorCoordinates[2] for point in (bottomLeft[0], bottomRight[0])) and personArea <= doorArea):

                todaysDate = dt.datetime.now()
                # Strftime Identifiers; %A Weekday, %H Hour, %M Minute, %p AM/PM
                # Correct 24hr to 12hr Format
                if (todaysDate.hour >= 12):
                    todaysDate = todaysDate.replace(hour=todaysDate.hour - 12)
                    todaysDate = todaysDate.strftime("%A,  %H:%M PM")
                else:
                    todaysDate = todaysDate.strftime("%A,  %H:%M AM")

                todaysWeekday = todaysDate.strftime("%A").lower()



                # Person is Within Door - Detected as Entering/Leaving
                # If Detected, Swap their Status to Opposite
                # Iterate Through Data Sheet
                # Compare Name to Name Found
                # Note WITH ALREADY CLOSES JSON FILE, with makes sure only 1 thread can read/write to json file in an instance/
                with json_lock:  
                    with open("roommateData.json") as json_file:
                        data = json.load(json_file)

                    # Update Roommate Status Alteration to Check Time Elapsed
                    # Ensures Only 1 Change Per Person, Per 30 Seconds
                    for roommate in data["roommateInfo"]:
                        if roommate["name"] == body_face:

                            # If TimeStamp Null, Set TimeStamp
                            if roommate["timeStamp"] == "Null":
                                roommate["timeStamp"] = str(time.time())

                            # If TimeStamp is Set, Check Elapsed Time
                            elif roommate["timeStamp"] != "Null":
                                elapsedTime = time.time() - int(roommate["timeStamp"])

                                # If Time Elapsed, Changes can occur
                                if elapsedTime <= 30:
                                    # Swap Status to Outside
                                    if roommate["status"] == "Inside":
                                        roommate["status"] = "Outside"

                                        # Update TimeStamp
                                        roommate["timeStamp"] = str(time.time())

                                        # Update Last Exit
                                        roommate["lastExist"] = todaysDate

                                        # Increment Weekday Left + ReCalculate Average
                                        roommate[todaysWeekday] += 1
                                        # Calculate Average Times Left/week
                                        # Take Total of Each Day / Current Day of Week
                                        currentDay = dt.datetime.now().weekday()
                                        weekdayValues = []
                                        for day in range (currentDay +1):
                                            weekdayValues.append(roommate[["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"][day]])
                                        roommate["avgTimeLeft"] = sum(weekdayValues)/len(weekdayValues)

                                        # Start Point to Calculate Avg Time Away
                                        

                                    # Swap Status to Inside
                                    else:
                                        roommate["status"] = "Inside"
                                        # Update Time Stamp
                                        roommate["timeStamp"] = str(time.time())
                                        # Update Last Enter
                                        roommate["lastEnter"] = todaysDate

                                        # End Point to Calculate Avg Time Away
                                        
                                        

                                else:
                                    continue

                    # Save Updated Info to JSON File
                    with open("roommateData.json", "w") as json_file:
                        json.dump(data, json_file, indent=4)

        # Camera Display w/ Facial Tracking and Body Tracking
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

app = create_app()

if __name__ == '__main__':
    video_thread = threading.Thread(target=video_processing)
    video_thread.start()
    app.run(debug=True, port=5000)
