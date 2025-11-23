CREATE DATABASE IF NOT EXISTS Jurassique;

use Jurassique;

CREATE TABLE
    CAMPAGNE (
        PRIMARY KEY (id_campagne),
        id_campagne int NOT NULL AUTO_INCREMENT,
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
        PRIMARY KEY (id_campagne, username),
        id_campagne int NOT NULL,
        username varchar(50) NOT NULL
    );

CREATE TABLE
    HABILITATION (
        PRIMARY KEY (id_habilitation),
        id_habilitation int NOT NULL AUTO_INCREMENT,
        nom_habilitation varchar(100) NOT NULL,
        description varchar(500)
    );

CREATE TABLE
    PLATEFORME (
        PRIMARY KEY (id_plateforme),
        id_plateforme int NOT NULL AUTO_INCREMENT,
        nom varchar(100) NOT NULL,
        min_nb_personne int CHECK (min_nb_personne > 0),
        cout_journalier decimal(10, 2),
        intervalle_maintenance int CHECK (intervalle_maintenance > 0)
    );

CREATE TABLE
    PLANIFIER (
        PRIMARY KEY (id_plateforme, id_campagne),
        id_plateforme int NOT NULL,
        id_campagne int NOT NULL
    );

CREATE TABLE
    LIEU_FOUILLE (
        PRIMARY KEY (id_lieu),
        id_lieu int NOT NULL AUTO_INCREMENT,
        nomLieu varchar(100) NOT NULL
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
        seqNucleotides varchar(1000) NOT NULL,
        commentairesEchantillon varchar(500)
    );

CREATE TABLE
    ESPECE (
        PRIMARY KEY (id_espece),
        id_espece int NOT NULL AUTO_INCREMENT,
        nomEspece varchar(100) NOT NULL,
        caracteristiques varchar(500)
    );

CREATE TABLE
    APPARTENIR (
        PRIMARY KEY (id_espece, id_echant),
        id_espece int NOT NULL,
        id_echant int NOT NULL
    );

CREATE TABLE
    HABILITER (
        PRIMARY KEY (username, id_habilitation),
        username varchar(50) NOT NULL,
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
    MATERIEL (
        PRIMARY KEY (id_materiel),
        id_materiel int NOT NULL AUTO_INCREMENT,
        nom varchar(100) NOT NULL,
        description varchar(500)
    );

CREATE TABLE
    UTILISER (
        PRIMARY KEY (id_materiel, id_plateforme),
        id_materiel int NOT NULL,
        id_plateforme int NOT NULL,
        quantite int CHECK (quantite > 0)
    );

CREATE TABLE
    NECESSITER (
        PRIMARY KEY (id_materiel, id_habilitation),
        id_materiel INT NOT NULL,
        id_habilitation INT NOT NULL
    );

CREATE TABLE
    MAINTENANCE (
        PRIMARY KEY (id_maintenance),
        id_maintenance int NOT NULL AUTO_INCREMENT,
        id_plateforme int NOT NULL,
        dateMaintenance date NOT NULL,
        duree_maintenance int NOT NULL DEFAULT 1,
        statut ENUM('PLANIFIEE', 'EN_COURS', 'TERMINEE') DEFAULT 'PLANIFIEE'
    );

ALTER TABLE NECESSITER ADD FOREIGN KEY (id_materiel) REFERENCES MATERIEL (id_materiel);

ALTER TABLE NECESSITER ADD FOREIGN KEY (id_habilitation) REFERENCES HABILITATION (id_habilitation);

ALTER TABLE UTILISER ADD FOREIGN KEY (id_materiel) REFERENCES MATERIEL (id_materiel);

ALTER TABLE UTILISER ADD FOREIGN KEY (id_plateforme) REFERENCES PLATEFORME (id_plateforme);

ALTER TABLE APPARTENIR ADD FOREIGN KEY (id_espece) REFERENCES ESPECE (id_espece);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (id_echant) REFERENCES ECHANTILLON (id_echant);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (id_campagne) REFERENCES CAMPAGNE (id_campagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (id_campagne) REFERENCES CAMPAGNE (id_campagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (id_lieu) REFERENCES LIEU_FOUILLE (id_lieu);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (id_campagne) REFERENCES CAMPAGNE (id_campagne);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (id_plateforme) REFERENCES PLATEFORME (id_plateforme);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (id_campagne) REFERENCES CAMPAGNE (id_campagne);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (username) REFERENCES PERSONNE (username);

ALTER TABLE HABILITER ADD FOREIGN KEY (username) REFERENCES PERSONNE (username);

ALTER TABLE HABILITER ADD FOREIGN KEY (id_habilitation) REFERENCES HABILITATION (id_habilitation);



ALTER TABLE MAINTENANCE ADD FOREIGN KEY (id_plateforme) REFERENCES PLATEFORME (id_plateforme);
