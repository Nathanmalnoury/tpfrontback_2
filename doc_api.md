# Documentation API


## Fonctionnalité de l'API: 
tout est accessible via le end point:
```angular2html
http://host:port/article
// Soit généralement :
http://127.0.0.1:5000/article
```
4 méthodes HTML sont utilisées GET, POST, PUT, DELETE

### Method GET : 
#### GET /article
Renvoie les titres d'articles et leur id:
```angular2html
{
    "result": [
        {
            "id": 1,
            "titre": "Final testing 1"
        },
        {
            "id": 2,
            "titre": "Final testing 2"
        }],
    "success":True
}
```

#### GET /article?id=1

La ligne complète d'id 1
```angular2html
{
    "result": [
        {
            "article": "is this working ?",
            "id": 1,
            "titre": "Final testing 3.2"
        }
    ],
    "success": true
}
```

## Methods POST /article:
Permet d'ajouter un nouvel article à la base de données. Prend un JSON en entrée.
Ex : 
```angular2html
// POST : 
{
"titre": "Ceci est un nouvel article",
"article": "<p>test d'ajout d'un article</p>"
}
//Returns :
{
    "result": [
        {
            "action": "add new",
            "id": 62,
            "titre": "Ceci est un nouvel article"
        }
    ],
    "success": true
}

// Si plusieurs articles ont le meme titre, renvoie :
{
    "result": [
        {
            "action": "add new",
            "id": 63,
            "titre": "Ceci est un nouvel article",
            "warning": "multiple (2) articles have the same title : [62, 63]"
        }
    ],
    "success": true
}
```

## Methods DELETE /article : 
Prend un JSON en entrée : 
```angular2html
// DELETE 1 article
{
	"id": 55
}
// Returns : 
{
    "result": [
        {
            "action": "delete"
        }
    ],
    "success": true
}

// ou DELETE plusieurs articles 
{
	"id": [55,56,57]
}
// Returns :
{
    "result": [
        {
            "action": "multiple delete"
        }
    ],
    "success": true
}
```
**ATTENTION** : Si l'article à supprimer n'existe pas, ne renvoie pas d'erreur


## Methods PUT : mettre à jour un article
Prends un JSON en entrée de type : 
```angular2html
{
"id":5,
"titre": "Final 3.3",
"article": "is this working ?"
}
// Returns:
{
    "result": [
        {
            "action": "updated id 5"
        }
    ],
    "success": true
}
```
**ATTENTION** : Si l'article à supprimer n'existe pas, ne renvoie pas d'erreur. Ne le crée pas.


## Fichiers de l'API : 

4 fichiers concernent l'API : 

### [config_database ](resources/config_database.py) : 
Fichier de configuration de l'API pour fonctionner avec votre implémentation. Sa configuration est donc obligatoire

### [utils](resources/utils.py) :
Fonctions de base pour la création de json notamment

### [functions](resources/functions.py) :
Fonctions de requêtes à la base de données. Utilise utils pour renvoyer des données au format JSON

### [api](api_v2.py):
L'API au sens propre, fait appel aux fonctions de *functions* à partir des méthodes et arguments donnés.
