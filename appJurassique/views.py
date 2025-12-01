from flask import render_template, request, url_for, redirect
from .app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from appJurassique.forms import LoginForm, RegisterForm, BudgetForm, MaintenanceForm
from appJurassique.models import PERSONNE, role_labo_enum, PLATEFORME
from appJurassique.utils import verifier_chevauchement_campagne


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil', current_page='index')

@app.route('/add_campagne/')
def add_campagne():
    return render_template('add_campagne.html', title='Ajouter une Campagne')

@app.route('/maintenance/', methods=['GET', 'POST'])
def maintenance():
    plateformes = PLATEFORME.query.all()
    form = MaintenanceForm()
    form.idPlateforme.choices = [('', 'Sélectionner une plateforme')] + [
        (p.idPlateforme, p.nom) for p in plateformes]
    
    message = None
    message_type = None
    
    if request.method == 'POST':
        form.process(formdata=request.form)
        if form.validate():
            try:
                erreur_chevauchement = verifier_chevauchement_campagne(
                    int(form.idPlateforme.data),
                    form.dateDebut.data,
                    form.duree.data
                )
                if erreur_chevauchement:
                    message = erreur_chevauchement
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
            'success' if request.args.get('success') else None
        )
    
    return render_template(
        'maintenance.html',
        title='Prévoir une maintenance',
        plateformes=plateformes,
        form=form,
        message=message,
        message_type=message_type
    )

@app.route('/login/')
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


