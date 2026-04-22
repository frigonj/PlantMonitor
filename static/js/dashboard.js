let tempChart, humChart, soilChart;



function loadCharts() {
    const range = document.getElementById("rangeSelect").value;
    fetch(`/api/history?range=${range}`)
        .then(res => res.json())
        .then(data => {

            const labels = data.timestamps.map(t => {
                const date = new Date(t + ' UTC');
                return date.toLocaleTimeString('en-US', {
                    hour: 'numeric',
                    minute: '2-digit'
                });
            });


            if (tempChart) tempChart.destroy();
            if (humChart) humChart.destroy();
            if (soilChart) soilChart.destroy();

            tempChart = createChart("tempChart", labels, data.temperature, "Temperature °F");
            humChart = createChart("humChart", labels, data.humidity, "Humidity %");
            soilChart = createChart("soilChart", labels, data.soil, "Soil Moisture");
            updateRangeLabel();
        });
}

function createChart(canvasId, labels, values, label) {
    return new Chart(document.getElementById(canvasId), {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: values,
                fill: false,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    ticks: { maxTicksLimit: 8 }
                }
            }
        }
    });
}

function updateRangeLabel() {
    const select = document.getElementById("rangeSelect");
    const label = select.options[select.selectedIndex].text;
    document.querySelectorAll(".chartRangeLabel").forEach(el => el.textContent = label);
}

window.onload = loadCharts;
