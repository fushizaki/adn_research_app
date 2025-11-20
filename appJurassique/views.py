from flask import render_template
from .app import app, db

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil', current_page='index')

@app.route('/login/')
def login():
    return render_template('login.html', title='Login', current_page='login')

if __name__ == "__main__":
    app.run()