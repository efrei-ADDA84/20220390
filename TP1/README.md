# Abisha JEYAVEL 20220390

# DEVOPS - TP1 - Docker

<img src="https://www.docker.com/wp-content/uploads/2022/03/vertical-logo-monochromatic.png" width=300>

---
## 1. Objectif du TP1 : 
---

Le but de ce TP est de créer un wrapper, qui retourne la météo d'un lieu donné avec sa latitude et sa longitude
(passées en variable d'environnement) en utilisant openweather API. Puis, on va packager ce code dans une image Docker et le mettre à disposition sur DockerHub. 

<br/>

---
## 2. Code Python wrapper.py
---

### 2.1 Import des librairies 

 - **requests** : une librairie permettant d'utiliser le protocole HTTP de façon simple

 - **sys** : Dans le module sys, on utilise la liste  ```sys.argv```, qui contient tous les arguments passés en ligne de commandes au script Python. On peut ainsi récupérer les valeurs pour ```lat``` (la latitude), ```long``` (la longitude) et ```api_rest``` (l'API key).  

 ### 2.2 URL pour OpenWeatherMap

Une fois avoir récupéré les valeurs des variables de ```lat```, ```long``` et ```api_rest```, on fait un appel à l'API d'OpenWeatherMap en utilisant l'url suivant : 

https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={API_KEY}


On envoie une requête GET à cet url, puis on affiche la réponse du serveur sous format json. 

```python
r = requests.get(url)
print(r.json())
``` 

<br/>


---
## 3. Création de notre propre image Docker
---
### 3.1 Dockerfile : Fichier de configuration

Dockerfile permet de configurer et créer rapidement une image Docker. Dans le Dockerfile, on écrit les instructions décrivant les actions que l’image Docker doit exécuter une fois qu’elle sera créée.

Voici les instructions pour notre image Docker :

```bash
FROM python:3.9
```
- Notre image Docker va être créée à partir de l'image de ```python:3.9```   

<br/>

```bash
ARG LAT 
ARG LONG 
ARG API_KEY 

ENV LAT = value1
ENV LONG = value2
ENV API_KEY = value3
```
- ```ARG LAT``` permet de définir la variable ```LAT```. ```ENV LAT = value1``` définit la variable d'environnement ```LAT``` sur la valeur ```value1```. On a effectué le même processus pour les variables ```LONG``` et ```API_REST```. 

<br/>

```bash
WORKDIR /app
```
- On définit le dossier de travail pour les autres commandes comme RUN, CMD.

<br/>

```bash
COPY wrapper.py ./ 
```
- On copie le fichier **wrapper.py** dans le conteneur Docker à partir de notre machine. 

<br/>

```bash
RUN pip3 install --no-cache-dir requests==2.7.0
```
- On lance la commande pour installer la librairie ```requests``` avec la version **2.7.0**, tout en désactivant le cache. La désactivation du cache permet de réduire la taille de l'image Docker. 

<br/>

```bash
CMD ["sh", "-c", "python3 ./wrapper.py ${LAT} ${LONG} ${API_KEY}"]
```
- La commande **CMD​** spécifie l'instruction qui doit être exécutée au démarrage du conteneur Docker. On exécute la commande ```python3 ./wrapper.py ${LAT} ${LONG} ${API_KEY}``` en mode shell. 

<br/>

### 3.2 On construit (build) notre image Docker

```bash
docker build . -t tp1:0.0.1 .
```
- On construit le conteneur en indiquant le tag du conteneur. 

<br/>

---
## 4.Mettre à disposition l'image Docker sur DockerHub
---

- On commence par créer un répertoire dans notre registry (le nom de ma registry est **abishaefrei**). Le nom de mon répertoire est **tp1devops**.

- Puis, on tag notre image Docker :
```bash
docker tag tp1:0.0.1 abishaefrei/tp1devops:0.0.1
```

- On se connecte à notre registry :
```bash
docker login -u abishaefrei
```

- On pousse (push) notre image Docker dans notre registry sur DockerHub :
```bash
docker push abishaefrei/tp1devops:0.0.1
```

<br/>

---
## 5. Test
---
On vérifie le bon fonctionnement de notre image Docker : 

- On télécharge notre image Docker depuis DockerHub : 
 ```bash
docker pull abishaefrei/tp1devops:0.0.1
```

- On exécute la commande suivante :  ```docker run --env LAT="31.2504" --env LONG="-99.2506" --env API_KEY=**** abishaefrei/tp1devops:0.0.1```, en précisant notre api key. 

On obtient bien le résultat attendu : 
 ```bash
{'coord': {'lon': -99.2506, 'lat': 31.2504}, 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01d'}], 'base': 'stations', 'main': {'temp': 296.12, 'feels_like': 294.99, 'temp_min': 296.12, 'temp_max': 297.45, 'pressure': 1015, 'humidity': 20}, 'visibility': 10000, 'wind': {'speed': 6.17, 'deg': 250}, 'clouds': {'all': 0}, 'dt': 1682866446, 'sys': {'type': 1, 'id': 3395, 'country': 'US', 'sunrise': 1682855595, 'sunset': 1682903701}, 'timezone': -18000, 'id': 4736286, 'name': 'Texas', 'cod': 200}
 ```

<br/>

---
## 6. Partie Bonus
---

- Hadolint permet de créer des images Docker conformes aux meilleures pratiques. À l'exécution de la commande suivante, on a 0 lint erreurs sur notre Dockerfile. 
```bash
docker run --rm -i hadolint/hadolint < Dockerfile
```

- Aucune donnée sensible n'est stockée dans l'image Docker. 

