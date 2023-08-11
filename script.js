async function fetchStockData() {
    const ticker = document.getElementById("ticker").value;
    const response = await fetch(`http://127.0.0.1:8000/stock/${ticker}`);
    const data = await response.json();
    console.log("Received data from server:", data); // Log the received data
    renderChart(data.data, data.red_prediction, data.blue_prediction, data.green_prediction);
}

function renderChart(data, redPrediction, bluePrediction, greenPrediction) {
    console.log('Data:', data); // Log the data
    console.log('Red Prediction:', redPrediction); // Log the red prediction
    console.log('Blue Prediction:', bluePrediction); // Log the blue prediction
    console.log('Green Prediction:', greenPrediction); // Log the green prediction

    const ctx = document.getElementById('stockChart').getContext('2d');

    const timeLabels = data.map((point, index) => index);
    const prices = data.map((point) => point.Close);
    const futureTimeLabels = [...timeLabels, timeLabels.length]; // Add one future time point

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: futureTimeLabels,
            datasets: [{
                label: 'Real-time Prices',
                data: prices,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
            },
            {
                label: 'Red Predicted Prices',
                data: [...prices, redPrediction],
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false
            },
            {
                label: 'Blue Predicted Prices',
                data: [...prices, bluePrediction],
                borderColor: 'rgba(100, 149, 237, 1)',
                fill: false
            },
            {
                label: 'Green Predicted Prices',
                data: [...prices, greenPrediction],
                borderColor: 'rgba(50, 205, 50, 1)',
                fill: false
            }]
        }
    });
}
