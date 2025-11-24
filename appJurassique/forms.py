from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, BooleanField
from wtforms.validators import DataRequired

class Form_plateforme(FlaskForm):
    nom_plateforme = StringField('nom_plateforme', validators = [DataRequired()])
    cout_journalier = StringField('cout_journalier', validators = [DataRequired()])
    minimum_personnes = StringField('minimum_personnes', validators = [DataRequired()])
    intervalle_maintenance = StringField('intervalle_maintenance', validators = [DataRequired()])
    hab_electrique = BooleanField('hab_electrique')
    hab_chimique = BooleanField('hab_chimique')
    hab_biologique = BooleanField('hab_biologique')
    hab_radiation = BooleanField('hab_radiation')
    
    def validate(self):
        # Si AUCUNE des habilitations n'est cochée
        if not (self.hab_electrique.data or self.hab_chimique.data or 
                self.hab_biologique.data or self.hab_radiation.data):
            
            # On ajoute une erreur à l'un des champs (par exemple le premier)
            # pour qu'elle puisse être affichée dans le template
            self.hab_electrique.errors.append("Vous devez sélectionner au moins une habilitation.")
            return False
            
        return True
    
    