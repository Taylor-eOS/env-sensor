from flask import Flask, jsonify
from omron_2jcie_bu01 import Omron2JCIE_BU01
import time
import csv
from datetime import datetime
from threading import Thread

app = Flask(__name__)
sensor = Omron2JCIE_BU01.serial("/dev/omron_sensor")
csv_file = 'sensor_readings.csv'

def append_to_csv(data):
    timestamp = datetime.now().strftime('%m-%d %H:%M:%S')
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, data['temperature'], data['humidity'], data['light'], 
                         data['pressure'], data['noise'], data['eTVOC'], data['eCO2'], data['thi'], data['wbgt']])

def collect_sensor_data():
    while True:
        data = sensor.latest_data_long()
        sensor_data = {
            'temperature': float(data.temperature),
            'humidity': float(data.humidity),
            'light': data.light,
            'pressure': float(data.pressure),
            'noise': float(data.noise),
            'eTVOC': data.eTVOC,
            'eCO2': data.eCO2,
            'thi': float(data.thi),
            'wbgt': float(data.wbgt),
        }
        append_to_csv(sensor_data)
        time.sleep(10)

@app.route('/data')
def get_sensor_data():
    data = sensor.latest_data_long()
    sensor_data = {
        'temperature': float(data.temperature),
        'humidity': float(data.humidity),
        'light': data.light,
        'pressure': float(data.pressure),
        'noise': float(data.noise),
        'eTVOC': data.eTVOC,
        'eCO2': data.eCO2,
        'thi': float(data.thi),
        'wbgt': float(data.wbgt),
    }
    return jsonify(sensor_data)

if __name__ == "__main__":
    thread = Thread(target=collect_sensor_data)
    thread.daemon = True
    thread.start()
    app.run(host='0.0.0.0', port=5001)

