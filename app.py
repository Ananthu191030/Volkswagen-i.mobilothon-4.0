from flask import Flask, request, jsonify, render_template
import json

app = Flask(__name__)

# Simulated database
car_parts = {
    "engine": {"status": "good", "problem": None},
    "brakes": {"status": "damaged", "problem": "Worn brake pads"},
    "transmission": {"status": "good", "problem": None}
}

# Route to get all parts
@app.route('/parts', methods=['GET'])
def get_parts():
    return jsonify(car_parts)

# Route to update a part
@app.route('/parts/update', methods=['POST'])
def update_part():
    data = request.json
    part = data.get("part")
    status = data.get("status")
    problem = data.get("problem")

    if part in car_parts:
        car_parts[part]["status"] = status
        car_parts[part]["problem"] = problem
        return jsonify({"message": "Part updated successfully"}), 200
    else:
        return jsonify({"error": "Part not found"}), 404

# Frontend for visualization
@app.route('/')
def index():
    return render_template("index.html", car_parts=car_parts)

if __name__ == "__main__":
    app.run(debug=True)
