from flask import Flask
import requests
import json
import os

app = Flask(__name__)

device = os.getenv('GOVEE_DEVICE')
api_key = os.getenv('GOVEE_API_KEY')

headers = {
    'Content-Type': 'application/json',
    'Govee-API-Key': api_key
}


@app.route("/")
def hello():
    return json.dumps({'message': 'govee-playground'})


@app.route("/devices")
def get_devices():
    url = "https://developer-api.govee.com/v1/devices"

    response = requests.request("GET", url, headers=headers)

    print(response.text)

    return json.loads(response.text)


@app.route("/state")
def get_device_state():
    url = "https://developer-api.govee.com/v1/devices/state?device=8f:b6:7c:a6:b0:19:5f:14&model=H6003"

    response = requests.request("GET", url, headers=headers)

    return json.loads(response.text)


@app.route("/switch")
def off():
    url = "https://developer-api.govee.com/v1/devices/control"
    url_device = "https://developer-api.govee.com/v1/devices/state?device=8f:b6:7c:a6:b0:19:5f:14&model=H6003"

    device_response = requests.request("GET", url_device, headers=headers)
    obj = device_response.json()
    power_state = obj['data']['properties'][1]

    if power_state.get('powerState') == "on":
        value = "off"
    else:
        value = "on"

    payload = {
        "device": device,
        "model": "H6003",
        "cmd": {
            "name": "turn",
            "value": value
        }
    }

    switch_response = requests.request("PUT", url, headers=headers, data=json.dumps(payload))

    print(switch_response.text)

    return value


if __name__ == "__main__":
    app.run(debug=True)
