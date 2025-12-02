from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField, SelectField, DateField, MultipleFileField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Optional
from .models import MAINTENANCE, PERSONNE, role_labo_enum, BUDGET_MENSUEL, statut
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
    budget_mensuel = StringField('Montant du budget',
                                 validators=[DataRequired()])
    next = HiddenField()

    def build_budget(self):
        return BUDGET_MENSUEL(
            annee=self.date.data.year,
            mois=self.date.data.month,
            budget=self.budget_mensuel.data,
        )
    
class AssociateFilesForm(FlaskForm):
    file = MultipleFileField("Fichiers d'échantillon",
                             validators=[DataRequired()])
    submit = SubmitField('Associer les fichiers')


class CampagneForm(FlaskForm):

    titre = StringField("Titre", validators=[Optional()])
    dateDebut = DateField(
        "Date de début",
        format="%Y-%m-%d",
        validators=[DataRequired(message="La date de début est obligatoire.")],
    )
    duree = IntegerField(
        "Durée en heures",
        validators=[
            DataRequired(message="La durée est obligatoire."),
            NumberRange(min=1, message="La durée doit être d'au moins 1 heure."),
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
