import json
import threading

json_lock = threading.Lock()

def update_roommate_status(name, new_status):
    with json_lock:
        with open("roommateData.json", "r") as json_file:
            roommate_data = json.load(json_file)

        for roommate in roommate_data["roommateInfo"]:
            if roommate["name"] == name:
                roommate["status"] = new_status
                break

        with open("roommateData.json", "w") as json_file:
            json.dump(roommate_data, json_file, indent=4)

    return {"message": "Status updated successfully"}

def statistics(name):
    