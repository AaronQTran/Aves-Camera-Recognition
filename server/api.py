from flask import Flask, request, jsonify
import json
import threading

json_lock = threading.Lock()

def create_app():
    app = Flask(__name__)

    @app.route('/api/manualFix', methods=['POST'])
    def manual_fix():
        # Extract JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        name = data.get('name')
        new_status = data.get('status')
        if not name or not new_status:
            return jsonify({"error": "Missing 'name' or 'status'"}), 400

        # NOTE WITH ALREADY CLOSES JSON FILE
        with json_lock:
            with open("roommateData.json", "r") as json_file:
                roommate_data = json.load(json_file)

            for roommate in roommate_data["roommateInfo"]:
                if roommate["name"] == name:
                    roommate["status"] = new_status
                    break

            with open("roommateData.json", "w") as json_file:
                json.dump(roommate_data, json_file, indent=4)

        # Return a success message
        return jsonify({"message": "Status updated successfully"}), 200

    return app
