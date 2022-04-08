# data-visualisation

  DONE

-> Dockerisation de l'ensemble de la chaine de production
-> Génération des données
-> Chiffrement et déchiffrement des json
-> Insertion en base de données
-> Ban des unitées lors de 5 requetes invalides


  TODO

-> Chiffrement décalage des bits
-> Débuter l'envoie de données après que la base de données soit mise en place (et non avant)
-> Poposer une reprise des données si insertions manquées
-> Configurer un conteneur docker pour l'affichage des données


Architecture globale
  schéma Architecture global : moyen de communication
  
![Architecture global](https://user-images.githubusercontent.com/45556519/162449498-30c04c65-85af-459b-bd01-815f9ba2df29.png)

  Schéma sur le chiffrement


  L’Unit

  Le Collecteur

  La Base de Données
    La Base de données est sous MySQL. Elle permet de stockée les valeurs des automates et des unités que le Collecteur lui envoie.

  L’API
    L’API reçoit un appel du front avec des paramètres. Elle appel la base de données pour récupérer les données stockées suivant les paramètres reçu, les traites puis les envoie au front.

  Le Front
    Le front appel l’API pour récupérer les données des automates stockées en base de données. Via les données reçues de l’API, il génère des graphiques puis les affiches.

 Lancer le projet
 -> docker-compose up 
