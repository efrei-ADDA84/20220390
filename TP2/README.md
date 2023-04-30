# Abisha JEYAVEL 20220390

# DEVOPS - TP2 - Docker

<img src="https://debest.fr/images/g/i/t/h/u/github-actions-dockerhub-f95c800d.png?g-dca45b00" width=800>

---
## 1. Objectif du TP2 : 
---

Le but de ce TP est de configurer un workflow Github Action, de tel sorte à publier automatiquement l'image Docker à chaque push sur DockerHub. Puis, on va transformer le wrapper du TP1 en API. 

<br/>

---
## 2. Configuration de Github Action
---
Dans ```.github/workflows```, on crée le fichier de workflow ```main.yml```. 

```bash
name: Docker Image CI
```
- On donne **Docker Image CI** comme nom à notre workflow

<br/>

```bash
on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]
```
- Le workflow s'exécute quand on fait un ```push``` ou on fait un ```pull_request``` sur la branche ```main``` du dépôt Github. 

<br/>

```bash
jobs:

  build-container:
    name : Build container
    runs-on: ubuntu-latest

    steps:
    - name : Checkout
      uses: actions/checkout@v3

    - name : Login to Docker Hub 
      uses : docker/login-action@v1
      with :
        username : ${{secrets.USERNAME_DOCKER_HUB}}
        password : ${{secrets.ACCESS_TOKEN_DOCKER_HUB}}

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Build and push to Docker Hub
      uses : docker/build-push-action@v2
      with:
        context : ./TP2
        push: true
        tags : abishaefrei/tp1devops:0.0.2b
```
- Dans ```jobs```, on regroupe toutes les jobs, qui doivent être exécutées dans notre workflow. ```build-container``` est le job id, puis on définit sur quel type de machine le job doit s'exécuter. Dans notre cas, on a mis ```ubuntu-latest```. 

- Dans ```steps```, on définit les étapes de notre workflow : 
    - 1ère étape : ```Checkout```, qui permet de télécharger notre repository sous $GITHUB_WORKSPACE, afin que le workflow puisse y accéder.
    ```bash
    name : Checkout
    uses: actions/checkout@v3
    ```

    - 2ème étape : ```Login to Docker Hub```, qui permet de se connecter à Docker Hub à l'aide de l'action Docker Login et de notre **username** et notre **access token**. Le **username** et l'**access token** sont stockers github secrets. 

    ```bash
    name : Login to Docker Hub 
    uses : docker/login-action@v1
    with :
        username : ${{secrets.USERNAME_DOCKER_HUB}}
        password : ${{secrets.ACCESS_TOKEN_DOCKER_HUB}}
    ```

    - 3ème étape : ```Set up Docker Buildx```, est un constructeur par défaut pour construire notre image Docker.

    ```bash
    name: Set up Docker Buildx
    uses: docker/setup-buildx-action@v2
    ```

    - 4ème étape : ```Build and push to Docker Hub```, qui génère l'image du conteneur et la dépose dans mon répertoire sur Docker Hub.

    ```bash
    name: Build and push to Docker Hub
    uses : docker/build-push-action@v2
    with:
        context : ./TP2
        push: true
        tags : abishaefrei/tp1devops:0.0.2b
    ```

<br/>

---
## 2. Code Python wrapperApi.py
---
Le but de ce script est de transformer le wrapper du TP1 en API. 


### 2.1 Import des librairies 

 - **requests** : une librairie permettant d'utiliser le protocole HTTP de façon simple

 - **sys** : Dans le module sys, on utilise la liste  ```sys.argv```, qui contient tous les arguments passés en ligne de commandes au script Python. On peut ainsi récupérer les valeurs pour ```lat``` (la latitude), ```long``` (la longitude) et ```api_rest``` (l'API key).  

 - **flask** : framework web Python, qui permet de créer une application web. Depuis ```flask```, on a importé la classe ```Flask``` et la fonction ```request```.

<br/>

 ### 2.2 Explication code wrapperApi.py

```python
app = Flask(__name__)
``` 
- On crée une instance de la classe ```Flask```. 

<br/>

```python
@app.route("/", methods=["GET"])
def result():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    API_KEY = argv[1]
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url).json()
``` 

- On utilise le décorateur ```@app.route("/", methods=["GET]```, pour indiquer à Flask, quelle URL et méthode doivent déclencher la fonction ```result```. 

- ```request.args.get('lat')``` permet de récupérer la valeur de la variable d'URL  ```lat```. On procède de la même manière pour récupérer la longitude. 

- La valeur de ```API_KEY``` est passée en argument en ligne de commande lors de l'exécution du script Python **wrapperApi.py**.

- Une fois avoir récupéré les valeurs des variables de ```lat```, ```long``` et ```api_rest```, on fait un appel à l'API d'OpenWeatherMap en utilisant l'url suivant : 

https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={long}&appid={API_KEY} 

- On envoie une requête GET à cet url et on retourne la réponse du serveur sous format json. 

<br/>

```python
if __name__ == '__main__':
    app.run(debug=True, port=8081, host="0.0.0.0")
``` 

- ```if __name__ == '__main__' :``` s'assure que le serveur ne s'exécute que si le script est exécuté directement depuis l'interpréteur Python. 

- ```app.run(debug=True, port=8081, host="0.0.0.0")``` permet d'exécuter l'application sur le port 8081

<br/>

**Problème rencontré** : Je n'avais pas créer et pousser l'image Docker avec Github Actions  
**Solution** : ajouter ```host="0.0.0.0"``` dans les paramètres de ```app.run``` dans **wrapperApi.py**. 

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
ARG API_KEY 

ENV API_KEY = value1
```
- ```ARG API_KEY``` permet de définir la variable ```API_KEY```. ```ENV API_KEY = value1``` définit la variable d'environnement ```API_KEY``` sur la valeur ```value1```. 

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
RUN pip3 install --no-cache-dir flask==2.3.1
```
- On lance la commande pour installer les librairies ```requests``` et ```flask```  avec les versions respectives **2.7.0** et **2.3.1**, tout en désactivant le cache. La désactivation du cache permet de réduire la taille de l'image Docker. 

<br/>

```bash
CMD ["sh", "-c", "python3 ./wrapperApi.py ${API_KEY}"]
```
- La commande **CMD​** spécifie l'instruction qui doit être exécutée au démarrage du conteneur Docker. On exécute la commande ```python3 ./wrapperApi.py ${API_KEY}``` en mode shell. 

<br/>

---
## 4. Test
---
- Grâce à notre workflow crée sur Github Actions, lorqu'on push notre travail sur Git, on crée automatiquement une image Docker, qui est mis à disposition dans ma registry sur DockerHub. 

- On pull cette image Docker, en exécutant la commande suivante : 
```bash
docker pull abishaefrei/tp1devops:0.0.2
```

- On exécute la commande ci-dessous, en mettant une API KEY :

```bash
docker run -p 8081:8081 -it --env API_KEY=**** abishaefrei/tp1devops:0.0.2
```

<br/>

**Problème rencontré** : La commande suivante ```docker run --network host --env API_KEY=**** abishaefrei/tp1devops:0.0.2``` n'est pas reconnue sur Mac.   
**Solution** : Remplacer ```--network host ``` par ```-p 8081:8081```. 

<br/>

- En effectuant un curl, on obtient bien le résultat attendu : 
```bash
curl "http://localhost:8081/?lat=5.902785&lon=102.754175"
```

Voici le résultat : 

```bash
{
  "base": "stations",
  "clouds": {
    "all": 74
  },
  "cod": 200,
  "coord": {
    "lat": 5.9028,
    "lon": 102.7542
  },
  "dt": 1682875552,
  "id": 1736405,
  "main": {
    "feels_like": 302.39,
    "grnd_level": 981,
    "humidity": 78,
    "pressure": 1008,
    "sea_level": 1008,
    "temp": 300,
    "temp_max": 300,
    "temp_min": 300
  },
  "name": "Jertih",
  "sys": {
    "country": "MY",
    "sunrise": 1682895378,
    "sunset": 1682939749
  },
  "timezone": 28800,
  "visibility": 10000,
  "weather": [
    {
      "description": "broken clouds",
      "icon": "04n",
      "id": 803,
      "main": "Clouds"
    }
  ],
  "wind": {
    "deg": 133,
    "gust": 5.06,
    "speed": 4.56
  }
}
```

<br/>

---
## 6. Partie Bonus
---
- Aucune donnée sensible n'est stockée dans l'image Docker. 

