# SAE 3.01a - Le Parc du Jurassique : Exploitation des Échantillons

## Installation et Lancement

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation des dépendances

```bash
cd /home/Kitcat/SAE_Dev_Web
pip install -r requirements.txt
```

### Structure du projet

```
SAE_Dev_Web/
├── algo/
│   ├── main.py                          # Fonctions principales de traitement ADN
│   ├── Espece.py                        # Classe Espece pour représenter les espèces
│   ├── constants.py                     # Constantes (bases ADN, etc.)
│   ├── app.py                           # Application terminal
│   └── data/                            # Fichiers .adn exemple
│       ├── abeille.adn
│       ├── eponge.adn
│       ├── humain.adn
│       ├── lapin.adn
│       ├── roadrunner.adn
│       └── trex.adn
├── bd/ 
    ├── script_creation.sql              # Script de création de la base de données
    ├── script_insert.sql                # Script d'insertion de données
    ├── script_trigger.sql               # Script des triggers
    ├── README.md                        # Ce fichier
    └── requirements.txt                 # Dépendances Python
```

### Lancement de l'application

####

```bash
cd algo/
python app.py
```

Cette application vous permet de :
- Générer des séquences ADN aléatoires
- Simuler des mutations (remplacements, insertions, délétions)
- Calculer les distances entre séquences
- Reconstruire un arbre phylogénétique