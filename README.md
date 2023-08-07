# Prefy76
## Quel est le but premier de Prefy76 ?
Prefy76 a pour objectif d'accompagner aux services *étrangers* des préfectures sur l'ensemble du territoire seinomarin.
## Que puis-je attendre de Prefy76 ?
A terme, Prefy76 permettra aux usagers de Seine-Maritime ou leurs aidants de :
- préparer la prise du créneau de rendez-vous en informant sur le déroulé de la démarche,
- recevoir une notification quand leur préfecture mettra en ligne le créneau qui les intéressent.
## Que ne dois-je pas attendre de Prefy76 ?
Prefy n'est pas ni ne sera :
- un outil pour prendre connaissance de ses droits,
- un outil pour prendre automatiquement un rendez-vous,
- un remplacement fiable d'une vérification manuelle.

# Roadmap
La mise à disposition des versions sur ce dépôt GitHub démarre à la version 2.5. Je garde mon _versionning_ d'origine par pure caprice !
## VERSION ACTUELLE : 2.5
- Notifications sur un serveur Discord dédié.
## 2.6
En préparation de la 2.7 :
- Le code sera plus modulaire et bien plus commenté.
- Les URL des différentes pages de la Préfecture ne seront plus dans le code. En effet, le script sera accompagné d'un fichier .csv qui contiendra toutes les informations nécessaires au fonctionnement du script afin de gagner en facilité de maintenance.
- Le script exportera des données.
## 2.7
- Le script renseignera ses trouvailles dans des fichiers mis à la disposition de tous.
## 3.0
Publication de l'application mobile ! Au minimum, celle-ci permettra à l'utilisateur de renseigner sa Préfecture et les démarches pour lesquelles il souhaite être notifié.
Le script sera adapté en conséquence.

# Remerciements
Merci aux inombrables ressources qui me servirent de point de départ dans la programmation en Python et en Javascript. Une pensée plus dirigée vers [OpenClassrooms](https://openclassrooms.com/fr) qui cultive mes expérimentations depuis de trèèèèès nombreuses années.
## Bibliothèques
Ce projet n'aurait sûrement jamais vu le jour sans les développeurs derrière les bibliothèques sur lesquelles reposent Prefy :
### Python
- [Selenium](https://github.com/SeleniumHQ/selenium) m'a permis d'automatiser la navigation sur un site Internet et d'approndir depuis sa documentation qualitative mes connaissances en HTML.
- [python-discord-webhook](https://github.com/lovvskillz/python-discord-webhook) m'a facilité l'intégration de Discord au projet. Un beau gain de temps pour une solution qui plus est intermédiaire.
