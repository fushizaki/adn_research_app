from flask import render_template, request, redirect, url_for
from datetime import datetime
from .app import app, db
from .models import CAMPAGNE, LIEU_FOUILLE, PLATEFORME, PERSONNE
from .utils import creer_campagne, obtenir_membres_compatibles


@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html', title='Accueil')

@app.route('/add_campagne/', methods=['GET', 'POST'])
def add_campagne():
    """Affiche le formulaire d'ajout de campagne."""
    lieux = LIEU_FOUILLE.query.all()
    plateformes = PLATEFORME.query.all()
    
    plateforme_selectionnee = None
    membres_compatibles = []
    membres_selectionnes = []
    message = request.args.get('error') or request.args.get('success')
    message_type = 'error' if request.args.get('error') else ('success' if request.args.get('success') else None)
    
    form_data = {
        'titre': request.args.get('titre') or request.form.get('titre', ''),
        'dateDebut': request.args.get('dateDebut') or request.form.get('dateDebut', ''),
        'duree': request.args.get('duree') or request.form.get('duree', ''),
        'idLieu': request.args.get('idLieu') or request.form.get('idLieu', '')
    }
    
    id_plateforme = request.args.get('idPlateforme') or request.form.get('idPlateforme')
    
    if id_plateforme:
        try:
            id_plateforme = int(id_plateforme)
            plateforme_selectionnee = PLATEFORME.query.get(id_plateforme)
            
            if plateforme_selectionnee:
                membres_compatibles = obtenir_membres_compatibles(id_plateforme)
                
                membres_selectionnes = request.form.getlist('membres')
        except ValueError:
            pass
    
    return render_template('add_campagne.html', 
                          title='Ajouter une Campagne',
                          lieux=lieux,
                          plateformes=plateformes,
                          plateforme_selectionnee=plateforme_selectionnee,
                          membres_compatibles=membres_compatibles,
                          membres_selectionnes=membres_selectionnes,
                          form_data=form_data,
                          message=message,
                          message_type=message_type)

@app.route('/create_campagne/', methods=['POST'])
@app.route('/create_campagne', methods=['POST'])
def creer_nouvelle_campagne():
    """Crée une nouvelle campagne avec validation des habilitations."""
    try:
        titre = request.form.get('titre', '').strip() or None
        date_debut_str = request.form.get('dateDebut', '')
        duree_str = request.form.get('duree', '')
        id_lieu_str = request.form.get('idLieu', '')
        id_plateforme_str = request.form.get('idPlateforme', '')
        membres_usernames = request.form.getlist('membres')
        
        if not date_debut_str:
            return redirect(url_for('add_campagne', error='La date de début est obligatoire'))
        
        if not duree_str:
            return redirect(url_for('add_campagne', error='La durée est obligatoire'))
        
        if not id_lieu_str:
            return redirect(url_for('add_campagne', error='Le lieu de fouille est obligatoire'))
        
        if not id_plateforme_str:
            return redirect(url_for('add_campagne', error='La plateforme est obligatoire'))
        
        if not membres_usernames:
            return redirect(url_for('add_campagne', 
                                  error='Vous devez sélectionner au moins un membre habilité',
                                  idPlateforme=id_plateforme_str,
                                  titre=titre or '',
                                  dateDebut=date_debut_str,
                                  duree=duree_str,
                                  idLieu=id_lieu_str))
        
        duree = int(duree_str)
        id_lieu = int(id_lieu_str)
        id_plateforme = int(id_plateforme_str)
        date_debut = datetime.strptime(date_debut_str, '%Y-%m-%d').date()
        duree_jours = max(1, duree // 24)

        campagne, error = creer_campagne( date_debut=date_debut,duree_jours=duree_jours,id_lieu=id_lieu,id_plateforme=id_plateforme,
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

@app.route('/login/')
def login():
    return render_template('login.html', title='Login')
