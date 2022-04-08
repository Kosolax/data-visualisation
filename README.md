# data-visualisation



Architecture globale
  schéma Architecture global : moyen de communication
  
![Architecture global](https://user-images.githubusercontent.com/45556519/162449498-30c04c65-85af-459b-bd01-815f9ba2df29.png)
![image](https://user-images.githubusercontent.com/51312073/162450701-2edfa4c6-baa9-4cb6-bd51-96408c6a834b.png)


  Schéma sur le chiffrement


  L'unitée

    Nos cinq conteneurs "Unit" ont pour role de simuler les données de production. Ainsi, toutes les minutes les données de chaque unitée sont envoyées au format JSON     à un autre conteneur docker
    nommée collecteur.

    Afin de garantir la confidentialitée des données nous chiffrons les fichiers JSON à l'aide d'une clef symétrique.
    Cette clef envoyée au préalable est changée toutes les heures pour des raisons de sécurité.

Le collecteur

  Le collecteur receptionne un bon nombre d'informations. Il doit dans un premier temps déchiffrer et stocker:
 	  - les masques de preuve de travail
	  - les clefs symétrique
	  - les noms des fichiers JSON 
	  - les JSON contenant les données

  Une fois ces données correctement sauvegardées dans la RAM le collecteur compare les noms des fichiers JSON
  avec les masques. Si correspondance, le collecteur fait un controle sur la pertinence des données avant insertion en base de données.

  Chaque action effectuée est sauvegardée dans un fichier de log (doublons, valeurs incoherantes, lecture/changement de clef ... ).
  Si un trop grand nombre d'envoi de données est admis, les unitées seront bannies et n'auront plus la possiblité de communiquer avec le collecteur. 


  La Base de Données
    La Base de données est sous MySQL. Elle permet de stockée les valeurs des automates et des unités que le Collecteur lui envoie.

  L’API
    L’API reçoit un appel du front avec des paramètres. Elle appel la base de données pour récupérer les données stockées suivant les paramètres reçu, les traites puis les envoie au front.

  Le Front
    Le front appel l’API pour récupérer les données des automates stockées en base de données. Via les données reçues de l’API, il génère des graphiques puis les affiches.

 Lancer le projet
 -> docker-compose up 
