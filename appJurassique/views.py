import algo
from zipfile import Path
from flask import flash, render_template, request, session, url_for, redirect, jsonify, current_app
from werkzeug.utils import secure_filename
from algo import constants
from algo.main import *
from pathlib import Path
from datetime import date, timedelta
from calendar import monthrange
from sqlalchemy.orm import joinedload
from .app import app, db
import algo
from flask_login import login_user, logout_user, login_required, current_user
from .utils import creer_campagne, obtenir_membres_compatibles
from sqlalchemy.exc import IntegrityError, DataError
from appJurassique.forms import *
from appJurassique.models import *
from appJurassique.utils import *

# ==================== ACCUEIL ====================


MONTH_NAMES_FR = [
    None,
    "Janvier",
    "Février",
    "Mars",
    "Avril",
    "Mai",
    "Juin",
    "Juillet",
    "Août",
    "Septembre",
    "Octobre",
    "Novembre",
    "Décembre",
]


@app.route('/')
@app.route('/index/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html', title='Accueil', current_page='index')

# ==================== AUTHENTIFICATION ====================


@app.route("/login/", methods=(
    "GET",
    "POST",
))
def login():
    unForm = LoginForm()
    unUser = None

    if not unForm.is_submitted():
        unForm.next.data = request.args.get('next')
    elif unForm.validate_on_submit():
        unUser = unForm.get_authenticated_user()

    if unUser:
        login_user(unUser)
        next = unForm.next.data or url_for("index", name=unUser.username)
        return redirect(next)
    return render_template("login.html", form=unForm)


@app.route("/register/", methods=("GET", "POST"))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()
    role_choices = [('', 'Sélectionner un rôle')
                    ] + [(role.value, role.value) for role in role_labo_enum]
    form.role_labo.choices = role_choices

    if not form.is_submitted():
        form.next.data = request.args.get('next')

    if form.validate_on_submit():
        if PERSONNE.query.get(form.username.data):
            form.username.errors.append("Cet identifiant est déjà utilisé.")
        else:
            user = form.build_user()
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                form.username.errors.append(
                    "Une erreur est survenue, merci de réessayer.")
            else:
                login_user(user)
                next_url = form.next.data or url_for("index",
                                                     name=user.username)
                return redirect(next_url)

    return render_template("register.html", form=form)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('index'))


# ==================== CAMPAGNES ====================


@app.route('/add_campagne/', methods=['GET', 'POST'])
@login_required
def add_campagne():
    """Crée une nouvelle campagne."""
    lieux = LIEU_FOUILLE.query.all()
    plateformes = PLATEFORME.query.all()

    form = CampagneForm()
    form.idLieu.choices = [('', 'Sélectionner un lieu')] + [
        (str(lieu.idLieu), lieu.nomLieu) for lieu in lieux
    ]
    form.idPlateforme.choices = [('', 'Sélectionner une plateforme')] + [
        (str(plateforme.idPlateforme), plateforme.nom)
        for plateforme in plateformes
    ]

    formdata = request.form if request.method == 'POST' else request.args
    if formdata:
        form.process(formdata=formdata)

    message = request.args.get('error') or request.args.get('success')
    message_type = 'error' if request.args.get('error') else (
        'success' if request.args.get('success') else None)

    plateforme_selectionnee = None
    membres_compatibles = []
    membres_selectionnes = []
    budget_mensuel = recuperer_budget_mensuel(form.dateDebut.data)
    budget_estime = None

    id_plateforme = form.idPlateforme.data or request.values.get(
        'idPlateforme')
    if id_plateforme is not None and id_plateforme != form.idPlateforme.data:
        form.idPlateforme.data = id_plateforme
    if id_plateforme:
        try:
            id_plateforme_int = int(id_plateforme)
            plateforme_selectionnee = PLATEFORME.query.get(id_plateforme_int)
            if plateforme_selectionnee:
                membres_compatibles = obtenir_membres_compatibles(
                    id_plateforme_int)
                form.membres.choices = [
                    (membre.username, f"{membre.nom} {membre.prenom}")
                    for membre, compatible in membres_compatibles
                ]
                if form.duree.data:
                    budget_estime = estimer_cout_campagne(
                        plateforme_selectionnee, form.duree.data)
                if form.membres.data:
                    membres_selectionnes = form.membres.data
        except ValueError:
            message = "Plateforme sélectionnée invalide."
            message_type = 'error'

    if request.method == 'POST':
        if request.form.get('action') == 'load_members':
            return render_template(
                'add_campagne.html',
                title='Ajouter une campagne',
                current_page='campagnes',
                form=form,
                lieux=lieux,
                plateformes=plateformes,
                plateforme_selectionnee=plateforme_selectionnee,
                membres_compatibles=membres_compatibles,
                membres_selectionnes=membres_selectionnes,
                budget_mensuel=budget_mensuel,
                budget_estime=budget_estime,
                message=message,
                message_type=message_type,
            )

        if not form.validate():
            first_error = next(iter(form.errors.values()))[0]
            message = first_error
            message_type = 'error'
        else:
            try:
                titre = (form.titre.data or '').strip() or None
                date_debut = form.dateDebut.data
                duree_jours = form.duree.data
                id_lieu = int(form.idLieu.data)
                id_plateforme_int = int(form.idPlateforme.data)
                membres_usernames = form.membres.data
            except ValueError as exc:
                message = f'Erreur de validation : {exc}'
                message_type = 'error'
            else:
                if not membres_usernames:
                    message = 'Vous devez sélectionner au moins un membre habilité'
                    message_type = 'error'
                else:
                    if not plateforme_selectionnee or plateforme_selectionnee.idPlateforme != id_plateforme_int:
                        plateforme_selectionnee = PLATEFORME.query.get(
                            id_plateforme_int)
                    budget_estime = estimer_cout_campagne(
                        plateforme_selectionnee, duree_jours)
                    campagne, error = creer_campagne(
                        date_debut=date_debut,
                        duree_jours=duree_jours,
                        id_lieu=id_lieu,
                        id_plateforme=id_plateforme_int,
                        noms_utilisateurs_membres=membres_usernames,
                        titre=titre)
                    if error:
                        message = error
                        message_type = 'error'
                    else:
                        return redirect(
                            url_for('liste_campagnes',
                                    success='Campagne créée avec succès !'))

    return render_template('add_campagne.html',
                           title='Ajouter une campagne',
                           current_page='campagnes',
                           form=form,
                           lieux=lieux,
                           plateformes=plateformes,
                           plateforme_selectionnee=plateforme_selectionnee,
                           membres_compatibles=membres_compatibles,
                           membres_selectionnes=membres_selectionnes,
                           budget_mensuel=budget_mensuel,
                           budget_estime=budget_estime,
                           message=message,
                           message_type=message_type)


@app.route("/campagnes/")
@login_required
def liste_campagnes():
    campagnes = CAMPAGNE.query.all()
    return render_template("liste_campagnes.html",
                           title="Liste des campagnes",
                           current_page="campagne",
                           campagnes=campagnes)


@app.route('/campagnes/<int:idCampagne>/view/')
@login_required
def view_campagnes(idCampagne):
    campagne = db.session.get(CAMPAGNE, idCampagne)
    if campagne is None:
        return render_template('404.html', message="Campagne non trouvée"), 404
    upload_form = AssociateFilesForm()
    return render_template('view_campagne.html',
                           title=f'Campagne {campagne.idCampagne}',
                           current_page='campagne',
                           campagne=campagne,
                           upload_form=upload_form)


@app.route('/campagnes/<int:idCampagne>/supprimer/')
@login_required
def supprimer_campagne(idCampagne):
    campagne = db.session.get(CAMPAGNE, idCampagne)
    if campagne is None:
        return render_template('404.html', message="Campagne non trouvée"), 404
    if campagne:
        db.session.delete(campagne)
        db.session.commit()
    return redirect(url_for('liste_campagnes'))


@app.route('/campagnes/<int:idCampagne>/view/associer-fichier',
           methods=('POST', ))
@login_required
def associer_fichier(idCampagne):
    campagne = db.session.get(CAMPAGNE, idCampagne)
    if campagne is None:
        return render_template('404.html', message="Campagne non trouvée"), 404

    form = AssociateFilesForm()
    if not form.validate_on_submit():
        return render_template('view_campagne.html',
                               title=f'Campagne {idCampagne}',
                               current_page='campagne',
                               campagne=campagne,
                               upload_form=form), 400

    upload_folder = current_app.config.get('ECHANTILLON_UPLOAD_FOLDER')
    if not upload_folder:
        upload_folder = Path(current_app.root_path) / 'data' / 'adn'

    try:
        for storage in form.file.data:
            if storage is None or storage.filename is None:
                continue
            filename = storage.filename
            if not filename:
                continue

            target_path = Path(upload_folder) / filename

            storage.save(target_path)

            echantillon = ECHANTILLON(fichierAdn=target_path.name)
            db.session.add(echantillon)
            db.session.flush()

            rapport = RAPPORTER(idEchantillon=echantillon.idEchantillon,
                                idCampagne=idCampagne)
            db.session.add(rapport)
        db.session.commit()
    except Exception as e:
        print("Erreur lors de l'association des fichiers:", e)
        db.session.rollback()

    return redirect(url_for('view_campagnes', idCampagne=idCampagne))


# ==================== PLATEFORMES ====================


@app.route("/plateformes/")
@login_required
def liste_plateformes():
    plateformes = PLATEFORME.query.all()
    return render_template("liste_plateformes.html",
                           title="Liste des plateformes",
                           current_page="plateformes",
                           plateformes=plateformes)


@app.route("/plateformes/<int:idPlateforme>/supprimer/")
@login_required
def supprimer_plateforme(idPlateforme):
    plateforme = PLATEFORME.query.filter_by(idPlateforme=idPlateforme).first()
    if plateforme:
        db.session.delete(plateforme)
        db.session.commit()
    return redirect(url_for('liste_plateformes'))


@app.route('/add_plateforme/', methods=['GET', 'POST'])
@login_required
def add_plateforme():

    if current_user.is_authenticated:
        form = Form_plateforme()

        if form.validate_on_submit():
            plateforme_existe = PLATEFORME.query.filter(
                PLATEFORME.nom == form.nom_plateforme.data).first()
            print(plateforme_existe)

            if not plateforme_existe:
                nouvelle_plateforme = PLATEFORME(
                    nom=form.nom_plateforme.data,
                    cout_journalier=form.cout_journalier.data,
                    min_nb_personne=form.minimum_personnes.data,
                    intervalle_maintenance=form.intervalle_maintenance.data)

                db.session.add(nouvelle_plateforme)
                db.session.commit()

                return redirect(
                    url_for('add_materiel',
                            idPlateforme=nouvelle_plateforme.idPlateforme))
            else:
                return render_template(
                    "add_plateforme.html",
                    form_plateforme=form,
                    message="Une plateforme avec le même nom existe déjà",
                    message_type='error')

        return render_template("add_plateforme.html", form_plateforme=form)
    else:
        return redirect(url_for('login'))


# ==================== MATERIELS ====================
@app.route("/materiels/")
@login_required
def liste_materiels():
    materiels = MATERIEL.query.all()
    return render_template("liste_materiels.html",
                           title="Liste des matériels",
                           current_page="materiels",
                           materiels=materiels)


@app.route('/materiels/<int:idMateriel>/supprimer/')
@login_required
def supprimer_materiel(idMateriel):
    materiel = db.session.get(MATERIEL, idMateriel)
    if materiel is None:
        return render_template('404.html', message="Matériel non trouvé"), 404
    db.session.delete(materiel)
    db.session.commit()
    return redirect(url_for('liste_materiels'))


@app.route("/add_materiel/<idPlateforme>/", methods=("GET", "POST"))
def add_materiel(idPlateforme):

    mat_dispo = db.session.query(MATERIEL).all()

    la_plateforme = PLATEFORME.query.get(idPlateforme)

    if la_plateforme is None:
        return render_template(
            "add_materiel.html",
            form_materiel=form_mat,
            message_type='error',
            message=
            'Erreur lors du chargement de la plateforme veuillez réessayer',
            plateforme=la_plateforme,
            materiel_dispo=mat_dispo,
            materiel_plateforme=mat_plat)

    mat_plat = mat_plat = db.session.query(UTILISER).filter(
        UTILISER.idPlateforme == la_plateforme.idPlateforme).all()

    form_mat = Form_materiel()

    if request.form.get("mat_id"):
        print("here")
        id_mat = request.form.get("mat_id", type=int)
        quantite_add = request.form.get("mat_qte", type=int)
        if quantite_add and id_mat and quantite_add > 0:
            update_qte(quantite_add, id_mat, la_plateforme.idPlateforme)
            db.session.commit()
            return redirect(
                url_for('add_materiel',
                        idPlateforme=la_plateforme.idPlateforme))

    elif form_mat.validate_on_submit():
        nouveau_mat = MATERIEL(
            nom=form_mat.nom_materiel.data,
            description=form_mat.description_mat.data,
        )
        db.session.add(nouveau_mat)
        db.session.commit()

        hab = db.session.query(HABILITATION).all()
        print(hab)

        necessite = None
        for item in form_mat.habilitations.data:
            match item:
                case "electrique":
                    necessite = NECESSITER(idHabilitation=1,
                                           idMateriel=nouveau_mat.idMateriel)
                    db.session.add(necessite)
                    db.session.commit()
                case "chimique":
                    necessite = NECESSITER(idHabilitation=2,
                                           idMateriel=nouveau_mat.idMateriel)
                    db.session.add(necessite)
                    db.session.commit()
                case "biologique":
                    necessite = NECESSITER(idHabilitation=3,
                                           idMateriel=nouveau_mat.idMateriel)
                    db.session.add(necessite)
                    db.session.commit()
                case "radiations":
                    necessite = NECESSITER(idHabilitation=4,
                                           idMateriel=nouveau_mat.idMateriel)
                    db.session.add(necessite)
                    db.session.commit()

        utilise = UTILISER(idMateriel=nouveau_mat.idMateriel,
                           idPlateforme=idPlateforme,
                           quantite=form_mat.quantite_mat.data)
        db.session.add(utilise)
        db.session.commit()

        print("ble ble ble")
        return render_template("add_materiel.html",
                               plateforme=la_plateforme,
                               form_materiel=form_mat,
                               materiel_dispo=mat_dispo,
                               materiel_plateforme=mat_plat)
    if not request.form.get("mat_id") and request.method == 'POST':
        return render_template("add_materiel.html",
                               form_materiel=form_mat,
                               message_type='error',
                               plateforme=la_plateforme,
                               materiel_dispo=mat_dispo,
                               materiel_plateforme=mat_plat)

    return render_template("add_materiel.html",
                           plateforme=la_plateforme,
                           form_materiel=form_mat,
                           materiel_dispo=mat_dispo,
                           materiel_plateforme=mat_plat)


# ==================== LIEUX ====================


@app.route("/lieux/")
@login_required
def liste_lieux():
    lieux = LIEU_FOUILLE.query.all()
    error = request.args.get('error')
    success = request.args.get('success')
    return render_template("liste_lieux.html",
                           title="Liste des lieux",
                           current_page="lieux",
                           lieux=lieux,
                           error=error,
                           success=success)


@app.route('/lieux/ajouter/', methods=['GET', 'POST'])
@login_required
def ajouter_lieu():
    unForm = LieuForm()

    if unForm.validate_on_submit():
        unLieu = unForm.build_lieu()
        db.session.add(unLieu)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            unForm.nom.errors.append(
                "Une erreur est survenue, merci de réessayer.")
        else:
            return redirect(
                url_for('liste_lieux', success='Lieu ajouté avec succès !'))

    return render_template('add_lieu.html',
                           title='Ajouter un lieu',
                           current_page='lieux',
                           form=unForm)


@app.route('/lieux/<int:idLieu>/supprimer/')
@login_required
def supprimer_lieu(idLieu):
    lieu = db.session.get(LIEU_FOUILLE, idLieu)
    if lieu is None:
        return render_template('404.html', message="Lieu non trouvé"), 404
    if lieu.campagnes:
        return redirect(
            url_for('liste_lieux',
                    error='Suppression impossible : campagnes associées'))
    db.session.delete(lieu)
    db.session.commit()
    return redirect(url_for('liste_lieux'))


# ==================== PERSONNELS ====================


@app.route("/personnels/")
@login_required
def liste_personnels():
    personnels = PERSONNE.query.all()
    return render_template("liste_personnels.html",
                           title="Liste des personnels",
                           current_page="personnels",
                           personnels=personnels)


@app.route("/personnels/ajouter/")
@login_required
def ajouter_personnel():
    # TODO
    return "Ajouter un personnel - Fonctionnalité à implémenter"


@app.route("/personnels/<string:username>/supprimer/")
@login_required
def supprimer_personnel(username):
    personnel = PERSONNE.query.filter_by(username=username).first()
    if personnel:
        db.session.delete(personnel)
        db.session.commit()
    return redirect(url_for('liste_personnels'))


@app.route("/add_personne/", methods=("GET", "POST"))
@login_required
def add_personne():

    if current_user.is_authenticated:

        form_pers = FormPersonne()

        role_choices = [('', 'Sélectionner un rôle')] + [
            (role.value, role.value) for role in role_labo_enum
        ]
        form_pers.role_labo.choices = role_choices

        if form_pers.validate_on_submit():

            username = form_pers.username.data
            personne_existe = PERSONNE.query.get(username)

            if not personne_existe:
                habiliter = None
                nouvelle_personne = PERSONNE(
                    nom=form_pers.nom.data,
                    prenom=form_pers.prenom.data,
                    username=form_pers.username.data,
                    password=form_pers.password.data,
                    role_labo=form_pers.role_labo.data)
                db.session.add(nouvelle_personne)
                db.session.commit()
                for item in form_pers.habilitations.data:
                    match item:
                        case "electrique":
                            habiliter = HABILITER(
                                idHabilitation=1,
                                username=form_pers.username.data)
                            db.session.add(habiliter)
                            db.session.commit()
                        case "chimique":
                            habiliter = HABILITER(
                                idHabilitation=2,
                                username=form_pers.username.data)
                            db.session.add(habiliter)
                            db.session.commit()
                        case "biologique":
                            habiliter = HABILITER(
                                idHabilitation=3,
                                username=form_pers.username.data)
                            db.session.add(habiliter)
                            db.session.commit()
                        case "radiations":
                            habiliter = HABILITER(
                                idHabilitation=4,
                                username=form_pers.username.data)
                            db.session.add(habiliter)
                            db.session.commit()

                return redirect(url_for('liste_personnels'))
            else:
                return render_template("add_personne.html",
                                       form_personne=form_pers,
                                       message_type='error',
                                       message="Le pseudo est déjà utilisé")

        if request.method == 'POST':
            return render_template("add_personne.html",
                                   form_personne=form_pers,
                                   message_type='error')

        return render_template("add_personne.html", form_personne=form_pers)
    else:
        return redirect(url_for('login'))


# ==================== BUDGET ====================


@app.route('/dashboard/set_budget/', methods=(
    'GET',
    'POST',
))
@login_required
def set_budget():
    unForm = BudgetForm()
    if not unForm.is_submitted():
        unForm.next.data = request.args.get('next')
    elif unForm.validate_on_submit():
        unBudget = unForm.build_budget()
        db.session.add(unBudget)
        try:
            db.session.commit()
        except (IntegrityError, DataError):
            db.session.rollback()
            unForm.budget_mensuel.errors.append(
                "Une erreur est survenue, merci de réessayer.")
        else:
            return redirect(unForm.next.data or url_for('index'))
    return render_template('set_budget.html',
                           title='Définir le budget',
                           current_page='budget',
                           form=unForm)


# ==================== MAINTENANCE ====================


@app.route('/maintenance/', methods=['GET', 'POST'])
@login_required
def maintenance():
    plateformes = PLATEFORME.query.all()
    form = MaintenanceForm()
    form.idPlateforme.choices = [('', 'Sélectionner une plateforme')] + [
        (p.idPlateforme, p.nom) for p in plateformes
    ]

    message = None
    message_type = None

    if request.method == 'POST':
        form.process(formdata=request.form)
        if form.validate():
            try:
                id_plateforme = int(form.idPlateforme.data)
                erreur_chevauchement = verifier_chevauchement_campagne(
                    id_plateforme, form.dateDebut.data, form.duree.data)
                if erreur_chevauchement:
                    message = erreur_chevauchement
                    message_type = 'error'
                else:
                    erreur_maintenance = verifier_chevauchement_maintenance(
                        id_plateforme, form.dateDebut.data, form.duree.data)
                    if erreur_maintenance:
                        message = erreur_maintenance
                        message_type = 'error'
                    else:
                        new_maintenance = form.build_maintenance()
                        db.session.add(new_maintenance)
                        db.session.commit()
                        message = 'Maintenance créée avec succès !'
                        message_type = 'success'
            except ValueError as e:
                message = f'Erreur de validation : {str(e)}'
                message_type = 'error'
            except Exception as e:
                message = f'Erreur : {str(e)}'
                message_type = 'error'
        else:
            first_error = next(iter(form.errors.values()))[0]
            message = first_error
            message_type = 'error'
    else:
        message = request.args.get('error') or request.args.get('success')
        message_type = 'error' if request.args.get('error') else (
            'success' if request.args.get('success') else None)

    return render_template('maintenance.html',
                           title='Prévoir une maintenance',
                           plateformes=plateformes,
                           form=form,
                           message=message,
                           message_type=message_type)


# ==================== ADN - UTILITAIRES ====================

DOSSIER_BASE = Path(__file__).resolve().parents[1]
DOSSIER_ADN = DOSSIER_BASE / "algo" / "data"


def assurer_dossier_adn() -> None:
    DOSSIER_ADN.mkdir(parents=True, exist_ok=True)


def notifier(message: str, categorie: str = 'info') -> None:
    flash(message, categorie)


def valider_sequence(chaine: str) -> bool:
    bases_autorisees = set(constants.bases)
    return bool(chaine) and all(base in bases_autorisees for base in chaine)


def lister_fichiers_adn() -> list[dict]:
    """Liste les fichiers ADN disponibles dans le dossier des données."""

    assurer_dossier_adn()
    fichiers = []
    for chemin in sorted(DOSSIER_ADN.glob("*.adn")):
        try:
            contenu = chemin.read_text().strip().upper()
        except OSError:
            contenu = ""
        apercu = contenu[:12] + ("..." if len(contenu) > 12 else "")
        fichiers.append({
            "nom": chemin.name,
            "taille": len(contenu),
            "apercu": apercu,
        })
    return fichiers


def charger_sequence_fichier(nom_fichier: str) -> str:
    """Charge une séquence ADN depuis un fichier .adn"""

    assurer_dossier_adn()
    chemin = DOSSIER_ADN / nom_fichier
    if not chemin.exists():
        raise FileNotFoundError(f"Le fichier {nom_fichier} est introuvable")
    return chemin.read_text().strip().upper()


# ==================== ADN - GESTION FICHIERS ====================


@app.route('/gerer_adn/', methods=['GET', 'POST'])
@login_required
def gerer_adn():
    fichiers_adn = lister_fichiers_adn()
    choix_fichiers = [(f['nom'], f"{f['nom']} ({f['taille']} bases)")
                      for f in fichiers_adn]

    form_generer = GenererSequenceForm()
    form_charger = ChargerSequenceForm()
    form_choisir = ChoisirSequenceForm()
    form_choisir.sequences.choices = choix_fichiers
    sequence_creee = None
    fichier_charge = None

    if form_generer.submit_generer.data and form_generer.validate_on_submit():
        try:
            longueur = form_generer.longueur.data
            nom_fichier = secure_filename(
                form_generer.nom_fichier.data.strip())
            if not nom_fichier:
                raise ValueError
            nouvelle_sequence = generer_sequence_adn_aleatoirement(
                constants.bases, longueur)
            try:
                sauvegarder_sequence(nouvelle_sequence, nom_fichier,
                                     DOSSIER_ADN)
            except TypeError:
                sauvegarder_sequence(nouvelle_sequence, nom_fichier)
            sequence_creee = {
                'nom': f"{nom_fichier}.adn",
                'contenu': nouvelle_sequence
            }
            notifier('Séquence générée et sauvegardée.', 'succes')
        except (ValueError, OSError):
            notifier('Impossible de générer la séquence.', 'erreur')
        fichiers_adn = lister_fichiers_adn()
        form_choisir.sequences.choices = [(f['nom'],
                                           f"{f['nom']} ({f['taille']} bases)")
                                          for f in fichiers_adn]

    elif form_charger.submit_charger.data and form_charger.validate_on_submit(
    ):
        try:
            fichier = form_charger.fichier_adn.data
            contenu = fichier.read().decode('utf-8').strip().upper()
            if not valider_sequence(contenu):
                raise ValueError
            nom_souhaite = form_charger.nom_souhaite.data.strip(
            ) if form_charger.nom_souhaite.data else ''
            nom_final = secure_filename(nom_souhaite) or secure_filename(
                Path(fichier.filename).stem)
            if not nom_final:
                raise ValueError
            assurer_dossier_adn()
            chemin = DOSSIER_ADN / f"{nom_final}.adn"
            chemin.write_text(contenu)
            fichier_charge = {'nom': chemin.name, 'taille': len(contenu)}
            notifier('Fichier chargé correctement.', 'succes')
        except (ValueError, OSError, UnicodeDecodeError):
            notifier('Le fichier ne peut pas être enregistré.', 'erreur')
        fichiers_adn = lister_fichiers_adn()
        form_choisir.sequences.choices = [(f['nom'],
                                           f"{f['nom']} ({f['taille']} bases)")
                                          for f in fichiers_adn]

    elif form_choisir.submit_traitements.data and form_choisir.validate_on_submit(
    ):
        if not form_choisir.sequences.data:
            notifier('Choisissez au moins un fichier.', 'erreur')
        else:
            return redirect(
                url_for('traitements_adn',
                        fichiers=','.join(form_choisir.sequences.data)))

    return render_template('gerer_adn.html',
                           title='Gerer les fichiers ADN',
                           current_page='gerer_adn',
                           fichiers=fichiers_adn,
                           form_generer=form_generer,
                           form_charger=form_charger,
                           form_choisir=form_choisir,
                           sequence_creee=sequence_creee,
                           fichier_charge=fichier_charge)


# ==================== ADN - TRAITEMENTS ====================


@app.route('/traitements_adn/', methods=['GET', 'POST'])
@login_required
def traitements_adn():
    fichiers_adn = lister_fichiers_adn()
    choix_fichiers = [(f['nom'], f['nom']) for f in fichiers_adn]
    preselection = [
        nom for nom in request.args.get('fichiers', '').split(',') if nom
    ]

    form_traitement = TraitementAdnForm()
    form_traitement.sequence_base.choices = choix_fichiers
    form_traitement.sequence_lev_a.choices = [('', 'Choisir un fichier')
                                              ] + choix_fichiers
    form_traitement.sequence_lev_b.choices = [('', 'Choisir un fichier')
                                              ] + choix_fichiers

    if not form_traitement.sequence_base.data and preselection:
        form_traitement.sequence_base.data = preselection[0]
    if not form_traitement.sequence_lev_a.data and preselection:
        form_traitement.sequence_lev_a.data = preselection[0]
    if not form_traitement.sequence_lev_b.data and len(preselection) > 1:
        form_traitement.sequence_lev_b.data = preselection[1]

    if form_traitement.validate_on_submit():
        if not choix_fichiers:
            notifier('Aucun fichier ADN disponible.', 'erreur')
            return redirect(url_for('gerer_adn'))

        try:
            sequence_depart = charger_sequence_fichier(
                form_traitement.sequence_base.data)
        except FileNotFoundError:
            notifier('Impossible de lire la séquence de base.', 'erreur')
            return redirect(url_for('traitements_adn'))

        proba = form_traitement.proba.data or 0.0
        mutations_cochees = [
            form_traitement.mutation_remplacement.data,
            form_traitement.mutation_insertion.data,
            form_traitement.mutation_deletion.data,
            form_traitement.calcul_levenshtein.data,
        ]
        if not any(mutations_cochees):
            notifier('Choisissez au moins une mutation ou un calcul.',
                     'erreur')
            return redirect(url_for('traitements_adn'))

        sequence_en_cours = sequence_depart
        liste_mutations = []
        compte_mutations = {'remplacement': 0, 'insertion': 0, 'deletion': 0}

        if form_traitement.mutation_remplacement.data:
            sequence_avant = sequence_en_cours
            sequence_en_cours = simuler_mutations_remplacements(
                sequence_avant, proba)
            delta = estimation_distance_mutation(sequence_avant,
                                                 sequence_en_cours)
            compte_mutations['remplacement'] = delta
            liste_mutations.append({
                'nom': 'Mutation par remplacement',
                'taille_avant': len(sequence_avant),
                'taille_apres': len(sequence_en_cours),
                'delta': delta,
                'sequence': sequence_en_cours,
            })

        if form_traitement.mutation_insertion.data:
            sequence_avant = sequence_en_cours
            sequence_en_cours = mutation_par_insertion(sequence_avant, proba)
            delta = max(len(sequence_en_cours) - len(sequence_avant), 0)
            compte_mutations['insertion'] = delta
            liste_mutations.append({
                'nom': 'Mutation par insertion',
                'taille_avant': len(sequence_avant),
                'taille_apres': len(sequence_en_cours),
                'delta': delta,
                'sequence': sequence_en_cours,
            })

        if form_traitement.mutation_deletion.data:
            sequence_avant = sequence_en_cours
            sequence_en_cours = mutation_par_deletion(sequence_avant, proba)
            delta = max(len(sequence_avant) - len(sequence_en_cours), 0)
            compte_mutations['deletion'] = delta
            liste_mutations.append({
                'nom': 'Mutation par deletion',
                'taille_avant': len(sequence_avant),
                'taille_apres': len(sequence_en_cours),
                'delta': delta,
                'sequence': sequence_en_cours,
            })

        distance_info = None
        if form_traitement.calcul_levenshtein.data:
            fichier_a = form_traitement.sequence_lev_a.data
            fichier_b = form_traitement.sequence_lev_b.data
            if not fichier_a or not fichier_b:
                notifier(
                    'Choisissez deux fichiers pour le calcul de distance.',
                    'erreur')
                return redirect(url_for('traitements_adn'))
            try:
                seq_a = charger_sequence_fichier(fichier_a)
                seq_b = charger_sequence_fichier(fichier_b)
                distance_info = {
                    'valeur': distance_de_levenshtein(seq_a, seq_b),
                    'fichier_a': fichier_a,
                    'fichier_b': fichier_b,
                }
            except FileNotFoundError:
                notifier('Impossible de charger les fichiers pour le calcul.',
                         'erreur')
                return redirect(url_for('traitements_adn'))

        resultat = {
            'fichier_base': form_traitement.sequence_base.data,
            'sequence_depart': sequence_depart,
            'probabilite': proba,
            'mutations': liste_mutations,
            'compte_mutations': compte_mutations,
            'sequence_finale': sequence_en_cours,
            'distance': distance_info,
            'horodatage': datetime.utcnow().isoformat(),
        }

        session['resultat_adn'] = resultat
        notifier('Traitements appliqués.', 'succes')
        return redirect(url_for('resultat'))

    return render_template('traitements_adn.html',
                           title='Traitements ADN',
                           current_page='traitements_adn',
                           fichiers=fichiers_adn,
                           preselection=preselection,
                           form_traitement=form_traitement)


@app.route("/view_resultats/", methods=["GET"])
@login_required
def resultat():
    if current_user.is_authenticated:

        resultat = session.get("resultat_adn")
        if not resultat:
            notifier(
                "Aucun résultat disponible. Lancez d’abord un traitement.",
                "erreur")
            return redirect(url_for("traitements_adn"))

        fichiersadn = lister_fichiers_adn()
        index_fichiers = {f["nom"]: f for f in fichiersadn}
        fichier_base_info = index_fichiers.get(resultat["fichier_base"])
        distance_info = resultat.get("distance")

        return render_template(
            "view_resultats.html",
            title="Résultats ADN",
            currentpage="resultatsadn",
            resultat=resultat,
            fichier_base_info=fichier_base_info,
            distance_info=distance_info,
        )
    else:
        return redirect(url_for('register'))

@app.route('/dashboard/', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DashboardPeriodForm()
    display_form = form
    today = date.today()

    selected_month = today.month
    selected_year = today.year

    if request.method == 'POST':
        if form.validate_on_submit():
            selected_month = form.month.data
            selected_year = form.year.data
        else:
            flash('La période sélectionnée est invalide.', 'error')
        display_form = DashboardPeriodForm()
    else:
        arg_month = request.args.get('month', type=int)
        arg_year = request.args.get('year', type=int)
        if arg_month:
            selected_month = arg_month
        if arg_year:
            selected_year = arg_year

    if selected_month < 1 or selected_month > 12:
        selected_month = today.month
    if selected_year < 1900 or selected_year > 2100:
        selected_year = today.year

    display_form.month.data = selected_month
    display_form.year.data = selected_year

    # date début et fin du mois sélectionné
    month_start = date(selected_year, selected_month, 1)
    last_day = monthrange(selected_year, selected_month)[1]
    month_end = date(selected_year, selected_month, last_day)

    previous_date = month_start - timedelta(days=1)
    next_date = month_end + timedelta(days=1)
    previous_period = {'month': previous_date.month, 'year': previous_date.year}
    next_period = {'month': next_date.month, 'year': next_date.year}

    def format_currency(value):
        if value is None:
            return None
        return f"{value:,.2f}".replace(',', ' ').replace('.', ',')

    campagnes = CAMPAGNE.query.all()

    active_campagnes = []
    active_personnel = set()
    for campagne in campagnes:
        duree = campagne.duree or 0
        fin_campagne = campagne.dateDebut + timedelta(days=max(duree - 1, 0))
        if fin_campagne < month_start or campagne.dateDebut > month_end:
            continue
        active_campagnes.append(campagne)
        for participation in campagne.participer:
            active_personnel.add(participation.username)

    # calcul des personne dispo
    total_personnel = PERSONNE.query.count()
    total_personnel_occupe = len(active_personnel)
    total_personnel_disponible = max(0, total_personnel - total_personnel_occupe)

    budget_record = BUDGET_MENSUEL.query.filter_by(
        annee=selected_year, mois=selected_month).first()
    budget_initial = float(budget_record.budget) if budget_record else None

    budget_depense = 0.0
    # calcul du budget dépensé
    for campagne in active_campagnes:
        duree = campagne.duree or 0
        fin_campagne = campagne.dateDebut + timedelta(days=max(duree - 1, 0))
        chevauchement_debut = max(campagne.dateDebut, month_start)
        chevauchement_fin = min(fin_campagne, month_end)
        overlap = (chevauchement_fin - chevauchement_debut).days + 1
        if overlap <= 0:
            continue
        for liaison in campagne.planifier:
            plateforme = liaison.plateforme
            if plateforme and plateforme.cout_journalier:
                budget_depense += float(plateforme.cout_journalier) * overlap

    budget_restant = (budget_initial - budget_depense
                      if budget_initial is not None else None)
    budget_restant = round(budget_restant, 2) if budget_restant is not None else None
    budget_depense = round(budget_depense, 2)

    budget_status = 'ok'
    if budget_restant is not None and budget_restant < 0:
        budget_status = 'alert'
    elif budget_restant is None:
        budget_status = 'undefined'

    # récupération des maintenances planifiées pour le mois
    maintenances = (MAINTENANCE.query
                    .filter(MAINTENANCE.dateMaintenance >= month_start)
                    .filter(MAINTENANCE.dateMaintenance <= month_end)
                    .filter(MAINTENANCE.statut == statut.PLANIFIEE)
                    .order_by(MAINTENANCE.dateMaintenance.asc())
                    .all())

    # préparation des items de maintenance
    maintenance_items = []
    for maintenance in maintenances:
        jours_restant = (maintenance.dateMaintenance - today).days
        if jours_restant > 0:
            relative = f"d'ici {jours_restant} jours"
        elif jours_restant == 0:
            relative = "aujourd'hui"
        else:
            relative = f"il y a {abs(jours_restant)} jours"
        maintenance_items.append({
            'id': maintenance.idMaintenance,
            'plateforme': maintenance.plateforme.nom if maintenance.plateforme else 'Plateforme inconnue',
            'date': maintenance.dateMaintenance,
            'date_label': maintenance.dateMaintenance.strftime('%d/%m/%Y'),
            'relative': relative,
        })

    selected_period_label = f"{MONTH_NAMES_FR[selected_month]} {selected_year}"

    return render_template(
        'dashboard.html',
        title='Tableau de bord',
        current_page='dashboard',
        form=display_form,
        month_start=month_start,
        month_end=month_end,
        selected_month=selected_month,
        selected_year=selected_year,
        selected_period_label=selected_period_label,
        previous_period=previous_period,
        next_period=next_period,
        personnel_metrics={
            'available': total_personnel_disponible,
            'total': total_personnel,
            'engaged': total_personnel_occupe,
        },
        active_campaigns_count=len(active_campagnes),
        budget_summary={
            'initial': budget_initial,
            'spent': budget_depense,
            'remaining': budget_restant,
            'remaining_label': format_currency(budget_restant) if budget_restant is not None else None,
            'initial_label': format_currency(budget_initial) if budget_initial is not None else None,
            'spent_label': format_currency(budget_depense),
            'status': budget_status,
        },
        maintenance_items=maintenance_items,
    )
      


if __name__ == "__main__":
    app.run()
