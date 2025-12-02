-- Insertion pour la BDD générer a l'aide de l'IA
INSERT into
    PERSONNE (username, nom, prenom, password, role_labo)
VALUES
    ('adurand', 'Durand', 'Alice', 'pass123', 'DIRECTION'),
    ('lmartin', 'Martin', 'Lucas', 'secure456', 'CHERCHEUR'),
    ('ebernard', 'Bernard', 'Emma', 'mypass789', 'TECHNICIEN'),
    ('npetit', 'Petit', 'Noah', 'password1', 'ADMINISTRATION'),
    ('lrobert', 'Robert', 'Léa', 'secret234', 'CHERCHEUR'),
    ('lrichard', 'Richard', 'Louis', 'login567', 'TECHNICIEN'),
    ('cdubois', 'Dubois', 'Chloé', 'access890', 'CHERCHEUR'),
    ('gmoreau', 'Moreau', 'Gabriel', 'user123', 'ADMINISTRATION'),
    ('jlaurent', 'Laurent', 'Jules', 'pass456', 'TECHNICIEN'),
    ('msimon', 'Simon', 'Manon', 'secure789', 'CHERCHEUR'),
    ('tmichel', 'Michel', 'Tom', 'mypass012', 'DIRECTION'),
    ('slefebvre', 'Lefebvre', 'Sarah', 'password345', 'TECHNICIEN'),
    ('rleroy', 'Leroy', 'Raphaël', 'secret678', 'CHERCHEUR'),
    ('lroux', 'Roux', 'Lina', 'login901', 'ADMINISTRATION'),
    ('ndavid', 'David', 'Nathan', 'access234', 'TECHNICIEN'),
    ('eblanc', 'Blanc', 'Eva', 'user567', 'CHERCHEUR'),
    ('hgarcia', 'Garcia', 'Hugo', 'pass890', 'DIRECTION'),
    ('zmuller', 'Muller', 'Zoé', 'secure123', 'TECHNICIEN'),
    ('efaure', 'Faure', 'Enzo', 'mypass456', 'CHERCHEUR'),
    ('clopez', 'Lopez', 'Camille', 'password789', 'ADMINISTRATION');

INSERT into
    PLATEFORME (
        nom,
        min_nb_personne,
        cout_journalier,
        intervalle_maintenance
    )
VALUES
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

INSERT into
    LIEU_FOUILLE (nomLieu)
VALUES
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

INSERT into
    HABILITATION (nom_habilitation, description, idMateriel)
VALUES
    ('électrique', 'Habilitation électrique', 1),
    ('chimique', 'Habilitation chimique', 2),
    ('biologique', 'Habilitation biologique', 3),
    ('radiations', 'Habilitation radiations', 4);

INSERT into
    HABILITER (username, idHabilitation)
VALUES
    ('adurand', 1),
    ('adurand', 2),
    ('lmartin', 3),
    ('lmartin', 4),
    ('ebernard', 1),
    ('ebernard', 3),
    ('npetit', 2),
    ('npetit', 4),
    ('lrobert', 1),
    ('lrobert', 4),
    ('lrichard', 2),
    ('lrichard', 3),
    ('cdubois', 1),
    ('cdubois', 2),
    ('cdubois', 3),
    ('gmoreau', 4),
    ('jlaurent', 1),
    ('jlaurent', 3),
    ('msimon', 2),
    ('msimon', 4),
    ('tmichel', 1),
    ('tmichel', 2),
    ('slefebvre', 3),
    ('slefebvre', 4),
    ('rleroy', 1),
    ('rleroy', 3),
    ('lroux', 2),
    ('lroux', 4),
    ('ndavid', 1),
    ('ndavid', 4),
    ('eblanc', 2),
    ('eblanc', 3),
    ('hgarcia', 1),
    ('hgarcia', 2),
    ('hgarcia', 3),
    ('hgarcia', 4),
    ('zmuller', 3),
    ('zmuller', 4),
    ('efaure', 1),
    ('efaure', 2),
    ('clopez', 3),
    ('clopez', 4);

INSERT into
    CAMPAGNE (dateDebut, duree)
VALUES
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

INSERT into
    PARTICIPER (idCampagne, username)
VALUES
    (1, 'adurand'),
    (1, 'lmartin'),
    (1, 'ebernard'),
    (1, 'npetit'),
    (2, 'lrobert'),
    (2, 'lrichard'),
    (2, 'cdubois'),
    (3, 'gmoreau'),
    (3, 'jlaurent'),
    (3, 'msimon'),
    (3, 'tmichel'),
    (3, 'slefebvre'),
    (4, 'rleroy'),
    (4, 'lroux'),
    (4, 'ndavid'),
    (5, 'eblanc'),
    (5, 'hgarcia'),
    (5, 'zmuller'),
    (5, 'efaure'),
    (6, 'clopez'),
    (6, 'adurand'),
    (6, 'lrobert'),
    (7, 'lmartin'),
    (7, 'lrichard'),
    (7, 'msimon'),
    (7, 'lroux'),
    (8, 'ebernard'),
    (8, 'cdubois'),
    (8, 'tmichel'),
    (9, 'npetit'),
    (9, 'gmoreau'),
    (9, 'slefebvre'),
    (9, 'eblanc'),
    (9, 'clopez'),
    (10, 'jlaurent'),
    (10, 'rleroy'),
    (10, 'hgarcia'),
    (10, 'zmuller'),
    (10, 'efaure');

INSERT into
    PLANIFIER (idPlateforme, idCampagne)
VALUES
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
    (1, 6),
    (3, 6),
    (2, 7),
    (4, 7),
    (6, 7),
    (5, 8),
    (7, 8),
    (8, 9),
    (9, 9),
    (10, 9),
    (1, 10),
    (2, 10),
    (3, 10);

INSERT into
    SEJOURNER (idCampagne, idLieu)
VALUES
    (1, 1),
    (1, 2),
    (2, 3),
    (2, 4),
    (3, 5),
    (3, 6),
    (3, 7),
    (4, 8),
    (5, 9),
    (5, 10),
    (6, 11),
    (6, 12),
    (7, 13),
    (7, 14),
    (7, 15),
    (8, 1),
    (8, 5),
    (9, 2),
    (9, 6),
    (9, 10),
    (10, 3),
    (10, 7),
    (10, 11);

INSERT into
    ECHANTILLON (seqNucleotides, commentairesEchantillon)
VALUES
    (
        'ATCGATCGATCGATCG',
        'Échantillon de dinosaure théropode'
    ),
    (
        'GCTAGCTAGCTAGCTA',
        'Fragment d\'ADN de tricératops'
    ),
    ('TTAATTAATTAATTAA', 'Séquence de ptérosaure'),
    (
        'CCGGCCGGCCGGCCGG',
        'ADN de stégosaure bien conservé'
    ),
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

INSERT into
    ESPECE (nomEspece, caracteristiques)
VALUES
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

INSERT into
    APPARTENIR (idEspece, idEchantillon)
VALUES
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

INSERT into
    RAPPORTER (idEchant, idCampagne)
VALUES
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

INSERT into
    BUDGET_MENSUEL (annee, mois, budget)
VALUES
    (2024, 1, 15000.00),
    (2024, 2, 12500.50),
    (2024, 3, 18750.25),
    (2024, 4, 16200.00),
    (2024, 5, 14800.75),
    (2024, 6, 17500.00),
    (2024, 7, 20000.50),
    (2024, 8, 19250.25),
    (2024, 9, 16800.00),
    (2024, 10, 21500.75),
    (2024, 11, 18900.00),
    (2024, 12, 22000.25),
    (2025, 1, 16500.00),
    (2025, 2, 14750.50),
    (2025, 3, 19500.75),
    (2025, 4, 17800.00),
    (2025, 5, 15600.25),
    (2025, 6, 18200.50),
    (2025, 7, 21800.75),
    (2025, 8, 20500.00),
    (2025, 9, 17900.25),
    (2025, 10, 23000.50);



INSERT into
    MATERIEL (nom, description)
VALUES
    (
        'Microscope électronique',
        'Microscope haute résolution pour analyse cellulaire'
    ),
    (
        'Centrifugeuse',
        'Équipement de séparation par force centrifuge'
    ),
    (
        'Séquenceur ADN',
        'Appareil de séquençage génétique automatisé'
    ),
    (
        'Spectromètre de masse',
        'Analyse de composition moléculaire'
    ),
    (
        'PCR Thermocycleur',
        'Amplification de séquences d''ADN'
    ),
    (
        'Électrophorèse',
        'Séparation de molécules par migration électrique'
    ),
    (
        'Autoclave',
        'Stérilisation haute pression et température'
    ),
    (
        'Hotte chimique',
        'Protection contre les vapeurs toxiques'
    ),
    (
        'Balance analytique',
        'Pesée de précision micrométrique'
    ),
    ('pH-mètre', 'Mesure du pH des solutions'),
    ('Incubateur', 'Contrôle température et humidité'),
    (
        'Agitateur magnétique',
        'Mélange homogène des solutions'
    ),
    (
        'Pipette automatique',
        'Prélèvement précis de volumes'
    ),
    (
        'Congélateur -80°C',
        'Conservation échantillons biologiques'
    ),
    (
        'Chromatographe',
        'Séparation et analyse de composés'
    );

INSERT into
    UTILISER (idMateriel, idPlateforme, quantite)
VALUES
    (1, 1, 2),
    (2, 1, 1),
    (3, 1, 1),
    (4, 2, 1),
    (5, 2, 2),
    (6, 2, 1),
    (7, 3, 1),
    (8, 3, 2),
    (9, 3, 3),
    (10, 4, 2),
    (11, 4, 1),
    (12, 4, 2),
    (13, 5, 4),
    (14, 5, 1),
    (15, 5, 1),
    (1, 6, 1),
    (5, 6, 1),
    (9, 6, 2),
    (2, 7, 1),
    (6, 7, 1),
    (10, 7, 1),
    (3, 8, 1),
    (7, 8, 1),
    (11, 8, 1),
    (4, 9, 1),
    (8, 9, 1),
    (12, 9, 2),
    (13, 10, 2),
    (14, 10, 1),
    (15, 10, 1);

INSERT into
    NECESSITER (idMateriel, idHabilitation)
VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (3, 3),
    (4, 1),
    (4, 2),
    (5, 1),
    (5, 3),
    (6, 1),
    (6, 2),
    (7, 1),
    (8, 2),
    (9, 1),
    (10, 2),
    (11, 1),
    (11, 3),
    (12, 1),
    (12, 2),
    (13, 3),
    (14, 1),
    (14, 3),
    (15, 1),
    (15, 4);

INSERT IGNORE into
    MAINTENANCE (idPlateforme, dateMaintenance, duree_maintenance, statut)
VALUES
    -- Maintenances pour Plateforme Alpha (intervalle 30 jours) - avant les campagnes
    (1, '2024-01-01', 2, 'TERMINEE'),
    (1, '2025-01-01', 2, 'TERMINEE'),
    -- Maintenances pour Plateforme Beta (intervalle 45 jours)
    (2, '2023-12-20', 1, 'TERMINEE'),
    (2, '2024-12-20', 1, 'TERMINEE'),
    -- Maintenances pour Plateforme Gamma (intervalle 21 jours)
    (3, '2024-01-01', 3, 'TERMINEE'),
    (3, '2024-12-01', 3, 'TERMINEE'),
    -- Maintenances pour Plateforme Delta (intervalle 60 jours)
    (4, '2023-11-20', 2, 'TERMINEE'),
    (4, '2024-11-20', 2, 'TERMINEE'),
    -- Maintenances pour Plateforme Epsilon (intervalle 28 jours)
    (5, '2024-01-01', 1, 'TERMINEE'),
    (5, '2024-12-01', 1, 'TERMINEE'),
    -- Maintenances pour Plateforme Zeta (intervalle 35 jours)
    (6, '2023-12-25', 2, 'TERMINEE'),
    (6, '2024-12-25', 2, 'TERMINEE'),
    -- Maintenances pour Plateforme Eta (intervalle 90 jours)
    (7, '2023-10-01', 4, 'TERMINEE'),
    (7, '2024-10-01', 4, 'TERMINEE'),
    -- Maintenances pour Plateforme Theta (intervalle 14 jours)
    (8, '2024-01-01', 1, 'TERMINEE'),
    (8, '2024-12-20', 1, 'TERMINEE'),
    -- Maintenances pour Plateforme Iota (intervalle 42 jours)
    (9, '2024-01-01', 2, 'TERMINEE'),
    (9, '2024-12-10', 2, 'TERMINEE'),
    -- Maintenances pour Plateforme Kappa (intervalle 56 jours)
    (10, '2023-12-01', 2, 'TERMINEE'),
    (10, '2024-12-01', 2, 'TERMINEE');