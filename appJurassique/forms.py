from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, SelectMultipleField, widgets, IntegerField
from wtforms.validators import DataRequired, ValidationError

#https://gist.github.com/doobeh/4668212

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    
class Form_plateforme(FlaskForm):
    id_plateforme = HiddenField('id_plateforme')
    nom_plateforme = StringField('nom_plateforme', validators = [DataRequired()])
    cout_journalier = IntegerField('cout_journalier', validators = [DataRequired()])
    minimum_personnes = IntegerField('minimum_personnes', validators = [DataRequired()])
    intervalle_maintenance = IntegerField('intervalle_maintenance', validators = [DataRequired()])

    