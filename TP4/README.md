# Abisha JEYAVEL 20220390

# DEVOPS - TP4 : Cloud - Terraform

<img src="https://hashicorp.github.io/field-workshops-terraform/slides/azure/terraform-oss/images/tfaz.png" width=800>

---
## 1. Objectif du TP4 : 
---

Le but de ce TP est de créer une machine virtuelle Azure (VM) avec une adresse IP publique dans un réseau
existant ( network-tp4 ) en utilisant Terraform. On doit se connecter à la VM avec SSH et mettre à disposition le code dans un repository Github. 

<br/>

---
## 2. Configuration de provider.tf
---
- Dans le bloc ```terraform```, on inclut un ```required_providers```, pour indiquer les providers nécessaires pour la configuration de Azure Provider source.  

```python
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}
```

<br/>

- Dans le bloc ```provider```, on configure la partie **Microsoft Azure Provider**, en indiquant notre ```subscription_id```. L'attribut ```subscription_id``` est défini sur la valeur de la variable ```subscription_id``` définie dans le fichier **variables.tf**. 


```python
provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}
```

<br/>

Une fois avoir crée le **provider.tf**, on exécute la commande ci-dessous dans le terminal pour initialiser l'environnement Terraform. 

```bash
transformer init
```

<br/>

---
## 3. Configuration de variables.tf
---
Dans **variables.tf**, on a défini les variables Terraform, pour spécifier des valeurs dans notre configuration. Voici les variables définis : 

```python
variable "location" {
  type = string
  default = "france central"
}

variable "resource_group_name" {
  type = string
  default = "ADDA84-CTP"
}

variable "network_tp4" {
  type = string
  default = "network-tp4"
}

variable "subscription_id" {
  type = string
  default = "765266c6-9a23-4638-af32-dd1e32613047"
}

variable "subnet_tp4" {
  type = string
  default = "internal"
}
```

<br/>


---
## 4. Configuration de data.tf
---

- Dans le bloc ```azurerm_virtual_network```, on récupère les détails du réseau virtuel portant le nom défini dans ```var.network_tp4```, à partir d'Azure. 

- Dans le bloc ```azurerm_subnet```, on récupère les détails du sous-réseau portant le nom défini dans ```var.subnet_tp4```, à partir d'Azure. 

```python
data "azurerm_virtual_network" "network_tp4" {
  name                = var.network_tp4
  resource_group_name = var.resource_group_name
}

data "azurerm_subnet" "subnet_tp4" {
  name                = var.subnet_tp4
  virtual_network_name = var.network_tp4
  resource_group_name = var.resource_group_name
}
```

<br/>


---
## 5. Configuration de interface.tf
---

- Dans le bloc ```azurerm_public_ip```, on crée une adresse IP publique, en spécifiant les paramètres suivants : 
    - ```name```: Le nom de l'adresse IP publique
    - ```resource_group_name```: Le nom du groupe de ressource, dans lequel on souhaite créer l'adresse IP publique
    - ```location```: L'emplacement où créer l'adresse IP publique
    - ```allocation_method```: la méthode d'allocation de l'adresse IP publique, ici on a spécifié **Static** comme méthode

<br/>

- Dans le bloc ```azurerm_network_interface```, on crée une interface réseau, en spécifiant les paramètres suivants : 
    - ```name```: Le nom de l'interface réseau 
    - ```location```: L'emplacement où créer l'interface réseau
    - ```resource_group_name```: Le nom du groupe de ressource, dans lequel on souhaite créer l'interface réseau

    À l'intérieur de ce bloc, on a un bloc ```ip_configuration``` pour configurer l'adresse IP pour l'interface réseau. Voici les paramètres qu'on a précisé : 
    - ```name```: Le nom de la configuration de l'adresse IP
    - ```subnet_id```: On spécifie l'id du sous-réseau défini précédemment. 
    - ```private_ip_address_allocation```: la méthode d'allocation d'adresse IP privée, ici on a spécifié **Dynamic** comme méthode 
    - ```public_ip_address_id```: l'id de l'adresse IP publique créée précédemment


<br/>


---
## 6. Configuration de output.tf
---

Dans output.tf, on configure deux outputs (sorties), pour afficher l'id du réseau virtuel et l'id du sous-réseau virtuel. 

```python
output "virtual_network_id" {
  value = data.azurerm_virtual_network.network_tp4.id
}

output "subnet_id" {
  value = data.azurerm_subnet.subnet_tp4.id
}
```

<br/>


---
## 7. Configuration de vm.tf
---

- Dans le bloc ```tls_private_key```, on crée une clé privée SSH. 

```python
resource "tls_private_key" "ssh_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}
```

<br/>

- Dans le bloc de output ```private_key```, on affiche la clé privée SSH générée. 

```python
output "private_key" {
  value = tls_private_key.ssh_key.private_key_pem
  sensitive = true
}
```

<br/>

- Dans le bloc ```azurerm_linux_virtual_machine```, on crée une machine virtuel Linux dans Azure. Pour cela, on définit les paramètres suivants : 

    - ```name```: Le nom de la machine virtuelle
    - ```location```: L'emplacement où déployer la machine virtuelle
    - ```resource_group_name```: Le nom du groupe de ressource d'Azure
    - ```network_interface_ids```: L'id de l'interface réseau associé à la machine virtuelle
    - ```size```: La taille de la machine virtuelle
    - ```source_image_reference```: les détails liés à l'image source pour créer la machine virtuelle
    - ```os_disk```: Les paramètres du disque système de la machine virtuelle
    - ```computer_name```: le nom de la machine virtuelle
    - ```admin_username```: Le nom d'utilisateur admin de la machine virtuelle 
    - ```disable_password_authentication```: Désactive l'authentification par mot de passe pour la machine virtuelle
    - ```admin_ssh_key```: la clé publique SSH
    - ```custom_data```: pour inclure l'installation de Docker sur la machine virtuelle, on fait appel au fichier ```cloud-init.yml```. Dans ```cloud-init.yml```, on précise qu'on souhaite installer Docker sur la machine virtuelle, à partir du package docker.io. 


<br/>

Puis on a fait les commandes suivantes sur le terminal :

- La commande ci-dessous permet de comparer l'état actuel de l'infrastructure avec Terraform et l'état souhaité. Cela permet de savoir les actions nécessaires pour atteindre l'état souhaité. 

```bash
terraform plan
```

<br/>

- La commande ci-dessous permet d'appliquer les actions définis dans la configuration Terraform à l'infrastructure réelle. Cela a permis dans notre cas de créer la machine virtuelle dans Azure. 

```bash
terraform apply
```

<br/>

On effectue la commande suivante pour stocker la clé privée SSH dans id_rsa : 

```bash
terraform output -raw private_key > id_rsa
```

<br/>

---
## 8. Test
---

Pour tester la machine virtuelle, je me suis connectée en ssh, à la machine virtuelle, en effectuant la commande ci-dessous, en indiquant l'adresse IP publique de la machine virtuelle : 

```bash
ssh -i id_rsa devops@20.188.63.28
```

<br/>

---
## 9. Partie Bonus
---
- Aucune duplication de code, des variables ont été crées dans **variables.tf** 

- Au démarrage de la machine, **docker** est installé avec la machine avec cloud-init.yml 

- Le code Terraform est correctement formaté. Pour cela, j'ai utilisé la commande suivante, pour formater le code Terraform, afin qu'il soit cohérant et lisible : 

```bash
terraform fmt
```

<br/>

 Voici le résultat de la commande : 
```bash 
data.tf
interface.tf
variables.tf
vm.tf
```


---
## 10. Commentaires Terraform VS Interface utilisateur ou CLI pour déployer des ressources sur le Cloud
---

Terraform présente plusieurs avantages pour déployer des ressources sur le Cloud par rapport l'interface utilisateur ou la CLI : 

- **Infrastructure as Code (IaC)** : Terraform permet de décrire la ressource/ infrastucture sous forme de code. On peut donc facilement gérer et partager notre infrastructure.  

- **Déploiement et gestion des ressources automatisés** : Terraform permet d'automatiser le déploiement et la gestion des ressources cloud. Grâce à notre code Terraform, on peut facilement créer, mettre à jour ou supprimer une ressource sur le Cloud. Tandis qu'avec la CLI ou l'interface utilisateur, on est amené à faire des tâches manuelles. On peut donc avoir un risque d'erreurs humaines. 

- **Prévisualiser les modifications** : Avec Terraform, on peut prévisualiser les modifications, qui seront apportées à la ressource/ infrastructure. Alors qu'avec la CLI ou l'interface utilisateur, on n'a pas cette possibilité. 