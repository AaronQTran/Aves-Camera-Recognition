from flask import Flask, request, jsonify
from services import update_roommate_status

def create_app():
    app = Flask(__name__)

    @app.route('/api/manualFix', methods=['POST'])
    def manual_fix():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        name = data.get('name')
        new_status = data.get('status')
        if not name or not new_status:
            return jsonify({"error": "Missing 'name' or 'status'"}), 400

        response = update_roommate_status(name, new_status)
        return jsonify(response), 200

    return app
