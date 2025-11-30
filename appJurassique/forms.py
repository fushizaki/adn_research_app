from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import (BooleanField, DateField, FloatField, HiddenField,
                     IntegerField, PasswordField, SelectField,
                     SelectMultipleField, StringField, SubmitField)
from wtforms.validators import DataRequired, EqualTo, NumberRange, Optional
from .models import PERSONNE, role_labo_enum, BUDGET_MENSUEL
from hashlib import sha256


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
    budget_mensuel = StringField('Montant du budget',
                                 validators=[DataRequired()])
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


class AjouterHistoriqueForm(FlaskForm):
    note = StringField('Note', validators=[Optional()])
    submit_historique = SubmitField('Ajouter a l\'historique')


class ReinitialiserResultatForm(FlaskForm):
    submit_reinitialiser = SubmitField('Reinitialiser les resultats')
