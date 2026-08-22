from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return jsonify({
        "message": "AI Predictive Maintenance Backend is running"
    })


@app.route("/api/vehicle", methods=["POST"])
def vehicle_data():

    data = request.get_json()

    return jsonify({
        "message": "Vehicle data received",
        "data": data
    })


if __name__ == "__main__":
    app.run(debug=True)