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
delimiter ;

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

delimiter |
CREATE TRIGGER verif_maintenance_necessaire
BEFORE INSERT ON PLANIFIER
FOR EACH ROW
BEGIN
    DECLARE temps_avant_maintenance INT;
    DECLARE intervalle_requis INT;
    
    SET temps_avant_maintenance = temps_restant_avant_maintenance(NEW.id_plateforme);
    
    SELECT intervalle_maintenance into intervalle_requis
    FROM PLATEFORME 
    WHERE id_plateforme = NEW.id_plateforme;
    
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
INSERT INTO MAINTENANCE (id_plateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m1, DATE_SUB(NOW(), INTERVAL 5 DAY), 1, 'terminée');

-- Cette insertion devrait RÉUSSIR car 5 < 30
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (@id_plat_m1, @id_camp_m1);

-- CAS 2: DEVRAIT ÉCHOUER - Maintenance ancienne (35 jours), intervalle 30 jours  
-- Dernière maintenance il y a 35 jours (> 30 jours requis)
INSERT INTO MAINTENANCE (id_plateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m2, DATE_SUB(NOW(), INTERVAL 35 DAY), 2, 'terminée');

-- Cette insertion devrait ÉCHOUER car 35 >= 30
-- INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (@id_plat_m2, @id_camp_m2);

-- CAS 3: DEVRAIT RÉUSSIR - Maintenance récente (45 jours), intervalle 60 jours
-- Dernière maintenance il y a 45 jours (< 60 jours requis)
INSERT INTO MAINTENANCE (id_plateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m3, DATE_SUB(NOW(), INTERVAL 45 DAY), 1, 'terminée');

-- Cette insertion devrait RÉUSSIR car 45 < 60
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (@id_plat_m3, @id_camp_m2);

-- CAS 4: DEVRAIT ÉCHOUER - Maintenance exactement à l'intervalle requis (60 jours = 60 jours)
-- Ajout d'une nouvelle plateforme pour ce test
INSERT INTO PLATEFORME (nom, min_nb_personne, cout_journalier, intervalle_maintenance) 
VALUES ('Plateforme Test M4', 2, 180.00, 60);
SET @id_plat_m4 = LAST_INSERT_ID();

INSERT INTO MAINTENANCE (id_plateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m4, DATE_SUB(NOW(), INTERVAL 60 DAY), 1, 'terminée');

-- Cette insertion devrait ÉCHOUER car 60 >= 60
-- INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (@id_plat_m4, @id_camp_m3);

-- CAS 5: DEVRAIT ÉCHOUER - Aucune maintenance terminée (considéré comme maintenance nécessaire)
-- Plateforme sans maintenance terminée
INSERT INTO PLATEFORME (nom, min_nb_personne, cout_journalier, intervalle_maintenance) 
VALUES ('Plateforme Test M5', 1, 120.00, 30);
SET @id_plat_m5 = LAST_INSERT_ID();

-- Ajout d'une maintenance planifiée seulement (pas terminée)
INSERT INTO MAINTENANCE (id_plateforme, date_maintenance, duree_maintenance, statut) 
VALUES (@id_plat_m5, '2025-11-20', 1, 'planifiée');

-- Cette insertion devrait ÉCHOUER car aucune maintenance terminée trouvée
-- La fonction temps_restant_avant_maintenance retournera une valeur très élevée (NULL -> NOW() - NULL)
-- INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (@id_plat_m5, @id_camp_m1);

-- TESTS D'ÉCHEC (commentés pour éviter les erreurs lors de l'exécution)
-- Décommenter individuellement pour tester chaque cas d'échec

-- Test du CAS 2:
-- INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (@id_plat_m2, @id_camp_m2);

-- Test du CAS 4:
-- INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (@id_plat_m4, @id_camp_m3);

-- Test du CAS 5:
-- INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (@id_plat_m5, @id_camp_m1);

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
        WHEN pl.id_plateforme IS NOT NULL THEN 'PLANIFIÉE' 
        ELSE 'NON PLANIFIÉE' 
    END AS 'Statut planification'
FROM PLATEFORME p
LEFT JOIN MAINTENANCE m ON p.id_plateforme = m.id_plateforme AND m.statut = 'terminée'
LEFT JOIN PLANIFIER pl ON p.id_plateforme = pl.id_plateforme
WHERE p.nom LIKE 'Plateforme Test M%'
GROUP BY p.id_plateforme, p.nom, p.intervalle_maintenance, pl.id_plateforme;

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
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-01-20', 10); -- Crée la campagne ID 11
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (11, 2);


-- SCÉNARIO 2 : La nouvelle campagne commence avant et se termine pendant l'ancienne.
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-01-10', 15); -- Crée la campagne ID 12
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (12, 2);


-- SCÉNARIO 3 : La nouvelle campagne commence pendant et se termine après l'ancienne.
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-02-10', 10); -- Crée la campagne ID 13
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (13, 2);


-- SCÉNARIO 4 : La nouvelle campagne englobe complètement l'ancienne.
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-01-10', 40); -- Crée la campagne ID 14
-- DEVRAIT ÉCHOUER :
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (14, 2);


-- SCÉNARIO 5 : La nouvelle campagne commence juste après la fin de l'ancienne (pas de chevauchement).
-- Cet INSERT DEVRAIT RÉUSSIR car il n'y a pas de conflit.
INSERT into CAMPAGNE (date_debut, duree) VALUES ('2024-02-15', 10); -- Crée la campagne ID 15
-- DEVRAIT RÉUSSIR :
INSERT into PARTICIPER (id_campagne, id_personne) VALUES (15, 2);

-------------------------------------------------------------------------------------------------------------------------

-- fonction qui affiche les habilitations du materiel

DELIMITER |
create or replace function retourne_habilites(p_id_plateforme int)
RETURNS varchar(100)
BEGIN
    declare p_nom_habilitation varchar(50);
    declare res varchar(100) default '';
    declare fini BOOLEAN default FALSE;
    declare les_habilites cursor for
    
        select DISTINCT nom_habilitation
        FROM PLATEFORME NATURAL JOIN UTILISER NATURAL JOIN MATERIEL 
        NATURAL JOIN NECESSITER NATURAL JOIN HABILITATION
        WHERE PLATEFORME.id_plateforme = p_id_plateforme;

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
SELECT id_plateforme, nom, retourne_habilites(id_plateforme) AS habilitations_requises
FROM PLATEFORME
WHERE id_plateforme IN (1, 2, 3, 5, 10);

-------------------------------------------------------------------------------------------------------------------------


DELIMITER |
create or replace trigger verif_habilite_personnes
before insert on PLANIFIER
for each row
begin
    declare hab_requises INT;
    declare hab_possedees INT;

    select COUNT(DISTINCT id_habilitation) into hab_requises
    FROM UTILISER NATURAL JOIN NECESSITER 
    WHERE id_plateforme = NEW.id_plateforme;

    select COUNT(DISTINCT id_habilitation) into hab_possedees
    FROM PARTICIPER NATURAL JOIN HABILITER
    WHERE id_campagne = NEW.id_campagne
    and idHabilitation in 
    
    (
        select distinct id_habilitation
        FROM UTILISER NATURAL JOIN NECESSITER
        WHERE id_plateforme = NEW.id_plateforme
    );

    IF hab_possedees < hab_requises THEN
        SIGNAL SQLSTATE '45000'
        set MESSAGE_TEXT = 'Erreur : Léquipe ne possède pas toutes les habilitations requises';
    end if;
end |
DELIMITER ;

-- La série de TESTS suivante a été générée par l'IA\
-- Test 1 : DOIT RÉUSSIR
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2027-01-15', 10);
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (LAST_INSERT_ID(), 19);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (3, LAST_INSERT_ID());

-- Test 2 : DOIT ÉCHOUER
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2027-03-01', 10);
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (LAST_INSERT_ID(), 2);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (2, LAST_INSERT_ID());

-- Test 3 : DOIT RÉUSSIR
INSERT INTO CAMPAGNE (date_debut, duree) VALUES ('2027-05-10', 10);
INSERT INTO PARTICIPER (id_campagne, id_personne) VALUES (LAST_INSERT_ID(), 13);
INSERT INTO PLANIFIER (id_plateforme, id_campagne) VALUES (1, LAST_INSERT_ID());

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

-- fonction alerte maintenance 
delimiter |

create or replace function alertemaintenance(p_idplateforme int)
returns varchar(20)
begin
    declare v_joursrestants int;
    declare v_intervalle int;
    declare v_dernierecampagne date;
    declare v_datemaintenance date;
    
    select intervalle_maintenance into v_intervalle
    from PLATEFORME
    where id_plateforme = p_idplateforme;
    
    select max(DATE_ADD(c.date_debut, interval c.duree day))
    into v_dernierecampagne
    from CAMPAGNE c NATURAL JOIN PLANIFIER p
    where p.id_plateforme = p_idplateforme;
    
    if v_dernierecampagne is null then
        return 'Tranquille';
    end if;
    
    set v_datemaintenance = DATE_ADD(v_dernierecampagne, interval v_intervalle day);
    set v_joursrestants = DATEDIFF(v_datemaintenance, curdate());
    
    if v_joursrestants <= 3 then
        return 'URGENT';
    elseif v_joursrestants <= 10 then
        return 'Modéré';
    else
        return 'Tranquille';
    end if;
end|

delimiter ;

--test
select id_plateforme, nom, alertemaintenance(id_plateforme) as alerte
from PLATEFORME;
    
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
CREATE or REPLACE FUNCTION calcul_budget_mensuel_restant(mois_param INT, annee_param INT) RETURNS DECIMAL(10,2)
BEGIN
    DECLARE budget_total DECIMAL(10,2);
    DECLARE depenses_total DECIMAL(10,2);
    DECLARE budget_restant DECIMAL(10,2);
    
    SELECT budget into budget_total
    FROM BUDGET_MENSUEL
    WHERE mois = mois_param and annee = annee_param;

    SELECT IFNULL(SUM(c.duree * p.cout_journalier),0.0) into depenses_total
    FROM CAMPAGNE c NATURAL JOIN PLANIFIER pl NATURAL JOIN PLATEFORME p
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
CREATE or REPLACE FUNCTION calcul_cout_total_campagne(idC INT) RETURNS DECIMAL(10,2)
BEGIN
    DECLARE cout_total DECIMAL(10,2);

    SELECT IFNULL(SUM(c.duree * p.cout_journalier), 0.0) INTO cout_total
    FROM CAMPAGNE c NATURAL JOIN PLANIFIER NATURAL JOIN PLATEFORME
    WHERE c.id_campagne = idC;

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
    WHERE id_plateforme=idP and statut = "terminée";

    set temps_restant = DATEDIFF(NOW(),derniere_maintenance);

    IF derniere_maintenance IS NULL THEN
        RETURN 9999;
    END IF;

    RETURN temps_restant;
END |
delimiter ;
