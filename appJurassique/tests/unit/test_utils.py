from appJurassique.app import db
from appJurassique.models import (PERSONNE, LIEU_FOUILLE, PLATEFORME, MATERIEL,
                                  HABILITATION, BUDGET_MENSUEL, MAINTENANCE,
                                  CAMPAGNE, HABILITER, UTILISER, PARTICIPER,
                                  PLANIFIER, SEJOURNER, NECESSITER,
                                  role_labo_enum, statut)
from appJurassique.utils import (
    calculer_date_fin, periodes_se_chevauchent,
    verifier_chevauchement_campagne, verifier_chevauchement_maintenance,
    verifier_nombre_membres, creer_campagne, verifier_disponibilite_plateforme,
    verifier_disponibilite_membres, verifier_habilitations_membres,
    verifier_maintenance_plateforme, obtenir_membres_compatibles,
    obtenir_plateformes_disponibles, recuperer_budget_mensuel,
    estimer_cout_campagne, update_qte)
from hashlib import sha256
from datetime import date, timedelta


def create_test_user():
    """Crée un utilisateur de test."""
    m = sha256()
    m.update("testpass".encode())
    user = PERSONNE(username="testuser",
                    nom="Test",
                    prenom="User",
                    password=m.hexdigest(),
                    role_labo=role_labo_enum.CHERCHEUR)
    db.session.add(user)
    db.session.commit()
    return user


def create_default_habilitations():
    """Crée les habilitations par défaut."""
    habs = [
        HABILITATION(idHabilitation=1,
                     nom_habilitation="Électrique",
                     description="electrique"),
        HABILITATION(idHabilitation=2,
                     nom_habilitation="Chimique",
                     description="chimique"),
        HABILITATION(idHabilitation=3,
                     nom_habilitation="Biologique",
                     description="biologique"),
        HABILITATION(idHabilitation=4,
                     nom_habilitation="Radiations",
                     description="radiations"),
    ]
    for h in habs:
        db.session.add(h)
    db.session.commit()
    return habs


# ==================== calculer_date_fin ====================


def test_calculer_date_fin_normal():
    date_debut = date(2025, 6, 1)
    result = calculer_date_fin(date_debut, 10)
    assert result == date(2025, 6, 10)


def test_calculer_date_fin_one_day():
    date_debut = date(2025, 6, 1)
    result = calculer_date_fin(date_debut, 1)
    assert result == date(2025, 6, 1)


def test_calculer_date_fin_none_date():
    result = calculer_date_fin(None, 10)
    assert result is None


def test_calculer_date_fin_zero_duree():
    date_debut = date(2025, 6, 1)
    result = calculer_date_fin(date_debut, 0)
    assert result == date(2025, 6, 1)  # min 1 jour


def test_calculer_date_fin_negative_duree():
    date_debut = date(2025, 6, 1)
    result = calculer_date_fin(date_debut, -5)
    assert result == date(2025, 6, 1)  # min 1 jour


# ==================== periodes_se_chevauchent ====================


def test_periodes_se_chevauchent_overlap():
    # Période A: 1-10, Période B: 5-15 -> chevauchement
    assert periodes_se_chevauchent(date(2025, 6, 1), date(2025, 6, 10),
                                   date(2025, 6, 5), date(2025, 6, 15)) is True


def test_periodes_se_chevauchent_no_overlap_before():
    # Période A: 1-5, Période B: 10-15 -> pas de chevauchement
    assert periodes_se_chevauchent(date(2025, 6, 1), date(2025, 6, 5),
                                   date(2025, 6, 10), date(2025, 6,
                                                           15)) is False


def test_periodes_se_chevauchent_no_overlap_after():
    # Période A: 10-15, Période B: 1-5 -> pas de chevauchement
    assert periodes_se_chevauchent(date(2025, 6, 10), date(2025, 6, 15),
                                   date(2025, 6, 1), date(2025, 6, 5)) is False


def test_periodes_se_chevauchent_adjacent():
    # Période A: 1-5, Période B: 6-10 -> pas de chevauchement (adjacent)
    assert periodes_se_chevauchent(date(2025, 6, 1), date(2025, 6, 5),
                                   date(2025, 6, 6), date(2025, 6,
                                                          10)) is False


def test_periodes_se_chevauchent_same_day():
    # Période A: 5-5, Période B: 5-5 -> chevauchement
    assert periodes_se_chevauchent(date(2025, 6, 5), date(2025, 6, 5),
                                   date(2025, 6, 5), date(2025, 6, 5)) is True


def test_periodes_se_chevauchent_contained():
    # Période A: 1-20, Période B: 5-10 -> chevauchement (B dans A)
    assert periodes_se_chevauchent(date(2025, 6, 1), date(2025, 6, 20),
                                   date(2025, 6, 5), date(2025, 6, 10)) is True


# ==================== verifier_chevauchement_campagne ====================


def test_verifier_chevauchement_campagne_no_campagne(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()
        result = verifier_chevauchement_campagne(plateforme.idPlateforme,
                                                 date(2025, 6, 1), 10)
        assert result is None


def test_verifier_chevauchement_campagne_with_conflict(testapp):
    with testapp.app_context():
        lieu = LIEU_FOUILLE(nomLieu="Lieu Test")
        db.session.add(lieu)
        db.session.commit()

        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        campagne = CAMPAGNE(dateDebut=date(2025, 6, 5),
                            duree=10,
                            idLieu=lieu.idLieu)
        db.session.add(campagne)
        db.session.commit()

        planifier = PLANIFIER(idPlateforme=plateforme.idPlateforme,
                              idCampagne=campagne.idCampagne)
        db.session.add(planifier)
        db.session.commit()

        result = verifier_chevauchement_campagne(plateforme.idPlateforme,
                                                 date(2025, 6, 1), 10)
        assert result is not None
        assert "Conflit" in result


def test_verifier_chevauchement_campagne_no_conflict(testapp):
    with testapp.app_context():
        lieu = LIEU_FOUILLE(nomLieu="Lieu Test")
        db.session.add(lieu)
        db.session.commit()

        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        campagne = CAMPAGNE(dateDebut=date(2025, 6, 20),
                            duree=10,
                            idLieu=lieu.idLieu)
        db.session.add(campagne)
        db.session.commit()

        planifier = PLANIFIER(idPlateforme=plateforme.idPlateforme,
                              idCampagne=campagne.idCampagne)
        db.session.add(planifier)
        db.session.commit()

        result = verifier_chevauchement_campagne(plateforme.idPlateforme,
                                                 date(2025, 6, 1), 5)
        assert result is None


# ==================== verifier_chevauchement_maintenance ====================


def test_verifier_chevauchement_maintenance_no_maintenance(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()
        result = verifier_chevauchement_maintenance(plateforme.idPlateforme,
                                                    date(2025, 6, 1), 10)
        assert result is None


def test_verifier_chevauchement_maintenance_with_conflict(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        maintenance = MAINTENANCE(dateMaintenance=date(2025, 6, 5),
                                  duree_maintenance=10,
                                  statut=statut.PLANIFIEE,
                                  idPlateforme=plateforme.idPlateforme)
        db.session.add(maintenance)
        db.session.commit()

        result = verifier_chevauchement_maintenance(plateforme.idPlateforme,
                                                    date(2025, 6, 1), 10)
        assert result is not None
        assert "Conflit" in result


def test_verifier_chevauchement_maintenance_no_conflict(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        maintenance = MAINTENANCE(dateMaintenance=date(2025, 6, 20),
                                  duree_maintenance=5,
                                  statut=statut.PLANIFIEE,
                                  idPlateforme=plateforme.idPlateforme)
        db.session.add(maintenance)
        db.session.commit()

        result = verifier_chevauchement_maintenance(plateforme.idPlateforme,
                                                    date(2025, 6, 1), 5)
        assert result is None


# ==================== verifier_nombre_membres ====================


def test_verifier_nombre_membres_enough(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=2,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        membres = [create_test_user()]
        m = sha256()
        m.update("pass2".encode())
        user2 = PERSONNE(username="user2",
                         nom="User2",
                         prenom="Test",
                         password=m.hexdigest(),
                         role_labo=role_labo_enum.CHERCHEUR)
        db.session.add(user2)
        db.session.commit()
        membres.append(user2)

        ok, error = verifier_nombre_membres(plateforme, membres)
        assert ok is True
        assert error is None


def test_verifier_nombre_membres_not_enough(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=3,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        membres = [create_test_user()]

        ok, error = verifier_nombre_membres(plateforme, membres)
        assert ok is False
        assert error is not None
        assert "minimum" in error


def test_verifier_nombre_membres_no_minimum(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=None,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        membres = [create_test_user()]

        ok, error = verifier_nombre_membres(plateforme, membres)
        assert ok is True
        assert error is None


# ==================== creer_campagne ====================


def test_creer_campagne_success(testapp):
    with testapp.app_context():
        user = create_test_user()
        lieu = LIEU_FOUILLE(nomLieu="Lieu Test")
        db.session.add(lieu)
        db.session.commit()

        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        campagne, error = creer_campagne(
            date_debut=date(2025, 6, 1),
            duree_jours=10,
            id_lieu=lieu.idLieu,
            id_plateforme=plateforme.idPlateforme,
            noms_utilisateurs_membres=[user.username])

        assert campagne is not None
        assert error is None
        assert campagne.duree == 10


def test_creer_campagne_plateforme_not_found(testapp):
    with testapp.app_context():
        user = create_test_user()
        lieu = LIEU_FOUILLE(nomLieu="Lieu Test")
        db.session.add(lieu)
        db.session.commit()

        campagne, error = creer_campagne(
            date_debut=date(2025, 6, 1),
            duree_jours=10,
            id_lieu=lieu.idLieu,
            id_plateforme=9999,
            noms_utilisateurs_membres=[user.username])

        assert campagne is None
        assert error is not None
        assert "introuvable" in error


def test_creer_campagne_membre_not_found(testapp):
    with testapp.app_context():
        lieu = LIEU_FOUILLE(nomLieu="Lieu Test")
        db.session.add(lieu)
        db.session.commit()

        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        campagne, error = creer_campagne(
            date_debut=date(2025, 6, 1),
            duree_jours=10,
            id_lieu=lieu.idLieu,
            id_plateforme=plateforme.idPlateforme,
            noms_utilisateurs_membres=["nonexistent"])

        assert campagne is None
        assert error is not None
        assert "trouvés" in error


def test_creer_campagne_not_enough_members(testapp):
    with testapp.app_context():
        user = create_test_user()
        lieu = LIEU_FOUILLE(nomLieu="Lieu Test")
        db.session.add(lieu)
        db.session.commit()

        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=5,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        campagne, error = creer_campagne(
            date_debut=date(2025, 6, 1),
            duree_jours=10,
            id_lieu=lieu.idLieu,
            id_plateforme=plateforme.idPlateforme,
            noms_utilisateurs_membres=[user.username])

        assert campagne is None
        assert error is not None
        assert "minimum" in error


# ==================== verifier_disponibilite_plateforme ====================


def test_verifier_disponibilite_plateforme(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        ok, error = verifier_disponibilite_plateforme(plateforme.idPlateforme,
                                                      date(2025, 6, 1),
                                                      date(2025, 6, 10))
        assert ok is True
        assert error is None


# ==================== verifier_disponibilite_membres ====================


def test_verifier_disponibilite_membres(testapp):
    with testapp.app_context():
        user = create_test_user()

        ok, error = verifier_disponibilite_membres([user], date(2025, 6, 1),
                                                   date(2025, 6, 10))
        assert ok is True
        assert error is None


# ==================== verifier_habilitations_membres ====================


def test_verifier_habilitations_membres(testapp):
    with testapp.app_context():
        user = create_test_user()
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        ok, error = verifier_habilitations_membres(plateforme.idPlateforme,
                                                   [user])
        assert ok is True
        assert error is None


# ==================== verifier_maintenance_plateforme ====================


def test_verifier_maintenance_plateforme(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        ok, error = verifier_maintenance_plateforme(plateforme,
                                                    date(2025, 6, 1),
                                                    date(2025, 6, 10))
        assert ok is True
        assert error is None


# ==================== obtenir_membres_compatibles ====================


def test_obtenir_membres_compatibles_no_plateforme(testapp):
    with testapp.app_context():
        result = obtenir_membres_compatibles(9999)
        assert result == []


def test_obtenir_membres_compatibles_no_materiels(testapp):
    with testapp.app_context():
        user = create_test_user()
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        result = obtenir_membres_compatibles(plateforme.idPlateforme)
        assert len(result) > 0
        assert result[0][0].username == user.username


def test_obtenir_membres_compatibles_with_habilitations(testapp):
    with testapp.app_context():
        create_default_habilitations()
        user = create_test_user()

        habiliter = HABILITER(username=user.username, idHabilitation=1)
        db.session.add(habiliter)
        db.session.commit()

        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        materiel = MATERIEL(nom="Test Mat", description="Test")
        db.session.add(materiel)
        db.session.commit()

        utiliser = UTILISER(idMateriel=materiel.idMateriel,
                            idPlateforme=plateforme.idPlateforme,
                            quantite=1)
        db.session.add(utiliser)
        db.session.commit()

        necessiter = NECESSITER(idHabilitation=1,
                                idMateriel=materiel.idMateriel)
        db.session.add(necessiter)
        db.session.commit()

        result = obtenir_membres_compatibles(plateforme.idPlateforme)
        assert len(result) > 0


def test_obtenir_membres_compatibles_with_dates(testapp):
    with testapp.app_context():
        user = create_test_user()
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        result = obtenir_membres_compatibles(plateforme.idPlateforme,
                                             date_debut=date(2025, 6, 1),
                                             date_fin=date(2025, 6, 10))
        assert len(result) > 0


# ==================== obtenir_plateformes_disponibles ====================


def test_obtenir_plateformes_disponibles_no_date():
    result = obtenir_plateformes_disponibles(None, 10)
    assert result == []


def test_obtenir_plateformes_disponibles_no_duree():
    result = obtenir_plateformes_disponibles(date(2025, 6, 1), None)
    assert result == []


def test_obtenir_plateformes_disponibles_success(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        result = obtenir_plateformes_disponibles(date(2025, 6, 1), 10)
        assert plateforme.idPlateforme in result


# ==================== recuperer_budget_mensuel ====================


def test_recuperer_budget_mensuel_none():
    result = recuperer_budget_mensuel(None)
    assert result is None


def test_recuperer_budget_mensuel_not_found(testapp):
    with testapp.app_context():
        result = recuperer_budget_mensuel(date(2099, 12, 1))
        assert result is None


def test_recuperer_budget_mensuel_found(testapp):
    with testapp.app_context():
        budget = BUDGET_MENSUEL(annee=2025, mois=6, budget=5000.0)
        db.session.add(budget)
        db.session.commit()

        result = recuperer_budget_mensuel(date(2025, 6, 15))
        assert result is not None
        assert result.budget == 5000.0


# ==================== estimer_cout_campagne ====================


def test_estimer_cout_campagne_none_plateforme():
    result = estimer_cout_campagne(None, 10)
    assert result is None


def test_estimer_cout_campagne_no_cout(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=None,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        result = estimer_cout_campagne(plateforme, 10)
        assert result is None


def test_estimer_cout_campagne_success(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100.0,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        result = estimer_cout_campagne(plateforme, 10)
        assert result == 1000.0


def test_estimer_cout_campagne_zero_duree(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100.0,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        result = estimer_cout_campagne(plateforme, 0)
        assert result == 100.0  # min 1 jour


# ==================== update_qte ====================


def test_update_qte_new_utilisation(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        materiel = MATERIEL(nom="Test Mat", description="Test")
        db.session.add(materiel)
        db.session.commit()

        result = update_qte(5, materiel.idMateriel, plateforme.idPlateforme)
        assert result is True

        utilisation = UTILISER.query.filter_by(
            idMateriel=materiel.idMateriel,
            idPlateforme=plateforme.idPlateforme).first()
        assert utilisation is not None
        assert utilisation.quantite == 5


def test_update_qte_existing_utilisation(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        materiel = MATERIEL(nom="Test Mat", description="Test")
        db.session.add(materiel)
        db.session.commit()

        utiliser = UTILISER(idMateriel=materiel.idMateriel,
                            idPlateforme=plateforme.idPlateforme,
                            quantite=10)
        db.session.add(utiliser)
        db.session.commit()

        result = update_qte(5, materiel.idMateriel, plateforme.idPlateforme)
        assert result is True

        utilisation = UTILISER.query.filter_by(
            idMateriel=materiel.idMateriel,
            idPlateforme=plateforme.idPlateforme).first()
        assert utilisation.quantite == 15


def test_update_qte_negative_result(testapp):
    with testapp.app_context():
        plateforme = PLATEFORME(nom="Test Plat",
                                cout_journalier=100,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()

        materiel = MATERIEL(nom="Test Mat", description="Test")
        db.session.add(materiel)
        db.session.commit()

        utiliser = UTILISER(idMateriel=materiel.idMateriel,
                            idPlateforme=plateforme.idPlateforme,
                            quantite=5)
        db.session.add(utiliser)
        db.session.commit()

        result = update_qte(-10, materiel.idMateriel, plateforme.idPlateforme)
        assert result is False
