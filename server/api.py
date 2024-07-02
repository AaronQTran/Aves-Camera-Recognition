from flask import Flask, jsonify
from main import get_attendance_data  # Import the function

def create_app():
    app = Flask(__name__)

    @app.route('/api/manualFix', methods=['GET'])
    def get_attendance():
        data = get_attendance_data()  # Call the function to get the data
        return jsonify(data)

    return app
