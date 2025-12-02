from flask import render_template, request, redirect, url_for
from .models import PLATEFORME
from .forms import Form_plateforme
from .app import app, db

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil')

@app.route('/login/')
def login():
    return render_template('login.html', title='Login')

@app.route('/add_plateforme/', methods=['GET', 'POST'])
def add_plateforme():   
    
    if current_user.is_authenticated:
        form = Form_plateforme()

        if form.validate_on_submit():
            plateforme_existe = PLATEFORME.query.filter(PLATEFORME.nom == form.nom_plateforme.data).first()
            print(plateforme_existe)

            if not plateforme_existe:
                nouvelle_plateforme = PLATEFORME(
                    nom=form.nom_plateforme.data,
                    cout_journalier=form.cout_journalier.data,
                    min_nb_personne=form.minimum_personnes.data,
                    intervalle_maintenance=form.intervalle_maintenance.data
                )

                db.session.add(nouvelle_plateforme)
                db.session.commit()

                return redirect(url_for('index'))
            else:
                return render_template("add_plateforme.html", form_plateforme=form, message="Une plateforme avec le même nom existe déjà", message_type='error') 

        return render_template("add_plateforme.html", form_plateforme=form)
    else:
        return redirect(url_for('register'))
    

if __name__ == "__main__":
    app.run()