DROP TABLE IF EXISTS HABILITER;
DROP TABLE IF EXISTS PLANIFIER;
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

INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES 
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
CREATE TRIGGER verif_intervalle_maintenance
BEFORE INSERT ON PLANNIFIER
FOR EACH ROW
BEGIN
    DECLARE dureeFouille INT;
    DECLARE intervalleMaintenance INT;

    SELECT duree INTO dureeFouille
    FROM CAMPAGNE
    WHERE idCampagne = NEW.idCampagne;

    SELECT intervalle_maintenance INTO intervalleMaintenance
    FROM PLATEFORME
    WHERE idPlateforme = NEW.idPlateforme;

    IF (intervalleMaintenance - dureeFouille < 0) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur : La durée de fouille empiète sur l’intervalle de maintenance de la plateforme.';
    END IF;
END |
DELIMITER ;


--CREATE TABLE CAMPAGNE(
--    PRIMARY KEY(idCampagne),
--    idCampagne int NOT NULL AUTO_INCREMENT,
--    date_debut date NOT NULL,
--    duree int NOT NULL
--);
--
--CREATE TABLE PARTICIPER(
--    PRIMARY KEY (idCampagne, idPersonne),
--    idCampagne int,
--    idPersonne int
--);


--Les personnes doivent être libres (ne doivent pas déjà travailler sur un autre site)
delimiter |
CREATE TRIGGER personnes_libres
BEFORE INSERT ON PARTICIPER
FOR EACH ROW
BEGIN
    declare date_debutC date;
    declare dureeC int default 0;
    declare date_finC date;
    declare libre int default 0;

    select date_debut, duree into date_debutC, dureeC
    from CAMPAGNE
    where idCampagne = new.idCampagne;

    set date_finC = DATE_ADD(date_debutC, INTERVAL dureeC DAY);

    select count(*) into libre
    from CAMPAGNE natural join PARTICIPER
    where idPersonne = new.idPersonne and idCampagne != new.idCampagne
            and date_debutC < DATE_ADD(date_debut, INTERVAL duree DAY) 
            and date_finC > date_debut;
                                      

    if (libre > 0) then
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur : La personne travaille déjà, ou va traivailler sur une sur une autre campagne.';
    end if;

end |
delimiter ;

-- SCÉNARIO 1 : La nouvelle campagne est entièrement incluse dans l'ancienne.
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-01-20', 10); -- Crée la campagne ID 11
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (idCampagne, idPersonne) VALUES (11, 2);


-- SCÉNARIO 2 : La nouvelle campagne commence avant et se termine pendant l'ancienne.
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-01-10', 15); -- Crée la campagne ID 12
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (idCampagne, idPersonne) VALUES (12, 2);


-- SCÉNARIO 3 : La nouvelle campagne commence pendant et se termine après l'ancienne.
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-02-10', 10); -- Crée la campagne ID 13
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (idCampagne, idPersonne) VALUES (13, 2);


-- SCÉNARIO 4 : La nouvelle campagne englobe complètement l'ancienne.
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-01-10', 40); -- Crée la campagne ID 14
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (idCampagne, idPersonne) VALUES (14, 2);


-- SCÉNARIO 5 : La nouvelle campagne commence juste après la fin de l'ancienne (pas de chevauchement).
-- Cet INSERT DEVRAIT RÉUSSIR car il n'y a pas de conflit.
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-02-15', 10); -- Crée la campagne ID 15
-- DEVRAIT RÉUSSIR :
INSERT INTO PARTICIPER (idCampagne, idPersonne) VALUES (15, 2);


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


-- Les plateformes doivent être libres ()
DELIMITER |
CREATE TRIGGER verif_dispo_plateforme
BEFORE INSERT ON PLANIFIER
FOR EACH ROW
BEGIN
    declare disponible int;

    declare date_debut_camp_insert date;
    declare date_fin_camp_insert date;
    declare duree_camp_insert int;

    SELECT date_debut, duree into date_debut_camp_insert, duree_camp_insert
    FROM CAMPAGNE
    WHERE idCampagne = NEW.idCampagne;

    -- https://www.w3schools.com/sql/func_mysql_date_add.asp
    set date_fin_camp_insert = DATE_ADD(date_debut_camp_insert, INTERVAL duree_camp_insert DAY);
    
    SELECT count(*) into disponible
    FROM PLATEFORME NATURAL JOIN PLANIFIER NATURAL JOIN CAMPAGNE
    WHERE idPlateforme = NEW.idPlateforme and 
            (date_debut_camp_insert>=date_debut and date_debut_camp_insert<DATE_ADD(date_debut, INTERVAL duree DAY)) 
            or
            (date_debut_camp_insert>date_debut and date_debut_camp_insert<=DATE_ADD(date_debut, INTERVAL duree DAY))
            or
            (date_debut_camp_insert<=date_debut and date_debut_camp_insert>=DATE_ADD(date_debut, INTERVAL duree DAY)); 

    IF (disponible>0) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur : La plateforme nest pas disponible pour cette campagne';
    END IF;
END |
DELIMITER ;

-- Test du trigger verif_dispo_plateforme générer a l'aide de l'IA

-- CAS 1: Insertion qui devrait REUSSIR (pas de conflit)
-- Campagne 1: du 2024-01-15 pour 30 jours (jusqu'au 2024-02-14)
-- Nouvelle campagne: du 2024-03-01 pour 20 jours (après la fin de la campagne 1)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-03-01', 20);
-- Cette insertion devrait réussir car pas de chevauchement
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (1, 11);

-- CAS 2: Insertion qui devrait ECHOUER (conflit total)
-- Campagne 2: du 2024-03-10 pour 45 jours (jusqu'au 2024-04-24)
-- Nouvelle campagne: du 2024-03-15 pour 30 jours (chevauche complètement)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-03-15', 30);
-- Cette insertion devrait échouer car la plateforme 3 est déjà utilisée par la campagne 2
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (3, 12);

-- CAS 3: Insertion qui devrait ECHOUER (début pendant une campagne existante)
-- Campagne 4: du 2024-07-05 pour 60 jours (jusqu'au 2024-09-03)
-- Nouvelle campagne: du 2024-08-01 pour 25 jours (commence pendant la campagne 4)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-08-01', 25);
-- Cette insertion devrait échouer car la plateforme 8 est déjà utilisée par la campagne 4
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (8, 13);

-- CAS 4: Insertion qui devrait ECHOUER (fin pendant une campagne existante)
-- Campagne 5: du 2024-09-12 pour 28 jours (jusqu'au 2024-10-10)
-- Nouvelle campagne: du 2024-08-20 pour 30 jours (se termine pendant la campagne 5)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-08-20', 30);
-- Cette insertion devrait échouer car la plateforme 9 est déjà utilisée par la campagne 5
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (9, 14);

-- CAS 5: Insertion qui devrait ECHOUER (englobe une campagne existante)
-- Campagne 8: du 2025-04-15 pour 25 jours (jusqu'au 2025-05-10)
-- Nouvelle campagne: du 2025-04-01 pour 45 jours (englobe complètement la campagne 8)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2025-04-01', 45);
-- Cette insertion devrait échouer car la plateforme 5 est déjà utilisée par la campagne 8
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (5, 15);

-- CAS 6: Insertion qui devrait REUSSIR (juste après une campagne)
-- Campagne 3: du 2024-05-20 pour 21 jours (jusqu'au 2024-06-10)
-- Nouvelle campagne: du 2024-06-11 pour 15 jours (commence le jour suivant)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-06-11', 15);
-- Cette insertion devrait réussir car commence après la fin de la campagne 3
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (5, 16);

-- CAS 7: Insertion qui devrait REUSSIR (juste avant une campagne)
-- Campagne 6: du 2024-11-01 pour 35 jours (à partir du 2024-11-01)
-- Nouvelle campagne: du 2024-10-15 pour 15 jours (se termine le 2024-10-30)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-10-15', 15);
-- Cette insertion devrait réussir car se termine avant le début de la campagne 6
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (1, 17);
