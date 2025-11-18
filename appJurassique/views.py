from flask import render_template
from .app import app, db

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil')

@app.route('/add_campagne')
@app.route('/add_campagne/')
def add_campagne():
    return render_template('add_campagne.html', title='Ajouter une Campagne')

@app.route('/login/')
def login():
    return render_template('login.html', title='Login')

if __name__ == "__main__":
    app.run()
