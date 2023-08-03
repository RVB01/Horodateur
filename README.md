# Horodateur
Script python pour horodater ses photos avant impression sans UX.

Téléchargez 'pillow' via PIP pour lancer ce script. 

```
pip3 install pillow
```

usage: horodateur [-h] -s SOURCE -d DESTINATION [-p [PRENOM ...]] -m {nom,metadonnees,metadonnées}

Ajoute la date des photos sur l'image

options:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        dossier contenant les photos à traiter
  -d DESTINATION, --destination DESTINATION
                        dossier de destination des photos traitées, crée si inexistant
  -p [PRENOM ...], --prenom [PRENOM ...]
                        ajoute le prénom et l'age de l'enfant à partir de sa date de naissance avec le format suivant Prénom:JJ/MM/AAAA
  -m {nom,metadonnees,metadonnées}, --methode {nom,metadonnees,metadonnées}
                        méthode de récupération de la date (dans le nom du fichier format YYYY-MM-DD ou dans les métadonnées)
