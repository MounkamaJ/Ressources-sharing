# Partage-de-ressources
Mise en place d'une plateforme peer-to-peer pour le partage des ressources pédagogiques au sein de l'Université de Yaoundé I pour le compte de l'UE PROJET.


FONCTIONNALITES:
• le partage de fichiers (texte, son, image, video, application) entre pairs
• la recherche 
• le telechargement
• le suivi de toutes les opérations éffectuées côté serveur (historiques des recherches, logs)
• l'enregistrement de toutes les ressources qui transitent entre les pairs dans un repertoire centralisé côté serveur sous le format   {nom_de_la_ressource, adresse_IP_du_pair_détenteur, numero_de_port_pour_le_téléchargement}


OUTILS ET TECHNOLOGIES:
   Langage Python pour le backend
   Interface graphique avec Tkinter


EQUIPE DE DEVELOPPEMENT:
Constituée à 100 pour cent des étudiants de M1 Réseaux


COMMENT TESTER L'APPLICATION:
  •Télécharger et installer au préalable Python3 et toutes ses bibliothèques
  •Cloner l'application Partage-de-ressources depuis le dépôt git https://github.com/MounkamaJ/Partage-de-ressources
  •Une fois dans le repertoire de l'application se placer dans le dossier du serveur et le lancer avec la commande
              python3 serveur.py
  •Se placer ensuite dans les dossiers des différents clients et les lancer avec la commande 
              python3 client.py
