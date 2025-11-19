from flask import render_template
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
    return render_template('add_plateforme.html', title= "Ajout d'une plateforme")

if __name__ == "__main__":
    app.run()