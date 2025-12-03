from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import *
from wtforms.validators import *
from .models import *
from hashlib import sha256
from datetime import date


class LoginForm(FlaskForm):
    username = StringField('Identifiant', validators=[DataRequired()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    next = HiddenField()

    def get_authenticated_user(self):
        unUser = PERSONNE.query.get(self.username.data)
        if unUser is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.password else None


class RegisterForm(FlaskForm):
    username = StringField('Identifiant', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    nom = StringField('Nom', validators=[DataRequired()])
    role_labo = SelectField(
        'Rôle dans le labo',
        choices=[],
        validators=[DataRequired()],
    )
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            DataRequired(),
            EqualTo('password',
                    message='Les mots de passe doivent correspondre.')
        ],
    )
    next = HiddenField()

    def build_user(self):
        m = sha256()
        m.update(self.password.data.encode())
        return PERSONNE(
            username=self.username.data,
            prenom=self.prenom.data,
            nom=self.nom.data,
            password=m.hexdigest(),
            role_labo=role_labo_enum(self.role_labo.data),
        )


class BudgetForm(FlaskForm):
    date = DateField('Date',
                     format='%Y-%m',
                     validators=[DataRequired()],
                     render_kw={'type': 'month'})
    budget_mensuel = DecimalField('Montant du budget',
                                  validators=[DataRequired(), NumberRange(min=0, max=99999.99)])
    next = HiddenField()

    def build_budget(self):
        return BUDGET_MENSUEL(
            annee=self.date.data.year,
            mois=self.date.data.month,
            budget=self.budget_mensuel.data,
        )
      

class GenererSequenceForm(FlaskForm):
    longueur = IntegerField('Longueur', validators=[DataRequired(), NumberRange(min=1, max=5000)])
    nom_fichier = StringField('Nom du fichier', validators=[DataRequired()])
    submit_generer = SubmitField('Generer et sauvegarder')


class ChargerSequenceForm(FlaskForm):
    fichier_adn = FileField('Fichier ADN', validators=[DataRequired()])
    nom_souhaite = StringField('Nom souhaite', validators=[Optional()])
    submit_charger = SubmitField('Charger le fichier')


class ChoisirSequenceForm(FlaskForm):
    sequences = SelectMultipleField('Fichiers ADN', choices=[], validators=[DataRequired()])
    submit_traitements = SubmitField('Acceder aux traitements')


class TraitementAdnForm(FlaskForm):
    sequence_base = SelectField('Sequence de base', choices=[], validators=[DataRequired()])
    proba = FloatField('Probabilite p', validators=[DataRequired(), NumberRange(min=0, max=1)])
    mutation_remplacement = BooleanField('Mutation remplacement')
    mutation_insertion = BooleanField('Mutation insertion')
    mutation_deletion = BooleanField('Mutation deletion')
    calcul_levenshtein = BooleanField('Calculer distance Levenshtein')
    sequence_lev_a = SelectField('Sequence A', choices=[], validators=[Optional()])
    sequence_lev_b = SelectField('Sequence B', choices=[], validators=[Optional()])
    submit_traiter = SubmitField('Appliquer les traitements')


class SauvegarderSequenceForm(FlaskForm):
    nom_sequence = StringField('Nom du fichier', validators=[DataRequired()])
    submit_sauvegarder = SubmitField('Sauvegarder la sequence')

class ResultatTraitemement(FlaskForm):
    telecharger_resultat =BooleanField('Télécharger les résultats')
    telecharger_sequences_mutees = BooleanField('Sauvegarder les séquences mutées')
    note = StringField('Note', validators=[Optional()])
    submit_historique = SubmitField('Ajouter a l\'historique')

class ReinitialiserResultatForm(FlaskForm):
    submit_reinitialiser = SubmitField('Reinitialiser les resultats')

    
class AssociateFilesForm(FlaskForm):
    file = MultipleFileField("Fichiers d'échantillon", validators=[DataRequired()])
    submit = SubmitField('Associer les fichiers')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    
<<<<<<< HEAD
class Form_plateforme(FlaskForm):
    id_plateforme = HiddenField('id_plateforme')
    nom_plateforme = StringField('nom_plateforme', validators = [DataRequired()])
    cout_journalier = IntegerField('cout_journalier', validators = [DataRequired()], render_kw={"min": "1"})
    minimum_personnes = IntegerField('minimum_personnes', validators = [DataRequired()], render_kw={"min": "1"})
    intervalle_maintenance = IntegerField('intervalle_maintenance', validators = [DataRequired()], render_kw={"min": "1"})

    

class FormPersonne(FlaskForm):
    idPersonne = HiddenField()
    nom = StringField('nom', validators=[DataRequired()])
    prenom = StringField('prenom', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    role_labo = SelectField(
        'Rôle dans le labo',
        choices=[],
        validators=[DataRequired()],
    )
=======
class Form_materiel(FlaskForm):
    idMateriel = HiddenField()
    idPlateforme = HiddenField()
    nom_materiel = StringField('nom_materiel', validators=[DataRequired()])
    description_mat = StringField('description_mat')
    quantite_mat = IntegerField('quantite_mat', validators=[DataRequired()])                     
>>>>>>> feature/page-ajout-materiel
    habilitations = MultiCheckboxField('Habilitations', choices=[
        ('electrique', 'Electrique'),
        ('chimique', 'Chimique'),
        ('biologique', 'Biologique'),
        ('radiation', 'Radiation')
    ])
        
    def validate_habilitations(self, field):
        if not field.data:
            raise ValidationError("Sélectionnez au moins une habilitation")
    
<<<<<<< HEAD

class CampagneForm(FlaskForm):

    titre = StringField("Titre", validators=[Optional()])
    dateDebut = DateField(
        "Date de début",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La date de début est obligatoire.")],
    )
    duree = IntegerField(
        "Durée en jours",
        validators=[
            DataRequired(message="La durée est obligatoire."),
            NumberRange(min=1, message="La durée doit être d'au moins 1 jour."),
        ],
    )
    idLieu = SelectField(
        "Lieu de fouille",
        choices=[],
        coerce=str,
        validators=[DataRequired(message="Le lieu de fouille est obligatoire.")],
    )
    idPlateforme = SelectField(
        "Plateforme",
        choices=[],
        coerce=str,
        validators=[DataRequired(message="La plateforme est obligatoire.")],
    )
    membres = SelectMultipleField(
        "Membres",
        choices=[],
        coerce=str,
    )
    

class LieuForm(FlaskForm):
    
    nomLieu = StringField("Nom du lieu", validators=[DataRequired()])
    next = HiddenField()
    
    def build_lieu(self):
        return LIEU_FOUILLE(
            nomLieu=self.nomLieu.data
        )


class MaintenanceForm(FlaskForm):

    dateDebut = DateField(
        "Date de début",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La date de début est obligatoire.")],
    )

    duree = IntegerField(
        "Durée (en jours)",
        validators=[
            DataRequired(message="La durée est obligatoire."),
            NumberRange(min=1, message="La durée doit être d'au moins 1 jour."),
        ],
    )

    idPlateforme = SelectField(
        "Plateforme",
        choices=[],
        coerce=str,
        validators=[DataRequired(message="La plateforme est obligatoire.")],
    )

    next = HiddenField()

    def validate_dateDebut(self, field):
        if field.data and field.data < date.today():
            raise ValidationError("La date ne peut pas être dans le passé.")

    def build_maintenance(self):
        return MAINTENANCE(
            dateMaintenance=self.dateDebut.data,
            duree_maintenance=self.duree.data,
            idPlateforme=int(self.idPlateforme.data),
            statut=statut.PLANIFIEE,
        )
=======
        
>>>>>>> feature/page-ajout-materiel
