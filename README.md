# TP Front-Back Niveau 2 : Gestion d'Articles.

## 1 / API : 

L'api a été faite en utilisant Python 3.6, Flask (Micro framework populaire), SQLAlchemy (Boite à outils SQL pour Python)
Il se trouve dans [./resource/flaskapi.py](./resource)
> Un fichier de Config est en cours.

### How to Setup avec **ubuntu**:

#### Installer Python 3.6

Python 3.6 a de fortes chances d'être déjà installé sur votre machine. Une manière de le vérifier est de taper :
 ```
 $ python3.6
 ```
 * Si vous obtenez quelque chose comme cela, c'est bon! 
 
 ```
Python 3.6.7 (default, Oct 22 2018, 11:32:17) 
[GCC 8.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
 ```
* Sinon, il faut l'installer avec : 
```
sudo apt-get install python3.6
```
 
 #### Installer pip3 : 
 Si vous ne l'avez pas déjà, il faut installer pip3 (le gestionnaire de packages python). Pour savoir si vous l'avez, utilisez la commande : 
 ```
 $ which pip3
 ```
 Si la commande ne retourne rien, executez : 
 ```
 $ sudo apt-get install pip3
 ```
 
 #### Installer les packages nécessaires:
 Placez-vous à la racine du dossier, executez:
 
 ```
 $ pip3 install -r requirements.txt
 ```
 
 #### Faire tourner le programme: 

Deux possibilités : 
* mode debug :

```
$ python3.6 path/to/resource/flaskapi.py
```

* mode sans debug :
```
$ export FLASK_APP=flaskapi.py
$ flask run
```
# Modifier le fichier de configuration de l'API:
**Obligatoire, l'accès à la database sera impossible sinon. modifier [config.py](./resource/config.py) **
