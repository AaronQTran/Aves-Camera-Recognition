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
from db_config import get_db_connection

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
unknown_faces = {}

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
                unknown_faces[body_id] = 0
            for identity, (fx1, fy1, fx2, fy2) in face_results:
                if fx1 >= bx1 and fy1 >= by1 and fx2 <= bx2 and fy2 <= by2:
                    if identity == 'unknown':
                        unknown_faces[body_id]+=1
                        if unknown_faces[body_id]>=5:
                            body_faces[body_id] = identity
                            unknown_faces[body_id] = 0
                        break
                    body_faces[body_id] = identity
                    unknown_faces[body_id] = 0
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
            if (doorCoordinates[0] <= bottomLeft[0] <= doorCoordinates[2] and doorCoordinates[0] <= bottomRight[0] <= doorCoordinates[2] and personArea <= doorArea):
                todaysDate = dt.datetime.now()
                # Strftime Identifiers; %A Weekday, %H Hour, %M Minute, %p AM/PM
                # Correct 24hr to 12hr Format
                if (todaysDate.hour > 12):
                    todaysDate = todaysDate.replace(hour=todaysDate.hour - 12)
                    todaysDate = todaysDate.strftime("%A,  %H:%M PM")
                else:
                    todaysDate = todaysDate.strftime("%A,  %H:%M AM")

                todaysWeekday = todaysDate.strftime("%A").lower()

                AvesDB = get_db_connection()
                AvesCur = AvesDB.cursor()

                # Grab DB Users
                AvesCur.execute("SELECT * FROM roommates WHERE name=%s",body_face)

                # Fetch User's Meeting Data
                AvesUser = AvesCur.fetchone()

                # Index Information
                # 0(ID), 1(Name), 2(Status), 3-9(Monday-Sunday), 10(LastEnter), 11(LastExit), 12(avgTimeAway), 13(avgTimeLeft), 14(timeStamp), 15(totaltimeAway), 16(timeInstance)

                # If User Grabbed
                if AvesUser:
                    # Check Time Stamp Information
                    if (AvesUser[14] == "Null"):
                        sql = "UPDATE roommates SET timeStamp =%s WHERE name = %s"
                        val = (str(time.time()), body_face)
                        AvesCur.execute(sql, val)
                    elif (AvesUser[14] != "Null"):
                        elapsedtime = time.time() - int(AvesUser[14])
                        # If Time Elapsed >= 30 Seconds
                        if elapsedtime >= 30:
                            if (AvesUser[2] == "Inside"):
                                # Swap Status
                                sql = "UPDATE roommates SET status =%s WHERE name = %s"
                                val = ("Outside", body_face)
                                AvesCur.execute(sql, val)

                                # Update TimeStamp
                                sql = "UPDATE roommates SET timeStamp =%s WHERE name = %s"
                                val = (str(time.time()), body_face)
                                AvesCur.execute(sql, val)

                                # Update LastExit
                                sql = "UPDATE roommates SET lastExit =%s WHERE name = %s"
                                val = (todaysDate, body_face)
                                AvesCur.execute(sql, val)

                                # Increment Weekday
                                for i in range(3,10):
                                    if (AvesUser[i] == todaysWeekday):
                                        sql = "UPDATE roommates SET %s = %s + 1 WHERE name = %s"
                                        val = (todaysWeekday, todaysWeekday, body_face)
                                        AvesCur.execute(sql, val)

                                # Calculate Average Times Left/week
                                # Take Total of Each Day / Current Day of Week
                                # .weekday() Returns Number of Day in Week Starting at 0. Monday is 0, Sunday is 6.

                                # Monday = 0, We Will Add 3 to this to match tuple indexes.
                                currentDay = dt.datetime.now().weekday() + 3

                                weekdayValues = []
                                for day in range(currentDay):
                                    weekdayValues.append(AvesUser[day])

                                # Total Values in Weekday
                                totalVal = 0
                                for i in range(len(weekdayValues)):
                                    totalVal += weekdayValues[i]

                                # Calculate Avg Time Left
                                # Total Values in WeekdayValues/len(weekdayValues)
                                avgTimeLeft = totalVal/len(weekdayValues)

                                # Update avgTimeLeft
                                sql = "UPDATE roommates SET avgTimeLeft = %s WHERE name = %s"
                                val = (avgTimeLeft, body_face)
                                AvesCur.execute(sql, val)

                                # Start Point to Calculate Avg Time Away
                                # Epoch Seconds
                                timeStart = time.time()
                            else:
                                # Swap Status
                                AvesUser[2] = "Inside"
                                sql = "UPDATE roommates SET status =%s WHERE name = %s"
                                val = ("Outside", body_face)
                                AvesCur.execute(sql, val)

                                # Update TimeStamp 
                                sql = "UPDATE roommates SET timeStamp =%s WHERE name = %s"
                                val = (str(time.time()), body_face)
                                AvesCur.execute(sql, val)

                                # Update LastEnter
                                sql = "UPDATE roommates SET lastEnter =%s WHERE name = %s"
                                val = (todaysDate, body_face)
                                AvesCur.execute(sql, val)

                                # Start Point to Calculate Avg Time Away
                                # Epoch Seconds
                                timeEnd = time.time()

                        # Calculate Difference in Seconds
                        timeDiff = timeEnd - timeStart

                        # Add Elapsed Time to totalTimeAway
                        sql = "UPDATE roommates SET totalTimeAway = totalTimeAway + %s WHERE name = %s"
                        val = (timeDiff, body_face)
                        AvesCur.execute(sql, val)

                        # Increment Time Instances
                        sql = "UPDATE roommates SET timeInstance = timeInstance + %s WHERE name = %s"
                        val = (1, body_face)
                        AvesCur.execute(sql, val)

                        # Calculate Average
                        avgEpoch = AvesUser[3:10]/AvesUser[16]

                        # Conversion of Epoch Seconds to Readable Time
                        # Epoch can be Converted to Datetime Object
                        epochConversion = dt.datetime.fromtimestamp(avgEpoch)

                        # Conversion of 24hr format to 12hr Format
                        if (epochConversion.hour > 12):
                            epochConversion = epochConversion.replace(hour=todaysDate.hour - 12)
                            epochConversion = epochConversion.strftime("%A,  %H:%M PM")
                        else:
                            epochConversion = epochConversion.strftime("%A,  %H:%M AM")

                        # Update Avg Time Away
                        sql = "UPDATE roommates SET lastExit = avgTimeAway + %s WHERE name = %s"
                        val = (epochConversion, body_face)
                        AvesCur.execute(sql, val)
                    else:
                        continue

            # Commit Changes
            AvesDB.commit()

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
    app.run(debug=False, port=5000)
