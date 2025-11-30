CREATE DATABASE IF NOT EXISTS Jurassique;

use Jurassique;

CREATE TABLE
    CAMPAGNE (
        PRIMARY KEY (idCampagne),
        idCampagne int NOT NULL AUTO_INCREMENT,
        dateDebut date NOT NULL,
        duree int NOT NULL
    );

CREATE TABLE
    PERSONNE (
        PRIMARY KEY (username),
        username varchar(50) NOT NULL,
        nom varchar(100) NOT NULL,
        prenom varchar(100) NOT NULL,
        password varchar(255) NOT NULL,
        role_labo varchar(100) NOT NULL
    );

CREATE TABLE
    PARTICIPER (
        PRIMARY KEY (idCampagne, username),
        idCampagne int NOT NULL,
        username varchar(50) NOT NULL
    );

CREATE TABLE
    HABILITATION (
        PRIMARY KEY (idHabilitation),
        idHabilitation int NOT NULL AUTO_INCREMENT,
        nom_habilitation varchar(100) NOT NULL,
        description varchar(500)
    );

CREATE TABLE
    PLATEFORME (
        PRIMARY KEY (idPlateforme),
        idPlateforme int NOT NULL AUTO_INCREMENT,
        nom varchar(100) NOT NULL,
        min_nb_personne int CHECK (min_nb_personne > 0),
        cout_journalier decimal(10, 2),
        intervalle_maintenance int CHECK (intervalle_maintenance > 0)
    );

CREATE TABLE
    PLANIFIER (
        PRIMARY KEY (idPlateforme, idCampagne),
        idPlateforme int NOT NULL,
        idCampagne int NOT NULL
    );

CREATE TABLE
    LIEU_FOUILLE (
        PRIMARY KEY (idLieu),
        idLieu int NOT NULL AUTO_INCREMENT,
        nomLieu varchar(100) NOT NULL
    );

CREATE TABLE
    SEJOURNER (
        PRIMARY KEY (idCampagne, idLieu),
        idCampagne int NOT NULL,
        idLieu int NOT NULL
    );

CREATE TABLE
    ECHANTILLON (
        PRIMARY KEY (idEchant),
        idEchant int NOT NULL AUTO_INCREMENT,
        seqNucleotides varchar(1000) NOT NULL,
        commentairesEchantillon varchar(500)
    );

CREATE TABLE
    ESPECE (
        PRIMARY KEY (idEspece),
        idEspece int NOT NULL AUTO_INCREMENT,
        nomEspece varchar(100) NOT NULL,
        caracteristiques varchar(500)
    );

CREATE TABLE
    APPARTENIR (
        PRIMARY KEY (idEspece, idEchant),
        idEspece int NOT NULL,
        idEchant int NOT NULL
    );

CREATE TABLE
    HABILITER (
        PRIMARY KEY (username, idHabilitation),
        username varchar(50) NOT NULL,
        idHabilitation int NOT NULL
    );

CREATE TABLE
    RAPPORTER (
        PRIMARY KEY (idEchant, idCampagne),
        idEchant int NOT NULL,
        idCampagne int NOT NULL
    );

CREATE TABLE
    BUDGET_MENSUEL (
        PRIMARY KEY (annee, mois),
        annee int NOT NULL,
        mois int NOT NULL,
        budget decimal(10, 2) NOT NULL
    );



CREATE TABLE
    MATERIEL (
        PRIMARY KEY (idMateriel),
        idMateriel int NOT NULL AUTO_INCREMENT,
        nom varchar(100) NOT NULL,
        quantite int NOT NULL,
        description varchar(500)
    );

CREATE TABLE
    UTILISER (
        PRIMARY KEY (idMateriel, idPlateforme),
        idMateriel int NOT NULL,
        idPlateforme int NOT NULL,
        quantite int CHECK (quantite > 0)
    );

CREATE TABLE
    NECESSITER (
        PRIMARY KEY (idMateriel, idHabilitation),
        idMateriel INT NOT NULL,
        idHabilitation INT NOT NULL
    );

CREATE TABLE
    MAINTENANCE (
        PRIMARY KEY (idMaintenance),
        idMaintenance int NOT NULL AUTO_INCREMENT,
        idPlateforme int NOT NULL,
        dateMaintenance date NOT NULL,
        duree_maintenance int NOT NULL DEFAULT 1,
        statut ENUM('PLANIFIEE', 'EN_COURS', 'TERMINEE') DEFAULT 'PLANIFIEE'
    );

ALTER TABLE NECESSITER ADD FOREIGN KEY (idMateriel) REFERENCES MATERIEL (idMateriel);

ALTER TABLE NECESSITER ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION (idHabilitation);

ALTER TABLE UTILISER ADD FOREIGN KEY (idMateriel) REFERENCES MATERIEL (idMateriel);

ALTER TABLE UTILISER ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);

ALTER TABLE APPARTENIR ADD FOREIGN KEY (idEspece) REFERENCES ESPECE (idEspece);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (idEchant) REFERENCES ECHANTILLON (idEchant);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (idLieu) REFERENCES LIEU_FOUILLE (idLieu);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (username) REFERENCES PERSONNE (username);

ALTER TABLE HABILITER ADD FOREIGN KEY (username) REFERENCES PERSONNE (username);

ALTER TABLE HABILITER ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION (idHabilitation);



ALTER TABLE MAINTENANCE ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);