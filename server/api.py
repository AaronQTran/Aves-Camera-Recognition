from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from services import update_roommate_status, get_statistics, get_image

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

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

    @app.route('/api/stat', methods=['GET'])
    def pull_data():
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Missing 'name'"}), 400

        response = get_statistics(name)
        return jsonify(response), 200

    @app.route('api/image', methods=['GET'])
    def pull_image():
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Missing 'name'"}), 400
        return get_image(name)
        
        
        
        
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    video_thread = threading.Thread(target=video_processing)
    video_thread.start()
    socketio.run(app, debug=False, port=5000)
