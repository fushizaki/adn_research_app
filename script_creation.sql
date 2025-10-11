CREATE DATABASE IF NOT EXISTS Jurassique;

use Jurassique;

CREATE TABLE
    CAMPAGNE (
        PRIMARY KEY (idCampagne),
        idCampagne int NOT NULL AUTO_INCREMENT,
        date_debut date NOT NULL,
        duree int NOT NULL
    );

CREATE TABLE
    PERSONNE (
        PRIMARY KEY (idPersonne),
        idPersonne int NOT NULL AUTO_INCREMENT,
        nom varchar(30) NOT NULL,
        prenom varchar(30) NOT NULL,
        role_labo varchar(30) NOT NULL
    );

CREATE TABLE
    PARTICIPER (
        PRIMARY KEY (idCampagne, idPersonne),
        idCampagne int NOT NULL,
        idPersonne int NOT NULL
    );

CREATE TABLE
    HABILITATION (
        PRIMARY KEY (idHabilitation),
        idHabilitation int NOT NULL AUTO_INCREMENT,
        nom_habilitation varchar(30) NOT NULL,
        description_hab varchar(30)
    );

CREATE TABLE
    PLATEFORME (
        PRIMARY KEY (idPlateforme),
        idPlateforme int NOT NULL AUTO_INCREMENT,
        nom varchar(48),
        min_nb_personne int NOT NULL CHECK (min_nb_personne > 0),
        cout_journalier decimal(6, 2) NOT NULL,
        intervalle_maintenance int NOT NULL CHECK (intervalle_maintenance > 0)
    );

CREATE TABLE
    PLANIFIER (
        PRIMARY KEY (idPlateforme, idCampagne),
        idPlateforme int NOT NULL,
        idCampagne int NOT NULL
    );

CREATE TABLE
    LIEU (
        PRIMARY KEY (idLieu),
        idLieu int NOT NULL AUTO_INCREMENT,
        nomLieu varchar(48) NOT NULL
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
        seq_nucleotides varchar(500) NOT NULL,
        commentaires_echant varchar(500)
    );

CREATE TABLE
    ESPECE (
        PRIMARY KEY (idEspece),
        idEspece int NOT NULL AUTO_INCREMENT,
        nom_espece varchar(48) NOT NULL,
        caracteristiques_esp varchar(48)
    );

CREATE TABLE
    APPARTENIR (
        PRIMARY KEY (idEspece, idEchant),
        idEspece int NOT NULL,
        idEchant int NOT NULL
    );

CREATE TABLE
    HABILITER (
        PRIMARY KEY (idPersonne, idHabilitation),
        idPersonne int NOT NULL,
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
    LOGIN (
        PRIMARY KEY (idPersonne),
        username varchar(30) NOT NULL,
        password varchar(30) NOT NULL,
        idPersonne int NOT NULL
    );

CREATE TABLE
    MATERIEL (
        PRIMARY KEY (idMateriel),
        idMateriel int NOT NULL AUTO_INCREMENT,
        nomMateriel varchar(50) NOT NULL,
        descriptionMateriel varchar(255)
    );

CREATE TABLE
    UTILISER (
        PRIMARY KEY (idMateriel, idPlateforme),
        idMateriel int NOT NULL,
        idPlateforme int NOT NULL,
        quantite int NOT NULL CHECK (quantite > 0)
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
        date_maintenance date NOT NULL,
        duree_maintenance int NOT NULL DEFAULT 1,
        statut ENUM('planifiée', 'en_cours', 'terminée') DEFAULT 'planifiée'
    );

ALTER TABLE NECESSITER ADD FOREIGN KEY (idMateriel) REFERENCES MATERIEL (idMateriel);

ALTER TABLE NECESSITER ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION (idHabilitation);

ALTER TABLE UTILISER ADD FOREIGN KEY (idMateriel) REFERENCES MATERIEL (idMateriel);

ALTER TABLE UTILISER ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);

ALTER TABLE APPARTENIR ADD FOREIGN KEY (idEspece) REFERENCES ESPECE (idEspece);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (idEchant) REFERENCES ECHANTILLON (idEchant);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (idLieu) REFERENCES LIEU (idLieu);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE (idCampagne);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (idPersonne) REFERENCES PERSONNE (idPersonne);

ALTER TABLE HABILITER ADD FOREIGN KEY (idPersonne) REFERENCES PERSONNE (idPersonne);

ALTER TABLE HABILITER ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION (idHabilitation);

ALTER TABLE LOGIN ADD FOREIGN KEY (idPersonne) REFERENCES PERSONNE (idPersonne);

ALTER TABLE MAINTENANCE ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);