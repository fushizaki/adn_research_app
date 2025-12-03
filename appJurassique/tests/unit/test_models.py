from appJurassique.models import (MATERIEL, PLATEFORME, HABILITATION,
                                  BUDGET_MENSUEL, LIEU_FOUILLE, PERSONNE,
                                  CAMPAGNE, PARTICIPER, PLANIFIER, SEJOURNER,
                                  ECHANTILLON, ESPECE, APPARTENIR, HABILITER,
                                  RAPPORTER, UTILISER, NECESSITER, MAINTENANCE,
                                  HISTORIQUE, role_labo_enum, statut)
from datetime import date, datetime


def test_materiel_repr():
    mat = MATERIEL(nom="Pelle", description="Une pelle")
    assert repr(mat) == "<MATERIEL Pelle>"


def test_plateforme_repr():
    plat = PLATEFORME(nom="Labo A", min_nb_personne=2, cout_journalier=100.0)
    assert repr(plat) == "<PLATEFORME Labo A>"


def test_habilitation_repr():
    hab = HABILITATION(nom_habilitation="Chimique",
                       description="Habilitation chimique")
    assert repr(hab) == "<HABILITATION Chimique>"


def test_budget_mensuel_repr():
    budget = BUDGET_MENSUEL(annee=2025, mois=12, budget=5000.0)
    assert repr(budget) == "<BUDGET_MENSUEL 2025-12 5000.0>"


def test_lieu_fouille_repr():
    lieu = LIEU_FOUILLE(nomLieu="Site A")
    assert repr(lieu) == "<LIEU_FOUILLE Site A>"


def test_role_labo_enum_get_roles():
    roles = role_labo_enum.get_roles()
    assert "DIRECTION" in roles
    assert "TECHNICIEN" in roles
    assert "ADMINISTRATION" in roles
    assert "CHERCHEUR" in roles


def test_personne_get_id():
    personne = PERSONNE(username="jdoe",
                        nom="Doe",
                        prenom="John",
                        password="hashedpwd",
                        role_labo=role_labo_enum.CHERCHEUR)
    assert personne.get_id() == "jdoe"


def test_personne_repr():
    personne = PERSONNE(username="jdoe",
                        nom="Doe",
                        prenom="John",
                        password="hashedpwd",
                        role_labo=role_labo_enum.CHERCHEUR)
    assert repr(personne) == "<PERSONNE John Doe>"


def test_personne_load_user(testapp):
    with testapp.app_context():
        from appJurassique.app import db
        personne = PERSONNE(username="testuser",
                            nom="Test",
                            prenom="User",
                            password="hashedpwd",
                            role_labo=role_labo_enum.CHERCHEUR)
        db.session.add(personne)
        db.session.commit()
        loaded = PERSONNE.load_user("testuser")
        assert loaded is not None
        assert loaded.username == "testuser"


def test_campagne_repr():
    campagne = CAMPAGNE(idCampagne=1,
                        dateDebut=date(2025, 6, 1),
                        duree=30,
                        idLieu=1)
    assert repr(campagne) == "<CAMPAGNE (1) 2025-06-01>"


def test_participer_repr():
    participer = PARTICIPER(username="jdoe", idCampagne=1)
    assert repr(participer) == "<PARTICIPER jdoe in 1>"


def test_planifier_repr():
    planifier = PLANIFIER(idPlateforme=1, idCampagne=2)
    assert repr(planifier) == "<PLANIFIER Plateforme 1 for Campagne 2>"


def test_sejourner_repr():
    sejourner = SEJOURNER(idCampagne=1, idLieu=2)
    assert repr(sejourner) == "<SEJOURNER Campagne 1 at Lieu 2>"


def test_echantillon_repr():
    echantillon = ECHANTILLON(idEchantillon=1, fichierAdn="test.adn")
    assert repr(echantillon) == "<ECHANTILLON 1>"


def test_espece_repr():
    espece = ESPECE(nomEspece="T-Rex", caracteristiques="Carnivore")
    assert repr(espece) == "<ESPECE T-Rex>"


def test_appartenir_repr():
    appartenir = APPARTENIR(idEchantillon=1, idEspece=2)
    assert repr(appartenir) == "<APPARTENIR Echantillon 1 to Espece 2>"


def test_habiliter_repr():
    habiliter = HABILITER(username="jdoe", idHabilitation=1)
    assert repr(habiliter) == "<HABILITER jdoe to Habilitation 1>"


def test_rapporter_repr():
    rapporter = RAPPORTER(idEchantillon=1, idCampagne=2)
    assert repr(rapporter) == "<RAPPORTER Echantillon 1 from Campagne 2>"


def test_utiliser_repr():
    utiliser = UTILISER(idMateriel=1, idPlateforme=2, quantite=5)
    assert repr(utiliser) == "<UTILISER Materiel 1 sur Plateforme 2>"


def test_necessiter_repr():
    necessiter = NECESSITER(idHabilitation=1, idMateriel=2)
    assert repr(necessiter) == "<NECESSITER Habilitation 1 for Materiel 2>"


def test_statut_enum():
    assert statut.PLANIFIEE.value == "PLANIFIEE"
    assert statut.EN_COURS.value == "EN_COURS"
    assert statut.TERMINEE.value == "TERMINEE"


def test_maintenance_repr():
    maintenance = MAINTENANCE(idMaintenance=1,
                              dateMaintenance=date(2025, 12, 1),
                              duree_maintenance=5,
                              statut=statut.PLANIFIEE)
    assert repr(maintenance) == "<MAINTENANCE 1 on 2025-12-01>"


def test_historique_repr():
    historique = HISTORIQUE(idHistorique=1,
                            nom_fichier_base="test.adn",
                            proba=0.5,
                            nb_remplacement=10,
                            nb_insertion=5,
                            nb_deletion=3,
                            note="Test note",
                            date_enregistrement=datetime(2025, 12, 1))
    assert repr(historique) == "<HISTORIQUE 1 test.adn>"
