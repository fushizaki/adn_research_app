CREATE DATABASE IF NOT EXISTS Jurassique;

use Jurassique;

CREATE TABLE
    CAMPAGNE (
        PRIMARY KEY (id_campagne),
        id_campagne int NOT NULL AUTO_INCREMENT,
        date_debut date NOT NULL,
        duree int NOT NULL
    );

CREATE TABLE
    PERSONNE (
        PRIMARY KEY (id_personne),
        id_personne int NOT NULL AUTO_INCREMENT,
        nom varchar(30) NOT NULL,
        prenom varchar(30) NOT NULL,
        role_labo varchar(30) NOT NULL
    );

CREATE TABLE
    PARTICIPER (
        PRIMARY KEY (id_campagne, id_personne),
        id_campagne int NOT NULL,
        id_personne int NOT NULL
    );

CREATE TABLE
    HABILITATION (
        PRIMARY KEY (id_habilitation),
        id_habilitation int NOT NULL AUTO_INCREMENT,
        nom_habilitation varchar(30) NOT NULL,
        description_hab varchar(30)
    );

CREATE TABLE
    PLATEFORME (
        PRIMARY KEY (id_plateforme),
        id_plateforme int NOT NULL AUTO_INCREMENT,
        nom varchar(48),
        min_nb_personne int NOT NULL CHECK (min_nb_personne > 0),
        cout_journalier decimal(6, 2) NOT NULL,
        intervalle_maintenance int NOT NULL CHECK (intervalle_maintenance > 0)
    );

CREATE TABLE
    PLANIFIER (
        PRIMARY KEY (id_plateforme, id_campagne),
        id_plateforme int NOT NULL,
        id_campagne int NOT NULL
    );

CREATE TABLE
    LIEU (
        PRIMARY KEY (id_lieu),
        id_lieu int NOT NULL AUTO_INCREMENT,
        nomLieu varchar(48) NOT NULL
    );

CREATE TABLE
    SEJOURNER (
        PRIMARY KEY (id_campagne, id_lieu),
        id_campagne int NOT NULL,
        id_lieu int NOT NULL
    );

CREATE TABLE
    ECHANTILLON (
        PRIMARY KEY (id_echant),
        id_echant int NOT NULL AUTO_INCREMENT,
        seq_nucleotides varchar(500) NOT NULL,
        commentaires_echant varchar(500)
    );

CREATE TABLE
    ESPECE (
        PRIMARY KEY (id_espece),
        id_espece int NOT NULL AUTO_INCREMENT,
        nom_espece varchar(48) NOT NULL,
        caracteristiques_esp varchar(48)
    );

CREATE TABLE
    APPARTENIR (
        PRIMARY KEY (id_espece, id_echant),
        id_espece int NOT NULL,
        id_echant int NOT NULL
    );

CREATE TABLE
    HABILITER (
        PRIMARY KEY (id_personne, id_habilitation),
        id_personne int NOT NULL,
        id_habilitation int NOT NULL
    );

CREATE TABLE
    RAPPORTER (
        PRIMARY KEY (id_echant, id_campagne),
        id_echant int NOT NULL,
        id_campagne int NOT NULL
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
        PRIMARY KEY (id_personne),
        username varchar(30) NOT NULL,
        password varchar(30) NOT NULL,
        id_personne int NOT NULL
    );

CREATE TABLE
    MATERIEL (
        PRIMARY KEY (id_materiel),
        id_materiel int NOT NULL AUTO_INCREMENT,
        nom_materiel varchar(50) NOT NULL,
        description_materiel varchar(255)
    );

CREATE TABLE
    UTILISER (
        PRIMARY KEY (id_materiel, id_plateforme),
        id_materiel int NOT NULL,
        id_plateforme int NOT NULL,
        quantite int NOT NULL CHECK (quantite > 0)
    );

CREATE TABLE
    NECESSITER (
        PRIMARY KEY (id_materiel, id_habilitation),
        id_materiel INT NOT NULL,
        id_habilitation INT NOT NULL
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

ALTER TABLE NECESSITER ADD FOREIGN KEY (id_habilitation) REFERENCES HABILITATION (id_habilitation);

ALTER TABLE UTILISER ADD FOREIGN KEY (id_materiel) REFERENCES MATERIEL (id_materiel);

ALTER TABLE UTILISER ADD FOREIGN KEY (id_plateforme) REFERENCES PLATEFORME (id_plateforme);

ALTER TABLE APPARTENIR ADD FOREIGN KEY (id_espece) REFERENCES ESPECE (id_espece);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (id_echant) REFERENCES ECHANTILLON (id_echant);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (id_campagne) REFERENCES CAMPAGNE (id_campagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (id_campagne) REFERENCES CAMPAGNE (id_campagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (id_lieu) REFERENCES LIEU (id_lieu);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (id_campagne) REFERENCES CAMPAGNE (id_campagne);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (id_plateforme) REFERENCES PLATEFORME (id_plateforme);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (id_campagne) REFERENCES CAMPAGNE (id_campagne);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (id_personne) REFERENCES PERSONNE (id_personne);

ALTER TABLE HABILITER ADD FOREIGN KEY (id_personne) REFERENCES PERSONNE (id_personne);

ALTER TABLE HABILITER ADD FOREIGN KEY (id_habilitation) REFERENCES HABILITATION (id_habilitation);

ALTER TABLE LOGIN ADD FOREIGN KEY (idPersonne) REFERENCES PERSONNE (idPersonne);

ALTER TABLE MAINTENANCE ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME (idPlateforme);
