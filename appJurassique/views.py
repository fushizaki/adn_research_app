from flask import render_template
from .app import app, db
from .models import CAMPAGNE, LIEU_FOUILLE, PLATEFORME, PERSONNE, PARTICIPER

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil')

@app.route('/add_campagne/')
def add_campagne():
    lieux = LIEU_FOUILLE.query.all()
    plateformes = PLATEFORME.query.all()
    lieux = []
    plateformes = []
    return render_template('add_campagne.html', title='Ajouter une Campagne',campagne=None,lieux=lieux,plateformes=plateformes)

@app.route('/login/')
def login():
    return render_template('login.html', title='Login')

