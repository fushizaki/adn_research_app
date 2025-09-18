DROP TABLE IF EXISTS HABILITER;
DROP TABLE IF EXISTS PLANNIFIER;
DROP TABLE IF EXISTS DETENIR;
DROP TABLE IF EXISTS HABILITATION;
DROP TABLE IF EXISTS PLATEFORME;
DROP TABLE IF EXISTS PARTICIPER;
DROP TABLE IF EXISTS SEJOURNER;
DROP TABLE IF EXISTS PERSONNE;
DROP TABLE IF EXISTS RAPPORTER;
DROP TABLE IF EXISTS CAMPAGNE;
DROP TABLE IF EXISTS LIEU;
DROP TABLE IF EXISTS APPARTENIR;
DROP TABLE IF EXISTS ECHANTILLON;
DROP TABLE IF EXISTS ESPECE;


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

CREATE TABLE PLANNIFIER(
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

ALTER TABLE APPARTENIR ADD FOREIGN KEY (idEchant) REFERENCES ECHANTILLON(idEchant);
ALTER TABLE APPARTENIR ADD FOREIGN KEY (idEspece) REFERENCES ESPECE(idEspece);

ALTER TABLE RAPPORTER ADD FOREIGN KEY (idEchant) REFERENCES ECHANTILLON(idEchant);
ALTER TABLE RAPPORTER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE(idCampagne);

ALTER TABLE SEJOURNER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE(idCampagne);
ALTER TABLE SEJOURNER ADD FOREIGN KEY (idLieu) REFERENCES LIEU(idLieu);

ALTER TABLE PLANNIFIER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE(idCampagne);
ALTER TABLE PLANNIFIER ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME(idPlateforme);

ALTER TABLE PARTICIPER ADD FOREIGN KEY (idCampagne) REFERENCES CAMPAGNE(idCampagne);
ALTER TABLE PARTICIPER ADD FOREIGN KEY (idPersonne) REFERENCES PERSONNE(idPersonne);

ALTER TABLE HABILITER ADD FOREIGN KEY (idPersonne) REFERENCES PERSONNE(idPersonne);
ALTER TABLE HABILITER ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION(idHabilitation);

ALTER TABLE DETENIR ADD FOREIGN KEY (idHabilitation) REFERENCES HABILITATION(idHabilitation);
ALTER TABLE DETENIR ADD FOREIGN KEY (idPlateforme) REFERENCES PLATEFORME(idPlateforme);


-- Insertion pour la BDD générer a l'aide de l'IA
INSERT INTO PERSONNE (nom, prenom) VALUES 
('Durand', 'Alice'),
('Martin', 'Lucas'),
('Bernard', 'Emma'),
('Petit', 'Noah'),
('Robert', 'Léa'),
('Richard', 'Louis'),
('Dubois', 'Chloé'),
('Moreau', 'Gabriel'),
('Laurent', 'Jules'),
('Simon', 'Manon'),
('Michel', 'Tom'),
('Lefebvre', 'Sarah'),
('Leroy', 'Raphaël'),
('Roux', 'Lina'),
('David', 'Nathan'),
('Blanc', 'Eva'),
('Garcia', 'Hugo'),
('Muller', 'Zoé'),
('Faure', 'Enzo'),
('Lopez', 'Camille');

INSERT INTO PLATEFORME (nom, min_nb_personne, cout_journalier, intervalle_maintenance) VALUES 
('Plateforme Alpha', 3, 150.50, 30),
('Plateforme Beta', 2, 120.75, 45),
('Plateforme Gamma', 4, 200.00, 21),
('Plateforme Delta', 5, 250.25, 60),
('Plateforme Epsilon', 2, 100.00, 28),
('Plateforme Zeta', 3, 175.80, 35),
('Plateforme Eta', 6, 300.15, 90),
('Plateforme Theta', 2, 95.50, 14),
('Plateforme Iota', 4, 180.90, 42),
('Plateforme Kappa', 3, 165.25, 56);

INSERT INTO LIEU (nomLieu) VALUES 
('Site de Lourinhã'),
('Carrière de Holzmaden'),
('Formation Morrison'),
('Gisement de Solnhofen'),
('Site de Dinosaur National Monument'),
('Carrière de Liaoning'),
('Formation Hell Creek'),
('Site de Burgess Shale'),
('Gisement de La Rioja'),
('Carrière de Tendaguru'),
('Site de Jehol'),
('Formation Yixian'),
('Gisement de Karoo'),
('Site de Ghost Ranch'),
('Formation Cedar Mountain');

INSERT INTO HABILITATION (nom_habilitation, description_hab) VALUES 
('électrique', 'Habilitation électrique'),
('chimique', 'Habilitation chimique'),
('biologique', 'Habilitation biologique'),
('radiations', 'Habilitation radiations');

INSERT INTO DETENIR (idHabilitation, idPlateforme) VALUES 
(1, 1), (2, 1),
(3, 2), (4, 2),
(1, 3), (3, 3),
(2, 4), (4, 4),
(1, 5), (4, 5),
(2, 6), (3, 6),
(1, 7), (2, 7), (3, 7),
(4, 8),
(1, 9), (3, 9),
(2, 10), (4, 10);

INSERT INTO HABILITER (idPersonne, idHabilitation) VALUES 
(1, 1), (1, 2),
(2, 3), (2, 4),
(3, 1), (3, 3),
(4, 2), (4, 4),
(5, 1), (5, 4),
(6, 2), (6, 3),
(7, 1), (7, 2), (7, 3),
(8, 4),
(9, 1), (9, 3),
(10, 2), (10, 4),
(11, 1), (11, 2),
(12, 3), (12, 4),
(13, 1), (13, 3),
(14, 2), (14, 4),
(15, 1), (15, 4),
(16, 2), (16, 3),
(17, 1), (17, 2), (17, 3), (17, 4),
(18, 3), (18, 4),
(19, 1), (19, 2),
(20, 3), (20, 4);

INSERT INTO CAMPAGNE (date_debut, duree) VALUES 
('2024-01-15', 30),
('2024-03-10', 45),
('2024-05-20', 21),
('2024-07-05', 60),
('2024-09-12', 28),
('2024-11-01', 35),
('2025-01-18', 42),
('2025-04-15', 25),
('2025-06-22', 38),
('2025-08-30', 50);

INSERT INTO PARTICIPER (idCampagne, idPersonne) VALUES 
(1, 1), (1, 2), (1, 3), (1, 4),
(2, 5), (2, 6), (2, 7),
(3, 8), (3, 9), (3, 10), (3, 11), (3, 12),
(4, 13), (4, 14), (4, 15),
(5, 16), (5, 17), (5, 18), (5, 19),
(6, 20), (6, 1), (6, 5),
(7, 2), (7, 6), (7, 10), (7, 14),
(8, 3), (8, 7), (8, 11),
(9, 4), (9, 8), (9, 12), (9, 16), (9, 20),
(10, 9), (10, 13), (10, 17), (10, 18), (10, 19);

INSERT INTO PLANNIFIER (idPlateforme, idCampagne) VALUES 
(1, 1), (2, 1),
(3, 2), (4, 2),
(5, 3), (6, 3), (7, 3),
(8, 4),
(9, 5), (10, 5),
(1, 6), (3, 6),
(2, 7), (4, 7), (6, 7),
(5, 8), (7, 8),
(8, 9), (9, 9), (10, 9),
(1, 10), (2, 10), (3, 10);

INSERT INTO SEJOURNER (idCampagne, idLieu) VALUES 
(1, 1), (1, 2),
(2, 3), (2, 4),
(3, 5), (3, 6), (3, 7),
(4, 8),
(5, 9), (5, 10),
(6, 11), (6, 12),
(7, 13), (7, 14), (7, 15),
(8, 1), (8, 5),
(9, 2), (9, 6), (9, 10),
(10, 3), (10, 7), (10, 11);

INSERT INTO ECHANTILLON (seq_nucleotides, commentaires_echant) VALUES 
('ATCGATCGATCGATCG', 'Échantillon de dinosaure théropode'),
('GCTAGCTAGCTAGCTA', 'Fragment d\'ADN de tricératops'),
('TTAATTAATTAATTAA', 'Séquence de ptérosaure'),
('CCGGCCGGCCGGCCGG', 'ADN de stégosaure bien conservé'),
('AGTCAGTCAGTCAGTC', 'Échantillon de brachiosaure'),
('TACGTACGTACGTACG', 'Fragment de vélociraptor'),
('CATGCATGCATGCATG', 'Séquence d\'allosaure'),
('GATTGATTGATTGATT', 'ADN de diplodocus'),
('CGCGCGCGCGCGCGCG', 'Échantillon de tyrannosaure'),
('ATATATATATATATA', 'Fragment de parasaurolophus'),
('GTGTGTGTGTGTGTGT', 'Séquence d\'ankylosaure'),
('ACACACACACACACAC', 'ADN de spinosaure'),
('TGTGTGTGTGTGTGTG', 'Échantillon de carnotaure'),
('GAGAGAGAGAGAGAGA', 'Fragment de compsognathus'),
('CTCTCTCTCTCTCTCT', 'Séquence d\'iguanodon');

INSERT INTO ESPECE (nom_espece, caracteristiques_esp) VALUES 
('Tyrannosaurus Rex', 'Grand prédateur bipède'),
('Triceratops', 'Herbivore à trois cornes'),
('Stegosaurus', 'Herbivore à plaques dorsales'),
('Brachiosaurus', 'Sauropode au long cou'),
('Velociraptor', 'Petit prédateur agile'),
('Allosaurus', 'Prédateur du Jurassique'),
('Diplodocus', 'Sauropode à longue queue'),
('Pteranodon', 'Reptile volant'),
('Ankylosaurus', 'Herbivore blindé'),
('Spinosaurus', 'Prédateur semi-aquatique'),
('Parasaurolophus', 'Herbivore à crête'),
('Carnotaurus', 'Prédateur à cornes'),
('Compsognathus', 'Petit prédateur'),
('Iguanodon', 'Herbivore à pouce-éperon'),
('Archaeopteryx', 'Dinosaure-oiseau primitif');

INSERT INTO APPARTENIR (idEspece, idEchant) VALUES 
(9, 1),
(2, 2),
(8, 3),
(3, 4),
(4, 5),
(5, 6),
(6, 7),
(7, 8),
(1, 9),
(11, 10),
(9, 11),
(10, 12),
(12, 13),
(13, 14),
(14, 15);

INSERT INTO RAPPORTER (idEchant, idCampagne) VALUES 
(1, 1),
(2, 1),
(3, 2),
(4, 2),
(5, 3),
(6, 3),
(7, 3),
(8, 4),
(9, 5),
(10, 5),
(11, 6),
(12, 6),
(13, 7),
(14, 7),
(15, 8),
(1, 9),
(2, 9),
(3, 10),
(4, 10),
(5, 10);


DELIMITER |

CREATE TRIGGER verif_habilite_personnes
BEFORE INSERT ON PLANNIFIER
FOR EACH ROW

BEGIN
    DECLARE hab_requises INT;
    DECLARE hab_people INT;
    
    SELECT COUNT(*) INTO hab_requises
    FROM DETENIR
    WHERE idPlateforme = NEW.idPlateforme;
    

    SELECT COUNT(DISTINCT h.idHabilitation) INTO hab_people
    FROM PARTICIPER p
    INNER JOIN HABILITER h ON p.idPersonne = h.idPersonne
    WHERE p.idCampagne = NEW.idCampagne
    AND h.idHabilitation IN (
        SELECT idHabilitation
        FROM DETENIR
        WHERE idPlateforme = NEW.idPlateforme
    );
    
    IF hab_people < hab_requises THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur : Léquipe ne possède pas toutes les habilitations requises';
    END IF;
END|

DELIMITER ;

-- La série de TESTS suivantes est générér à l'IA

-- Test 1: DEVRAIT RÉUSSIR
-- Campagne 1: personnes 1,2,3,4 
-- Personne 1: hab 1,2 | Personne 2: hab 3,4 | Personne 3: hab 1,3 | Personne 4: hab 2,4
-- Plateforme 8 requiert seulement l'habilitation 4 -> OK (personne 2 et 4 l'ont)
INSERT INTO PLANNIFIER (idPlateforme, idCampagne) VALUES (8, 1);

-- Test 2: DEVRAIT ÉCHOUER  
-- Campagne 8: personnes 3,7,11
-- Personne 3: hab 1,3 | Personne 7: hab 1,2,3 | Personne 11: hab 1,2
-- Plateforme 4 requiert hab 2,4 -> ÉCHEC (aucune personne n'a l'hab 4)
INSERT INTO PLANNIFIER (idPlateforme, idCampagne) VALUES (4, 8);

-- Test 3: DEVRAIT RÉUSSIR
-- Campagne 4: personnes 13,14,15  
-- Personne 13: hab 1,3 | Personne 14: hab 2,4 | Personne 15: hab 1,4
-- Plateforme 6 requiert hab 2,3 -> OK (personne 14 a hab 2, personne 13 a hab 3)
INSERT INTO PLANNIFIER (idPlateforme, idCampagne) VALUES (6, 4);

-- Vérification des résultats
SELECT 'Tests effectués:' AS info;
SELECT p.nom AS plateforme, c.idCampagne, 'AJOUTÉ' AS statut
FROM PLANNIFIER pl
JOIN PLATEFORME p ON pl.idPlateforme = p.idPlateforme  
JOIN CAMPAGNE c ON pl.idCampagne = c.idCampagne
WHERE (pl.idPlateforme = 8 AND pl.idCampagne = 1)
   OR (pl.idPlateforme = 4 AND pl.idCampagne = 8) 
   OR (pl.idPlateforme = 6 AND pl.idCampagne = 4); 