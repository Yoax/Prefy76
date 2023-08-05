# Prefy, kézako ?
Travaillant dans un service public autour de l'inclusion numérique auprès d'un public majoritairement étranger, j'ai constaté un accès et un maintien des droits en France qui bloque trop souvent sur une *simple* prise de rendez-vous sur une plateforme en ligne. En effet, trop d'usagers rencontrent une rupture de leurs droits sociaux suite à l'expiration d'un titre de séjour et ce même s'ils anticipent les délais.
## Quel est le but premier de Prefy ?
Prefy a pour objectif d'accompagner aux services *étrangers* des préfectures sur l'ensemble du territoire français.
## Que puis-je attendre de Prefy ?
A terme, Prefy permettra aux usagers ou leurs aidants de :
- préparer la prise du créneau de rendez-vous en informant sur le déroulé de la démarche,
- recevoir une notification quand leur préfecture mettra en ligne le créneau qui les intéressent.
## Que ne dois-je pas attendre de Prefy ?
Prefy n'est pas ni ne sera :
- un outil pour prendre connaissance de ses droits,
- un outil pour prendre automatiquement un rendez-vous,
- un remplacement 100% fiable d'une vérification manuelle.

# Comment ça marche ?
Pour plus de lisibilité, éclatons ce qui compose Prefy.
## Une automatisation
Au tout départ, Prefy s'appellait _NotSoEasyPref_. Son but n'était alors que de recenser le nombre de créneaux disponibles et d'en sortir un graphique pour analyser et comprendre _quand_ sont mis en ligne les rendez-vous. Historiquement, l'automatisation de Prefy se nomme donc toujours _NotSoEasyPref_
Un programme informatique est capable de naviguer sur Internet. En lui donnant les bonnes instructions, il peut se rendre où nous le souhaitons ! Dans cette logique, _NotSoEasyPref_ parcourt les pages de la préfecture pour _essayer_ de prendre un rendez-vous comme monsieur tout le monde. Il analyse ensuite ce qui lui est proposé : peut-il choisir un créneau ? si oui, combien en a-t-il à disposition ?..
Concrêtement, _NotSoEasyPref_ regarde à intervales réguliers si des créneaux sont mis en ligne pour chaque démarche. Il informe ensuite le serveur de ses trouvailles.
## Un serveur
Pour que tout ce travail sorte de mon ordinateur, Prefy doit reposer sur un serveur. Il travaille dans un serveur, y stocke ses données et permet à l'application d'y accéder !
Actuellement, c'est un Raspeberry Pi 4 qui est accueille Prefy.
## Une application
Ma première idée était que Prefy repose sur des SMS. Néanmoins, cela me pose deux problèmes majeurs : l'acquisition et le stockages des numéros de téléphone doivent respecter les règles autour des données personnelles. Deuxième problème : utiliser une carte SIM personnelle dans ce genre d'usages est illégal et les plateformes légales pour l'envoi de SMS facturent... au SMS. Pour une application qui est censée un nombre indéfini de notifications, ça ne le fait pas.
Dans sa première itération, Prefy repose sur Discord pour notifier ses utilisateurs. C'est peu optimal et me pose des problèmes de confidentialité : chaque utilisateur doit s'identifier à Discord et rejoindre le serveur Prefy. Faire un usage détourné de cet outil n'est pas une solution pérenne.
Afin de permettre une intégration plus naturelle dans la vie de tout un chacun, Prefy sera une application mobile sur les _smartphones_ Android et iOS. Aucune inscription ne sera nécessaire puisqu'un identifiant aléatoire unique sera créé pour chaque utilisateur. Grâce à cela, les données personnelles restent personnelles ! C'est aussi un des meilleurs moyens pour envoyer des notifications et permettre un accès rapide à la plateforme de prise de rendez-vous sur Internet.
C'est la partie _application_ qui fut la plus hardue à définir. Les contraintes éthiques et économiques revenaient à chaque hypothèse. Il n'est pas question de faire payer l'utilisateur et je ne souhaite pas avoir besoin d'un statut légal d'entreprise pour faire tourner Prefy ! Donc évitons les données personnelles ou les pertes sèches sur mon compte bancaire...

# Roadmap
La mise à disposition des versions sur ce dépôt GitHub démarre à la version 2.5. Je garde mon _versionning_ d'origine par pure caprice !
## [x] 2.5
- Prise en charge uniquement de la Préfecture de la Seine-Maritime à Rouen.
- Notifications sur un serveur Discord dédié.
## [] 2.6
En préparation de la 2.7 :
- Le code sera plus modulaire.
- Les URL des différentes pages de la Préfecture ne seront plus dans le code. En effet, le script sera accompagné d'un fichier .csv qui contiendra toutes les informations nécessaires au fonctionnement du script afin de gagner en facilité de maintenance.
## [] 2.7
- Prise en charge de toutes les Préfectures et Sous-Préfectures. Le CSV sera mis en ligne.
- Le script renseignera ses trouvailles dans des fichiers mis à disposition de tous.
Les notifications Discord resteront pour la Préfecture de la Seine-Maritime jusqu'à la sortie de l'application mobile en 3.0.
## [] 3.0
Publication de l'application mobile !

# Remerciements
Merci aux inombrables ressources qui me servirent de point de départ dans la programmation en Python et en Javascript. Une pensée plus dirigée vers [OpenClassrooms](https://openclassrooms.com/fr) qui cultive mes expérimentations depuis de trèèèèès nombreuses années.
## Bibliothèques
Ce projet n'aurait sûrement jamais vu le jour sans les développeurs derrière les bibliothèques sur lesquelles reposent Prefy :
### Python
- [Selenium](https://github.com/SeleniumHQ/selenium) m'a permis d'automatiser la navigation sur un site Internet et d'approndir depuis sa documentation qualitative mes connaissances en HTML.
- [python-discord-webhook](https://github.com/lovvskillz/python-discord-webhook) m'a facilité l'intégration de Discord au projet. Un beau gain de temps pour une solution qui plus est intermédiaire.
