from flask import Flask, jsonify, render_template_string
from omron_2jcie_bu01 import Omron2JCIE_BU01
import time

app = Flask(__name__)

#sensor = Omron2JCIE_BU01.serial("/dev/ttyUSB0")
sensor = Omron2JCIE_BU01.serial("/dev/omron_sensor")

@app.route('/data')
def get_sensor_data():
    data = sensor.latest_data_long()
    return jsonify({
        'temperature': float(data.temperature),
        'humidity': float(data.humidity),
        'light': data.light,
        'pressure': float(data.pressure),
        'noise': float(data.noise),
        'TVOC': data.eTVOC,
        'CO2': data.eCO2,
        'thi': float(data.thi),
        'wbgt': float(data.wbgt),
        'niceness': 100
    })

@app.route('/')
def index():
    return render_template_string('''
        <html>
        <head>
            <title>Readings</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    color: #b23368;  /* Apply the custom color */
                    text-align: center;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    background-color: #b23368;  /* Apply the custom color */
                    color: white;
                    padding: 20px;
                    margin: 0;
                }
                .container {
                    margin: 20px;
                    padding: 20px;
                    background-color: white;
                    border-radius: 10px;
                    box-shadow: 0px 0px 10px 0px rgba(0, 0, 0, 0.1);
                }
                p {
                    font-size: 1.5em;
                    margin: 10px;
                }
                .value {
                    font-weight: bold;
                    color: #b23368;  /* Apply the custom color */
                }
                .footer {
                    margin-top: 20px;
                    padding: 10px;
                    font-size: 0.9em;
                    color: #999;
                }
            </style>
            <script>
                function updateData() {
                    fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('temperature').innerText = data.temperature;
                        document.getElementById('humidity').innerText = data.humidity;
                        document.getElementById('light').innerText = data.light;
                        document.getElementById('pressure').innerText = data.pressure;
                        document.getElementById('noise').innerText = data.noise;
                        document.getElementById('eTVOC').innerText = data.eTVOC;
                        document.getElementById('eCO2').innerText = data.eCO2;
                        document.getElementById('thi').innerText = data.thi;
                        document.getElementById('wbgt').innerText = data.wbgt;
                        document.getElementById('niceness').innerText = data.niceness + '%';
                    });
                }
                setInterval(updateData, 1000);  // Update every second
                updateData();  // Initial call to populate data
            </script>
        </head>
        <body>
            <h1>Readings</h1>
            <div class="container">
                <p>Temperature: <span class="value" id="temperature"></span> °C</p>
                <p>Humidity: <span class="value" id="humidity"></span> %</p>
                <p>Light: <span class="value" id="light"></span> lux</p>
                <p>Pressure: <span class="value" id="pressure"></span> hPa</p>
                <p>Noise: <span class="value" id="noise"></span> dB</p>
                <p>TVOC: <span class="value" id="eTVOC"></span> ppb</p>
                <p>CO2: <span class="value" id="eCO2"></span> ppm</p>
                <p>THI: <span class="value" id="thi"></span></p>
                <p>WBGT: <span class="value" id="wbgt"></span> °C</p>
                <p>Niceness: <span class="value" id="niceness">100%</span></p>
            </div>
            <div class="footer">
                Sensor data updates every second
            </div>
        </body>
        </html>
    ''')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
