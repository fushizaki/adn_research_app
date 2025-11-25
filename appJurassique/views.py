from flask import render_template, request, redirect, url_for
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
def add_platefrome():
    new_plateforme = Form_plateforme()
    return render_template("add_plateforme.html", form_plateforme= new_plateforme)

@app.route('/create_campagne', methods=['POST'])
def create_plateforme():
    """Crée une nouvelle campagne avec validation des habilitations."""
    
    message = request.args.get('error') or request.args.get('success')
    message_type = 'error' if request.args.get('error') else ('success' if request.args.get('success') else None)
    
    new_plateforme = Form_plateforme(request.args.get('nom_plateforme'), 
                                     request.args.get('cout_journalier'), 
                                     request.args.get('minimum_personnes'),
                                     request.args.get('intervalle_maintenance'),
                                     request.args.get('hab_electrique'),
                                     request.args.get('hab_chimique'),
                                     request.args.get('hab_biologique'),
                                     request.args.get('hab_radiation'))
    
    id_plateforme = request.args.get('idPlateforme') or request.form.get('idPlateforme')
    
    if id_plateforme:
        id_plateforme = int(id_plateforme)
        plateforme_selectionnee = PLATEFORME.query.get(id_plateforme)
    try:
        nom_plareforme = request.form.get('nom_plareforme', '')
        cout_journalier = request.form.get('cout_journalier', '')
        minimum_personnes = request.form.get('minimum_personnes', '')
        intervalle_maintenance = request.form.get('intervalle_maintenance', '')
        hab_electrique = request.form.get('hab_electrique', '')
        hab_chimique = request.form.get('hab_chimique')
        hab_biologique = request.form.get('hab_biologique')
        hab_radiation = request.form.get('hab_radiation')
        
        if not nom_plareforme:
            return redirect(url_for('add_platefrome', error='Le nom de la plateforme est requis'))
        
        if not cout_journalier:
            return redirect(url_for('add_platefrome', error='Le cout journalier est requis'))
        
        if not minimum_personnes:
            return redirect(url_for('add_platefrome', error='Le minimum de personnes est requis'))
        
        if not intervalle_maintenance:
            return redirect(url_for('add_platefrome', error="L'intervalle de maintenance est requis"))
        
        if not hab_electrique and not hab_chimique and not hab_biologique and not hab_radiation:
            return redirect(url_for('add_platefrome', error='La plateforme est obligatoire'))
        
        duree = int(duree_str)
        id_lieu = int(id_lieu_str)
        id_plateforme = int(id_plateforme_str)
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
        duree_jours = max(1, duree // 24)

        campagne, error = create_plateforme( date_debut=date_debut,duree_jours=duree_jours,id_lieu=id_lieu,id_plateforme=id_plateforme,
                                        noms_utilisateurs_membres=membres_usernames,titre=titre
        )
        
        if error:
            return redirect(url_for('add_campagne', error=error,idPlateforme=id_plateforme_str,titre=titre or '',dateDebut=date_debut_str,
                                  duree=duree_str,idLieu=id_lieu_str))
        return redirect(url_for('index', success='Campagne créée avec succès !'))

    except ValueError as e:
        return redirect(url_for('add_campagne', error=f'Erreur de validation : {str(e)}'))
    except Exception as e:
        return redirect(url_for('add_campagne', error=f'Erreur : {str(e)}'))
    

if __name__ == "__main__":
    app.run()