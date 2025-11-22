from flask import render_template
from .forms import Form_plateforme
from .app import app, db

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil')

@app.route('/login/')
def login():
    return render_template('login.html', title='Login')

@app.route('/add_plateforme/')
def add_plateforme():
    form_plat = Form_plateforme()
    return render_template('add_plateforme.html', form_plateforme = form_plat, plateforme_existante = False,  title = "Ajout d'une plateforme")

if __name__ == "__main__":
    app.run()