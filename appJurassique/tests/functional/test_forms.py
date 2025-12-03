from appJurassique.app import db
from appJurassique.models import (PERSONNE, LIEU_FOUILLE, PLATEFORME, MATERIEL,
                                  HABILITATION, BUDGET_MENSUEL, MAINTENANCE,
                                  CAMPAGNE, HABILITER, UTILISER,
                                  role_labo_enum, statut)
from hashlib import sha256
from datetime import date


def login(client, username, password, next_url="/"):
    """Helper pour se connecter."""
    m = sha256()
    m.update(password.encode())
    return client.post("/login/",
                       data={
                           "username": username,
                           "password": password,
                           "next": next_url
                       },
                       follow_redirects=True)


def create_test_user(db):
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


def create_default_habilitations(db):
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


# ==================== LOGIN FORM ====================


def test_login_form_success(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    response = login(client, "testuser", "testpass", "/")
    assert response.status_code == 200


def test_login_form_invalid_user(client, testapp):
    with testapp.app_context():
        pass
    response = login(client, "invalid", "password", "/login/")
    assert response.status_code == 200
    assert b"Identifiant" in response.data


def test_login_form_wrong_password(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    response = login(client, "testuser", "wrongpass", "/login/")
    assert response.status_code == 200


# ==================== REGISTER FORM ====================


def test_register_form_success(client, testapp):
    with testapp.app_context():
        pass
    response = client.post("/register/",
                           data={
                               "username": "newuser",
                               "prenom": "New",
                               "nom": "User",
                               "role_labo": "CHERCHEUR",
                               "password": "newpassword",
                               "confirm_password": "newpassword"
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        user = PERSONNE.query.get("newuser")
        assert user is not None
        assert user.prenom == "New"
        assert user.nom == "User"


def test_register_form_duplicate_username(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    response = client.post("/register/",
                           data={
                               "username": "testuser",
                               "prenom": "Another",
                               "nom": "User",
                               "role_labo": "CHERCHEUR",
                               "password": "password",
                               "confirm_password": "password"
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    assert "utilisé" in response.data.decode('utf-8')


def test_register_form_password_mismatch(client, testapp):
    with testapp.app_context():
        pass
    response = client.post("/register/",
                           data={
                               "username": "newuser",
                               "prenom": "New",
                               "nom": "User",
                               "role_labo": "CHERCHEUR",
                               "password": "password1",
                               "confirm_password": "password2"
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    assert "correspondre" in response.data.decode('utf-8')


# ==================== BUDGET FORM ====================


def test_budget_form_success(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.post("/dashboard/set_budget/",
                           data={
                               "date": "2025-12",
                               "budget_mensuel": "5000.00"
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        budget = BUDGET_MENSUEL.query.filter_by(annee=2025, mois=12).first()
        assert budget is not None
        assert float(budget.budget) == 5000.00


# ==================== LIEU FORM ====================


def test_lieu_form_success(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.post("/lieux/ajouter/",
                           data={"nomLieu": "Site de Fouille Alpha"},
                           follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        lieu = LIEU_FOUILLE.query.filter_by(
            nomLieu="Site de Fouille Alpha").first()
        assert lieu is not None


def test_lieu_supprimer(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        lieu = LIEU_FOUILLE(nomLieu="Lieu Test")
        db.session.add(lieu)
        db.session.commit()
        id_lieu = lieu.idLieu
    login(client, "testuser", "testpass")
    response = client.get(f"/lieux/{id_lieu}/supprimer/",
                          follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        lieu = LIEU_FOUILLE.query.get(id_lieu)
        assert lieu is None


# ==================== PLATEFORME FORM ====================


def test_plateforme_form_access(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.get("/add_plateforme/", follow_redirects=True)
    assert response.status_code == 200


def test_plateforme_form_duplicate(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        plateforme = PLATEFORME(nom="Labo Existant",
                                cout_journalier=50,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()
    login(client, "testuser", "testpass")
    response = client.post("/add_plateforme/",
                           data={
                               "nom_plateforme": "Labo Existant",
                               "cout_journalier": "100",
                               "minimum_personnes": "2",
                               "intervalle_maintenance": "30"
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    assert "existe" in response.data.decode('utf-8')


def test_plateforme_supprimer(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        plateforme = PLATEFORME(nom="Plateforme Test",
                                cout_journalier=50,
                                min_nb_personne=1,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()
        id_plat = plateforme.idPlateforme
    login(client, "testuser", "testpass")
    response = client.get(f"/plateformes/{id_plat}/supprimer/",
                          follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        plateforme = PLATEFORME.query.get(id_plat)
        assert plateforme is None


# ==================== PERSONNE FORM ====================


def test_personne_form_success(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        create_default_habilitations(db)
    login(client, "testuser", "testpass")
    response = client.post("/add_personne/",
                           data={
                               "nom": "Dupont",
                               "prenom": "Jean",
                               "username": "jdupont",
                               "password": "securepass",
                               "role_labo": "CHERCHEUR",
                               "habilitations": ["electrique", "chimique"]
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        personne = PERSONNE.query.get("jdupont")
        assert personne is not None
        assert personne.nom == "Dupont"


def test_personne_form_duplicate(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        create_default_habilitations(db)
    login(client, "testuser", "testpass")
    response = client.post("/add_personne/",
                           data={
                               "nom": "Test",
                               "prenom": "User",
                               "username": "testuser",
                               "password": "anotherpass",
                               "role_labo": "CHERCHEUR",
                               "habilitations": ["electrique"]
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    assert "utilisé" in response.data.decode('utf-8')


def test_personne_supprimer(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        m = sha256()
        m.update("pass".encode())
        personne = PERSONNE(username="todelete",
                            nom="Delete",
                            prenom="Me",
                            password=m.hexdigest(),
                            role_labo=role_labo_enum.TECHNICIEN)
        db.session.add(personne)
        db.session.commit()
    login(client, "testuser", "testpass")
    response = client.get("/personnels/todelete/supprimer/",
                          follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        personne = PERSONNE.query.get("todelete")
        assert personne is None


# ==================== MAINTENANCE FORM ====================


def test_maintenance_form_success(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        plateforme = PLATEFORME(nom="Labo Maintenance",
                                cout_journalier=100,
                                min_nb_personne=2,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()
        id_plat = plateforme.idPlateforme
    login(client, "testuser", "testpass")
    future_date = date(2026, 6, 1)
    response = client.post("/maintenance/",
                           data={
                               "dateDebut": future_date.strftime("%Y-%m-%d"),
                               "duree": "5",
                               "idPlateforme": str(id_plat)
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        maintenance = MAINTENANCE.query.filter_by(idPlateforme=id_plat).first()
        assert maintenance is not None
        assert maintenance.duree_maintenance == 5


def test_maintenance_form_past_date(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        plateforme = PLATEFORME(nom="Labo Test",
                                cout_journalier=100,
                                min_nb_personne=2,
                                intervalle_maintenance=30)
        db.session.add(plateforme)
        db.session.commit()
        id_plat = plateforme.idPlateforme
    login(client, "testuser", "testpass")
    past_date = date(2020, 1, 1)
    response = client.post("/maintenance/",
                           data={
                               "dateDebut": past_date.strftime("%Y-%m-%d"),
                               "duree": "5",
                               "idPlateforme": str(id_plat)
                           },
                           follow_redirects=True)
    assert response.status_code == 200
    assert "passé" in response.data.decode('utf-8')


# ==================== MATERIEL FORM ====================


def test_materiel_supprimer(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        materiel = MATERIEL(nom="Materiel Test", description="Test")
        db.session.add(materiel)
        db.session.commit()
        id_mat = materiel.idMateriel
    login(client, "testuser", "testpass")
    response = client.get(f"/materiels/{id_mat}/supprimer/",
                          follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        materiel = MATERIEL.query.get(id_mat)
        assert materiel is None


# ==================== CAMPAGNE FORM ====================


def test_campagne_form_access(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.get("/add_campagne/")
    assert response.status_code == 200


def test_campagne_supprimer(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        lieu = LIEU_FOUILLE(nomLieu="Lieu Camp")
        db.session.add(lieu)
        db.session.commit()
        campagne = CAMPAGNE(dateDebut=date(2025, 6, 1),
                            duree=30,
                            idLieu=lieu.idLieu)
        db.session.add(campagne)
        db.session.commit()
        id_camp = campagne.idCampagne
    login(client, "testuser", "testpass")
    response = client.get(f"/campagnes/{id_camp}/supprimer/",
                          follow_redirects=True)
    assert response.status_code == 200
    with testapp.app_context():
        campagne = CAMPAGNE.query.get(id_camp)
        assert campagne is None


def test_campagne_view(client, testapp):
    with testapp.app_context():
        create_test_user(db)
        lieu = LIEU_FOUILLE(nomLieu="Lieu View")
        db.session.add(lieu)
        db.session.commit()
        campagne = CAMPAGNE(dateDebut=date(2025, 6, 1),
                            duree=30,
                            idLieu=lieu.idLieu)
        db.session.add(campagne)
        db.session.commit()
        id_camp = campagne.idCampagne
    login(client, "testuser", "testpass")
    response = client.get(f"/campagnes/{id_camp}/view/")
    assert response.status_code == 200


def test_campagne_view_not_found(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.get("/campagnes/9999/view/")
    assert response.status_code == 404


# ==================== LISTES ====================


def test_liste_campagnes(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.get("/campagnes/")
    assert response.status_code == 200


def test_liste_plateformes(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.get("/plateformes/")
    assert response.status_code == 200


def test_liste_materiels(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.get("/materiels/")
    assert response.status_code == 200


def test_liste_lieux(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.get("/lieux/")
    assert response.status_code == 200


def test_liste_personnels(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.get("/personnels/")
    assert response.status_code == 200


# ==================== LOGOUT ====================


def test_logout(client, testapp):
    with testapp.app_context():
        create_test_user(db)
    login(client, "testuser", "testpass")
    response = client.get("/logout/", follow_redirects=True)
    assert response.status_code == 200
