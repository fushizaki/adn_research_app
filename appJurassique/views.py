from flask import render_template
from models import PLATEFORME
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
@login_required
def add_plateforme():
    form_plat = Form_plateforme()
    new_plateforme = PLATEFORME.query.filter(PLATEFORME.Nom == form_plat.nom_plateforme.data).first()
    
    if(new_plateforme == None):
        if form_plat.validate_on_submit():
            new_plateforme = Plateforme(Nom=unForm.Nom.data)
            db.session.add(insertedAuteur)
            db.session.commit()
            insertedId = Auteur.query.count()
            return redirect(url_for('viewAuteur', idA=insertedId))
    return render_template('add_plateforme.html', form_plateforme = form_plat, plateforme_existante = False,  title = "Ajout d'une plateforme")


def insertAuteur():
    insertedAuteur = None
    unForm = FormAuteur()
    unAuteur = Auteur.query.filter(Auteur.Nom == unForm.Nom.data).first()
    
    if(unAuteur == None):
        if unForm.validate_on_submit():
            insertedAuteur = Auteur(Nom=unForm.Nom.data)
            db.session.add(insertedAuteur)
            db.session.commit()
            insertedId = Auteur.query.count()
            return redirect(url_for('viewAuteur', idA=insertedId))
    return render_template("auteur_create.html", createForm=unForm, auteur_existant=True)

if __name__ == "__main__":
    app.run()