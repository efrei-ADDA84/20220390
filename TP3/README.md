# Abisha JEYAVEL 20220390

# DEVOPS - TP3 - Docker

<img src="https://res.cloudinary.com/practicaldev/image/fetch/s--4L3erdCy--/c_imagga_scale,f_auto,fl_progressive,h_420,q_auto,w_1000/https://dev-to-uploads.s3.amazonaws.com/uploads/articles/g6rnn7cs2mvxtctvl702.png" width=800>

---
## 1. Objectif du TP3 : 
---

Le but de ce TP est de mettre à disposition le code 
du wrapper (qui retourne la météo d'un lieu donné en utilisant openweather API) dans un repository Github. Puis, on mets à disposition l'image Docker sur Azure Container Registry (ACR) en utilisant Github Actions. On
déploie sur Azure Container Instance (ACI) en utilisant Github Actions.

<br/>

Pour ce TP, on a utilisé le code wrapperApi.py et  Dockerfile du TP2.

<br/>

---
## 2. Configuration de Github Action
---
Dans ```.github/workflows```, on crée le fichier de workflow ```main3.yml```. 

```bash
on: [push]
```
- Le workflow s'exécute quand on fait un ```push``` sur Github. 

<br/>

```bash
name: Deploy Image Docker on ACR
```
- On donne **Deploy Image Docker on ACR** comme nom à notre workflow

<br/>


```bash
jobs:
    build-and-deploy:
        runs-on: ubuntu-latest
        steps:
        # checkout the repo
        - name: 'Checkout GitHub Action'
          uses: actions/checkout@main
          
        - name: 'Login via Azure CLI'
          uses: azure/login@v1
          with:
            creds: ${{ secrets.AZURE_CREDENTIALS }}
        
        - name: 'Build and push image'
          uses: azure/docker-login@v1
          with:
            login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
            username: ${{ secrets.REGISTRY_USERNAME }}
            password: ${{ secrets.REGISTRY_PASSWORD }}
        - run: |
            docker build ./TP3 -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220390:${{ github.sha }}
            docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220390:${{ github.sha }}

        - name: 'Deploy to Azure Container Instances'
          uses: 'azure/aci-deploy@v1'
          with:
            resource-group: ${{ secrets.RESOURCE_GROUP }}
            dns-name-label: devops-20220390
            image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220390:${{ github.sha }}
            registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
            registry-username: ${{ secrets.REGISTRY_USERNAME }}
            registry-password: ${{ secrets.REGISTRY_PASSWORD }}
            name: 20220390
            location: 'france south'
            ports : 8081
            environment-variables: API_KEY=${{ secrets.API_KEY }}  
```
- Dans ```jobs```, on regroupe toutes les jobs, qui doivent être exécutées dans notre workflow. ```build-and-deploy``` est le job id, puis on définit sur quel type de machine le job doit s'exécuter. Dans notre cas, on a mis ```ubuntu-latest```. 

- Dans ```steps```, on définit les étapes de notre workflow : 
    - 1ère étape : ```Checkout GitHub Action```, qui permet de télécharger notre repository sous $GITHUB_WORKSPACE, afin que le workflow puisse y accéder.
    ```bash
    name: 'Checkout GitHub Action'
    uses: actions/checkout@main
    ```

    - 2ème étape : ```Login via Azure CLI``` permet de se connecter à Azure à l'aide de l'action Docker Login et de notre **creds**. Le **creds** est stocké dans github secrets de l'organisation efrei-ADDA84. 

    ```bash
    name: 'Login via Azure CLI'
    uses: azure/login@v1
    with:
      creds: ${{ secrets.AZURE_CREDENTIALS }}
    ```

    - 3ème étape ```Build and push image```,  
    ```Build and push image``` génère l'image du conteneur et la dépose dans Azure Container Registry

    ```bash
    - name: 'Build and push image'
      uses: azure/docker-login@v1
      with:
        login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}
 
    - run: |
        docker build ./TP3 -t ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220390:${{ github.sha }}
        docker push ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220390:${{ github.sha }}
    ```

<br/>

  - 4ème étape ```Deploy to Azure Container Instances```,  
      ```Deploy to Azure Container Instances``` permet de déployer une instance d'Azure Container Instances (ACI). On définit le nom de cette étape comme **Déploiement vers Azure Container Instances**. L'action **aci-deploy** fournie par Azure permet de déployer des instances d'Azure Container Instances. Dans le **with**, on fournit des paramètres à cette action, tels que **ressource-group, dns-name-label, image, registry-login-server, registry-username, registry-password, name, location, ports et environment-variables**

   ```bash
      name: 'Deploy to Azure Container Instances'
      uses: 'azure/aci-deploy@v1'
      with:
        resource-group: ${{ secrets.RESOURCE_GROUP }}
        dns-name-label: devops-20220390
        image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220390:${{ github.sha }}
        registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
        registry-username: ${{ secrets.REGISTRY_USERNAME }}
        registry-password: ${{ secrets.REGISTRY_PASSWORD }}
        name: 20220390
        location: 'france south'
        ports : 8081
        environment-variables: API_KEY=${{ secrets.API_KEY }}  
    ```

<br/>


        ```bash
        resource-group: ${{ secrets.RESOURCE_GROUP }}
        ```
  - On indique le ressource groupe dans lequel on souhaite déployer notre instance d'ACI
<br/>

        ```bash
        dns-name-label: devops-20220390
        ```
  - On indique l'étiquette du DNS pour l'instance d'ACI
<br/>

        ```bash
        registry-login-server: ${{ secrets.REGISTRY_LOGIN_SERVER }}
        ```
  - On indique le chemin de l'image Docker 
<br/>

        ```bash
        image: ${{ secrets.REGISTRY_LOGIN_SERVER }}/20220390:${{ github.sha }}
        ```
  - On indique le serveur de connexion du registre de conteneurs 
<br/>

        ```bash
        registry-username: ${{ secrets.REGISTRY_USERNAME }}
        ```
  - On indique le nom d'utilisateur pour accéder au registre de conteneurs 
<br/>

        ```bash
        registry-password: ${{ secrets.REGISTRY_PASSWORD }}
        ```
  - On indique le mot de passe pour accéder au registre de conteneurs 
<br/>

        ```bash
        name: 20220390
        ```
  - On définit le nom de l'instance d'ACI
<br/>

        ```bash
        location: 'france south'
        ```
  - On définit la région Azure dans laquelle on déploie l'instance d'ACI.
<br/>

        ```bash
        ports : 8081
        ```
  - On indique le port sur lequel l'application dans l'instance d'ACI sera exposée.
<br/>

        ```bash
        environment-variables: API_KEY=${{ secrets.API_KEY }}
        ```
  - On spécifie les variables d'anvironnements. Dans notre cas, on a la variable d'environnement **API_KEY**
<br/>

---
## 2. Test
---
- Grâce à notre workflow crée sur Github Actions, lorsqu'on push notre travail sur Git, on crée automatiquement une image Docker, qui est mis à disposition sur Azure Container Registry (ACR).

En effectuant un curl, on obtient bien le résultat attendu : 
```bash
curl "http://devops-20220390.francesouth.azurecontainer.io:8081/?lat=5.902785&lon=102.754175"
```

Voici le résultat : 

```bash
{
  "base": "stations",
  "clouds": {
    "all": 79
  },
  "cod": 200,
  "coord": {
    "lat": 5.9028,
    "lon": 102.7542
  },
  "dt": 1685006647,
  "id": 1736405,
  "main": {
    "feels_like": 305.65,
    "grnd_level": 981,
    "humidity": 69,
    "pressure": 1008,
    "sea_level": 1008,
    "temp": 302.13,
    "temp_max": 302.13,
    "temp_min": 302.13
  },
  "name": "Jertih",
  "sys": {
    "country": "MY",
    "sunrise": 1684968805,
    "sunset": 1685013517
  },
  "timezone": 28800,
  "visibility": 10000,
  "weather": [
    {
      "description": "broken clouds",
      "icon": "04d",
      "id": 803,
      "main": "Clouds"
    }
  ],
  "wind": {
    "deg": 37,
    "gust": 3.99,
    "speed": 4.44
  }
}
```

<br/>

---
## 6. Partie Bonus
---
- Aucune donnée sensible n'est stockée dans l'image Docker ou le code source. 

