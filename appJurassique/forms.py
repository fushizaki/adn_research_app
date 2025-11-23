from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, PasswordField
from wtforms.validators import DataRequired
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
        return unUser if passwd == unUser.Password else None