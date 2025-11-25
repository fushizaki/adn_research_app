from flask import render_template, request, url_for, redirect
from .app import app, db
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from appJurassique.forms import LoginForm, RegisterForm, BudgetForm, MaintenanceForm
from appJurassique.models import PERSONNE, role_labo_enum, PLATEFORME


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
    
    formdata = request.form if request.method == 'POST' else request.args
    if formdata:
        form.process(formdata=formdata)
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

@app.route('/creer_maintenance/', methods=['POST'])
def creer_maintenance():
    try:
        plateformes = PLATEFORME.query.all()
        form = MaintenanceForm()
        form.idPlateforme.choices = [('', 'Sélectionner une plateforme')] + [
            (p.idPlateforme, p.nom) for p in plateformes
        ]
        form.process(formdata=request.form)
        if not form.validate():
            first_error = next(iter(form.errors.values()))[0]
            return redirect(url_for('maintenance', error=first_error))

        maintenance = form.build_maintenance()
        db.session.add(maintenance)
        db.session.commit()

        return redirect(url_for(
            'maintenance',
            success='Maintenance créée avec succès !',
            idPlateforme=form.idPlateforme.data or '',
            dateDebut=form.dateDebut.data.strftime('%Y-%m-%d') if form.dateDebut.data else '',
            duree=form.duree.data or ''
        ))

    except ValueError as e:
        return redirect(url_for('maintenance', error=f'Erreur de validation : {str(e)}'))
    except Exception as e:
        return redirect(url_for('maintenance', error=f'Erreur : {str(e)}'))

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


