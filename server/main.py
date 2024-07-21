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
from services import get_statistics
from flask_socketio import SocketIO, emit
import time
import os

dir = './images'
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

mtcnn = MTCNN(image_size=160, margin=20, keep_all=True, device=device)
resnet = InceptionResnetV1(pretrained='vggface2').eval().to(device)

cap = cv2.VideoCapture('../KamTestFinal.mp4')

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
    cv2.namedWindow('Video', cv2.WINDOW_NORMAL)  # Create a window named 'Video'
    cv2.resizeWindow('Video', 1280,720)  # Resize the window to the desired dimensions
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
        
        weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

        # Find Area of Door Box
        # When Coordinates Implemented
        # doorCoordinates = [x1, y1, x2, y2]
        doorCoordinates = [350,50,700,715]

        dx1 = doorCoordinates[0]
        dx2 = doorCoordinates[2]
        dy1 = doorCoordinates[1]
        dy2 = doorCoordinates[3]

        doorTopLeft = (dx1, dy1)
        doorBottomLeft = (dx1, dy2)
        doorTopRight = (dx2, dy1)
        doorBottomRight = (dx2, dy2)

        doorHeight = dy2 - dy1
        doorWidth = dx2 - dx1
        doorArea = doorHeight * doorWidth

        

        # Find Area of Persons Box
        for (bx1, by1, bx2, by2, body_id, body_face) in body_results:
            if body_face == 'unknown':
                continue
            personHeight = by2 - by1
            personWidth = bx2 - bx1
            personArea = personHeight*personWidth

            # Tuples to Store Coordinates of All 4 Corners
            personTopLeft = (bx1, by1)
            personBottomLeft = (bx1, by2)
            personTopRight = (bx2, by1)
            personBottomRight = (bx2, by2)
            # Check if Persons X Values are Within Doors X Values+1
            # Check if Area of Persons Box is Equal to or Less Than the Doors Area
            # Tuple of Bottom Left X Value, and Bottom Right X Value
            if (doorBottomLeft[0] <= personBottomLeft[0] <= doorBottomRight[0] and doorBottomLeft[0] <= personBottomRight[0] <= doorBottomRight[0] and personArea <= doorArea):
                todaysDate = dt.datetime.now()
                # Strftime Identifiers; %A Weekday, %H Hour, %M Minute, %p AM/PM
                # Correct 24hr to 12hr Format
                if todaysDate.hour == 0:
                    todaysDate = todaysDate.replace(hour=12)
                    todaysDate = todaysDate.strftime("%a, %I:%M AM")
                elif todaysDate.hour == 12:
                    todaysDate = todaysDate.strftime("%a, %I:%M PM")
                elif todaysDate.hour > 12:
                    todaysDate = todaysDate.replace(hour=todaysDate.hour - 12)
                    todaysDate = todaysDate.strftime("%a, %I:%M PM")
                else:
                    todaysDate = todaysDate.strftime("%a, %I:%M AM")

                todaysWeekday = dt.datetime.now().strftime("%A").lower()

                AvesDB = get_db_connection()
                AvesCur = AvesDB.cursor()

                # Grab DB Users
                body_face = body_face.title()
                AvesUser = get_statistics(body_face.title())
                
                # send jpg to images folder
                if(body_face == 'Andrew'):
                    frame_path = os.path.join(dir, f'Andrew.jpg')
                    if(os.path.exists(frame_path)):
                        os.remove(frame_path)
                    cv2.imwrite(frame_path, frame)
                elif(body_face == 'Kamryn'):
                    frame_path = os.path.join(dir, f'Kamryn.jpg')
                    if(os.path.exists(frame_path)):
                        os.remove(frame_path)
                    cv2.imwrite(frame_path, frame)
                elif(body_face == 'Jordan'):
                    frame_path = os.path.join(dir, f'Jordan.jpg')
                    if(os.path.exists(frame_path)):
                        os.remove(frame_path)
                    cv2.imwrite(frame_path, frame)
                elif(body_face == 'Nick'):
                    frame_path = os.path.join(dir, f'Nick.jpg')
                    if(os.path.exists(frame_path)):
                        os.remove(frame_path)
                    cv2.imwrite(frame_path, frame)

                if (AvesUser["timeStamp"] != "Null"):
                    elapsedTime = time.time() - float(AvesUser["timeStamp"])
                    if (elapsedTime >= 30):

                        if (AvesUser["status"] == "Inside"):
                            print('inside')
                            # Swap Status --------------------------------------------------------------------- #
                            sql = "UPDATE roommates SET status =%s WHERE name = %s"
                            val = ("Outside", body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            # --------------------------------------------------------------------------------- #


                            # Update LastExit
                            sql = "UPDATE roommates SET lastExit = %s WHERE name = %s"
                            val = (todaysDate, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            # --------------------------------------------------------------------------------- #


                            # Increment Weekday --------------------------------------------------------------- #
                            sql = f"UPDATE roommates SET {todaysWeekday} = %s WHERE name = %s"
                            value = AvesUser[todaysWeekday] + 1
                            val = (value, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            # --------------------------------------------------------------------------------- #


                            # Avg Times Left/week ------------------------------------------------------------- #
                            totalTime = 0

                            # Iterate Through Weekdays, Total Amount of Times Left - Resets Each Week
                            weekdayNum = dt.datetime.now().weekday()
                            for x in range(weekdayNum + 1):
                                totalTime += AvesUser[weekdays[x]]

                            # Calculate AvgTimesLeft
                            avgTimesLeft = totalTime/(weekdayNum+1)
                            # Update avgTimesLeft
                            sql = "UPDATE roommates SET avgTimesLeft = %s WHERE name = %s"
                            val = (avgTimesLeft, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            
                            # Reset Weekday Values Sunday at Midnight
                            # >>>> Bottom Code Set

                            # --------------------------------------------------------------------------------- #


                            # Reset TimeStamp ----------------------------------------------------------------- #
                            sql = "UPDATE roommates SET timeStamp =%s WHERE name = %s"
                            val = (str(time.time()), body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            socketio.emit('db_change', 1)
                            # --------------------------------------------------------------------------------- #


                            if(AvesUser["check1"] == 0):
                                print('check1 within inside')
                                sql = "UPDATE roommates SET timeStart =%s WHERE name = %s"
                                time1 = time.time()
                                val = (time1, body_face)
                                AvesCur.execute(sql, val)
                                AvesDB.commit()

                                sql = "UPDATE roommates SET check1 =%s WHERE name = %s"
                                val = (1, body_face)
                                AvesCur.execute(sql, val)
                                AvesDB.commit()

                        elif (AvesUser["status"] == "Outside"):
                            print('outside')
                            # Swap Status --------------------------------------------------------------------- #
                            sql = "UPDATE roommates SET status =%s WHERE name = %s"
                            val = ("Inside", body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            # --------------------------------------------------------------------------------- #


                            # Update LastEnter ---------------------------------------------------------------- #
                            sql = "UPDATE roommates SET lastEnter =%s WHERE name = %s"
                            val = (todaysDate, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            # --------------------------------------------------------------------------------- #


                            # Update TimeStamp 
                            sql = "UPDATE roommates SET timeStamp =%s WHERE name = %s"
                            val = (str(time.time()), body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            socketio.emit('db_change', 1)
                            # --------------------------------------------------------------------------------- #

                            if (AvesUser["check2"] == 0):
                                print("check2 within outside")
                                sql = "UPDATE roommates SET timeEnd =%s WHERE name = %s"
                                time2 = time.time()
                                val = (time2, body_face)
                                AvesCur.execute(sql, val)
                                AvesDB.commit()

                                sql = "UPDATE roommates SET check2 =%s WHERE name = %s"
                                val = (1, body_face)
                                AvesCur.execute(sql, val)
                                AvesDB.commit()
                                time.sleep(12)

                if (AvesUser["check1"] == 1 and AvesUser["check2"] == 1):
                            # Calculate Epoch Time Difference
                            timeDiff = AvesUser["timeEnd"] - AvesUser["timeStart"]

                            # Add That Difference to totalTimeAway
                            # 1. Pull Current Total
                            # 2. Add timeDiff to that Total
                            # 3. Update
                            currentDiff = AvesUser["totalTimeAway"]
                            diff = timeDiff + currentDiff

                            sql = "UPDATE roommates SET totalTimeAway =%s WHERE name = %s"
                            val = (diff, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()

                            # =================================================================== #

                            # Increment Instances for Dividend Now
                            instances = AvesUser["timeInstances"]
                            instances += 1
                            
                            # Update Time Instances
                            sql = "UPDATE roommates SET timeInstances =%s WHERE name = %s"
                            val = (instances, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()

                            # =================================================================== #

                            # Calcualte Mean Epoch
                            epochTotal = AvesUser["totalTimeAway"]
                            dividend = AvesUser["timeInstances"]

                            meanEpoch = epochTotal/dividend

                            # Now Input Mean Epoch into Conversion
                            hours, remainder = divmod(meanEpoch.total_seconds(), 3600)
                            minutes = remainder // 60

                            if hours == 0:
                                formattedTime = f"{int(minutes)}m"
                            else:
                                formattedTime = f"{int(hours):02}h {int(minutes):02}m"

                            sql = "UPDATE roommates SET avgTimeAway =%s WHERE name = %s"
                            val = (formattedTime, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()

                            # Reset Check1 & Check2
                            sql = "UPDATE roommates SET check1 =%s WHERE name = %s"
                            val = (0, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            
                            sql = "UPDATE roommates SET check2 =%s WHERE name = %s"
                            val = (0, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()

                            # Reset timeStart and timeEnd
                            sql = "UPDATE roommates SET timeStart = %s WHERE name = %s"
                            val = (0, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()
                            
                            sql = "UPDATE roommates SET timeEnd =%s WHERE name = %s"
                            val = (0, body_face)
                            AvesCur.execute(sql, val)
                            AvesDB.commit()

        # Running Every Frame
        # Check if Time is Midnight on a Sunday
        # If So, Reset Weekday Values
        resetDate = dt.datetime.now()
        # If Todays Date is Sunday(6) and Hour is Midnight(24)
        if (resetDate.weekday() == 6 and resetDate.hour == 24):
            # 7 Days in Week
            for x in range(7):
                sql = f"UPDATE roommates SET {weekdays[x]} = 0"
                AvesCur.execute(sql)
                AvesDB.commit()


        # Camera Display w/ Facial Tracking and Body Tracking
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    app, socketio = create_app()
    socketio_thread = threading.Thread(target=video_processing)
    socketio_thread.start()
    socketio.run(app, port=5000)
