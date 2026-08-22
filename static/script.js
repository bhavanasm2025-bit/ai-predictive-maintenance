document.addEventListener("DOMContentLoaded", function () {

    fetch("/api/vehicles")
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to fetch vehicle data");
            }

            return response.json();
        })

        .then(data => {

            console.log("Vehicle data:", data);

            const tableBody =
                document.getElementById("vehicle-table-body");

            const totalVehicles =
                document.getElementById("total-vehicles");

            const healthyVehicles =
                document.getElementById("healthy-vehicles");

            const attentionVehicles =
                document.getElementById("attention-vehicles");

            totalVehicles.textContent = data.length;

            let healthy = 0;
            let attention = 0;

            data.forEach(vehicle => {

                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${vehicle.vehicle_id}</td>
                    <td>${vehicle.model}</td>
                    <td>${vehicle.mileage}</td>
                    <td>${vehicle.temperature}</td>
                    <td>${vehicle.fuel_consumption}</td>
                    <td>${vehicle.status}</td>
                `;

                tableBody.appendChild(row);

                if (
                    vehicle.status &&
                    vehicle.status.toLowerCase() === "healthy"
                ) {
                    healthy++;
                } else {
                    attention++;
                }
            });

            healthyVehicles.textContent = healthy;
            attentionVehicles.textContent = attention;
        })

        .catch(error => {
            console.error("Error:", error);
        });

});