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


DELIMITER |
CREATE TRIGGER verif_intervalle_maintenance
BEFORE INSERT ON PLANIFIER
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

-- La série de TESTS suivante a été générée par l'IA

-- Tests trigger verif_intervalle_maintenance

-- Test 1: DEVRAIT RÉUSSIR
-- Plateforme 1: intervalle_maintenance = 30 jours
-- Nouvelle campagne: durée = 20 jours (< 30 jours)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-03-01', 20);
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (1, 11);

-- Test 2: DEVRAIT ÉCHOUER
-- Plateforme 2: intervalle_maintenance = 15 jours
-- Nouvelle campagne: durée = 30 jours (> 15 jours)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-04-01', 30);
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (2, 12);

-- Test 3: DEVRAIT RÉUSSIR
-- Plateforme 3: intervalle_maintenance = 45 jours
-- Nouvelle campagne: durée = 45 jours (= 45 jours)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-05-01', 45);
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (3, 13);

-- Test 4: DEVRAIT ÉCHOUER
-- Plateforme 4: intervalle_maintenance = 20 jours
-- Nouvelle campagne: durée = 25 jours (> 20 jours)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-06-01', 25);
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (4, 14);

-- Test 5: DEVRAIT RÉUSSIR
-- Plateforme 5: intervalle_maintenance = 35 jours
-- Nouvelle campagne: durée = 10 jours (< 35 jours)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-07-01', 10);
INSERT INTO PLANIFIER (idPlateforme, idCampagne) VALUES (5, 15);


-------------------------------------------------------------------------------------------------------------------------


--Les personnes doivent être libres (ne doivent pas déjà travailler sur un autre site)
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


-------------------------------------------------------------------------------------------------------------------------

-- procédure qui affiche les habilitations du materiel

DELIMITER |
create or replace function retourne_habilites(p_id_plateforme int)
RETURNS varchar(100)
BEGIN
    declare p_nom_habilitation varchar(50);
    declare res varchar(100) default '';
    declare fini BOOLEAN default FALSE;
    declare les_habilites cursor for
    
        select nom_habilitation
        FROM PLATEFORME NATURAL JOIN UTILISER NATURAL JOIN MATERIEL 
        NATURAL JOIN NECESSITER NATURAL JOIN HABILITATION
        WHERE PLATEFORME.idPlateforme = p_id_plateforme;

        declare continue handler for not found set fini = true;

        open les_habilites;
        while not fini do
            fetch les_habilites into p_nom_habilitation;
        
            if not fini then
                set res = concat (res,' ',p_nom_habilitation,' ');
                end if;
        end while;
    close les_habilites;
    return res;
end |
delimiter ;

-- La série de TESTS suivante a été générée par l'IA

-- Test 1: Plateforme avec plusieurs habilitations
SELECT retourne_habilites(1) AS 'Habilitations Plateforme 1';

-- Test 2: Plateforme avec habilitations variées
SELECT retourne_habilites(2) AS 'Habilitations Plateforme 2';

-- Test 3: Plateforme avec matériel chimique
SELECT retourne_habilites(3) AS 'Habilitations Plateforme 3';

-- Test 4: Plateforme avec peu de matériel
SELECT retourne_habilites(8) AS 'Habilitations Plateforme 8';

-- Test 5: Vérifier toutes les plateformes
SELECT idPlateforme, nom, retourne_habilites(idPlateforme) AS habilitations_requises
FROM PLATEFORME
WHERE idPlateforme IN (1, 2, 3, 5, 10);


-- trigger qui verifie si le groupe de personne possede bien les habilitations demandées
/*
DELIMITER |

CREATE TRIGGER verif_habilite_personnes
BEFORE INSERT ON PLANIFIER
FOR EACH ROW

BEGIN
    DECLARE hab_requises varchar(50);
    DECLARE hab_possedees INT;
    
    SELECT COUNT(*) INTO hab_requises
    FROM DETENIR
    WHERE idPlateforme = NEW.idPlateforme;

    IF hab_people < hab_requises THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Erreur : L équipe ne possède pas toutes les habilitations requises';
    END IF;
END|

DELIMITER ;
*/


-------------------------------------------------------------------------------------------------------------------------

delimiter |
CREATE or REPLACE FUNCTION personne_disponible(idP INT, date_debut_param DATE, duree_param INT) RETURNS BOOLEAN
BEGIN
    DECLARE date_fin DATE;
    DECLARE disponible INT;
    SET date_fin = DATE_ADD(date_debut_param, INTERVAL duree_param DAY);

    SELECT count(*) INTO disponible
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

    SELECT count(*) INTO disponible
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

    SELECT count(*) INTO disponible
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
    
    SELECT budget INTO budget_total
    FROM BUDGET_MENSUEL
    WHERE mois = mois_param and annee = annee_param;

    SELECT SUM(c.duree * p.cout_journalier) INTO depenses_total
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

    SELECT SUM(c.duree * p.cout_journalier) INTO cout_total
    FROM CAMPAGNE c NATURAL JOIN PLANIFIER NATURAL JOIN PLATEFORME
    WHERE c.idCampagne = idC;

    RETURN cout_total;
END |
delimiter ;

-------------------------------------------------------------------------------------------------------------------------

