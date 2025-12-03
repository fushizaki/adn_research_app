CREATE DATABASE IF NOT EXISTS Jurassique;

USE Jurassique;

CREATE TABLE CAMPAGNE (
    idCampagne INT NOT NULL AUTO_INCREMENT,
    dateDebut DATE NOT NULL,
    duree INT NOT NULL,
    idLieu INT NOT NULL,
    PRIMARY KEY (idCampagne)
);

CREATE TABLE PERSONNE (
    username VARCHAR(50) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role_labo ENUM('DIRECTION', 'TECHNICIEN', 'ADMINISTRATION', 'CHERCHEUR') NOT NULL,
    PRIMARY KEY (username)
);

CREATE TABLE PARTICIPER (
    username VARCHAR(50) NOT NULL,
    idCampagne INT NOT NULL,
    PRIMARY KEY (username, idCampagne)
);

CREATE TABLE HABILITATION (
    idHabilitation INT NOT NULL AUTO_INCREMENT,
    nom_habilitation VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    PRIMARY KEY (idHabilitation)
);

CREATE TABLE PLATEFORME (
    idPlateforme INT NOT NULL AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    min_nb_personne INT CHECK (min_nb_personne > 0),
    cout_journalier DECIMAL(10, 2),
    intervalle_maintenance INT CHECK (intervalle_maintenance > 0),
    PRIMARY KEY (idPlateforme)
);

CREATE TABLE PLANIFIER (
    idPlateforme INT NOT NULL,
    idCampagne INT NOT NULL,
    PRIMARY KEY (idPlateforme, idCampagne)
);

CREATE TABLE LIEU_FOUILLE (
    idLieu INT NOT NULL AUTO_INCREMENT,
    nomLieu VARCHAR(100) NOT NULL,
    PRIMARY KEY (idLieu)
);

CREATE TABLE SEJOURNER (
    idCampagne INT NOT NULL,
    idLieu INT NOT NULL,
    PRIMARY KEY (idCampagne, idLieu)
);

CREATE TABLE ECHANTILLON (
    idEchantillon INT NOT NULL AUTO_INCREMENT,
    fichierAdn VARCHAR(100),
    commentairesEchantillion VARCHAR(500),
    PRIMARY KEY (idEchantillon)
);

CREATE TABLE ESPECE (
    idEspece INT NOT NULL AUTO_INCREMENT,
    nomEspece VARCHAR(100) NOT NULL,
    caracteristiques VARCHAR(500),
    PRIMARY KEY (idEspece)
);

CREATE TABLE APPARTENIR (
    idEchantillon INT NOT NULL,
    idEspece INT NOT NULL,
    PRIMARY KEY (idEchantillon, idEspece)
);

CREATE TABLE HABILITER (
    username VARCHAR(50) NOT NULL,
    idHabilitation INT NOT NULL,
    PRIMARY KEY (username, idHabilitation)
);

CREATE TABLE RAPPORTER (
    idEchantillon INT NOT NULL,
    idCampagne INT NOT NULL,
    PRIMARY KEY (idEchantillon, idCampagne)
);

CREATE TABLE BUDGET_MENSUEL (
    annee INT NOT NULL,
    mois INT NOT NULL,
    budget DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (annee, mois)
);



CREATE TABLE HISTORIQUE (
    idHistorique INT NOT NULL AUTO_INCREMENT,
    nom_fichier_base VARCHAR(255),
    proba FLOAT,
    nb_remplacement INT,
    nb_insertion INT,
    nb_deletion INT,
    note VARCHAR(255),
    date_enregistrement DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (idHistorique)
);



CREATE TABLE MATERIEL (
    idMateriel INT NOT NULL AUTO_INCREMENT,
    nom VARCHAR(100) NOT NULL,
    description VARCHAR(500),
    PRIMARY KEY (idMateriel)
);

CREATE TABLE UTILISER (
    idMateriel INT NOT NULL,
    idPlateforme INT NOT NULL,
    quantite INT NOT NULL CHECK (quantite > 0),
    PRIMARY KEY (idMateriel, idPlateforme)
);

CREATE TABLE NECESSITER (
    idHabilitation INT NOT NULL,
    idMateriel INT NOT NULL,
    PRIMARY KEY (idHabilitation, idMateriel)
);

CREATE TABLE MAINTENANCE (
    idMaintenance INT NOT NULL AUTO_INCREMENT,
    idPlateforme INT NOT NULL,
    dateMaintenance DATE NOT NULL,
    duree_maintenance INT NOT NULL DEFAULT 1 CHECK (duree_maintenance > 0),
    statut ENUM('PLANIFIEE', 'EN_COURS', 'TERMINEE') NOT NULL DEFAULT 'PLANIFIEE',
    PRIMARY KEY (idMaintenance)
);

ALTER TABLE NECESSITER ADD FOREIGN KEY (idMateriel) REFERENCES MATERIEL (idMateriel);

ALTER TABLE NECESSITER ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION (idHabilitation);

ALTER TABLE UTILISER ADD FOREIGN KEY (idMateriel) REFERENCES MATERIEL (idMateriel);

ALTER TABLE UTILISER ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);

ALTER TABLE APPARTENIR ADD FOREIGN KEY (idEchantillon) REFERENCES ECHANTILLON (idEchantillon);

ALTER TABLE APPARTENIR ADD FOREIGN KEY (idEspece) REFERENCES ESPECE (idEspece);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (idEchantillon) REFERENCES ECHANTILLON (idEchantillon);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (idLieu) REFERENCES LIEU_FOUILLE (idLieu);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (username) REFERENCES PERSONNE (username);

ALTER TABLE CAMPAGNE ADD FOREIGN KEY (idLieu) REFERENCES LIEU_FOUILLE (idLieu);

ALTER TABLE HABILITER ADD FOREIGN KEY (username) REFERENCES PERSONNE (username);

ALTER TABLE HABILITER ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION (idHabilitation);

ALTER TABLE MAINTENANCE ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);
