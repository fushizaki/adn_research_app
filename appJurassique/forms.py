from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.validators import DataRequired

class Form_plateforme(FlaskForm):
    nom_plateforme = StringField('nom_plateforme', validators = [DataRequired()])
    cout_journalier = StringField('cout_journalier', validators = [DataRequired()])
    minimum_personnes = StringField('minimum_personnes', validators = [DataRequired()])
    intervalle_maintenance = StringField('intervalle_maintenance', validators = [DataRequired()])
    