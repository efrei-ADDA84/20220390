from flask import Flask, request
import requests
from sys import argv

app = Flask(__name__)

@app.route("/", methods=["GET"])
def result():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    API_KEY = argv[1]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url).json()

if __name__ == '__main__':
    app.run(debug=True, port=8081, host="0.0.0.0")