-- Insertion pour la BDD générer a l'aide de l'IA
INSERT into PERSONNE (nom, prenom) VALUES 
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

INSERT into PLATEFORME (nom, min_nb_personne, cout_journalier, intervalle_maintenance) VALUES 
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

INSERT into LIEU (nomLieu) VALUES 
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

INSERT into HABILITATION (nom_habilitation, description_hab) VALUES 
('électrique', 'Habilitation électrique'),
('chimique', 'Habilitation chimique'),
('biologique', 'Habilitation biologique'),
('radiations', 'Habilitation radiations');

INSERT into DETENIR (idHabilitation, idPlateforme) VALUES 
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

INSERT into HABILITER (idPersonne, idHabilitation) VALUES 
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

INSERT into CAMPAGNE (date_debut, duree) VALUES 
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

INSERT into PARTICIPER (idCampagne, idPersonne) VALUES 
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

INSERT into PLANIFIER (idPlateforme, idCampagne) VALUES 
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

INSERT into SEJOURNER (idCampagne, idLieu) VALUES 
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

INSERT into ECHANTILLON (seq_nucleotides, commentaires_echant) VALUES 
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

INSERT into ESPECE (nom_espece, caracteristiques_esp) VALUES 
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

INSERT into APPARTENIR (idEspece, idEchant) VALUES 
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

INSERT into RAPPORTER (idEchant, idCampagne) VALUES 
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