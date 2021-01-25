from flask import Flask
import requests
import json
import os

app = Flask(__name__)

device = os.getenv('GOVEE_DEVICE')
api_key = os.getenv('GOVEE_API_KEY')


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/devices")
def get_devices():
    url = "https://developer-api.govee.com/v1/devices"

    headers = {
        'Content-Type': 'application/json',
        'Govee-API-Key': api_key
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)

    return json.loads(response.text)


@app.route("/state")
def get_device_state():
    url = "https://developer-api.govee.com/v1/devices/state?device=8f:b6:7c:a6:b0:19:5f:14&model=H6003"

    headers = {
        'Content-Type': 'application/json',
        'Govee-API-Key': api_key
    }

    response = requests.request("GET", url, headers=headers)

    print(response.text)

    return json.loads(response.text)


@app.route("/switch")
def off():
    url = "https://developer-api.govee.com/v1/devices/control"

    payload = {
        "device": device,
        "model": "H6003",
        "cmd": {
            "name": "turn",
            "value": "on"
        }
    }

    headers = {
        'Content-Type': 'application/json',
        'Govee-API-Key': api_key
    }

    response = requests.request("PUT", url, headers=headers, data=json.dumps(payload))

    print(response.text)

    return "OFF"


if __name__ == "__main__":
    app.run(debug=True)
