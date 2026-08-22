
document.addEventListener("DOMContentLoaded", function () {

    fetch("/api/vehicles")

        .then(response => {

            if (!response.ok) {
                throw new Error("Failed to fetch vehicle data");
            }

            return response.json();
        })

        .then(async data => {

            console.log("Vehicle data received:", data);

            const vehicles = Array.isArray(data)
                ? data
                : (data.vehicles || []);


            // -----------------------------------------
            // GET HTML ELEMENTS
            // -----------------------------------------

            const tableBody =
                document.getElementById("vehicle-table-body");

            const analysisContainer =
                document.getElementById("analysis-container");

            const totalVehicles =
                document.getElementById("total-vehicles");

            const healthyVehicles =
                document.getElementById("healthy-vehicles");

            const attentionVehicles =
                document.getElementById("attention-vehicles");

            const maintenanceVehicles =
                document.getElementById("maintenance-vehicles");


            if (!tableBody) {
                console.error("vehicle-table-body not found");
                return;
            }


            // -----------------------------------------
            // CLEAR EXISTING DATA
            // -----------------------------------------

            tableBody.innerHTML = "";

            if (analysisContainer) {
                analysisContainer.innerHTML = "";
            }


            // -----------------------------------------
            // SUMMARY
            // -----------------------------------------

            if (totalVehicles) {
                totalVehicles.textContent = vehicles.length;
            }


            let healthy = 0;
            let attention = 0;
            let maintenance = 0;


            // -----------------------------------------
            // PROCESS EACH VEHICLE
            // -----------------------------------------

            for (const vehicle of vehicles) {

                const vehicleId =
                    vehicle.vehicle ?? `Vehicle ${vehicle.id}`;


                // -----------------------------------------
                // GET 7 AI FEATURES
                // -----------------------------------------

                const mileage =
                    vehicle.mileage ?? "-";

                const temperature =
                    vehicle.temperature ?? "-";

                const fuelConsumption =
                    vehicle.fuel_consumption ?? "-";

                const batteryVoltage =
                    vehicle.battery_voltage ?? "-";

                const engineVibration =
                    vehicle.engine_vibration ??
                    vehicle.vibration ??
                    "-";

                const oilLevel =
                    vehicle.oil_level ?? "-";

                const tirePressure =
                    vehicle.tire_pressure ??
                    vehicle.pressure ??
                    "-";


                // -----------------------------------------
                // GET EXISTING STATUS
                // -----------------------------------------

                const status =
                    vehicle.status ?? "Unknown";


                // -----------------------------------------
                // AI PREDICTION
                // -----------------------------------------

                let prediction = "Not available";


                try {

                    // Only send prediction request when
                    // all 7 values are available.

                    if (
                        mileage !== "-" &&
                        temperature !== "-" &&
                        fuelConsumption !== "-" &&
                        batteryVoltage !== "-" &&
                        engineVibration !== "-" &&
                        oilLevel !== "-" &&
                        tirePressure !== "-"
                    ) {

                        const predictionResponse =
                            await fetch("/api/predict", {

                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body: JSON.stringify({

                                    mileage:
                                        mileage,

                                    temperature:
                                        temperature,

                                    fuel_consumption:
                                        fuelConsumption,

                                    battery_voltage:
                                        batteryVoltage,

                                    engine_vibration:
                                        engineVibration,

                                    oil_level:
                                        oilLevel,

                                    tire_pressure:
                                        tirePressure
                                })
                            });


                        const predictionData =
                            await predictionResponse.json();


                        if (predictionResponse.ok) {

                            prediction =
                                predictionData.prediction;

                            console.log(
                                vehicleId,
                                "AI Prediction:",
                                prediction
                            );

                        }

                        else {

                            console.error(
                                "Prediction error:",
                                predictionData
                            );
                        }
                    }

                }

                catch (error) {

                    console.error(
                        "AI prediction request failed:",
                        error
                    );
                }


                // -----------------------------------------
                // HEALTH SCORE
                // -----------------------------------------

                let healthScore = 0;


                if (
                    status.toLowerCase() === "healthy"
                ) {

                    healthScore = 100;
                }

                else if (
                    status.toLowerCase() === "needs attention"
                ) {

                    healthScore = 60;
                }

                else {

                    healthScore = 30;
                }


                // -----------------------------------------
                // COUNT STATUS
                // -----------------------------------------

                if (status === "Healthy") {

                    healthy++;
                }

                else if (status === "Needs Attention") {

                    attention++;
                }

                else {

                    maintenance++;
                }


                // -----------------------------------------
                // CREATE TABLE ROW
                // -----------------------------------------

                const row =
                    document.createElement("tr");


                row.innerHTML = `

                    <td>${vehicleId}</td>

                    <td>${prediction}</td>

                    <td>${mileage}</td>

                    <td>${temperature}</td>

                    <td>${fuelConsumption}</td>

                    <td>${batteryVoltage}</td>

                    <td>${engineVibration}</td>

                    <td>${oilLevel}</td>

                    <td>${tirePressure}</td>

                    <td>${healthScore}%</td>

                    <td>${status}</td>

                `;


                tableBody.appendChild(row);


                // -----------------------------------------
                // ANALYSIS CARD
                // -----------------------------------------

                if (analysisContainer) {

                    const analysisCard =
                        document.createElement("div");


                    analysisCard.className =
                        "analysis-card";


                    let problemText;
                    let recommendationText;


                    if (
                        status === "Healthy"
                    ) {

                        problemText =
                            "No major problems detected.";

                        recommendationText =
                            "Continue regular vehicle maintenance.";
                    }

                    else if (
                        status === "Needs Attention"
                    ) {

                        problemText =
                            "Vehicle requires attention.";

                        recommendationText =
                            "Inspect the vehicle and monitor its parameters.";
                    }

                    else {

                        problemText =
                            "Maintenance is required.";

                        recommendationText =
                            "Schedule vehicle maintenance.";
                    }


                    analysisCard.innerHTML = `

                        <h3>${vehicleId}</h3>

                        <p>
                            <strong>AI Prediction:</strong>
                            ${prediction}
                        </p>

                        <p>
                            <strong>Mileage:</strong>
                            ${mileage}
                        </p>

                        <p>
                            <strong>Temperature:</strong>
                            ${temperature}
                        </p>

                        <p>
                            <strong>Fuel Consumption:</strong>
                            ${fuelConsumption}
                        </p>

                        <p>
                            <strong>Battery Voltage:</strong>
                            ${batteryVoltage}
                        </p>

                        <p>
                            <strong>Engine Vibration:</strong>
                            ${engineVibration}
                        </p>

                        <p>
                            <strong>Oil Level:</strong>
                            ${oilLevel}
                        </p>

                        <p>
                            <strong>Tire Pressure:</strong>
                            ${tirePressure}
                        </p>

                        <p>
                            <strong>Health Score:</strong>
                            ${healthScore}%
                        </p>

                        <p>
                            <strong>Status:</strong>
                            ${status}
                        </p>

                        <h4>Problems Detected</h4>

                        <p>
                            ${problemText}
                        </p>

                        <h4>Recommendation</h4>

                        <p>
                            ${recommendationText}
                        </p>

                    `;


                    analysisContainer.appendChild(
                        analysisCard
                    );
                }

            }


            // -----------------------------------------
            // UPDATE SUMMARY
            // -----------------------------------------

            if (healthyVehicles) {

                healthyVehicles.textContent =
                    healthy;
            }


            if (attentionVehicles) {

                attentionVehicles.textContent =
                    attention;
            }


            if (maintenanceVehicles) {

                maintenanceVehicles.textContent =
                    maintenance;
            }


            // -----------------------------------------
            // CONSOLE INFORMATION
            // -----------------------------------------

            console.log(
                "Total Vehicles:",
                vehicles.length
            );

            console.log(
                "Healthy:",
                healthy
            );

            console.log(
                "Needs Attention:",
                attention
            );

            console.log(
                "Maintenance Required:",
                maintenance
            );

        })


        .catch(error => {

            console.error(
                "Vehicle API Error:",
                error
            );

        });

});