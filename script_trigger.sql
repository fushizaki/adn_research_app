-- Les plateformes doivent être libres ()
delimiter |
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
delimiter ;

-- La série de TESTS suivante a été générée par l'IA

-- Tests trigger verif_dispo_plateforme

-- CAS 1: Insertion qui devrait REUSSIR (pas de conflit)
-- Campagne 1: du 2024-01-15 pour 30 jours (jusqu'au 2024-02-14)
-- Nouvelle campagne: du 2024-03-01 pour 20 jours (après la fin de la campagne 1)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-03-01', 20);
-- Cette insertion devrait réussir car pas de chevauchement
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (1, 11);

-- CAS 2: Insertion qui devrait ECHOUER (conflit total)
-- Campagne 2: du 2024-03-10 pour 45 jours (jusqu'au 2024-04-24)
-- Nouvelle campagne: du 2024-03-15 pour 30 jours (chevauche complètement)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-03-15', 30);
-- Cette insertion devrait échouer car la plateforme 3 est déjà utilisée par la campagne 2
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (3, 12);

-- CAS 3: Insertion qui devrait ECHOUER (début pendant une campagne existante)
-- Campagne 4: du 2024-07-05 pour 60 jours (jusqu'au 2024-09-03)
-- Nouvelle campagne: du 2024-08-01 pour 25 jours (commence pendant la campagne 4)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-08-01', 25);
-- Cette insertion devrait échouer car la plateforme 8 est déjà utilisée par la campagne 4
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (8, 13);

-- CAS 4: Insertion qui devrait ECHOUER (fin pendant une campagne existante)
-- Campagne 5: du 2024-09-12 pour 28 jours (jusqu'au 2024-10-10)
-- Nouvelle campagne: du 2024-08-20 pour 30 jours (se termine pendant la campagne 5)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-08-20', 30);
-- Cette insertion devrait échouer car la plateforme 9 est déjà utilisée par la campagne 5
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (9, 14);

-- CAS 5: Insertion qui devrait ECHOUER (englobe une campagne existante)
-- Campagne 8: du 2025-04-15 pour 25 jours (jusqu'au 2025-05-10)
-- Nouvelle campagne: du 2025-04-01 pour 45 jours (englobe complètement la campagne 8)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2025-04-01', 45);
-- Cette insertion devrait échouer car la plateforme 5 est déjà utilisée par la campagne 8
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (5, 15);

-- CAS 6: Insertion qui devrait REUSSIR (juste après une campagne)
-- Campagne 3: du 2024-05-20 pour 21 jours (jusqu'au 2024-06-10)
-- Nouvelle campagne: du 2024-06-11 pour 15 jours (commence le jour suivant)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-06-11', 15);
-- Cette insertion devrait réussir car commence après la fin de la campagne 3
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (5, 16);

-- CAS 7: Insertion qui devrait REUSSIR (juste avant une campagne)
-- Campagne 6: du 2024-11-01 pour 35 jours (à partir du 2024-11-01)
-- Nouvelle campagne: du 2024-10-15 pour 15 jours (se termine le 2024-10-30)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-10-15', 15);
-- Cette insertion devrait réussir car se termine avant le début de la campagne 6
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (1, 17);


-------------------------------------------------------------------------------------------------------------------------

delimiter |
CREATE TRIGGER verif_maintenance_necessaire
BEFORE INSERT ON PLANIFIER
FOR EACH ROW
BEGIN
    DECLARE temps_avant_maintenance INT;
    DECLARE intervalle_requis INT;
    
    SET temps_avant_maintenance = temps_restant_avant_maintenance(NEW.idPlateforme);
    
    SELECT intervalle_maintenance into intervalle_requis
    FROM PLATEFORME 
    WHERE idPlateforme = NEW.idPlateforme;
    
    IF temps_avant_maintenance >= intervalle_requis THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur : Maintenance requise avant utilisation de la plateforme.';
    END IF;
END |
delimiter ;

-- La série de TESTS suivante pour le trigger verif_maintenance_necessaire

-- PRÉPARATION DES DONNÉES DE TEST
-- Insertion de plateformes de test avec différents intervalles de maintenance
INSERT INTO PLATEFORME (nom, min_nb_personne, cout_journalier, intervalle_maintenance) 
VALUES 
    ('Plateforme Test M1', 2, 150.00, 30),  -- Maintenance tous les 30 jours
    ('Plateforme Test M2', 3, 200.00, 60),  -- Maintenance tous les 60 jours
    ('Plateforme Test M3', 1, 100.00, 90);  -- Maintenance tous les 90 jours

-- Récupération des IDs des plateformes de test
SET @id_plat_m1 = LAST_INSERT_ID();
SET @id_plat_m2 = @id_plat_m1 + 1;
SET @id_plat_m3 = @id_plat_m1 + 2;

-- Insertion de campagnes de test
INSERT INTO CAMPAGNE (date_debut, duree) VALUES 
    ('2025-11-01', 15),  -- Campagne future pour tests
    ('2025-11-15', 20),  -- Autre campagne future
    ('2025-12-01', 10);  -- Campagne future

SET @id_camp_m1 = LAST_INSERT_ID();
SET @id_camp_m2 = @id_camp_m1 + 1;
SET @id_camp_m3 = @id_camp_m1 + 2;

-- CAS 1: DEVRAIT RÉUSSIR - Maintenance récente (5 jours), intervalle 30 jours
-- Dernière maintenance il y a 5 jours (< 30 jours requis)
INSERT INTO MAINTENANCE (idPlateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m1, DATE_SUB(NOW(), INTERVAL 5 DAY), 1, 'terminée');

-- Cette insertion devrait RÉUSSIR car 5 < 30
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (@id_plat_m1, @id_camp_m1);

-- CAS 2: DEVRAIT ÉCHOUER - Maintenance ancienne (35 jours), intervalle 30 jours  
-- Dernière maintenance il y a 35 jours (> 30 jours requis)
INSERT INTO MAINTENANCE (idPlateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m2, DATE_SUB(NOW(), INTERVAL 35 DAY), 2, 'terminée');

-- Cette insertion devrait ÉCHOUER car 35 >= 30
-- INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (@id_plat_m2, @id_camp_m2);

-- CAS 3: DEVRAIT RÉUSSIR - Maintenance récente (45 jours), intervalle 60 jours
-- Dernière maintenance il y a 45 jours (< 60 jours requis)
INSERT INTO MAINTENANCE (idPlateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m3, DATE_SUB(NOW(), INTERVAL 45 DAY), 1, 'terminée');

-- Cette insertion devrait RÉUSSIR car 45 < 60
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (@id_plat_m3, @id_camp_m2);

-- CAS 4: DEVRAIT ÉCHOUER - Maintenance exactement à l'intervalle requis (60 jours = 60 jours)
-- Ajout d'une nouvelle plateforme pour ce test
INSERT INTO PLATEFORME (nom, min_nb_personne, cout_journalier, intervalle_maintenance) 
VALUES ('Plateforme Test M4', 2, 180.00, 60);
SET @id_plat_m4 = LAST_INSERT_ID();

INSERT INTO MAINTENANCE (idPlateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m4, DATE_SUB(NOW(), INTERVAL 60 DAY), 1, 'terminée');

-- Cette insertion devrait ÉCHOUER car 60 >= 60
-- INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (@id_plat_m4, @id_camp_m3);

-- CAS 5: DEVRAIT ÉCHOUER - Aucune maintenance terminée (considéré comme maintenance nécessaire)
-- Plateforme sans maintenance terminée
INSERT INTO PLATEFORME (nom, min_nb_personne, cout_journalier, intervalle_maintenance) 
VALUES ('Plateforme Test M5', 1, 120.00, 30);
SET @id_plat_m5 = LAST_INSERT_ID();

-- Ajout d'une maintenance planifiée seulement (pas terminée)
INSERT INTO MAINTENANCE (idPlateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m5, '2025-11-20', 1, 'planifiée');

-- Cette insertion devrait ÉCHOUER car aucune maintenance terminée trouvée
-- La fonction temps_restant_avant_maintenance retournera une valeur très élevée (NULL -> NOW() - NULL)
-- INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (@id_plat_m5, @id_camp_m1);

-- TESTS D'ÉCHEC (commentés pour éviter les erreurs lors de l'exécution)
-- Décommenter individuellement pour tester chaque cas d'échec

-- Test du CAS 2:
-- INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (@id_plat_m2, @id_camp_m2);

-- Test du CAS 4:
-- INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (@id_plat_m4, @id_camp_m3);

-- Test du CAS 5:
-- INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (@id_plat_m5, @id_camp_m1);

-- VÉRIFICATION DES RÉSULTATS
SELECT 'Tests trigger verif_maintenance_necessaire - Résultats:' AS Info;

SELECT 
    p.nom AS 'Plateforme',
    p.intervalle_maintenance AS 'Intervalle requis (jours)',
    COALESCE(MAX(m.date_maintenance), 'Aucune maintenance') AS 'Dernière maintenance',
    CASE 
        WHEN MAX(m.date_maintenance) IS NOT NULL 
        THEN DATEDIFF(NOW(), MAX(m.date_maintenance))
        ELSE 'N/A' 
    END AS 'Jours écoulés',
    CASE 
        WHEN pl.idPlateforme IS NOT NULL THEN 'PLANIFIÉE' 
        ELSE 'NON PLANIFIÉE' 
    END AS 'Statut planification'
FROM PLATEFORME p
LEFT JOIN MAINTENANCE m ON p.idPlateforme = m.idPlateforme AND m.statut = 'terminée'
LEFT JOIN PLANIFIER pl ON p.idPlateforme = pl.idPlateforme
WHERE p.nom LIKE 'Plateforme Test M%'
GROUP BY p.idPlateforme, p.nom, p.intervalle_maintenance, pl.idPlateforme;

-------------------------------------------------------------------------------------------------------------------------


--Les personnes doivent être libres (ne doivent pas déjà travailler sur un autre site)
--Vérifier qu'une personne ne soit pas enregistrer dans une autre campagne qui se déroule après la notre
delimiter |
CREATE TRIGGER verif_personnes_libres
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

-- La série de TESTS suivante a été générée par l'IA

-- Tests trigger verif_personnes_libres

-- SCÉNARIO 1 : La nouvelle campagne est entièrement incluse dans l'ancienne.
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-01-20', 10); -- Crée la campagne ID 11
-- DEVRAIT ÉCHOUER :
INSERT into PARTICIPER (idCampagne, idPersonne) VALUES (11, 2);


-- SCÉNARIO 2 : La nouvelle campagne commence avant et se termine pendant l'ancienne.
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-01-10', 15); -- Crée la campagne ID 12
-- DEVRAIT ÉCHOUER :
INSERT into PARTICIPER (idCampagne, idPersonne) VALUES (12, 2);


-- SCÉNARIO 3 : La nouvelle campagne commence pendant et se termine après l'ancienne.
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-02-10', 10); -- Crée la campagne ID 13
-- DEVRAIT ÉCHOUER :
INSERT into PARTICIPER (idCampagne, idPersonne) VALUES (13, 2);


-- SCÉNARIO 4 : La nouvelle campagne englobe complètement l'ancienne.
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-01-10', 40); -- Crée la campagne ID 14
-- DEVRAIT ÉCHOUER :
INSERT into PARTICIPER (idCampagne, idPersonne) VALUES (14, 2);


-- SCÉNARIO 5 : La nouvelle campagne commence juste après la fin de l'ancienne (pas de chevauchement).
-- Cet INSERT DEVRAIT RÉUSSIR car il n'y a pas de conflit.
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-02-15', 10); -- Crée la campagne ID 15
-- DEVRAIT RÉUSSIR :
INSERT into PARTICIPER (idCampagne, idPersonne) VALUES (15, 2);


-------------------------------------------------------------------------------------------------------------------------


delimiter |

CREATE TRIGGER verif_habilite_personnes
BEFORE INSERT ON PLANIFIER
FOR EACH ROW

BEGIN
    DECLARE hab_requises INT;
    DECLARE hab_people INT;
    
    SELECT COUNT(*) into hab_requises
    FROM DETENIR
    WHERE idPlateforme = NEW.idPlateforme;
    

    SELECT COUNT(DISTINCT h.idHabilitation) into hab_people
    FROM PARTICIPER p
    INNER JOIN HABILITER h ON p.idPersonne = h.idPersonne
    WHERE p.idCampagne = NEW.idCampagne
    and h.idHabilitation IN (
        SELECT idHabilitation
        FROM DETENIR
        WHERE idPlateforme = NEW.idPlateforme
    );
    
    IF hab_people < hab_requises THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur : Léquipe ne possède pas toutes les habilitations requises';
    END IF;
END|

delimiter ;

-- La série de TESTS suivante a été générée par l'IA

-- Tests trigger verif_habilite_personnes

-- Test 1: DEVRAIT RÉUSSIR
-- Campagne 1: personnes 1,2,3,4 
-- Personne 1: hab 1,2 | Personne 2: hab 3,4 | Personne 3: hab 1,3 | Personne 4: hab 2,4
-- Plateforme 8 requiert seulement l'habilitation 4 -> OK (personne 2 et 4 l'ont)
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (8, 1);

-- Test 2: DEVRAIT ÉCHOUER  
-- Campagne 8: personnes 3,7,11
-- Personne 3: hab 1,3 | Personne 7: hab 1,2,3 | Personne 11: hab 1,2
-- Plateforme 4 requiert hab 2,4 -> ÉCHEC (aucune personne n'a l'hab 4)
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (4, 8);

-- Test 3: DEVRAIT RÉUSSIR
-- Campagne 4: personnes 13,14,15  
-- Personne 13: hab 1,3 | Personne 14: hab 2,4 | Personne 15: hab 1,4
-- Plateforme 6 requiert hab 2,3 -> OK (personne 14 a hab 2, personne 13 a hab 3)
INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES (6, 4);

-- Vérification des résultats
SELECT 'Tests effectués:' AS info;
SELECT p.nom AS plateforme, c.idCampagne, 'AJOUTÉ' AS statut
FROM PLANIFIER pl
JOIN PLATEFORME p ON pl.idPlateforme = p.idPlateforme  
JOIN CAMPAGNE c ON pl.idCampagne = c.idCampagne
WHERE (pl.idPlateforme = 8 and pl.idCampagne = 1)
OR (pl.idPlateforme = 4 and pl.idCampagne = 8)
OR (pl.idPlateforme = 6 and pl.idCampagne = 4);

-------------------------------------------------------------------------------------------------------------------------

delimiter |
CREATE or REPLACE FUNCTION personne_disponible(idP INT, date_debut_param DATE, duree_param INT) RETURNS BOOLEAN
BEGIN
    DECLARE date_fin DATE;
    DECLARE disponible INT;
    SET date_fin = DATE_ADD(date_debut_param, INTERVAL duree_param DAY);

    SELECT count(*) into disponible
    FROM PARTICIPER p NATURAL JOIN CAMPAGNE c
    WHERE p.idPersonne = idP and (
        (date_debut_param < DATE_ADD(c.date_debut, INTERVAL c.duree DAY) and date_fin > c.date_debut)
    );
    IF disponible > 0 THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END |
delimiter ;

delimiter |
CREATE or REPLACE FUNCTION plateforme_disponible(idPl INT, date_debut_param DATE, duree_param INT) RETURNS BOOLEAN
BEGIN
    DECLARE date_fin DATE;
    DECLARE disponible INT;
    SET date_fin = DATE_ADD(date_debut_param, INTERVAL duree_param DAY);

    SELECT count(*) into disponible
    FROM PLANIFIER p NATURAL JOIN CAMPAGNE c
    WHERE p.idPlateforme = idPl and (
        (date_debut_param < DATE_ADD(c.date_debut, INTERVAL c.duree DAY) and date_fin > c.date_debut)
    );

    IF disponible > 0 THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END |
delimiter ;

delimiter |
CREATE or REPLACE FUNCTION lieu_fouille_disponible(idL INT, date_debut_param DATE, duree_param INT) RETURNS BOOLEAN
BEGIN
    DECLARE date_fin DATE;
    DECLARE disponible INT;
    SET date_fin = DATE_ADD(date_debut_param, INTERVAL duree_param DAY);

    SELECT count(*) into disponible
    FROM SEJOURNER s NATURAL JOIN CAMPAGNE c
    WHERE s.idLieu = idL and (
        (date_debut_param < DATE_ADD(c.date_debut, INTERVAL c.duree DAY) and date_fin > c.date_debut)
    );
    IF disponible > 0 THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END |
delimiter ;

delimiter |
CREATE or REPLACE FUNCTION calcul_budget_mensuelle_restant(mois_param INT, annee_param INT) RETURNS DECIMAL(10,2)
BEGIN
    DECLARE budget_total DECIMAL(10,2);
    DECLARE depenses_total DECIMAL(10,2);
    DECLARE budget_restant DECIMAL(10,2);
    
    SELECT budget into budget_total
    FROM BUDGET_MENSUEL
    WHERE mois = mois_param and annee = annee_param;

    SELECT SUM(c.duree * p.cout_journalier) into depenses_total
    FROM CAMPAGNE c
    NATURAL JOIN PLANIFIER pl
    NATURAL JOIN PLATEFORME p
    WHERE MONTH(c.date_debut) = mois_param and YEAR(c.date_debut) = annee_param;

    SET budget_restant = COALESCE(budget_total, 0) - depenses_total;
    RETURN budget_restant;
END |
delimiter ;

delimiter |
CREATE or REPLACE FUNCTION calcul_cout_total_campagne(idC INT) RETURNS DECIMAL(10,2)
BEGIN
    DECLARE cout_total DECIMAL(10,2);

    SELECT SUM(c.duree * p.cout_journalier) into cout_total
    FROM CAMPAGNE c NATURAL JOIN PLANIFIER NATURAL JOIN PLATEFORME
    WHERE c.idCampagne = idC;

    RETURN cout_total;
END |
delimiter ;


-- Permet de calculer le temps restants avant la prochaine maintenance a prévoir
delimiter |
CREATE or REPLACE FUNCTION temps_restant_avant_maintenance(idP INT) RETURNS INT
BEGIN
    DECLARE derniere_maintenance DATE;
    DECLARE temps_restant INT;

    SELECT MAX(date_maintenance) into derniere_maintenance
    FROM MAINTENANCE
    WHERE idPlateforme=idP and statut = "terminée";

    set temps_restant = DATEDIFF(NOW(),derniere_maintenance);

    IF derniere_maintenance IS NULL THEN
        RETURN 9999;
    END IF;

    RETURN temps_restant;
END |
delimiter ;

