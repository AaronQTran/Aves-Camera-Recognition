from flask import Flask, request, jsonify
import json
import threading

json_lock = threading.Lock()

def create_app():
    app = Flask(__name__)
    #we handle the manual fix button here, no func in main
    @app.route('/api/manualFix', methods=['POST'])
    def manual_fix():
        #extract JSON data from the request
        data = request.get_json()
        name = data.get('name')
        new_status = data.get('status')
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

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
