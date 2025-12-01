from flask import (render_template, request, url_for, redirect, current_app)
from .app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from appJurassique.forms import (LoginForm, RegisterForm, BudgetForm,
                                 AssociateFilesForm, Form_materiel)
from appJurassique.models import (CAMPAGNE, PERSONNE, role_labo_enum,
                                  ECHANTILLON, RAPPORTER, MATERIEL, UTILISER, PLATEFORME, NECESSITER)
from pathlib import Path
from .utils import update_qte


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


@app.route("/add_materiel/<idPlateforme>/", methods=("GET", "POST"))
def add_materiel(idPlateforme):
    
    mat_dispo = db.session.query(MATERIEL).all()
    
    la_plateforme = PLATEFORME.query.get(idPlateforme)
    
    mat_plat = mat_plat = db.session.query(UTILISER).filter(UTILISER.idPlateforme == la_plateforme.idPlateforme).all()
    
    print(mat_plat)
    
    form_mat = Form_materiel()
    
    if request.form.get("mat_id"):
            print("here")
            id_mat = request.form.get("mat_id", type=int)
            quantite_add = request.form.get("mat_qte", type=int)
            if quantite_add and id_mat and quantite_add > 0:
                update_qte(quantite_add, id_mat, la_plateforme.idPlateforme)
                db.session.commit()
                return redirect(url_for('add_materiel', idPlateforme=la_plateforme.idPlateforme))

    elif form_mat.validate_on_submit():
        nouveau_mat = MATERIEL(
            nom=form_mat.nom_materiel.data,
            description=form_mat.description_mat.data,
        )
        db.session.add(nouveau_mat)
        db.session.commit()
        
        necessite = None
        for item in form_mat.habilitations.data:
            match item:
                case "electrique":
                    necessite = NECESSITER(idHabilitation=1, idMateriel=nouveau_mat.idMateriel)
                    db.session.add(necessite)
                    db.session.commit()
                case "chimique":
                    necessite = NECESSITER(idHabilitation=2, idMateriel=nouveau_mat.idMateriel)
                    db.session.add(necessite)
                    db.session.commit()
                case "biologique":
                    necessite = NECESSITER(idHabilitation=3, idMateriel=nouveau_mat.idMateriel)
                    db.session.add(necessite)
                    db.session.commit()
                case "radiations":
                    necessite = NECESSITER(idHabilitation=4, idMateriel=nouveau_mat.idMateriel)
                    db.session.add(necessite)
                    db.session.commit()
                
                
        utilise = UTILISER(idMateriel=nouveau_mat.idMateriel, idPlateforme=idPlateforme, quantite=form_mat.quantite_mat.data)
        db.session.add(utilise)
        db.session.commit()

        
        return render_template("add_materiel.html", plateforme=la_plateforme, form_materiel=form_mat, materiel_dispo= mat_dispo, materiel_plateforme=mat_plat)
    if not request.form.get("mat_id") and request.method == 'POST':
        return render_template(
            "add_materiel.html",
            form_materiel=form_mat,
            message_type='error',
            plateforme=la_plateforme,
            materiel_dispo= mat_dispo,
            materiel_plateforme=mat_plat)

    return render_template("add_materiel.html", plateforme=la_plateforme, form_materiel=form_mat, materiel_dispo= mat_dispo, materiel_plateforme=mat_plat)
    
    
    