from flask import Flask, request, jsonify
from deadlock_detector import DeadlockDetector
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
detector = DeadlockDetector()

@app.route('/')
def home():
    return "Deadlock Detection API is running!"

@app.route('/add_process', methods=['POST'])
def add_process():
    """API to add a process requesting a resource."""
    data = request.get_json()
    process_id = data.get("process_id")
    resource_id = data.get("resource_id")

    if not process_id or not resource_id:
        return jsonify({"error": "Both process_id and resource_id are required"}), 400

    detector.add_process(process_id, resource_id)
    return jsonify({"message": f"Process {process_id} requests Resource {resource_id}"}), 200

@app.route('/add_resource', methods=['POST'])
def add_resource():
    """API to add a resource allocated to a process."""
    data = request.get_json()
    resource_id = data.get("resource_id")
    process_id = data.get("process_id")

    if not process_id or not resource_id:
        return jsonify({"error": "Both resource_id and process_id are required"}), 400

    detector.add_resource(resource_id, process_id)
    return jsonify({"message": f"Resource {resource_id} allocated to Process {process_id}"}), 200

@app.route('/detect_deadlock', methods=['GET'])
def detect_deadlock():
    """API to check if a deadlock exists."""
    deadlock, cycle = detector.detect_deadlock()
    return jsonify({"deadlock": deadlock, "cycle": cycle}), 200

@app.route('/get_graph', methods=['GET'])
def get_graph():
    """API to get the graph structure for visualization."""
    return jsonify(detector.get_graph_structure()), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
