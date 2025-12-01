from flask_wtf import FlaskForm
from wtforms import (StringField, HiddenField, PasswordField, SelectField,
                     DateField, MultipleFileField, SubmitField, SelectMultipleField, widgets)
from wtforms.validators import DataRequired, EqualTo, ValidationError
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


class AssociateFilesForm(FlaskForm):
    file = MultipleFileField("Fichiers d'échantillon",
                             validators=[DataRequired()])
    submit = SubmitField('Associer les fichiers')

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

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
    habilitations = MultiCheckboxField('Habilitations', choices=[
        ('electrique', 'Electrique'),
        ('chimique', 'Chimique'),
        ('biologique', 'Biologique'),
        ('radiation', 'Radiation')
    ])
        
    def validate_habilitations(self, field):
        if not field.data:
            raise ValidationError("Sélectionnez au moins une habilitation")
    
