"""TP1 : DevOps Docker

Création d'un wrapper qui retourne la météo d'un lieu donné 
avec sa latitude et sa longitude(passées en variable d'environnement) 
en utilisant openweather API un code Python 

Abisha JEYAVEL 20220390"""

#import libraries
import requests 
from sys import argv

#On recupere les valeurs des variables d'environnements lat, long et API_KEY
lat = argv[1]
long = argv[2]
API_KEY = argv[3] #API key of openweather

#url pour open map API
url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={API_KEY}"

#Envoie la requete
r = requests.get(url)

#affiche en json la reponse de la requete 
print(r.json())