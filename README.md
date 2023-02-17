# Analytiques
Analytiques de l'étude de marché avec son fichier CSV.


## But
Ce dépôt contient un fichier python permettant de générer des statistiques et des graphiques depuis un fichier csv.


Il est utilisé pour analyser les résultats de [l'étude de marché Planteqr](https://opnform.com/forms/la-plante-qr)


## Documentation

### Télécharger le fichier csv

Le fichier csv n'est pas publiquement visible, car il contient des données sensibles... Il faut donc aller le chercher sur le Nextcloud.

> Les graphiques ne contenant pas de données sensibles seront publiés

### Lancer le programme

1. Dépendances

Paquets python
```shell
pip install -r requirements.txt
```

2. Lancer le script

```shell
python3 analytics.py
```

// Répondre "y" à la question "Générer des graphiques" générera des images dans `graphs/`

