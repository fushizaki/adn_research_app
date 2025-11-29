from flask import render_template, request, url_for, redirect, jsonify
from .app import app, db
import algo
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.exc import IntegrityError
from appJurassique.forms import LoginForm, RegisterForm, BudgetForm, ADNForm
from appJurassique.models import PERSONNE, role_labo_enum, ECHANTILLON


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil', current_page='index')

@app.route('/add_campagne/')
def add_campagne():
    return render_template('add_campagne.html', title='Ajouter une Campagne')

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