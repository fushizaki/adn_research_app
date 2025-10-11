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
    WHERE id_campagne = NEW.id_campagne;

    -- https://www.w3schools.com/sql/func_mysql_date_add.asp
    set date_fin_camp_insert = DATE_ADD(date_debut_camp_insert, INTERVAL duree_camp_insert DAY);
    
    SELECT count(*) into disponible
    FROM PLATEFORME NATURAL JOIN PLANIFIER NATURAL JOIN CAMPAGNE
    WHERE id_plateforme = NEW.id_plateforme and 
            (date_debut_camp_insert >= date_debut and date_fin_camp_insert <= DATE_ADD(date_debut, INTERVAL duree DAY)) 
            or
            (date_debut_camp_insert <= date_debut and date_fin_camp_insert >= date_debut)
            or
            (date_debut_camp_insert >= date_debut and date_fin_camp_insert >= DATE_ADD(date_debut, INTERVAL duree DAY)); 

    IF (disponible>0) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = "Erreur : La plateforme n'est pas disponible pour cette campagne";
    END IF;
END |
DELIMITER ;

-- La série de TESTS suivante a été générée par l'IA

-- Tests trigger verif_dispo_plateforme

-- TEST 1: DEVRAIT RÉUSSIR (pas de conflit)
-- Campagne 1: du 2026-01-15 pour 30 jours (jusqu'au 2026-02-14)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2026-01-15', 20);
-- Cette insertion devrait réussir car pas de chevauchement avec la plateforme 1
INSERT into PLANIFIER (id_plateforme, id_campagne) VALUES (1, 11);

-- TEST 2: DEVRAIT ÉCHOUER (conflit total)
-- Campagne 2: du 2026-03-10 pour 45 jours (jusqu'au 2026-04-24)
-- Nouvelle campagne: du 2026-03-15 pour 30 jours (chevauche complètement)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2026-03-15', 30);
-- Cette insertion devrait échouer car la plateforme 3 est déjà utilisée par la campagne 2
INSERT into PLANIFIER (id_plateforme, id_campagne) VALUES (3, 12);

-- TEST 3: DEVRAIT ÉCHOUER (début pendant une campagne existante)
-- Campagne 4: du 2026-07-05 pour 60 jours (jusqu'au 2026-09-03)
-- Nouvelle campagne: du 2026-08-01 pour 25 jours (commence pendant la campagne 4)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2026-08-01', 25);
-- Cette insertion devrait échouer car la plateforme 8 est déjà utilisée par la campagne 4
INSERT into PLANIFIER (id_plateforme, id_campagne) VALUES (8, 13);

-- TEST 4: DEVRAIT ÉCHOUER (englobe une campagne existante)
-- Campagne 8: du 2025-04-15 pour 25 jours (jusqu'au 2025-05-10)
-- Nouvelle campagne: du 2025-04-01 pour 45 jours (englobe complètement la campagne 8)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2026-04-01', 45);
-- Cette insertion devrait échouer car la plateforme 5 est déjà utilisée par la campagne 8
INSERT into PLANIFIER (id_plateforme, id_campagne) VALUES (5, 14);

-- TEST 5: DEVRAIT RÉUSSIR (juste avant une campagne)
-- Campagne 6: du 2026-11-01 pour 35 jours (à partir du 2026-11-01)
-- Nouvelle campagne: du 2026-10-15 pour 15 jours (se termine le 2026-10-30)
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2026-10-15', 15);
-- Cette insertion devrait réussir car se termine avant le début de la campagne 6
INSERT into PLANIFIER (id_plateforme, id_campagne) VALUES (1, 15);


-------------------------------------------------------------------------------------------------------------------------


DELIMITER |
CREATE TRIGGER verif_intervalle_maintenance
BEFORE INSERT ON PLANIFIER
FOR EACH ROW
BEGIN
    DECLARE duree_fouille INT;
    DECLARE intervalle_maintenance INT;

    SELECT duree INTO duree_fouille
    FROM CAMPAGNE
    WHERE id_campagne = NEW.id_campagne;

    SELECT intervalle_maintenance INTO intervalle_maintenance
    FROM PLATEFORME
    WHERE id_plateforme = NEW.id_plateforme;

    IF (intervalle_maintenance - duree_fouille < 0) THEN
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
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (1, 11);

-- Test 2: DEVRAIT ÉCHOUER
-- Plateforme 2: intervalle_maintenance = 15 jours
-- Nouvelle campagne: durée = 30 jours (> 15 jours)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-04-01', 30);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (2, 12);

-- Test 3: DEVRAIT RÉUSSIR
-- Plateforme 3: intervalle_maintenance = 45 jours
-- Nouvelle campagne: durée = 45 jours (= 45 jours)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-05-01', 45);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (3, 13);

-- Test 4: DEVRAIT ÉCHOUER
-- Plateforme 4: intervalle_maintenance = 20 jours
-- Nouvelle campagne: durée = 25 jours (> 20 jours)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-06-01', 25);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (4, 14);

-- Test 5: DEVRAIT RÉUSSIR
-- Plateforme 5: intervalle_maintenance = 35 jours
-- Nouvelle campagne: durée = 10 jours (< 35 jours)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-07-01', 10);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (5, 15);


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
    where id_campagne = new.id_campagne;

    set date_finC = DATE_ADD(date_debutC, INTERVAL dureeC DAY);

    select count(*) into libre
    from CAMPAGNE natural join PARTICIPER
    where id_personne = new.id_personne and id_campagne != new.id_campagne
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
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (11, 2);


-- SCÉNARIO 2 : La nouvelle campagne commence avant et se termine pendant l'ancienne.
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-01-10', 15); -- Crée la campagne ID 12
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (12, 2);


-- SCÉNARIO 3 : La nouvelle campagne commence pendant et se termine après l'ancienne.
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-02-10', 10); -- Crée la campagne ID 13
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (13, 2);


-- SCÉNARIO 4 : La nouvelle campagne englobe complètement l'ancienne.
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-01-10', 40); -- Crée la campagne ID 14
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (14, 2);


-- SCÉNARIO 5 : La nouvelle campagne commence juste après la fin de l'ancienne (pas de chevauchement).
-- Cet INSERT DEVRAIT RÉUSSIR car il n'y a pas de conflit.
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-02-15', 10); -- Crée la campagne ID 15
-- DEVRAIT RÉUSSIR :
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (15, 2);


-------------------------------------------------------------------------------------------------------------------------


--DELIMITER |
--
--CREATE TRIGGER verif_habilite_personnes
--BEFORE INSERT ON PLANIFIER
--FOR EACH ROW
--
--BEGIN
--    DECLARE hab_requises INT;
--    DECLARE hab_people INT;
--    
--    SELECT COUNT(*) INTO hab_requises
--    FROM DETENIR
--    WHERE id_plateforme = NEW.id_plateforme;
--    
--
--    SELECT COUNT(DISTINCT h.id_habilitation) INTO hab_people
--    FROM PARTICIPER p
--    INNER JOIN HABILITER h ON p.id_personne = h.id_personne
--    WHERE p.id_campagne = NEW.id_campagne
--    and h.id_habilitation IN (
--        SELECT id_habilitation
--        FROM DETENIR
--        WHERE id_plateforme = NEW.id_plateforme
--    );
--    
--    IF hab_people < hab_requises THEN
--        SIGNAL SQLSTATE '45000'
--        SET MESSAGE_TEXT = 'Erreur : Léquipe ne possède pas toutes les habilitations requises';
--    END IF;
--END|
--
--DELIMITER ;

-- La série de TESTS suivante a été générée par l'IA

-- Tests trigger verif_habilite_personnes

-- Test 1: DEVRAIT RÉUSSIR
-- Campagne 1: personnes 1,2,3,4 
-- Personne 1: hab 1,2 | Personne 2: hab 3,4 | Personne 3: hab 1,3 | Personne 4: hab 2,4
-- Plateforme 8 requiert seulement l'habilitation 4 -> OK (personne 2 et 4 l'ont)
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (8, 1);

-- Test 2: DEVRAIT ÉCHOUER  
-- Campagne 8: personnes 3,7,11
-- Personne 3: hab 1,3 | Personne 7: hab 1,2,3 | Personne 11: hab 1,2
-- Plateforme 4 requiert hab 2,4 -> ÉCHEC (aucune personne n'a l'hab 4)
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (4, 8);

-- Test 3: DEVRAIT RÉUSSIR
-- Campagne 4: personnes 13,14,15  
-- Personne 13: hab 1,3 | Personne 14: hab 2,4 | Personne 15: hab 1,4
-- Plateforme 6 requiert hab 2,3 -> OK (personne 14 a hab 2, personne 13 a hab 3)
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (6, 4);

-- Vérification des résultats
SELECT 'Tests effectués:' AS info;
SELECT p.nom AS plateforme, c.id_campagne, 'AJOUTÉ' AS statut
FROM PLANIFIER pl
JOIN PLATEFORME p ON pl.id_plateforme = p.id_plateforme  
JOIN CAMPAGNE c ON pl.id_campagne = c.id_campagne
WHERE (pl.id_plateforme = 8 and pl.id_campagne = 1)
OR (pl.id_plateforme = 4 and pl.id_campagne = 8) 
OR (pl.id_plateforme = 6 and pl.id_campagne = 4);


-------------------------------------------------------------------------------------------------------------------------


DELIMITER |

CREATE OR REPLACE TRIGGER verif_budget_mensuel
BEFORE INSERT ON PLANIFIER
FOR EACH ROW
BEGIN
    DECLARE date_debut_camp_insert DATE;
    DECLARE cout_total DECIMAL(10,2);
    DECLARE budget_mensuel_restant DECIMAL(10,2);
    DECLARE depassement DECIMAL(10,2);
    DECLARE res varchar(500) default '';
    
    SET cout_total = calcul_cout_total_campagne_non_planifie(new.id_campagne, new.id_plateforme);

    SELECT date_debut INTO date_debut_camp_insert
    FROM CAMPAGNE 
    WHERE id_campagne = new.id_campagne;

    SET budget_mensuel_restant = calcul_budget_mensuel_restant(MONTH(date_debut_camp_insert), YEAR(date_debut_camp_insert));

    IF budget_mensuel_restant - cout_total < 0 THEN
        SET depassement = cout_total - budget_mensuel_restant;
        SET res = CONCAT(res, 'Erreur : Le budget de la campagne dépasse le budget mensuel restant de : ', depassement, ' euros');
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = res;
    END IF;
END |

DELIMITER ;

-- La série de TESTS suivante a été générée par l'IA

-- Tests trigger verif_budget_mensuel

-- Test 1: DEVRAIT RÉUSSIR
-- Budget octobre 2025: 23000.50€, supposons aucune dépense engagée
-- Campagne courte et pas chère: 10 jours sur plateforme 1 (cout_journalier = 150.50€)
-- Coût total: 10 × 150.50 = 1505€ (< budget disponible)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2025-10-05', 10);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (1, 29);

-- Test 2: DEVRAIT ÉCHOUER
-- Budget janvier 2024: 8500€
-- Campagne très longue et chère: 80 jours sur plateforme 7 (cout_journalier = 300.15€)
-- Coût total: 80 × 300.15 = 24012€ (>> budget disponible)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-01-10', 80);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (7, 30);

-- Test 3: DEVRAIT RÉUSSIR (limite)
-- Budget février 2024: 7250.50€
-- Campagne modérée: 30 jours sur plateforme 2 (cout_journalier = 165.25€)
-- Coût total: 30 × 165.25 = 4957.50€ (< budget disponible si pas d'autres dépenses)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-02-01', 30);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (2, 31);

-- Test 4: DEVRAIT ÉCHOUER
-- Budget mars 2024: 9100.25€
-- Campagne très chère: 50 jours sur plateforme 10 (cout_journalier = 275.80€)
-- Coût total: 50 × 275.80 = 13790€ (> budget disponible)
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2024-03-15', 50);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (10, 32);

    
-------------------------------------------------------------------------------------------------------------------------



delimiter |
CREATE or REPLACE FUNCTION personne_disponible(idP INT, date_debut_param DATE, duree_param INT) RETURNS BOOLEAN
BEGIN
    DECLARE date_fin DATE;
    DECLARE disponible INT;
    SET date_fin = DATE_ADD(date_debut_param, INTERVAL duree_param DAY);

    SELECT count(*) INTO disponible
    FROM PARTICIPER p NATURAL JOIN CAMPAGNE c
    WHERE p.id_personne = idP and (
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
    WHERE p.id_plateforme = idPl and (
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
CREATE or REPLACE FUNCTION calcul_budget_mensuel_restant(mois_param INT, annee_param INT) RETURNS DECIMAL(10,2)
BEGIN
    DECLARE budget_total DECIMAL(10,2);
    DECLARE depenses_total DECIMAL(10,2);
    DECLARE budget_restant DECIMAL(10,2);
    
    SELECT budget INTO budget_total
    FROM BUDGET_MENSUEL
    WHERE mois = mois_param and annee = annee_param;

    SELECT IFNULL(SUM(c.duree * p.cout_journalier), 0) into depenses_total
    FROM CAMPAGNE c
    NATURAL JOIN PLANIFIER pl
    NATURAL JOIN PLATEFORME p
    WHERE MONTH(c.date_debut) = mois_param and YEAR(c.date_debut) = annee_param;

    SET budget_restant = COALESCE(budget_total, 0) - depenses_total;
    RETURN budget_restant;
END |
delimiter ;

delimiter |
CREATE or REPLACE FUNCTION calcul_cout_total_campagne_non_planifie(idC INT, idP INT) RETURNS DECIMAL(10,2)
BEGIN
    DECLARE cout_total DECIMAL(10,2);
    DECLARE cout_journalier_plateforme DECIMAL(10,2);
    DECLARE duree_camp INT DEFAULT 0;

    SELECT cout_journalier INTO cout_journalier_plateforme
    FROM PLATEFORME
    WHERE id_plateforme = idP;

    SELECT duree INTO duree_camp
    FROM CAMPAGNE
    where id_campagne = idC;

    SET cout_total = duree_camp * cout_journalier_plateforme; 

    RETURN cout_total;
END |
delimiter ;

delimiter |
CREATE or REPLACE FUNCTION calcul_cout_total_campagne_planifie(idC INT) RETURNS DECIMAL(10,2)
BEGIN
    DECLARE cout_total DECIMAL(10,2);

    SELECT SUM(c.duree * p.cout_journalier) INTO cout_total
    FROM CAMPAGNE c NATURAL JOIN PLANIFIER NATURAL JOIN PLATEFORME
    WHERE c.idCampagne = idC;

    RETURN cout_total;
END |
delimiter ;

-- Permet de calculer le temps restants avant la prochaine intervalle
delimiter |
CREATE or REPLACE FUNCTION temps_restant_intervalle(idP INT) RETURNS INT
BEGIN
    DECLARE temps_restant INT;
    DECLARE intervalle_maintenance_p INT;

    SELECT intervalle_maintenance into intervalle_maintenance_p
    FROM PLATEFORME
    WHERE idP = idPlateforme;

    set temps_restant = intervalle_maintenance_p-DAY(NOW());

    RETURN temps_restant;
END |
delimiter ;


