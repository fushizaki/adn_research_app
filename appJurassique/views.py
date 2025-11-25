from flask import render_template, request, redirect, url_for
from .app import app
from .forms import CampagneForm
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
    form = CampagneForm()
    form.idLieu.choices = [('', 'Sélectionner un lieu')] + [
        (str(lieu.idLieu), lieu.nomLieu) for lieu in lieux
    ]
    form.idPlateforme.choices = [('', 'Sélectionner une plateforme')] + [
        (str(plateforme.idPlateforme), plateforme.nom) for plateforme in plateformes
    ]

    formdata = request.form if request.method == 'POST' else request.args
    if formdata:
        form.process(formdata=formdata)

    plateforme_selectionnee = None
    membres_compatibles = []
    membres_selectionnes = form.membres.data or []
    message = request.args.get('error') or request.args.get('success')
    message_type = 'error' if request.args.get('error') else (
        'success' if request.args.get('success') else None
    )

    id_plateforme = form.idPlateforme.data

    if id_plateforme:
        try:
            id_plateforme_int = int(id_plateforme)
            plateforme_selectionnee = PLATEFORME.query.get(id_plateforme_int)

            if plateforme_selectionnee:
                membres_compatibles = obtenir_membres_compatibles(id_plateforme_int)
        except ValueError:
            pass

    return render_template(
        'add_campagne.html',
        title='Ajouter une Campagne',
        lieux=lieux,
        plateformes=plateformes,
        plateforme_selectionnee=plateforme_selectionnee,
        membres_compatibles=membres_compatibles,
        membres_selectionnes=membres_selectionnes,
        form=form,
        message=message,
        message_type=message_type
    )

@app.route('/create_campagne/', methods=['POST'])

def creer_nouvelle_campagne():
    """Crée une nouvelle campagne avec validation des habilitations."""
    try:
        lieux = LIEU_FOUILLE.query.all()
        plateformes = PLATEFORME.query.all()
        form = CampagneForm()
        form.idLieu.choices = [('', 'Sélectionner un lieu')] + [
            (str(lieu.idLieu), lieu.nomLieu) for lieu in lieux
        ]
        form.idPlateforme.choices = [('', 'Sélectionner une plateforme')] + [
            (str(plateforme.idPlateforme), plateforme.nom) for plateforme in plateformes
        ]
        form.process(formdata=request.form)

        if not form.validate():
            first_error = next(iter(form.errors.values()))[0]
            return redirect(url_for('add_campagne', error=first_error, 
                                    ))

        titre = (form.titre.data or '').strip() or None
        date_debut = form.dateDebut.data
        duree_heures = form.duree.data
        id_lieu = int(form.idLieu.data)
        id_plateforme = int(form.idPlateforme.data)
        membres_usernames = form.membres.data

        if not membres_usernames:
            return redirect(
                url_for(
                    'add_campagne',
                    error='Vous devez sélectionner au moins un membre habilité',
                    titre=form.titre.data or '',
                    dateDebut=form.dateDebut.data.strftime('%Y-%m-%d') if form.dateDebut.data else '',
                    duree=form.duree.data or '',
                    idLieu=form.idLieu.data or '',
                    idPlateforme=form.idPlateforme.data or ''
                )
            )

        duree_jours = max(1, duree_heures // 24)

        campagne, error = creer_campagne(
            date_debut=date_debut,
            duree_jours=duree_jours,
            id_lieu=id_lieu,
            id_plateforme=id_plateforme,
            noms_utilisateurs_membres=membres_usernames,
            titre=titre
        )

        if error:
            return redirect(url_for(
                'add_campagne',
                error=error,
                titre=form.titre.data or '',
                dateDebut=form.dateDebut.data.strftime('%Y-%m-%d') if form.dateDebut.data else '',
                duree=form.duree.data or '',
                idLieu=form.idLieu.data or '',
                idPlateforme=form.idPlateforme.data or ''
            ))
        return redirect(url_for('index', success='Campagne créée avec succès !'))

    except ValueError as e:
        return redirect(url_for('add_campagne', error=f'Erreur de validation : {str(e)}'))
    except Exception as e:
        return redirect(url_for('add_campagne', error=f'Erreur : {str(e)}'))

@app.route('/login/')
def login():
    return render_template('login.html', title='Login')
