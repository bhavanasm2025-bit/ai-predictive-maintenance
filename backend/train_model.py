import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import pickle
import os


# -----------------------------------------
# LOAD DATASET
# -----------------------------------------

data_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "data",
    "vehicle_data.csv"
)

data = pd.read_csv(data_path)


# -----------------------------------------
# INPUT FEATURES
# -----------------------------------------

features = [
    "mileage",
    "temperature",
    "fuel_consumption",
    "battery_voltage",
    "engine_vibration",
    "oil_level",
    "tire_pressure"
]


X = data[features]

y = data["maintenance_risk"]


# -----------------------------------------
# SPLIT DATA
# -----------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -----------------------------------------
# CREATE MODEL
# -----------------------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


# -----------------------------------------
# TRAIN MODEL
# -----------------------------------------

model.fit(X_train, y_train)


# -----------------------------------------
# TEST MODEL
# -----------------------------------------

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)


print("Model training completed.")

print(
    "Model accuracy:",
    round(accuracy * 100, 2),
    "%"
)


# -----------------------------------------
# SAVE MODEL
# -----------------------------------------

model_path = os.path.join(
    os.path.dirname(__file__),
    "predictive_model.pkl"
)


with open(model_path, "wb") as file:

    pickle.dump(model, file)


print(
    "Model saved to:",
    model_path
)