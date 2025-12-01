from pathlib import Path
from flask import (render_template, request, url_for, redirect, current_app)
from .app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from appJurassique.forms import (LoginForm, RegisterForm, BudgetForm,
                                 AssociateFilesForm, CampagneForm, LieuForm)
from appJurassique.models import (CAMPAGNE, PERSONNE, role_labo_enum,
                                  ECHANTILLON, RAPPORTER, LIEU_FOUILLE, PLATEFORME)
from .utils import creer_campagne, obtenir_membres_compatibles


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil', current_page='index')

@app.route('/add_campagne/', methods=['GET', 'POST'])
def add_campagne():
    """Affiche le formulaire d'ajout de campagne."""
    lieux = LIEU_FOUILLE.query.all()
    plateformes = PLATEFORME.query.all()
    form = CampagneForm()
    form.idLieu.choices = [('', 'Sélectionner un lieu')] + [
        (str(lieu.idLieu), lieu.nomLieu) for lieu in lieux
    ]
    form.idPlateforme.choices = [('', 'Sélectionner une plateforme')] + [
        (str(plateforme.idPlateforme), plateforme.nom) for plateforme in plateformes
    ]

    formdata = request.form if request.method == 'POST' else request.args
    if formdata:
        form.process(formdata=formdata)

    plateforme_selectionnee = None
    membres_compatibles = []
    membres_selectionnes = form.membres.data or []
    message = request.args.get('error') or request.args.get('success')
    message_type = 'error' if request.args.get('error') else (
        'success' if request.args.get('success') else None
    )

    id_plateforme = form.idPlateforme.data

    if id_plateforme:
        try:
            id_plateforme_int = int(id_plateforme)
            plateforme_selectionnee = PLATEFORME.query.get(id_plateforme_int)

            if plateforme_selectionnee:
                membres_compatibles = obtenir_membres_compatibles(id_plateforme_int)
        except ValueError:
            pass

    return render_template(
        'add_campagne.html',
        title='Ajouter une Campagne',
        lieux=lieux,
        plateformes=plateformes,
        plateforme_selectionnee=plateforme_selectionnee,
        membres_compatibles=membres_compatibles,
        membres_selectionnes=membres_selectionnes,
        form=form,
        message=message,
        message_type=message_type
    )

@app.route('/create_campagne/', methods=['POST'])

def creer_nouvelle_campagne():
    """Crée une nouvelle campagne avec validation des habilitations."""
    try:
        lieux = LIEU_FOUILLE.query.all()
        plateformes = PLATEFORME.query.all()
        form = CampagneForm()
        form.idLieu.choices = [('', 'Sélectionner un lieu')] + [
            (str(lieu.idLieu), lieu.nomLieu) for lieu in lieux
        ]
        form.idPlateforme.choices = [('', 'Sélectionner une plateforme')] + [
            (str(plateforme.idPlateforme), plateforme.nom) for plateforme in plateformes
        ]
        form.process(formdata=request.form)

        if not form.validate():
            first_error = next(iter(form.errors.values()))[0]
            return redirect(url_for('add_campagne', error=first_error, 
                                    ))

        titre = (form.titre.data or '').strip() or None
        date_debut = form.dateDebut.data
        duree_heures = form.duree.data
        id_lieu = int(form.idLieu.data)
        id_plateforme = int(form.idPlateforme.data)
        membres_usernames = form.membres.data

        if not membres_usernames:
            return redirect(
                url_for(
                    'add_campagne',
                    error='Vous devez sélectionner au moins un membre habilité',
                    titre=form.titre.data or '',
                    dateDebut=form.dateDebut.data.strftime('%Y-%m-%d') if form.dateDebut.data else '',
                    duree=form.duree.data or '',
                    idLieu=form.idLieu.data or '',
                    idPlateforme=form.idPlateforme.data or ''
                )
            )

        duree_jours = max(1, duree_heures // 24)

        campagne, error = creer_campagne(
            date_debut=date_debut,
            duree_jours=duree_jours,
            id_lieu=id_lieu,
            id_plateforme=id_plateforme,
            noms_utilisateurs_membres=membres_usernames,
            titre=titre
        )

        if error:
            return redirect(url_for(
                'add_campagne',
                error=error,
                titre=form.titre.data or '',
                dateDebut=form.dateDebut.data.strftime('%Y-%m-%d') if form.dateDebut.data else '',
                duree=form.duree.data or '',
                idLieu=form.idLieu.data or '',
                idPlateforme=form.idPlateforme.data or ''
            ))
        return redirect(url_for('liste_campagnes', success='Campagne créée avec succès !'))

    except ValueError as e:
        return redirect(url_for('add_campagne', error=f'Erreur de validation : {str(e)}'))
    except Exception as e:
        return redirect(url_for('add_campagne', error=f'Erreur : {str(e)}'))

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
                           current_page='budget',
                           form=unForm)

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
    

@app.route('/campagnes/<int:idCampagne>/view/associer-fichier', methods=(
    'POST',))
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


@app.route("/personnels/")
@login_required
def liste_personnels():
    personnels = PERSONNE.query.all()
    return render_template("liste_personnels.html",
                           title="Liste des personnels",
                           current_page="personnels",
                           personnels=personnels)


@app.route("/personnels/<string:username>/supprimer/")
@login_required
def supprimer_personnel(username):
    personnel = PERSONNE.query.filter_by(username=username).first()
    if personnel:
        db.session.delete(personnel)
        db.session.commit()
    return redirect(url_for('liste_personnels'))

@app.route("/personnels/ajouter/")
@login_required
def ajouter_personnel():
    # TODO
    return "Ajouter un personnel - Fonctionnalité à implémenter"


@app.route("/campagnes/")
@login_required
def liste_campagnes():
    campagnes = CAMPAGNE.query.all()
    return render_template("liste_campagnes.html",
                           title="Liste des campagnes",
                           current_page="campagne",
                           campagnes=campagnes)


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

@app.route('/lieux/<int:idLieu>/supprimer/')
@login_required
def supprimer_lieu(idLieu):
    lieu = db.session.get(LIEU_FOUILLE, idLieu)
    if lieu is None:
        return render_template('404.html', message="Lieu non trouvé"), 404
    if lieu.campagnes:
        return redirect(url_for('liste_lieux', error='Suppression impossible : campagnes associées'))
    db.session.delete(lieu)
    db.session.commit()
    return redirect(url_for('liste_lieux'))

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
            return redirect(url_for('liste_lieux', success='Lieu ajouté avec succès !'))

    return render_template('add_lieu.html',
                           title='Ajouter un lieu',
                           current_page='lieux',
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


