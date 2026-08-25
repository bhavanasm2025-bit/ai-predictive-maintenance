from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import pickle


# ==================================================
# FLASK APP CONFIGURATION
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

CORS(app)


# ==================================================
# LOAD AI PREDICTIVE MAINTENANCE MODEL
# ==================================================

MODEL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "predictive_model.pkl"
)

model = None

try:

    with open(MODEL_PATH, "rb") as file:
        model = pickle.load(file)

    print("AI model loaded successfully.")

except FileNotFoundError:

    print("WARNING: predictive_model.pkl was not found.")
    print("Run: python train_model.py")

except Exception as e:

    print("ERROR loading model:", e)


# ==================================================
# VEHICLE DATA
# ==================================================

vehicles = [

    {
        "id": 1,
        "vehicle": "Vehicle 001",

        "mileage": 15000,
        "temperature": 72,
        "fuel_consumption": 7.8,
        "battery_voltage": 12.6,
        "engine_vibration": 1.1,
        "oil_level": 90,
        "tire_pressure": 32,

        # Compatibility with existing dashboard
        "vibration": 1.1,
        "pressure": 32,

        "status": "Healthy"
    },


    {
        "id": 2,
        "vehicle": "Vehicle 002",

        "mileage": 50000,
        "temperature": 92,
        "fuel_consumption": 10.5,
        "battery_voltage": 11.9,
        "engine_vibration": 3.2,
        "oil_level": 60,
        "tire_pressure": 28,

        # Compatibility with existing dashboard
        "vibration": 3.2,
        "pressure": 28,

        "status": "Needs Attention"
    },


    {
        "id": 3,
        "vehicle": "Vehicle 003",

        "mileage": 75000,
        "temperature": 112,
        "fuel_consumption": 14.0,
        "battery_voltage": 11.0,
        "engine_vibration": 5.0,
        "oil_level": 20,
        "tire_pressure": 21,

        # Compatibility with existing dashboard
        "vibration": 5.0,
        "pressure": 21,

        "status": "Needs Attention"
    }

]


# ==================================================
# HOME PAGE
# ==================================================

@app.route("/")
def home():

    return render_template("index.html")


# ==================================================
# GET ALL VEHICLES
# ==================================================

@app.route("/api/vehicles", methods=["GET"])
def get_vehicles():

    return jsonify(vehicles)


# ==================================================
# ADD NEW VEHICLE
# ==================================================

@app.route("/api/vehicles", methods=["POST"])
def add_vehicle():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "No vehicle data provided"
        }), 400


    new_vehicle = {

        "id": len(vehicles) + 1,

        "vehicle": data.get(
            "vehicle",
            f"Vehicle {len(vehicles) + 1:03d}"
        ),

        "mileage": data.get(
            "mileage",
            0
        ),

        "temperature": data.get(
            "temperature",
            0
        ),

        "fuel_consumption": data.get(
            "fuel_consumption",
            0
        ),

        "battery_voltage": data.get(
            "battery_voltage",
            0
        ),

        "engine_vibration": data.get(
            "engine_vibration",
            data.get("vibration", 0)
        ),

        "oil_level": data.get(
            "oil_level",
            0
        ),

        "tire_pressure": data.get(
            "tire_pressure",
            data.get("pressure", 0)
        ),

        # Compatibility fields
        "vibration": data.get(
            "vibration",
            data.get("engine_vibration", 0)
        ),

        "pressure": data.get(
            "pressure",
            data.get("tire_pressure", 0)
        ),

        "status": data.get(
            "status",
            "Unknown"
        )

    }


    vehicles.append(new_vehicle)


    return jsonify({

        "message":
            "Vehicle added successfully",

        "vehicle":
            new_vehicle

    }), 201


# ==================================================
# AI PREDICTION
# ==================================================

@app.route("/api/predict", methods=["POST"])
def predict():

    # ----------------------------------------------
    # Check model
    # ----------------------------------------------

    if model is None:

        return jsonify({

            "error":
                "AI model is not loaded. "
                "Run train_model.py first."

        }), 500


    # ----------------------------------------------
    # Get request data
    # ----------------------------------------------

    data = request.get_json()


    if not data:

        return jsonify({

            "error":
                "No sensor data provided"

        }), 400


    try:

        # ------------------------------------------
        # Get all 7 model features
        # ------------------------------------------

        mileage = float(
            data.get("mileage", 0)
        )

        temperature = float(
            data.get("temperature", 0)
        )

        fuel_consumption = float(
            data.get("fuel_consumption", 0)
        )

        battery_voltage = float(
            data.get("battery_voltage", 0)
        )

        engine_vibration = float(
            data.get("engine_vibration", 0)
        )

        oil_level = float(
            data.get("oil_level", 0)
        )

        tire_pressure = float(
            data.get("tire_pressure", 0)
        )


        # ------------------------------------------
        # IMPORTANT:
        # Keep EXACT same order as train_model.py
        # ------------------------------------------

        input_data = [[

            mileage,
            temperature,
            fuel_consumption,
            battery_voltage,
            engine_vibration,
            oil_level,
            tire_pressure

        ]]


        # ------------------------------------------
        # AI MODEL PREDICTION
        # ------------------------------------------

        prediction = model.predict(
            input_data
        )


        result = prediction[0]


        # Convert NumPy value if necessary
        if hasattr(result, "item"):

            result = result.item()


        # ------------------------------------------
        # Return prediction
        # ------------------------------------------

        return jsonify({

            "mileage":
                mileage,

            "temperature":
                temperature,

            "fuel_consumption":
                fuel_consumption,

            "battery_voltage":
                battery_voltage,

            "engine_vibration":
                engine_vibration,

            "oil_level":
                oil_level,

            "tire_pressure":
                tire_pressure,

            "prediction":
                result

        })


    except Exception as e:

        return jsonify({

            "error":
                str(e)

        }), 400


# ==================================================
# HEALTH SUMMARY
# ==================================================

@app.route("/api/health", methods=["GET"])
def health_summary():

    total_vehicles = len(vehicles)


    healthy = sum(

        1

        for vehicle in vehicles

        if vehicle.get("status")
        == "Healthy"

    )


    needs_attention = sum(

        1

        for vehicle in vehicles

        if vehicle.get("status")
        == "Needs Attention"

    )


    maintenance = sum(

        1

        for vehicle in vehicles

        if vehicle.get("status")
        not in [
            "Healthy",
            "Needs Attention"
        ]

    )


    return jsonify({

        "total_vehicles":
            total_vehicles,

        "healthy":
            healthy,

        "needs_attention":
            needs_attention,

        "maintenance":
            maintenance

    })


# ==================================================
# RUN FLASK SERVER
# ==================================================

if __name__ == "__main__":

    print("----------------------------------------")
    print("AI Predictive Maintenance System")
    print("----------------------------------------")

    print(
        "Model path:",
        MODEL_PATH
    )


    if model is not None:

        print(
            "Model status: Loaded"
        )

    else:

        print(
            "Model status: Not Loaded"
        )


    print(
        "Starting Flask server..."
    )

    print(
        "Open: http://127.0.0.1:5000"
    )


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )