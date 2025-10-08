CREATE DATABASE IF NOT EXISTS Jurassique;
use Jurassique;


CREATE TABLE CAMPAGNE(
    PRIMARY KEY(idCampagne),
    idCampagne int NOT NULL AUTO_INCREMENT,
    date_debut date NOT NULL,
    duree int NOT NULL
);

CREATE TABLE PERSONNE(
    PRIMARY KEY(idPersonne),
    idPersonne int NOT NULL AUTO_INCREMENT,
    nom varchar(30),
    prenom varchar(30)
);

CREATE TABLE PARTICIPER(
    PRIMARY KEY (idCampagne, idPersonne),
    idCampagne int,
    idPersonne int
);

CREATE TABLE HABILITATION(
    PRIMARY KEY(idHabilitation),
    idHabilitation int NOT NULL AUTO_INCREMENT,
    nom_habilitation varchar(30),
    description_hab varchar(30)
);

CREATE TABLE PLATEFORME(
    PRIMARY KEY(idPlateforme),
    idPlateforme int NOT NULL AUTO_INCREMENT,
    nom varchar(48),
    min_nb_personne int NOT NULL,
    cout_journalier float(6,2) NOT NULL,
    intervalle_maintenance int
);

CREATE TABLE DETENIR(
    PRIMARY KEY(idHabilitation, idPlateforme),
    idHabilitation int,
    idPlateforme int
);

CREATE TABLE PLANIFIER(
    PRIMARY KEY(idPlateforme, idCampagne),
    idPlateforme int,
    idCampagne int
);

CREATE TABLE LIEU(
    PRIMARY KEY(idLieu) ,
    idLieu int NOT NULL AUTO_INCREMENT,
    nomLieu varchar(48)
);

CREATE TABLE SEJOURNER(
    PRIMARY KEY(idCampagne, idLieu),
    idCampagne int,
    idLieu int    
);

CREATE TABLE ECHANTILLON (
    PRIMARY KEY(idEchant),
    idEchant int NOT NULL AUTO_INCREMENT,
    seq_nucleotides varchar (500) NOT NULL,
    commentaires_echant varchar(500)
);

CREATE TABLE ESPECE(
    PRIMARY KEY(idEspece),
    idEspece int NOT NULL AUTO_INCREMENT,
    nom_espece varchar(48),
    caracteristiques_esp varchar(48)
);

CREATE TABLE APPARTENIR(
    PRIMARY KEY(idEspece, idEchant),
    idEspece int,
    idEchant int
);

CREATE TABLE HABILITER(
    PRIMARY KEY(idPersonne, idHabilitation),
    idPersonne int,
    idHabilitation int
);

CREATE TABLE RAPPORTER(
    PRIMARY KEY(idEchant, idCampagne),
    idEchant int,
    idCampagne int
);

CREATE TABLE BUDGET_MENSUEL(
    PRIMARY KEY(annee, mois),
    annee int NOT NULL,
    mois int NOT NULL,
    budget decimal(6,2)
);

CREATE TABLE LOGIN(
    PRIMARY KEY(idPersonne ,username),
    username varchar(30),
    password varchar(30),
    idPersonne int
);

CREATE TABLE MATERIEL(
        PRIMARY KEY (idMateriel),
        idMateriel int NOT NULL AUTO_INCREMENT,
        nomMateriel varchar(50) NOT NULL,
        descriptionMateriel varchar(255)
);

CREATE TABLE UTILISER(
        PRIMARY KEY (idMateriel, idPlateforme),
        idMateriel int NOT NULL,
        idPlateforme int NOT NULL,
        quantite int NOT NULL CHECK (quantite > 0)
);

CREATE TABLE NECESSITER(
        PRIMARY KEY (idMateriel, idHabilitation),
        idMateriel INT NOT NULL,
        idHabilitation INT NOT NULL
);

ALTER TABLE APPARTENIR ADD FOREIGN KEY (idEchant) REFERENCES ECHANTILLON(idEchant);
ALTER TABLE APPARTENIR ADD FOREIGN KEY (idEspece) REFERENCES ESPECE(idEspece);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (idEchant) REFERENCES ECHANTILLON(idEchant);
ALTER TABLE RAPPORTER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE(idCampagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE(idCampagne);
ALTER TABLE SEJOURNER ADD FOREIGN KEY (idLieu) REFERENCES LIEU(idLieu);

ALTER TABLE PLANIFIER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE(idCampagne);
ALTER TABLE PLANIFIER ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME(idPlateforme);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE(idCampagne);
ALTER TABLE PARTICIPER ADD FOREIGN KEY (idPersonne) REFERENCES PERSONNE(idPersonne);

ALTER TABLE HABILITER ADD FOREIGN KEY (idPersonne) REFERENCES PERSONNE(idPersonne);
ALTER TABLE HABILITER ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION(idHabilitation);

ALTER TABLE DETENIR ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION(idHabilitation);
ALTER TABLE DETENIR ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME(idPlateforme);

ALTER TABLE NECESSITER ADD FOREIGN KEY (idMateriel) REFERENCES MATERIEL(idMateriel);
ALTER TABLE NECESSITER ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION(idHabilitation);

ALTER TABLE UTILISER ADD FOREIGN KEY (idMateriel) REFERENCES MATERIEL(idMateriel);
ALTER TABLE UTILISER ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME(idPlateforme);

ALTER TABLE LOGIN ADD FOREIGN KEY (idPersonne) REFERENCES PERSONNE(idPersonne);