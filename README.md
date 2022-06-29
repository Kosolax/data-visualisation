Schéma de bdd

# Avancement sur le projet "Au bon beurre"

## Installation et lancement du projet
Pour pouvoir lancer le projet il suffit d'installer docker.
Une fois docker installé il suffit de taper dans un CMD lancé à la racine du projet : docker compose up

## Architecture globale
![Architecture global](https://user-images.githubusercontent.com/45556519/162449498-30c04c65-85af-459b-bd01-815f9ba2df29.png)

## Flux de chiffrement entre les unités et le collecteur
![image](https://user-images.githubusercontent.com/51312073/162450701-2edfa4c6-baa9-4cb6-bd51-96408c6a834b.png)

## Algorithme de preuve de travail
Afin de vérifier l'identité de la personne qui envoie des JSON au collecteur, un algorithme a été mis en place.
L'unité va générer un nombre aléatoire en 1 et 999 avec 2 chiffres après la virgule potentiels.
Elle va ensuite transformer ce chiffre en une liste de 64 bits, ce qui correspondra à notre masque.

En parrallèle, elle va récupérer l'epoch qui correspond au moment où le fichier JSON a été généré.
Puis transformer l'epoch en une liste de 64 bits.

Enfin, elle va appliquer un XOR entre chacun des bits de notre masque et de la liste de l'epoch.

## Description de chaque conteneur
### L'unitée
Nos cinqs conteneurs "Unit" ont pour rôle de simuler les données de production. Ainsi, toutes les minutes les données de chaque unitées sont envoyées au format JSON à un autre conteneur docker nommé collecteur.

Afin de garantir la confidentialité des données, nous chiffrons les fichiers JSON à l'aide d'une clef symétrique.
Cette clef est changée toutes les heures pour des raisons de sécurité.

Elles produisent aussi une preuve de travail.

### Le collecteur
Le collecteur doit dans un premier temps déchiffrer et stocker:
- les masques de preuve de travail
- les clefs symétrique
- les noms des fichiers JSON 
- les JSON contenant les données

Une fois ces données correctement sauvegardées dans la RAM le collecteur compare les epochs contenus dans le nom des fichiers JSON
avec les masques. Si correspondance, le collecteur fait un contrôl sur la pertinence des données avant insertion en base de données.

Chaque action effectuée est sauvegardée dans un fichier de log (doublons, valeurs incohérentes, lecture/changement de clef ... ).
Si un trop grand nombre d'envoi de données eronnées est atteint, l'unité concernée sera bannie et n'aura plus la possiblité de communiquer avec le collecteur. 

### La Base de données

![bdd](https://user-images.githubusercontent.com/45556519/162461577-c2ad852f-6cd6-40bf-93b7-d7242cff4aad.png)

La Base de données est sous MySQL. Elle permet de stocker les valeurs des automates et des unitées que le Collecteur lui envoi.

### L’API
L'api peut requêter la base de données afin de récupérer différentes valeurs tel que :
	- Les unitées
	- La liste des automates d'une unitée
	- La production d'un automate d'une unitée en fonction du temps

### Le Front
Le front permet d'afficher le résultat des requêtes faites vers l'API et de les afficher dans des graphiques. Pour cela il est possible de choisir l'unitée, l'automate et le champ à visualiser au travers de liste déroulante.
