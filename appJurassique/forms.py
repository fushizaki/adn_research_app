from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from .models import PERSONNE
from hashlib import sha256

class LoginForm(FlaskForm):
    username = StringField ('Identifiant')
    password = PasswordField ('Mot de passe')
    next = HiddenField()

    def get_authenticated_user (self):
        unUser = PERSONNE.query.get(self.username.data)
        if unUser is None:
            return None
        m = sha256 ()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return unUser if passwd == unUser.password else None


class RegisterForm(FlaskForm):
    username = StringField('Identifiant', validators=(DataRequired(),))
    prenom = StringField('Prénom', validators=(DataRequired(),))
    nom = StringField('Nom', validators=(DataRequired(),))
    role_labo = StringField('Rôle dans le labo', validators=(DataRequired(),))
    password = PasswordField('Mot de passe', validators=(DataRequired(),))
    confirm_password = PasswordField(
        'Confirmer le mot de passe',
        validators=(DataRequired(), EqualTo('password', message='Les mots de passe doivent correspondre.'),),
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
            role_labo=self.role_labo.data,
        )