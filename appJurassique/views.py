from zipfile import Path
from flask import flash, render_template, request, url_for, redirect, jsonify
from werkzeug.utils import secure_filename
from algo import constants
from algo.main import *
from .app import app, db
import algo
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from appJurassique.forms import *
from appJurassique.models import *


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil', current_page='index')


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
        except IntegrityError:
            db.session.rollback()
            unForm.date.errors.append(
                "Une erreur est survenue, merci de réessayer.")
        else:
            return redirect(unForm.next.data or url_for('index'))
    return render_template('set_budget.html',
                           title='Définir le budget',
                           current_page='dashboard',
                           form=unForm)


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


@app.route("/register/", methods=(
    "GET",
    "POST",
))
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

@app.route('/traitements_adn/', methods=['GET', 'POST'])
def traitements_adn():
    echantillons =  ECHANTILLON.query.all()

    return render_template('traitements_adn.html',
                           title='Traitements ADN',
                           current_page='traitements_adn',
                           echantillons=echantillons)    


@app.route('/gerer_adn/', methods=['GET', 'POST'])
def gerer_adn():
    echantillons =  ECHANTILLON.query.all()
    
    return render_template('gerer_adn.html',
                           title='Gérer les fichiers ADN',
                           current_page='gerer_adn',
                           echantillons=echantillons)    


#===================== PARTIE ADN  ====================

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


@app.route('/gerer_adn/', methods=['GET', 'POST'])
def gerer_adn():
    fichiers_adn = lister_fichiers_adn()
    choix_fichiers = [(f['nom'], f"{f['nom']} ({f['taille']} bases)") for f in fichiers_adn]

    form_generer = GenererSequenceForm()
    form_charger = ChargerSequenceForm()
    form_choisir = ChoisirSequenceForm()
    form_choisir.sequences.choices = choix_fichiers
    sequence_creee = None
    fichier_charge = None

    if form_generer.submit_generer.data and form_generer.validate_on_submit():
        try:
            longueur = form_generer.longueur.data
            nom_fichier = secure_filename(form_generer.nom_fichier.data.strip())
            if not nom_fichier:
                raise ValueError
            nouvelle_sequence = generer_sequence_adn_aleatoirement(constants.bases, longueur)
            try:
                sauvegarder_sequence(nouvelle_sequence, nom_fichier, DOSSIER_ADN)
            except TypeError:
                sauvegarder_sequence(nouvelle_sequence, nom_fichier)
            sequence_creee = {'nom': f"{nom_fichier}.adn", 'contenu': nouvelle_sequence}
            notifier('Séquence générée et sauvegardée.', 'succes')
        except (ValueError, OSError):
            notifier('Impossible de générer la séquence.', 'erreur')
        fichiers_adn = lister_fichiers_adn()
        form_choisir.sequences.choices = [(f['nom'], f"{f['nom']} ({f['taille']} bases)") for f in fichiers_adn]

    elif form_charger.submit_charger.data and form_charger.validate_on_submit():
        try:
            fichier = form_charger.fichier_adn.data
            contenu = fichier.read().decode('utf-8').strip().upper()
            if not valider_sequence(contenu):
                raise ValueError
            nom_souhaite = form_charger.nom_souhaite.data.strip() if form_charger.nom_souhaite.data else ''
            nom_final = secure_filename(nom_souhaite) or secure_filename(Path(fichier.filename).stem)
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
        form_choisir.sequences.choices = [(f['nom'], f"{f['nom']} ({f['taille']} bases)") for f in fichiers_adn]

    elif form_choisir.submit_traitements.data and form_choisir.validate_on_submit():
        if not form_choisir.sequences.data:
            notifier('Choisissez au moins un fichier.', 'erreur')
        else:
            return redirect(url_for('traitements_adn', fichiers=','.join(form_choisir.sequences.data)))

    return render_template('gerer_adn.html',
                           title='Gerer les fichiers ADN',
                           current_page='gerer_adn',
                           fichiers=fichiers_adn,
                           form_generer=form_generer,
                           form_charger=form_charger,
                           form_choisir=form_choisir,
                           sequence_creee=sequence_creee,
                           fichier_charge=fichier_charge)
