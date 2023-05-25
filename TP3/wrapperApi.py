"""TP2 : DevOps Docker

Configuration d'un workflow Github Action, 
de tel sorte à publier automatiquement l'image Docker à chaque push sur DockerHub. 
Transformation du wrapper du TP1 en API

Abisha JEYAVEL 20220390"""

#import libraries
from flask import Flask, request
import requests
from sys import argv

#creation de l'application Flask
app = Flask(__name__)

#pour indiquer à Flask, quelle URL et méthode doivent déclencher cette fonction
@app.route("/", methods=["GET"])
def result():
    #latitude récupéré à partir de la variable d'URL 'lat'
    lat = request.args.get('lat') 

    #longitude récupéré à partir de la variable d'URL 'lon'
    lon = request.args.get('lon')

    API_KEY = argv[1] #API key of openweather

    #url pour openWeather Map API
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"

    #retourne la reponse de la requete sous json
    return requests.get(url).json()

#exécuter l'application sur le port 8081
if __name__ == '__main__':
    app.run(debug=True, port=8081, host="0.0.0.0")