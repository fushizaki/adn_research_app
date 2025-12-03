# SAE 3.01a - Le Parc du Jurassique : Exploitation des Échantillons

## Installation et Lancement

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Node.js et npm (pour Tailwind CSS)
- MariaDB/MySQL

### Installation des dépendances

```bash
cd SAE_Dev_Web
pip install -r requirements.txt
cd appJurassique
npm install
```

### Configuration de la base de données MariaDB

1. **Installer MariaDB** (si ce n'est pas déjà fait) :
   ```bash
   # Ubuntu/Debian
   sudo apt install mariadb-server mariadb-client

   # Arch Linux
   sudo pacman -S mariadb

   # Fedora
   sudo dnf install mariadb-server
   ```

2. **Démarrer le service MariaDB** :
   ```bash
   sudo systemctl start mariadb
   sudo systemctl enable mariadb  # Pour démarrer au boot
   ```

3. **Créer la base de données et les tables** :
   ```bash
   # Se connecter à MariaDB
   mysql -u root -p
   
   # Créer la databases
   CREATE DATABASE IF NOT EXISTS jurassique_db;
   ```

### Configuration de l'environnement (.env)

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```bash
DB_USER="votre_utilisateur"
DB_PASSWORD="votre_mot_de_passe"
DB_NAME="jurassique_db"
```

### Lancement de l'application Web Flask

```bash
cd SAE_Dev_Web
flask run
```

Ou en mode debug :
```bash
flask --debug run 
```

L'application sera accessible à l'adresse : http://127.0.0.1:5000


### Compilation Tailwind CSS (développement)

Pour recompiler les styles CSS lors du développement :
```bash
cd appJurassique
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

### Lancement de l'application Gestion ADN

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

## Tests et Couverture de Code

### Exécuter les tests

Pour lancer tous les tests du projet :

```bash
cd SAE_Dev_Web

# Tout les tests
coverage run -m pytest

# Pour avoir un rapport
coverage report -m

# Rapport HTML
coverage html
```